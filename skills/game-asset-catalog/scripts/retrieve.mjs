#!/usr/bin/env node
// Portable, standalone catalog retrieval. Grants and signed URLs are never logged.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const CHUNK = 1024 * 1024;
const MAX_JSON = 4 * CHUNK;
const COVERAGE = 'glb-gltf-obj-mtl-textureatlas-bmfont-tiled';
const DESCRIPTORS = new Set(['.gltf', '.glb', '.obj', '.mtl', '.xml', '.json', '.fnt', '.tsx', '.tmx', '.tx']);
const MEDIA = new Set('.png .jpg .jpeg .webp .gif .svg .avif .bmp .tga .exr .hdr .wav .ogg .mp3 .flac .m4a .aac .mp4 .webm .ttf .otf .woff .woff2 .glb .gltf .obj .mtl .fbx .blend .dae .bin'.split(' '));
class CatalogError extends Error {
  constructor(code, message, details = {}) { super(message); this.result = { ok: false, code, message, ...details }; }
}
const fail = (code, message, details) => { throw new CatalogError(code, message, details); };
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const readJson = (file, limit = MAX_JSON) => {
  if (fs.statSync(file).size > limit) fail('input_too_large', 'Read a smaller JSON input.');
  const raw = fs.readFileSync(file); let text;
  try {
    if (raw[0] === 0xff && raw[1] === 0xfe) text = new TextDecoder('utf-16le', { fatal: true }).decode(raw);
    else if (raw[0] === 0xfe && raw[1] === 0xff) text = new TextDecoder('utf-16be', { fatal: true }).decode(raw);
    else text = new TextDecoder('utf-8', { fatal: true }).decode(raw);
    return JSON.parse(text.replace(/^\uFEFF/, ''));
  } catch { fail('invalid_json', 'Save complete JSON using UTF-8 or BOM-marked UTF-16, then retry.'); }
};
const hash = value => { if (typeof value !== 'string' || !/^[0-9a-f]{64}$/.test(value)) fail('invalid_digest', 'Expected a lowercase SHA-256 value.'); return value; };
const memberName = value => {
  if (typeof value !== 'string' || !value || value.length > 1024 || value.startsWith('/') || /[\\:\x00-\x1f]/.test(value) || value.split('/').some(p => !p || p === '.' || p === '..')) fail('unsafe_path', 'Use a canonical relative member path.');
  return value;
};
const outputName = value => {
  memberName(value);
  if (/[<>"|?*]/.test(value) || value.split('/').some(p => /[. ]$/.test(p) || /^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(p))) fail('unsafe_path', 'A ZIP member cannot be extracted safely on Windows.');
  return value;
};
function noSymlinks(value) {
  const absolute = path.resolve(value);
  let current = path.parse(absolute).root;
  for (const part of absolute.slice(current.length).split(path.sep).filter(Boolean)) {
    current = path.join(current, part);
    try { if (fs.lstatSync(current).isSymbolicLink()) fail('unsafe_destination', 'Destination and cache paths must not contain symlinks.'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  return absolute;
}
function destination(value, directory = true) {
  if (value.split(/[\\/]/).includes('..')) fail('unsafe_destination', 'Use a normalized game-owned destination under assets/.');
  const target = noSymlinks(value), parts = target.split(path.sep);
  const group = p => p.normalize('NFKC').trim().toLowerCase().replace(/_/g, '-').replace(/[^\p{L}\p{N}_]+/gu, '-').replace(/^-|-$/g, '');
  if (!parts.includes('assets') || parts.some((p, i) => p.toLowerCase() === 'assets' && parts[i + 1] && group(parts[i + 1]) === 'template')) fail('unsafe_destination', 'Use a game-owned lowercase assets/ directory outside template assets.');
  if (directory && fs.existsSync(target) && !fs.statSync(target).isDirectory()) fail('unsafe_destination', 'The destination must be a directory.');
  let ancestor = directory ? target : path.dirname(target);
  while (!fs.existsSync(ancestor)) ancestor = path.dirname(ancestor);
  if (!fs.statSync(ancestor).isDirectory() || !hasWriteAccess(ancestor)) fail('destination_unavailable', 'The destination parent must be a writable, accessible directory.');
  return target;
}
function hasWriteAccess(value) { try { fs.accessSync(value, fs.constants.W_OK | fs.constants.X_OK); return true; } catch { return false; } }
function grantUrl(value) {
  if (typeof value !== 'string' || /[\x00-\x20]/.test(value)) fail('invalid_grant', 'The download grant must contain a valid HTTPS URL.');
  try { const url = new URL(value); if (url.protocol !== 'https:' || !url.hostname || url.username || url.password) throw Error(); }
  catch { fail('invalid_grant', 'The download grant must contain a valid HTTPS URL.'); }
  return value;
}
function grantBody(value) {
  if (value && ['webdev-mcp', 'game-assets'].includes(value.server)) {
    value = value.result;
    if (typeof value === 'string') { if (Buffer.byteLength(value) > MAX_JSON) fail('input_too_large', 'Read a smaller JSON input.'); try { value = JSON.parse(value); } catch { fail('invalid_grant', 'Save the complete access response to a local file.'); } }
  }
  if (!value || typeof value !== 'object' || typeof value.snapshotId !== 'string') fail('invalid_grant', 'Save the complete access response to a local file.');
  return value;
}
function grantItems(body) {
  const entries = body.files ?? (body.bootstrap && [{ ...body.bootstrap, path: 'bootstrap.tar.gz' }]);
  if (!Array.isArray(entries) || entries.length < 1 || entries.length > 32) fail('invalid_grant', 'Request 1–32 exact catalog paths with webdev.access_game_assets.');
  for (const entry of entries) {
    if (!entry || typeof entry !== 'object') fail('invalid_grant', 'A download entry is invalid.');
    memberName(entry.path); hash(entry.sha256); grantUrl(entry.url);
    if (!Number.isSafeInteger(entry.sizeBytes) || entry.sizeBytes < 0) fail('invalid_grant', 'A download entry has an invalid byte size.');
  }
  return entries;
}
function sourceFor(snapshot, entry) {
  return /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(snapshot) ? { snapshotId: snapshot, catalogPath: entry.path } : null;
}
function fileHash(file) {
  const fd = fs.openSync(file, 'r'), block = Buffer.allocUnsafe(CHUNK), digest = crypto.createHash('sha256');
  try { let bytes; while ((bytes = fs.readSync(fd, block, 0, block.length, null))) digest.update(block.subarray(0, bytes)); }
  finally { fs.closeSync(fd); }
  return digest.digest('hex');
}
function gameRoot(start) {
  let current = path.resolve(start);
  if (fs.existsSync(current) && fs.statSync(current).isFile()) current = path.dirname(current);
  while (true) {
    const candidate = path.join(current, 'project.godot');
    if (fs.existsSync(candidate) && fs.statSync(candidate).isFile() && !fs.lstatSync(candidate).isSymbolicLink()) return current;
    const parent = path.dirname(current); if (parent === current) return null; current = parent;
  }
}
function provenance(events, start) {
  try {
    const root = gameRoot(start ?? process.cwd()); if (!root) return { status: 'unbound' };
    const installed = process.env.GAME_RUNTIME && path.isAbsolute(process.env.GAME_RUNTIME) ? path.join(process.env.GAME_RUNTIME, 'scripts/asset-provenance.mjs') : null;
    const script = [installed, path.join(root, '.manus-game-tools/scripts/asset-provenance.mjs')].find(p => p && fs.existsSync(noSymlinks(p)));
    if (!script) return { status: 'deferred' };
    const temp = path.join(os.tmpdir(), `manus-asset-provenance-${crypto.randomUUID()}.json`);
    try { fs.writeFileSync(temp, JSON.stringify(events), { flag: 'wx', mode: 0o600 }); const run = spawnSync(process.execPath, [script, 'record', '--event-file', temp, '--project', root], { cwd: root, stdio: 'ignore', timeout: 15000 }); return { status: run.status === 0 ? 'recorded' : 'deferred' }; }
    finally { fs.rmSync(temp, { force: true }); }
  } catch { return { status: 'deferred' }; }
}
function cacheSources(base, digest, size) {
  try {
    const meta = readJson(noSymlinks(base + '.json'), 65536);
    return meta.sha256 === digest && meta.sizeBytes === size && Array.isArray(meta.catalogSources)
      ? meta.catalogSources.slice(0, 64).filter(x => x && /^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$/.test(x.snapshotId) && typeof x.catalogPath === 'string' && validMember(x.catalogPath)) : [];
  } catch { return []; }
}
function validMember(value) { try { memberName(value); return true; } catch { return false; } }
const metadataIdentity = source => [source.snapshotId, source.catalogPath.slice(0, -'/metadata.json'.length)];
const metadataName = (cache, source) => {
  const ascii = value => JSON.stringify(value).replace(/[\x7f-\uffff]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
  return noSymlinks(path.join(cache, `catalog-metadata-${sha('[' + metadataIdentity(source).map(ascii).join(', ') + ']')}.json`));
};
function rememberMetadata(cache, source, local, expected) {
  if (!source?.catalogPath.endsWith('/metadata.json')) return;
  try {
    const value = readJson(local, 8 * CHUNK);
    if (!value || typeof value !== 'object' || Array.isArray(value)) return;
    const metadataPath = source.catalogPath, catalogPath = metadataPath.slice(0, -'metadata.json'.length) + 'assets.zip';
    const text = x => typeof x === 'string' && x.length > 0 && x.length <= 1024 && !/[\x00-\x1f]/.test(x) ? x : undefined;
    const publicUrl = x => { try { const u = new URL(text(x)); return ['http:', 'https:'].includes(u.protocol) && !u.username && !u.password && !u.search && !u.hash ? x : undefined; } catch { return undefined; } };
    const license = value.license && typeof value.license === 'object' ? value.license : {};
    const sourceFacts = { packId: text(value.id), name: text(value.name), author: text(value.creator) ?? text(value.author), url: publicUrl(value.canonical_url) ?? publicUrl(value.source_url), metadataPath, metadataSha256: `sha256:${expected}` };
    const licenseFacts = { id: text(value.selected_license) ?? text(value.license_id) ?? text(license.selected_license) ?? text(license.license_id) ?? text(value.license), url: publicUrl(value.license_url) ?? publicUrl(license.license_url), attribution: text(value.attribution_text) ?? text(license.attribution_text) };
    const booleans = {
      attributionRequired: ['attribution_required'], copyrightNoticeRequired: ['copyright_notice_required'],
      licenseNoticeRequired: ['license_notice_required'], modificationNoticeRequired: ['modification_notice_required'],
      commercialUseAllowed: ['commercial_use_allowed', 'free_commercial_use'], modificationAllowed: ['modification_allowed'],
      redistributionAllowed: ['redistribution_allowed'], editableProjectDistributionAllowed: ['editable_project_distribution_allowed'],
      reusableTemplateDistributionAllowed: ['reusable_template_distribution_allowed'],
    };
    for (const [field, aliases] of Object.entries(booleans)) {
      const explicit = [value, license].flatMap(record => [...aliases, field].map(key => record[key])).find(v => typeof v === 'boolean');
      if (explicit !== undefined) licenseFacts[field] = explicit;
    }
    const projected = { ...source, catalogPath, metadataPath, metadataSha256: expected,
      ...(typeof value.archive_sha256 === 'string' && /^[a-f0-9]{64}$/.test(value.archive_sha256) ? { archiveSha256: value.archive_sha256 } : {}),
      source: Object.fromEntries(Object.entries(sourceFacts).filter(([, v]) => v !== undefined)),
      license: Object.fromEntries(Object.entries(licenseFacts).filter(([, v]) => v !== undefined)) };
    const target = metadataName(cache, source), temporary = target + '.' + crypto.randomUUID() + '.tmp';
    try { fs.writeFileSync(temporary, JSON.stringify(projected), { flag: 'wx', mode: 0o600 }); fs.renameSync(temporary, target); }
    finally { fs.rmSync(temporary, { force: true }); }
  } catch { /* Optional enrichment must not deny a verified download. */ }
}
function matchingMetadata(archive, digest, sources, expectedMetadata) {
  const results = [];
  for (const source of sources) {
    try {
      const descriptor = { ...source, catalogPath: source.catalogPath.slice(0, -'assets.zip'.length) + 'metadata.json' };
      const canonical = metadataName(path.dirname(archive), descriptor);
      const legacy = noSymlinks(path.join(path.dirname(archive), `catalog-metadata-${sha(JSON.stringify(metadataIdentity(descriptor)))}.json`));
      const record = readJson(fs.existsSync(canonical) ? canonical : legacy, 65536);
      if (record.snapshotId !== source.snapshotId || record.catalogPath !== source.catalogPath || record.metadataPath !== descriptor.catalogPath || (record.archiveSha256 && record.archiveSha256 !== digest) || (expectedMetadata && record.metadataSha256 !== expectedMetadata)) continue;
      hash(record.metadataSha256); results.push(record);
    } catch { /* An absent sidecar never becomes invented metadata. */ }
  }
  return results;
}
function verifyCache(base, identity) {
  if (fs.statSync(base).size !== identity.sizeBytes || fileHash(base) !== identity.sha256) fail('cache_integrity_failed', 'Cached bytes changed; remove this cache entry and retry.');
}
function cacheLease(lock) {
  const owner = `owner-${process.pid}-${crypto.randomUUID()}.json`, candidate = lock + '.' + crypto.randomUUID();
  fs.mkdirSync(candidate, { mode: 0o700 });
  fs.writeFileSync(path.join(candidate, owner), JSON.stringify({ pid: process.pid, createdAt: Date.now() }), { flag: 'wx', mode: 0o600 });
  try {
    try { fs.renameSync(candidate, lock); }
    catch (error) {
      if (!['EEXIST', 'ENOTEMPTY', 'EPERM'].includes(error.code)) throw error;
      const names = fs.readdirSync(lock);
      if (!names.length) {
        // A reclaimer can exit after removing its dead-owner marker. rmdir only
        // removes an empty directory, never a complete live lease.
        try { fs.rmdirSync(lock); fs.renameSync(candidate, lock); }
        catch { fail('cache_busy', 'Another retrieval changed the cache lease; retry.'); }
      } else {
        if (names.length !== 1 || !/^owner-\d+-[a-f0-9-]+\.json$/.test(names[0])) fail('cache_busy', 'The cache lock needs inspection before retrying.');
        const ownerPath = noSymlinks(path.join(lock, names[0])), prior = readJson(ownerPath, 1024);
        if (!Number.isSafeInteger(prior.pid) || prior.pid <= 0) fail('cache_busy', 'The cache lock needs inspection before retrying.');
        try { process.kill(prior.pid, 0); fail('cache_busy', 'Another retrieval owns this cache entry; retry after it completes.'); }
        catch (error) { if (error.code !== 'ESRCH') throw error; }
        // Delete only the dead owner's unique marker. A competing reclaimer cannot
        // delete a new owner's marker, and nonempty-directory rename preserves leases.
        try { fs.unlinkSync(ownerPath); fs.rmdirSync(lock); fs.renameSync(candidate, lock); }
        catch { fail('cache_busy', 'Another retrieval changed the cache lease; retry.'); }
      }
    }
    return () => {
      fs.unlinkSync(path.join(lock, owner));
      try { fs.rmdirSync(lock); } catch (error) { if (!['ENOTEMPTY', 'EEXIST', 'ENOENT'].includes(error.code)) throw error; }
    };
  } finally { fs.rmSync(candidate, { recursive: true, force: true }); }
}
async function download(entry, dir, source, legacyDir) {
  const base = noSymlinks(path.join(dir, entry.sha256));
  const partial = noSymlinks(base + '.part'), record = noSymlinks(base + '.json'), lock = noSymlinks(base + '.lock');
  const release = cacheLease(lock);
  try {
    const identity = { sha256: entry.sha256, sizeBytes: entry.sizeBytes };
    const legacy = noSymlinks(path.join(legacyDir, entry.sha256));
    if (!fs.existsSync(base) && !fs.existsSync(partial)) {
      if (fs.existsSync(legacy)) {
        verifyCache(legacy, identity); fs.copyFileSync(legacy, base, fs.constants.COPYFILE_EXCL); verifyCache(base, identity);
        fs.writeFileSync(record, JSON.stringify({ ...identity, catalogSources: cacheSources(legacy, entry.sha256, entry.sizeBytes) }));
        for (const meta of matchingMetadata(legacy, entry.sha256, cacheSources(legacy, entry.sha256, entry.sizeBytes))) {
          fs.writeFileSync(metadataName(dir, { ...meta, catalogPath: meta.metadataPath }), JSON.stringify(meta), { mode: 0o600 });
        }
      } else if (fs.existsSync(noSymlinks(legacy + '.part')) && fs.existsSync(noSymlinks(legacy + '.json'))) {
        const prior = readJson(legacy + '.json');
        if (prior.sha256 === identity.sha256 && prior.sizeBytes === identity.sizeBytes) {
          fs.copyFileSync(legacy + '.part', partial, fs.constants.COPYFILE_EXCL);
          fs.writeFileSync(record, JSON.stringify({ ...identity, catalogSources: cacheSources(legacy, entry.sha256, entry.sizeBytes) }));
        }
      }
    }
    const prior = fs.existsSync(record) ? readJson(record) : {};
    if (fs.existsSync(record) && (prior.sha256 !== identity.sha256 || prior.sizeBytes !== identity.sizeBytes)) fail('cache_identity_mismatch', 'Cache identity differs; choose a clean cache directory.');
    const sources = cacheSources(base, entry.sha256, entry.sizeBytes);
    if (source && !sources.some(x => x.snapshotId === source.snapshotId && x.catalogPath === source.catalogPath) && sources.length < 64) sources.push(source);
    const next = { ...identity, ...(sources.length ? { catalogSources: sources.sort((a, b) => (a.snapshotId + a.catalogPath).localeCompare(b.snapshotId + b.catalogPath)) } : {}) };
    if (fs.existsSync(base)) { verifyCache(base, identity); if (JSON.stringify(prior) !== JSON.stringify(next)) fs.writeFileSync(record, JSON.stringify(next)); return { cachePath: base, reused: true }; }
    if (fs.existsSync(partial) && !fs.existsSync(record)) fail('cache_identity_mismatch', 'Partial download has no identity; choose a clean cache directory.');
    fs.writeFileSync(record, JSON.stringify(next));
    let offset = fs.existsSync(partial) ? fs.statSync(partial).size : 0;
    if (offset > entry.sizeBytes) fail('cache_integrity_failed', 'Partial download is larger than expected; remove it and retry.');
    if (offset < entry.sizeBytes) {
      let response, current = entry.url;
      const controller = new AbortController(); let timer;
      const progress = () => { clearTimeout(timer); timer = setTimeout(() => controller.abort(), 60000); timer.unref?.(); };
      progress();
      try {
        for (let redirect = 0; redirect <= 5; redirect++) {
          grantUrl(current);
          response = await fetch(current, { headers: { 'Accept-Encoding': 'identity', ...(offset ? { Range: `bytes=${offset}-` } : {}) }, redirect: 'manual', signal: controller.signal });
          progress();
          if ([301, 302, 303, 307, 308].includes(response.status)) {
            if (redirect === 5) fail('download_failed', 'Too many redirects.');
            const location = response.headers.get('location');
            if (!location) fail('invalid_grant', 'Redirects must provide a valid HTTPS URL.');
            current = new URL(location, current).href; grantUrl(current);
            await response.body?.cancel(); continue;
          }
          break;
        }
        if (response.status === 401 || response.status === 403) fail('renewal_required', 'Request fresh webdev.access_game_assets links for the same catalog paths.');
        if (response.status === 206) {
          if (response.headers.get('content-range') !== `bytes ${offset}-${entry.sizeBytes - 1}/${entry.sizeBytes}`) fail('invalid_range', 'The server returned an inconsistent byte range; retry with a fresh grant.');
        } else if (response.status === 200) offset = 0;
        else fail('download_failed', 'The server did not return the requested object.');
        const length = response.headers.get('content-length');
        if (length !== null && (!/^\d+$/.test(length) || Number(length) !== entry.sizeBytes - offset)) fail('invalid_range', 'The response byte count differs from the requested object.');
        if (response.headers.get('content-encoding') && response.headers.get('content-encoding') !== 'identity') fail('invalid_range', 'The response transformed the requested bytes.');
        const output = fs.openSync(partial, offset ? 'a' : 'w', 0o600);
        try {
          let received = offset;
          for await (const block of response.body) {
            if (block.length) progress();
            received += block.length;
            if (received > entry.sizeBytes) fail('size_mismatch', 'The download exceeded its declared byte size.');
            fs.writeSync(output, block);
          }
          if (received !== entry.sizeBytes) fail('download_interrupted', 'Download stopped early; request fresh links and retry to resume.');
        } finally { fs.closeSync(output); }
      } catch (error) {
        if (error instanceof CatalogError) throw error;
        fail('download_interrupted', 'Transfer interrupted; request fresh links and retry to resume.');
      } finally { clearTimeout(timer); }
    } else if (!fs.existsSync(partial)) fs.writeFileSync(partial, '', { flag: 'wx', mode: 0o600 });
    if (fs.statSync(partial).size !== entry.sizeBytes || fileHash(partial) !== entry.sha256) { fs.rmSync(partial); fail('integrity_failed', 'Downloaded bytes differ from the catalog object; retry with a fresh grant.'); }
    fs.renameSync(partial, base);
    return { cachePath: base, reused: false };
  } finally { release(); }
}
async function fetchGrants(value, cacheDir, budget, target) {
  if (target) destination(target);
  const body = grantBody(value), entries = grantItems(body);
  if (entries.reduce((n, e) => n + e.sizeBytes, 0) > budget) fail('download_budget_exceeded', 'Selected objects exceed --max-total-bytes.');
  const legacyDir = noSymlinks(cacheDir), dir = noSymlinks(path.join(legacyDir, 'node-v1'));
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  const result = [], events = [];
  const accessRequest = body.files == null && body.bootstrap ? {} : { snapshotId: body.snapshotId, paths: entries.map(e => e.path) };
  try {
    for (const entry of entries) {
      const source = sourceFor(body.snapshotId, entry), local = await download(entry, dir, source, legacyDir);
      rememberMetadata(dir, source, local.cachePath, entry.sha256);
      result.push({ path: entry.path, ...local, sha256: entry.sha256, sizeBytes: entry.sizeBytes });
      if (source) events.push({ kind: 'download', ...source, sha256: entry.sha256, size: entry.sizeBytes });
    }
  } catch (error) {
    if (error instanceof CatalogError) Object.assign(error.result, { snapshotId: body.snapshotId, paths: entries.map(e => e.path), accessRequest, completed: result });
    throw error;
  }
  return { ok: true, snapshotId: body.snapshotId, files: result, provenance: provenance(events, target) };
}
async function selectedArchive(grant, archivePath, cacheDir, budget, target) {
  memberName(archivePath);
  if (!archivePath.endsWith('/assets.zip')) fail('invalid_archive_path', 'Use the exact collection archivePath returned by catalog search.');
  const body = grantBody(grant), entries = grantItems(body), found = entries.filter(e => e.path === archivePath);
  if (new Set(entries.map(e => e.path)).size !== entries.length) fail('invalid_grant', 'The access response contains duplicate paths.');
  if (!found.length) fail('missing_archive_grant', 'Request this exact archivePath with webdev.access_game_assets.');
  const archive = found[0], metaPath = archivePath.slice(0, -'assets.zip'.length) + 'metadata.json';
  let metadata = entries.find(e => e.path === metaPath);
  if (archive.metadata != null) {
    if (archive.metadata.path !== metaPath) fail('invalid_grant', 'Archive metadata must name the same collection.');
    grantItems({ snapshotId: body.snapshotId, files: [archive.metadata] });
    if (metadata && (metadata.sha256 !== archive.metadata.sha256 || metadata.sizeBytes !== archive.metadata.sizeBytes)) fail('invalid_grant', 'The access response contains conflicting metadata identities.');
    metadata = archive.metadata;
  }
  const fetched = await fetchGrants({ ...body, files: [archive] }, cacheDir, budget, target);
  if (metadata && metadata.sizeBytes <= budget - archive.sizeBytes) {
    try { await fetchGrants({ ...body, files: [metadata] }, cacheDir, budget - archive.sizeBytes, target); }
    catch (error) { if (!(error instanceof CatalogError) || !['download_failed', 'download_interrupted', 'renewal_required', 'cache_busy'].includes(error.result.code)) throw error; }
  }
  if (metadata) fetched.metadataSha256 = metadata.sha256;
  return fetched;
}
const CP437 = "ÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴┬├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ ";
function zipName(bytes, flags) {
  if (!(flags & 0x800)) return [...bytes].map(b => b < 128 ? String.fromCharCode(b) : CP437[b - 128]).join('');
  try { return new TextDecoder('utf-8', { fatal: true }).decode(bytes); }
  catch { fail('invalid_archive_encoding', 'A UTF-8 ZIP member name is malformed; inspect with retrieve.py.'); }
}
// ZIP central-directory reader: never run an archive member, trust no local name or size.
function zipOpen(file, digest, budget, caseSensitive = false) {
  if (!fs.statSync(file).isFile()) fail('input_or_io_error', 'The local archive file is unavailable.');
  if (digest && fileHash(file) !== hash(digest)) fail('integrity_failed', 'Archive bytes differ from the expected catalog object.');
  const fd = fs.openSync(file, 'r'), size = fs.fstatSync(fd).size;
  try {
    const tail = Buffer.alloc(Math.min(size, 65557)); fs.readSync(fd, tail, 0, tail.length, size - tail.length);
    let end = -1;
    for (let i = tail.length - 22; i >= 0; i--) if (tail.readUInt32LE(i) === 0x06054b50 && i + 22 + tail.readUInt16LE(i + 20) === tail.length) { end = i; break; }
    if (end < 0) fail('unsupported_archive', 'This command accepts ZIP archives only.');
    const count = tail.readUInt16LE(end + 10), centralSize = tail.readUInt32LE(end + 12), offset = tail.readUInt32LE(end + 16);
    if (count > 100000 || count === 65535 || centralSize === 0xffffffff || offset === 0xffffffff || centralSize > 32 * CHUNK || offset + centralSize > size) fail('unsafe_archive', 'Archive has an unsupported or oversized directory.');
    if (tail.readUInt16LE(end + 4) || tail.readUInt16LE(end + 6) || count !== tail.readUInt16LE(end + 8)) fail('unsafe_archive', 'Multi-volume ZIPs are unsupported.');
    const central = Buffer.alloc(centralSize); fs.readSync(fd, central, 0, centralSize, offset);
    const entries = new Map(), folded = new Set(); let pos = 0, expanded = 0;
    for (let i = 0; i < count; i++) {
      if (pos + 46 > central.length || central.readUInt32LE(pos) !== 0x02014b50) fail('unsafe_archive', 'Archive central directory is malformed.');
      const flags = central.readUInt16LE(pos + 8), method = central.readUInt16LE(pos + 10), crc = central.readUInt32LE(pos + 16);
      const compressed = central.readUInt32LE(pos + 20), length = central.readUInt32LE(pos + 24), nameSize = central.readUInt16LE(pos + 28);
      const extra = central.readUInt16LE(pos + 30), comment = central.readUInt16LE(pos + 32), mode = (central.readUInt32LE(pos + 38) >>> 16) & 0xf000, local = central.readUInt32LE(pos + 42);
      if (compressed === 0xffffffff || length === 0xffffffff || local === 0xffffffff || pos + 46 + nameSize + extra + comment > central.length || flags & 1 || (mode !== 0 && mode !== 0x8000 && mode !== 0x4000)) fail('unsafe_archive', 'Encrypted, special or unsupported archive members are unsupported.');
      const bytes = central.subarray(pos + 46, pos + 46 + nameSize), original = zipName(bytes, flags);
      const directory = original.endsWith('/'), name = memberName(directory ? original.slice(0, -1) : original);
      const key = name.normalize('NFC').toLowerCase();
      if (entries.has(name) || (!caseSensitive && folded.has(key)) || (mode === 0x4000 && !directory) || (directory && mode === 0x8000)) fail('unsafe_archive', 'Archive contains duplicate, case-colliding or special paths.');
      folded.add(key); expanded += length;
      if (expanded > (budget ?? 8 * 1024 ** 3) || (budget == null && (length > 512 * CHUNK || length > Math.max(1, compressed) * 1000))) fail('unsafe_archive', 'Archive exceeds inspection or decompression bounds.', { archiveExpandedBytes: expanded });
      entries.set(name, { name, directory, sizeBytes: length, compressed, method, crc, local, flags });
      pos += 46 + nameSize + extra + comment;
    }
    if (pos !== central.length) fail('unsafe_archive', 'Archive directory contains trailing entries.');
    for (const entry of entries.values()) {
      let parent = path.posix.dirname(entry.name);
      while (parent !== '.') { if (entries.has(parent) && !entries.get(parent).directory) fail('unsafe_archive', 'Archive contains conflicting file and directory paths.'); parent = path.posix.dirname(parent); }
    }
    const read = entry => {
      if (entry.directory) fail('missing_member', 'The selected member is a directory.');
      if (![0, 8].includes(entry.method)) fail('unsupported_compression', 'This selected ZIP member requires the advanced retrieve.py helper.', { member: entry.name });
      if (entry.sizeBytes > 512 * CHUNK) fail('unsafe_archive', 'A member exceeds the bounded in-memory reader.');
      const head = Buffer.alloc(30); if (fs.readSync(fd, head, 0, 30, entry.local) !== 30 || head.readUInt32LE(0) !== 0x04034b50) fail('unsafe_archive', 'Archive local header is malformed.');
      if (head.readUInt16LE(8) !== entry.method || (head.readUInt16LE(6) & 1)) fail('unsafe_archive', 'Archive local header conflicts with directory.');
      const nameLen = head.readUInt16LE(26), start = entry.local + 30 + nameLen + head.readUInt16LE(28), localName = Buffer.alloc(nameLen);
      fs.readSync(fd, localName, 0, nameLen, entry.local + 30);
      if (zipName(localName, head.readUInt16LE(6)) !== entry.name || start + entry.compressed > offset) fail('unsafe_archive', 'Archive local member bounds or name differ.');
      const packed = Buffer.alloc(entry.compressed); fs.readSync(fd, packed, 0, packed.length, start);
      let data;
      try { data = entry.method === 0 ? packed : zlib.inflateRawSync(packed, { maxOutputLength: entry.sizeBytes + 1 }); }
      catch { fail('integrity_failed', 'Archive member failed decompression.'); }
      if (data.length !== entry.sizeBytes || crc32(data) !== entry.crc) fail('integrity_failed', 'Archive member integrity check failed.');
      return data;
    };
    return { entries, read, close: () => fs.closeSync(fd) };
  } catch (error) { fs.closeSync(fd); throw error; }
}
const crcTable = Uint32Array.from({ length: 256 }, (_, n) => { for (let j = 0; j < 8; j++) n = (n & 1) ? (0xedb88320 ^ (n >>> 1)) : n >>> 1; return n >>> 0; });
function crc32(data) { let value = 0xffffffff; for (const byte of data) value = crcTable[(value ^ byte) & 255] ^ (value >>> 8); return (value ^ 0xffffffff) >>> 0; }
function dependency(parent, uri) {
  if (typeof uri !== 'string') fail('unsupported_dependencies', 'A referenced dependency has an invalid path.');
  if (uri.startsWith('data:')) return null;
  if (/^[a-z][\w+.-]*:/i.test(uri) || uri.startsWith('//') || uri.includes('?') || uri.includes('#')) fail('unsupported_dependencies', 'External model references must be inspected separately.');
  const ref = decodeURIComponent(uri);
  if (ref.startsWith('/') || /[\\:]/.test(ref)) fail('unsafe_archive', 'A dependency leaves its archive.');
  const parts = parent.split('/').slice(0, -1);
  for (const part of ref.split('/')) { if (!part || part === '.') continue; if (part === '..') { if (!parts.length) fail('unsafe_archive', 'A dependency leaves its archive.'); parts.pop(); } else parts.push(part); }
  return memberName(parts.join('/'));
}
function gltf(raw, name, required) {
  let document; try { document = JSON.parse(raw.toString('utf8').replace(/^\uFEFF/, '')); } catch { fail('unsupported_dependencies', 'glTF dependency data is malformed.', { member: name }); }
  if (!document || typeof document !== 'object' || Array.isArray(document)) fail('unsupported_dependencies', 'glTF dependency data must be an object.', { member: name });
  const extensions = document.extensionsRequired ?? [];
  if (!Array.isArray(extensions) || extensions.length > 64 || extensions.some(x => typeof x !== 'string' || !/^[A-Za-z][A-Za-z0-9_]{0,127}$/.test(x))) fail('unsupported_dependencies', 'glTF required extensions must be a bounded array.', { member: name });
  if (extensions.length) required.push({ member: name, requiredExtensions: [...new Set(extensions)].sort() });
  const refs = [];
  for (const field of ['buffers', 'images']) {
    const items = document[field] ?? [];
    if (!Array.isArray(items) || items.some(x => !x || typeof x !== 'object' || Array.isArray(x))) fail('unsupported_dependencies', 'glTF dependency entries must be object arrays.', { member: name });
    for (const item of items) if ('uri' in item) { if (typeof item.uri !== 'string' || !item.uri) fail('unsupported_dependencies', 'glTF dependency URIs must be nonempty strings.', { member: name }); refs.push(item.uri); }
  }
  return refs;
}
function xmlTree(text, member) {
  const invalid = () => fail('unsupported_dependencies', 'XML descriptor is malformed or uses unsupported declarations.', { member });
  // Accept the UTF-8 document header; other processing instructions and declarations
  // still fail in the token parser. Comments are data, never entity declarations.
  text = text.replace(/^<\?xml\s+version\s*=\s*(?:"1\.[01]"|'1\.[01]')(?:\s+encoding\s*=\s*(?:"UTF-8"|'UTF-8'))?(?:\s+standalone\s*=\s*(?:"(?:yes|no)"|'(?:yes|no)'))?\s*\?>/i, '');
  const decode = raw => {
    if (raw.replace(/&(?:#x[0-9a-f]+|#[0-9]+|amp|lt|gt|quot|apos);/gi, '').includes('&')) invalid();
    return raw.replace(/&([^;]+);/g, (_, name) => {
    const predefined = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };
    if (name in predefined) return predefined[name];
    const code = /^#x[0-9a-f]+$/i.test(name) ? parseInt(name.slice(2), 16) : /^#[0-9]+$/.test(name) ? Number(name.slice(1)) : -1;
    if (code < 0 || code > 0x10ffff || code >= 0xd800 && code <= 0xdfff) invalid();
    return String.fromCodePoint(code);
    });
  };
  const stack = [], nodes = []; let cursor = 0, root;
  const tokens = text.match(/<!--[\s\S]*?-->|<[^>]*>|[^<]+/g) ?? [];
  for (const token of tokens) {
    cursor += token.length; if (nodes.length > 100000) invalid();
    if (token.startsWith('<!--')) {
      if (!token.endsWith('-->') || /--|-$/.test(token.slice(4, -3))) invalid();
      continue;
    }
    if (!token.startsWith('<')) {
      if (token.includes('&') && !/&(?:#x[0-9a-f]+|#[0-9]+|amp|lt|gt|quot|apos);/gi.test(token)) invalid();
      if (stack.length) stack.at(-1).text += decode(token);
      else if (token.trim()) invalid();
      continue;
    }
    if (/^<\/([A-Za-z][\w:.-]*)\s*>$/.test(token)) {
      if (stack.pop()?.tag !== token.match(/^<\/([^\s>]+)/)[1]) invalid();
      continue;
    }
    const match = token.match(/^<([A-Za-z][\w:.-]*)([\s\S]*?)\s*(\/?)>$/); if (!match) invalid();
    const attrs = {}, pattern = /\s+([A-Za-z][\w:.-]*)\s*=\s*(?:"([^"]*)"|'([^']*)')/gy;
    const raw = match[2]; let index = 0;
    while (index < raw.length && raw.slice(index).trim()) {
      pattern.lastIndex = index; const attr = pattern.exec(raw); if (!attr || attr[1] in attrs) invalid();
      attrs[attr[1]] = decode(attr[2] ?? attr[3]); index = pattern.lastIndex;
    }
    const node = { tag: match[1], attrs, children: [], text: '' };
    if (stack.length) stack.at(-1).children.push(node);
    else if (root) invalid(); else root = node;
    nodes.push(node);
    if (!match[3]) stack.push(node);
  }
  if (cursor !== text.length || stack.length || !root) invalid();
  return { root, nodes };
}
function descriptorTerms(line, member, comments = true) {
  const terms = []; let word = '', quote = null, active = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === '\\' && quote !== "'") {
      if (++i === line.length) fail('unsupported_dependencies', 'Descriptor has an incomplete escape.', { member });
      word += line[i]; active = true;
    } else if (quote) {
      if (c === quote) quote = null; else word += c;
    } else if (c === '"' || c === "'") { quote = c; active = true; }
    else if (comments && c === '#') break;
    else if (/\s/.test(c)) { if (active) terms.push(word); word = ''; active = false; }
    else { word += c; active = true; }
  }
  if (quote) fail('unsupported_dependencies', 'Descriptor has an unclosed quote.', { member });
  if (active) terms.push(word);
  return terms;
}
function fontReferences(common, pages, characters, member) {
  const integer = value => typeof value === 'string' && /^\d+$/.test(value) ? Number(value) : NaN;
  const count = integer(common.pages), ids = pages.map(p => integer(p.id));
  if (!Number.isInteger(count) || count < 1 || count > 1000 || ids.sort((a, b) => a - b).some((id, i) => id !== i) || pages.length !== count || characters.some(c => !ids.includes(integer(c.page)))) fail('unsupported_dependencies', 'Bitmap font page coverage is inconsistent.', { member });
  return pages.map(p => {
    if (typeof p.file !== 'string' || !p.file.trim()) fail('unsupported_dependencies', 'A descriptor has a missing dependency path.', { member });
    return p.file;
  });
}
function modelRequirementsSummary(required) {
  if (!required.length) return {};
  return {
    modelsWithRequiredExtensions: required.length,
    modelRequirements: required.slice(0, 8),
    modelRequirementsInReceipt: required.length > 8,
    modelImportCompatibility: 'not_verified',
    ...(required.some(row => row.requiredExtensions.includes('KHR_mesh_quantization')) ? {
      modelCompatibilityNote: 'Godot 4.7.2.stable.official.ed1daf0bf rejects required KHR_mesh_quantization. For this engine, choose an unquantized catalog member or procedural geometry before integration. Other engines are not assessed.',
    } : {}),
  };
}
function references(raw, name, required, limitations) {
  const ext = path.posix.extname(name).toLowerCase();
  if (ext === '.glb') {
    if (raw.length < 20 || raw.toString('ascii', 0, 4) !== 'glTF' || raw.readUInt32LE(4) !== 2 || raw.readUInt32LE(8) !== raw.length || raw.readUInt32LE(16) !== 0x4e4f534a || raw.readUInt32LE(12) > MAX_JSON || raw.readUInt32LE(12) + 20 > raw.length) fail('unsupported_dependencies', 'GLB must begin with a bounded, complete JSON chunk.', { member: name });
    return gltf(raw.subarray(20, 20 + raw.readUInt32LE(12)), name, required);
  }
  if (ext === '.gltf') return gltf(raw, name, required);
  if (!DESCRIPTORS.has(ext)) return [];
  if (raw.length > MAX_JSON) fail('unsupported_dependencies', 'Descriptor exceeds the inspection bound.', { member: name });
  let text; try { text = new TextDecoder('utf-8', { fatal: true }).decode(raw).replace(/^\uFEFF/, ''); }
  catch { if (ext === '.fnt') { limitations.add(ext); return []; } fail('unsupported_dependencies', 'Descriptor encoding requires explicit inspection.', { member: name }); }
  if (ext === '.obj' || ext === '.mtl') {
    const found = [];
    for (const line of text.split(/\r?\n/)) {
      const terms = descriptorTerms(line, name);
      if (ext === '.obj' && terms[0]?.toLowerCase() === 'mtllib') found.push(...terms.slice(1));
      if (ext === '.mtl' && (/^map_/i.test(terms[0]) || ['bump', 'disp', 'decal', 'refl', 'norm'].includes(terms[0]?.toLowerCase()))) {
        if (terms.length !== 2 || terms[1].startsWith('-')) fail('unsupported_dependencies', 'MTL map options require explicit inspection.', { member: name });
        found.push(terms[1]);
      }
    }
    return found;
  }
  if (ext === '.json') {
    try { const data = JSON.parse(text); if (data?.meta && typeof data.meta === 'object' && 'frames' in data) { if (!data.meta.image) fail('unsupported_dependencies', 'Atlas image path is absent.', { member: name }); return [data.meta.image]; } }
    catch (error) { if (error instanceof CatalogError) throw error; }
    limitations.add(ext); return [];
  }
  if (!text.trimStart().startsWith('<')) {
    if (ext === '.fnt') {
      const lines = text.split(/\r?\n/).filter(line => line.trim()).map(line => descriptorTerms(line, name, false));
      if (['info', 'common'].includes(lines[0]?.[0])) {
        let common = {}; const pages = [], characters = [];
        for (const [kind, ...values] of lines) {
          const attrs = Object.fromEntries(values.filter(value => value.includes('=')).map(value => { const index = value.indexOf('='); return [value.slice(0, index), value.slice(index + 1)]; }));
          if (kind === 'common') common = attrs;
          else if (kind === 'page') pages.push(attrs);
          else if (kind === 'char') characters.push(attrs);
        }
        return fontReferences(common, pages, characters, name);
      }
    }
    if (ext === '.tsx' || ext === '.tmx') fail('unsupported_dependencies', 'Tiled descriptor is malformed.', { member: name });
    limitations.add(ext); return [];
  }
  const { root, nodes } = xmlTree(text, name);
  const requiredPath = value => { if (typeof value !== 'string' || !value.trim()) fail('unsupported_dependencies', 'A descriptor has a missing dependency path.', { member: name }); return value; };
  if (root.tag === 'TextureAtlas') return [requiredPath(root.attrs.imagePath)];
  if (root.tag === 'font') {
    const pages = root.children.find(n => n.tag === 'pages')?.children.filter(n => n.tag === 'page') ?? [];
    const characters = (root.children.find(n => n.tag === 'chars')?.children ?? []).filter(n => n.tag === 'char');
    return fontReferences(root.children.find(n => n.tag === 'common')?.attrs ?? {}, pages.map(p => p.attrs), characters.map(c => c.attrs), name);
  }
  if (['map', 'tileset', 'template'].includes(root.tag)) {
    const paths = [];
    for (const node of nodes) {
      const ref = node.tag === 'image' && (node.attrs.source !== undefined || !node.children.some(child => child.tag === 'data')) ? requiredPath(node.attrs.source)
        : node.tag === 'tileset' && node.attrs.source !== undefined ? requiredPath(node.attrs.source)
        : node.tag === 'object' && node.attrs.template !== undefined ? requiredPath(node.attrs.template)
        : node.tag === 'property' && node.attrs.type === 'file' ? requiredPath(node.attrs.value || node.text) : null;
      if (ref) paths.push(ref);
    }
    return paths;
  }
  limitations.add(ext); return [];
}
function selectedMembers(selected) {
  if (!Array.isArray(selected) || !selected.length || selected.length > 10000) fail('invalid_members', 'Select 1–10,000 exact member paths in a JSON array.');
  if (selected.some(x => x && typeof x === 'object' && !Array.isArray(x) && 'containers' in x && 'member' in x)) fail('unsupported_nested_selection', 'Typed nested locators require scripts/retrieve.py; see references/retrieval.md.');
  if (selected.some(x => typeof x !== 'string')) fail('invalid_members', 'Select exact flat ZIP member strings in a JSON array.');
  selected.forEach(outputName);
  return selected;
}
function scope(zip, selected) {
  selectedMembers(selected);
  const pending = [...selected], included = new Set(), limitations = new Set(), required = [];
  while (pending.length) {
    const name = outputName(pending.pop()); if (included.has(name)) continue;
    const entry = zip.entries.get(name); if (!entry || entry.directory) fail('missing_member', 'An exact selected member or dependency is absent.', { member: name });
    included.add(name);
    const ext = path.posix.extname(name).toLowerCase();
    if (DESCRIPTORS.has(ext)) for (const uri of references(zip.read(entry), name, required, limitations)) {
      const dep = dependency(name, uri); if (dep) pending.push(dep);
    }
    if (['.fbx', '.blend', '.dae', '.godot', '.tscn', '.tres', '.material', '.atlas'].includes(ext)) limitations.add(ext);
  }
  return { names: [...included].sort(), limitations: [...limitations].sort(), required };
}
function sourceRecords(archive, digest, selected, metadataSha256) {
  const sources = selected ?? cacheSources(archive, digest, fs.statSync(archive).size);
  const metadata = matchingMetadata(archive, digest, sources, metadataSha256);
  return { ...(sources.length ? { catalogSources: sources } : {}), ...(metadata.length ? { catalogMetadata: metadata } : {}) };
}
function extract(archive, members, target, digest, budget, expanded, caseSensitive, sources, metadataSha256) {
  const dest = destination(target); hash(digest);
  const zip = zipOpen(archive, digest, expanded, caseSensitive);
  const created = [], records = [];
  try {
    const { names, limitations, required } = scope(zip, members);
    if (names.reduce((total, name) => total + zip.entries.get(name).sizeBytes, 0) > budget) fail('extraction_budget_exceeded', 'Selected files and dependencies exceed --max-bytes.');
    for (const name of names) destination(path.join(dest, ...name.split('/')), false);
    // A case-sensitive host can contain files which would alias on Windows; never reuse or add over those.
    for (const name of names) {
      let parent = dest;
      for (const segment of name.split('/')) {
        if (fs.existsSync(parent)) {
          const folded = segment.normalize('NFC').toLowerCase();
          if (fs.readdirSync(parent).some(existing => existing !== segment && existing.normalize('NFC').toLowerCase() === folded)) fail('destination_conflict', 'An existing output has a case-variant name.');
        }
        parent = path.join(parent, segment);
      }
    }
    fs.mkdirSync(dest, { recursive: true });
    const seen = new Set();
    for (const name of names) {
      const key = name.normalize('NFC').toLowerCase(); if (seen.has(key)) fail('destination_conflict', 'Select case-variant members into separate destinations.'); seen.add(key);
      const output = noSymlinks(path.join(dest, ...name.split('/'))), data = zip.read(zip.entries.get(name)), checksum = sha(data);
      fs.mkdirSync(path.dirname(output), { recursive: true });
      if (fs.existsSync(output)) {
        if (!fs.statSync(output).isFile() || fs.statSync(output).size !== data.length || fileHash(output) !== checksum) fail('destination_conflict', 'An existing file differs; choose a separate destination.', { member: name });
      } else { fs.writeFileSync(output, data, { flag: 'wx' }); created.push(output); if (fileHash(output) !== checksum) fail('integrity_failed', 'Extracted bytes failed verification.', { member: name }); }
      records.push({ member: name, sha256: checksum, sizeBytes: data.length });
    }
    if (fileHash(archive) !== digest) fail('integrity_failed', 'Source archive changed during extraction.');
    const receipt = { version: 1, archiveSha256: digest, archiveSizeBytes: fs.statSync(archive).size, members: records, dependencyCoverage: COVERAGE, limitations, ...(required.length ? { modelRequirements: required.sort((a, b) => a.member.localeCompare(b.member)) } : {}), ...sourceRecords(archive, digest, sources, metadataSha256) };
    const payload = JSON.stringify(receipt, null, 2) + '\n', receiptPath = noSymlinks(path.join(dest, `.catalog-retrieval-${sha(JSON.stringify(receipt)).slice(0, 16)}.json`));
    if (fs.existsSync(receiptPath)) { if (fs.readFileSync(receiptPath, 'utf8') !== payload) fail('destination_conflict', 'An existing provenance receipt differs.'); }
    else { fs.writeFileSync(receiptPath, payload, { flag: 'wx' }); created.push(receiptPath); }
    const root = gameRoot(dest), events = root ? records.filter(r => MEDIA.has(path.posix.extname(r.member).toLowerCase())).map(r => {
      const metadata = receipt.catalogMetadata?.length === 1 && receipt.catalogSources?.length === 1 ? receipt.catalogMetadata[0] : null;
      const source = { memberPath: r.member, ...(receipt.catalogSources?.length === 1 ? receipt.catalogSources[0] : {}), ...metadata?.source };
      const license = metadata?.license ?? {};
      const { memberPath, ...archiveSource } = source;
      return { kind: 'asset', path: path.relative(root, path.join(dest, ...r.member.split('/'))).split(path.sep).join('/'), origin: 'catalog', sha256: r.sha256, source, license, inputs: [{ sha256: digest, source: archiveSource, license }] };
    }) : [];
    return { ok: true, destination: dest, fileCount: records.length, fileBytes: records.reduce((n, r) => n + r.sizeBytes, 0), receipt: receiptPath, provenance: provenance(events, dest), dependencyCoverage: COVERAGE, limitations, ...modelRequirementsSummary(required), nextAction: limitations.length ? 'Inspect dependencies for listed formats and explicitly select required files.' : null };
  } catch (error) { for (const file of created.reverse()) fs.rmSync(file, { force: true }); throw error; }
  finally { zip.close(); }
}
function argsOf(argv) {
  const [command, ...tokens] = argv; const args = {};
  const flags = {
    'check-destination': ['destination'],
    fetch: ['grant-file', 'cache-dir', 'max-total-bytes', 'destination'],
    retrieve: ['grant-file', 'archive-path', 'members-file', 'cache-dir', 'destination', 'max-total-bytes', 'max-bytes', 'max-archive-bytes', 'case-sensitive-members'],
    extract: ['archive', 'sha256', 'members-file', 'destination', 'max-bytes', 'max-archive-bytes', 'case-sensitive-members'],
    members: ['archive', 'sha256', 'grant-file', 'archive-path', 'cache-dir', 'max-total-bytes', 'max-archive-bytes', 'case-sensitive-members', 'query', 'limit', 'offset'],
  };
  const allowed = new Set((flags[command] ?? []).map(flag => '--' + flag));
  for (let i = 0; i < tokens.length; i++) {
    const key = tokens[i]; if (!allowed.has(key) || key in args) fail('invalid_arguments', 'Use documented command flags only.');
    if (key === '--case-sensitive-members') args[key] = true;
    else if (tokens[i + 1] === undefined || tokens[i + 1].startsWith('--')) fail('invalid_arguments', 'A required flag value is missing.');
    else args[key] = tokens[++i];
  }
  const val = (name, fallback) => { const value = args['--' + name]; if (value == null) { if (fallback !== undefined) return fallback; fail('invalid_arguments', `Missing --${name}.`); } return value; };
  const number = (name, fallback, minimum = 0, maximum = Number.MAX_SAFE_INTEGER) => { const raw = val(name, String(fallback)); if (!/^\d+$/.test(raw) || Number(raw) < minimum || Number(raw) > maximum) fail('invalid_retrieval_budget', `Use a bounded integer --${name}.`); return Number(raw); };
  const expanded = () => args['--max-archive-bytes'] == null ? null : number('max-archive-bytes', 0, 1, 8 * 1024 ** 3);
  const caseSensitive = !!args['--case-sensitive-members'];
  return { command, args, val, number, expanded, caseSensitive };
}
async function main(argv) {
  const { command, args, val, number, expanded, caseSensitive } = argsOf(argv);
  const budget = () => number('max-total-bytes', 256 * CHUNK);
  if (command === 'check-destination') return { ok: true, destination: destination(val('destination')) };
  if (command === 'fetch') return fetchGrants(readJson(val('grant-file')), val('cache-dir'), budget(), args['--destination']);
  if (command === 'retrieve') {
    const grant = readJson(val('grant-file')), selected = readJson(val('members-file')), target = val('destination');
    destination(target); selectedMembers(selected);
    const fetched = await selectedArchive(grant, val('archive-path'), val('cache-dir'), budget(), target);
    const item = fetched.files[0], result = extract(item.cachePath, selected, target, item.sha256, number('max-bytes', 256 * CHUNK), expanded(), caseSensitive, [sourceFor(fetched.snapshotId, item)].filter(Boolean), fetched.metadataSha256);
    return { ...result, snapshotId: fetched.snapshotId, archivePath: item.path, download: { cachePath: item.cachePath, sha256: item.sha256, sizeBytes: item.sizeBytes, reused: item.reused } };
  }
  if (command === 'extract') return extract(val('archive'), readJson(val('members-file')), val('destination'), val('sha256'), number('max-bytes', 256 * CHUNK), expanded(), caseSensitive);
  if (command === 'members') {
    let archive = args['--archive'], digest = args['--sha256'], fetched;
    if (args['--grant-file']) { fetched = await selectedArchive(readJson(args['--grant-file']), val('archive-path'), val('cache-dir'), budget()); archive = fetched.files[0].cachePath; digest = fetched.files[0].sha256; }
    if (!archive || !digest) fail('invalid_member_query', 'Use a verified archive or a saved access grant.');
    const zip = zipOpen(archive, digest, expanded(), caseSensitive);
    try {
      const query = args['--query'] ?? '', limit = number('limit', 5, 1, 100), offset = number('offset', 0);
      if (query.length > 256 || /[\x00-\x1f]/.test(query)) fail('invalid_member_query', 'Use a query of at most 256 characters.');
      const normalize = value => value.normalize('NFKC').toLowerCase();
      const terms = [...new Set(normalize(query).split(/\s+/).filter(Boolean))];
      const entries = [...zip.entries.values()].filter(x => !x.directory).sort((a, b) => a.name.localeCompare(b.name));
      const matches = entries.filter(x => terms.every(term => normalize(x.name).includes(term)));
      if (offset > matches.length) fail('invalid_member_query', 'The offset exceeds matching members.');
      const result = { ok: true, query, matchMode: 'literal_path_terms', coverage: { scope: 'verified_archive_inventory', archiveSha256: digest, measurementStatus: 'not_supplied', purposeCoverage: 'unknown', note: 'Searches every safe member name in the hash-verified ZIP; geometry and visual facing remain unmeasured.' }, inputFileCount: entries.length, matchingFileCount: matches.length, offset, nextOffset: null, pageComplete: true, outputLimited: false, files: [] };
      if (fetched) Object.assign(result, { snapshotId: fetched.snapshotId, archivePath: fetched.files[0].path, download: { cachePath: fetched.files[0].cachePath, sha256: digest, sizeBytes: fetched.files[0].sizeBytes, reused: fetched.files[0].reused } });
      for (const item of matches.slice(offset, offset + limit)) {
        result.files.push({ path: item.name, sizeBytes: item.sizeBytes });
        if (Buffer.byteLength(JSON.stringify(result)) > 3900) {
          result.files.pop(); result.outputLimited = true;
          if (!result.files.length) result.files.push({ path: item.name, detailsOmitted: true, nextAction: 'Inspect this exact member in the supplied local metadata.' });
          break;
        }
      }
      result.pageComplete = offset + result.files.length >= matches.length;
      result.nextOffset = result.pageComplete ? null : offset + result.files.length;
      if (Buffer.byteLength(JSON.stringify(result)) > 4000) fail('metadata_output_too_large', 'Shorten the query or inspect the exact local member.');
      return result;
    } finally { zip.close(); }
  }
  fail('invalid_arguments', 'Use fetch, retrieve, extract, members or check-destination.');
}
export { main, extract, fetchGrants, selectedArchive, CatalogError };
let direct = false;
try { direct = !!process.argv[1] && import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href; } catch { /* Library imports need no file-based entrypoint. */ }
if (direct) {
  try { console.log(JSON.stringify(await main(process.argv.slice(2)))); }
  catch (error) {
    const result = error instanceof CatalogError ? error.result : { ok: false, code: 'input_or_io_error', message: 'Inspect local inputs, file permissions and archive integrity, then retry.' };
    console.log(JSON.stringify(result)); process.exitCode = 1;
  }
}
