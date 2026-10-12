#!/usr/bin/env python3
import argparse
import contextlib
import gzip
import bz2
import lzma
import hashlib
import http.client
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import selectors
import stat
import struct
import subprocess
import sys
import tarfile
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import zlib
import xml.etree.ElementTree as ET

CHUNK = 1024 * 1024
MAX_JSON = 4 * CHUNK
MAX_METADATA = 8 * CHUNK
MAX_METADATA_OUTPUT = 4000
MAX_ARCHIVE_BYTES = 8 * 1024**3
DEPENDENCY_COVERAGE = "glb-gltf-obj-mtl-textureatlas-bmfont-tiled"
UNINSPECTED_DEPENDENCY_FORMATS = {
    ".fbx", ".blend", ".dae", ".godot", ".tscn", ".tres", ".material",
    ".tsx", ".tmx", ".fnt", ".atlas", ".xml", ".json",
}
PROVENANCE_MEDIA_EXTENSIONS = set(".png .jpg .jpeg .webp .gif .svg .avif .bmp .tga .exr .hdr .wav .ogg .mp3 .flac .m4a .aac .mp4 .webm .ttf .otf .woff .woff2 .glb .gltf .obj .mtl .fbx .blend .dae .bin".split())
PROVENANCE_LICENSE_BOOLEANS = {
    "attributionRequired": ("attribution_required",),
    "copyrightNoticeRequired": ("copyright_notice_required",),
    "licenseNoticeRequired": ("license_notice_required",),
    "modificationNoticeRequired": ("modification_notice_required",),
    "commercialUseAllowed": ("commercial_use_allowed", "free_commercial_use"),
    "modificationAllowed": ("modification_allowed",),
    "redistributionAllowed": ("redistribution_allowed",),
    "editableProjectDistributionAllowed": ("editable_project_distribution_allowed",),
    "reusableTemplateDistributionAllowed": ("reusable_template_distribution_allowed",),
}


class CatalogError(Exception):
    def __init__(self, code, message, **details):
        self.result = {"ok": False, "code": code, "message": message, **details}


def fail(code, message, **details):
    raise CatalogError(code, message, **details)


def read_json(path, limit=MAX_JSON):
    with open(path, "rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        fail("input_too_large", "Read a smaller JSON input.")
    return json.loads(raw)


def digest(path):
    checksum = hashlib.sha256()
    with open(path, "rb") as stream:
        while block := stream.read(CHUNK):
            checksum.update(block)
    return checksum.hexdigest()


def hash_value(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        fail("invalid_digest", "Expected a lowercase SHA-256 value.")
    return value


def relative_name(name):
    if (not isinstance(name, str) or not name or len(name) > 1024 or name.startswith("/") or "\\" in name
            or any(ord(c) < 32 for c in name) or ":" in name):
        fail("unsafe_path", "Use a canonical relative member path.")
    parts = name.split("/")
    if any(p in ("", ".", "..") for p in parts):
        fail("unsafe_path", "Use a canonical relative member path.")
    return name


def no_symlinks(path):
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            fail("unsafe_destination", "Destination and cache paths must not contain symlinks.")
    return absolute


def destination_path(path, directory=True):
    if ".." in Path(path).parts:
        fail("unsafe_destination", "Use a normalized game-owned destination under assets/.")
    target = no_symlinks(path)
    parts = target.parts
    def normalized_group(value):
        value = unicodedata.normalize("NFKC", value).strip().lower()
        return re.sub(r"[^\w]+", "-", value.replace("_", "-"), flags=re.UNICODE).strip("-")
    if any(parts[i].lower() == "assets" and normalized_group(parts[i + 1]) == "template"
           for i in range(len(parts) - 1)):
        fail("unsafe_destination", "Choose a game-owned directory outside every template asset tree.")
    if "assets" not in parts:
        fail("unsafe_destination", "New media must use the exact lowercase assets/ directory.")
    asset_root = parts.index("assets")
    if asset_root + 1 < len(parts):
        group = normalized_group(parts[asset_root + 1])
        if group == "template":
            fail("unsafe_destination", "Choose a game-owned group outside the reserved template group.")
    if directory and target.exists() and not target.is_dir():
        fail("unsafe_destination", "The destination must be a directory.")
    existing = target if directory else target.parent
    while not existing.exists():
        existing = existing.parent
    if not existing.is_dir() or not os.access(existing, os.W_OK | os.X_OK):
        fail("destination_unavailable", "The destination parent must be a writable, accessible directory.")
    return target


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_url(url):
    if not isinstance(url, str) or any(ord(char) <= 32 for char in url):
        fail("invalid_grant", "The download grant must contain a valid HTTPS URL.")
    try:
        parsed = urllib.parse.urlsplit(url)
        parsed.port
    except ValueError:
        fail("invalid_grant", "The download grant must contain a valid HTTPS URL.")
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        fail("invalid_grant", "The download grant must contain a valid HTTPS URL.")


@contextlib.contextmanager
def lease(path):
    fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "r+b") as stream:
        try:
            if os.name == "nt":
                import msvcrt
                if not path.stat().st_size:
                    stream.write(b"0")
                    stream.flush()
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            fail("cache_busy", "Another retrieval owns this cache entry; retry after it completes.")
        try:
            yield
        finally:
            if os.name == "nt":
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def grant_body(value):
    if isinstance(value, dict) and value.get("server") in ("webdev-mcp", "game-assets"):
        value = value.get("result")
        if isinstance(value, str):
            if len(value.encode("utf-8")) > MAX_JSON:
                fail("input_too_large", "Read a smaller JSON input.")
            try:
                value = json.loads(value)
            except ValueError:
                fail("invalid_grant", "Save the complete webdev.access_game_assets JSON response to a local file.")
    if not isinstance(value, dict) or not isinstance(value.get("snapshotId"), str):
        fail("invalid_grant", "Save the complete webdev.access_game_assets JSON response to a local file.")
    return value


def grant_items(value):
    value = grant_body(value)
    entries = value.get("files")
    if entries is None and isinstance(value.get("bootstrap"), dict):
        entries = [{**value["bootstrap"], "path": "bootstrap.tar.gz"}]
    if not isinstance(entries, list) or not 1 <= len(entries) <= 32:
        fail("invalid_grant", "Request 1–32 exact catalog paths with webdev.access_game_assets.")
    for entry in entries:
        if not isinstance(entry, dict):
            fail("invalid_grant", "A download entry is invalid.")
        relative_name(entry.get("path"))
        hash_value(entry.get("sha256"))
        if type(entry.get("sizeBytes")) is not int or entry["sizeBytes"] < 0:
            fail("invalid_grant", "A download entry has an invalid byte size.")
        validate_url(entry.get("url", ""))
    return value["snapshotId"], entries


def catalog_source(snapshot, entry):
    """Copy only durable identity fields, never grant URLs, headers or expiry."""
    if not isinstance(snapshot, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", snapshot):
        return None
    try:
        path = relative_name(entry.get("path"))
    except CatalogError:
        return None
    return {"snapshotId": snapshot, "catalogPath": path}


def provenance_text(value):
    return value if isinstance(value, str) and 0 < len(value) <= 1024 and not any(ord(c) < 32 for c in value) else None


def provenance_url(value):
    if not provenance_text(value):
        return None
    try:
        parsed = urllib.parse.urlsplit(value)
        if parsed.scheme in ("http", "https") and parsed.hostname and not (parsed.username or parsed.password or parsed.query or parsed.fragment):
            return value
    except ValueError:
        pass
    return None


def catalog_metadata_projection(value):
    """Known published metadata fields only; source download URLs are never copied."""
    if not isinstance(value, dict):
        return {"source": {}, "license": {}}
    nested = value.get("license") if isinstance(value.get("license"), dict) else {}
    source = {"packId": provenance_text(value.get("id")), "name": provenance_text(value.get("name")),
              "author": provenance_text(value.get("creator")) or provenance_text(value.get("author")),
              "url": provenance_url(value.get("canonical_url")) or provenance_url(value.get("source_url"))}
    license = {"id": provenance_text(value.get("selected_license")) or provenance_text(value.get("license_id"))
                   or provenance_text(nested.get("selected_license")) or provenance_text(nested.get("license_id"))
                   or provenance_text(value.get("license")),
               "url": provenance_url(value.get("license_url")) or provenance_url(nested.get("license_url")),
               "attribution": provenance_text(value.get("attribution_text")) or provenance_text(nested.get("attribution_text"))}
    for field, aliases in PROVENANCE_LICENSE_BOOLEANS.items():
        explicit = next((record[key] for record in (value, nested) for key in (*aliases, field)
                         if type(record.get(key)) is bool), None)
        if explicit is not None:
            license[field] = explicit
    return {"source": {key: item for key, item in source.items() if item},
            "license": {key: item for key, item in license.items() if item is not None}}


def catalog_metadata_path(cache, source):
    identity = [source["snapshotId"], source["catalogPath"].rsplit("/", 1)[0]]
    key = hashlib.sha256(json.dumps(identity, separators=(",", ":")).encode()).hexdigest()
    return no_symlinks(Path(cache) / ("catalog-metadata-" + key + ".json"))


def remember_catalog_metadata(cache, source, local, expected_sha256):
    if not source or not source["catalogPath"].endswith("/metadata.json"):
        return
    try:
        value = read_json(local, MAX_METADATA)
        projection = catalog_metadata_projection(value)
        projection["source"].update(metadataPath=source["catalogPath"], metadataSha256="sha256:" + expected_sha256)
        record = {**source, "catalogPath": source["catalogPath"].rsplit("/", 1)[0] + "/assets.zip",
                  "metadataPath": source["catalogPath"], "metadataSha256": expected_sha256, **projection}
        if isinstance(value, dict) and isinstance(value.get("archive_sha256"), str) and re.fullmatch(r"[a-f0-9]{64}", value["archive_sha256"]):
            record["archiveSha256"] = value["archive_sha256"]
        target = catalog_metadata_path(cache, source)
        # Atomic replacement prevents a concurrent extraction from observing partial JSON.
        with tempfile.NamedTemporaryFile(mode="w", dir=cache, prefix=".catalog-metadata-", delete=False, encoding="utf-8") as stream:
            temporary = Path(stream.name)
            json.dump(record, stream, sort_keys=True)
        try:
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    except (OSError, ValueError, TypeError, CatalogError):
        pass  # Verified retrieval remains available when optional metadata cannot be retained.


def cached_catalog_metadata(archive_path, expected_sha256, sources):
    records = []
    for source in sources:
        try:
            value = read_json(catalog_metadata_path(Path(archive_path).parent, source), 16 * 1024)
            metadata_path = source["catalogPath"].rsplit("/", 1)[0] + "/metadata.json"
            if (value.get("snapshotId") != source["snapshotId"] or value.get("catalogPath") != source["catalogPath"]
                    or value.get("metadataPath", metadata_path) != metadata_path
                    or value.get("archiveSha256", expected_sha256) != expected_sha256):
                continue
            hash_value(value.get("metadataSha256"))
            facts = value.get("source", {})
            metadata_hash = facts.get("metadataSha256", value["metadataSha256"])
            if (facts.get("snapshotId", source["snapshotId"]) != source["snapshotId"]
                    or facts.get("catalogPath", source["catalogPath"]) != source["catalogPath"]
                    or facts.get("metadataPath", metadata_path) != metadata_path
                    or not isinstance(metadata_hash, str)
                    or metadata_hash.removeprefix("sha256:") != value["metadataSha256"]):
                continue
            record = {**source, "metadataPath": metadata_path, "metadataSha256": value["metadataSha256"],
                      "source": {"metadataPath": metadata_path, "metadataSha256": "sha256:" + value["metadataSha256"]}, "license": {}}
            if "archiveSha256" in value:
                record["archiveSha256"] = value["archiveSha256"]
            for kind, fields in (("source", ("packId", "name", "author", "url")), ("license", ("id", "url", "attribution"))):
                for key in fields:
                    item = value.get(kind, {}).get(key)
                    item = provenance_url(item) if key == "url" else provenance_text(item)
                    if item:
                        record[kind][key] = item
            for field in PROVENANCE_LICENSE_BOOLEANS:
                item = value.get("license", {}).get(field)
                if type(item) is bool:
                    record["license"][field] = item
            records.append(record)
        except (OSError, ValueError, TypeError, AttributeError, CatalogError):
            continue
    return records


def cache_catalog_sources(archive_path, expected_sha256):
    """Read optional lineage only from the matching verified cache sidecar."""
    try:
        path = no_symlinks(Path(archive_path).with_suffix(".json"))
        value = read_json(path, 64 * 1024)
        if value.get("sha256") != expected_sha256 or value.get("sizeBytes") != Path(archive_path).stat().st_size:
            return []
        result = []
        for item in value.get("catalogSources", [])[:64]:
            if isinstance(item, dict):
                source = catalog_source(item.get("snapshotId"), {"path": item.get("catalogPath")})
                if source and source not in result:
                    result.append(source)
        return sorted(result, key=lambda item: (item["snapshotId"], item["catalogPath"]))
    except (OSError, ValueError, TypeError, AttributeError, CatalogError):
        return []


def receipt_catalog_sources(archive_path, expected_sha256, selected_sources=None, metadata_sha256=None):
    # A grant-driven retrieve knows its selected collection. A standalone extract
    # sees only cache aliases, which must remain explicitly ambiguous.
    sources = cache_catalog_sources(archive_path, expected_sha256)
    if selected_sources is not None:
        selected = []
        for item in selected_sources:
            candidate = catalog_source(item.get("snapshotId"), {"path": item.get("catalogPath")}) if isinstance(item, dict) else None
            if candidate and candidate not in selected:
                selected.append(candidate)
        if selected:
            sources = selected
    fields = {"catalogSources": sources} if sources else {}
    if len({item["catalogPath"] for item in sources}) > 1:
        fields.update(catalogSourceStatus="ambiguous",
                      catalogSourceNote="Cached archive matches multiple catalog collections; no source was selected for this extraction.")
    metadata = cached_catalog_metadata(archive_path, expected_sha256, sources)
    if metadata_sha256 is not None:
        metadata = [record for record in metadata if record["metadataSha256"] == metadata_sha256]
    if metadata:
        fields["catalogMetadata"] = metadata
    return fields


def provenance_project(start):
    """A receipt may be standalone; never infer a game from another directory."""
    try:
        current = no_symlinks(start)
        if current.is_file():
            current = current.parent
        for root in (current, *current.parents):
            project = root / "project.godot"
            if project.is_file() and not project.is_symlink():
                return root
    except (OSError, ValueError, TypeError, CatalogError):
        pass
    return None


def provenance_runtime(root):
    """Use the explicit installed runtime; legacy project tools remain a fallback."""
    candidates = []
    installed = os.environ.get("GAME_RUNTIME", "")
    if installed.strip() and Path(installed).is_absolute() and ".." not in Path(installed).parts:
        candidates.append(Path(installed) / "scripts/asset-provenance.mjs")
    candidates.append(root / ".manus-game-tools/scripts/asset-provenance.mjs")
    for candidate in candidates:
        try:
            runtime = no_symlinks(candidate)
            if runtime.is_file():
                return runtime
        except (OSError, ValueError, CatalogError):
            continue
    return None


def record_provenance(events, start=None):
    """One optional runtime call per batch; durable receipts remain the fallback."""
    root = provenance_project(start if start is not None else Path.cwd())
    if root is None:
        return {"status": "unbound"}
    try:
        runtime = provenance_runtime(root)
        if runtime is None or not shutil.which("node"):
            return {"status": "deferred"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", prefix="manus-asset-provenance-", encoding="utf-8") as event_file:
            json.dump(events, event_file, sort_keys=True)
            event_file.flush()
            completed = subprocess.run(["node", str(runtime), "record", "--event-file", event_file.name, "--project", str(root)],
                                       cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15, check=False)
        return {"status": "recorded" if completed.returncode == 0 else "deferred"}
    except (OSError, ValueError, subprocess.SubprocessError, CatalogError):
        return {"status": "deferred"}


def record_extracted_provenance(target, receipt):
    root = provenance_project(target)
    if root is None:
        return {"status": "unbound"}
    sources = receipt.get("catalogSources", [])
    collection_paths = {item["catalogPath"] for item in sources}
    metadata = receipt.get("catalogMetadata", [])
    events = []
    for member in receipt["members"]:
        output = member.get("outputPath", member["member"])
        # A nested member's outputPath is provided by its validated extraction plan.
        if not isinstance(output, str) or PurePosixPath(output).suffix.lower() not in PROVENANCE_MEDIA_EXTENSIONS:
            continue
        locator = member["member"]
        source = {"memberPath": locator if isinstance(locator, str) else locator["member"]}
        license = {}
        if len(sources) == 1:
            source.update(sources[0])
            if len(metadata) == 1:
                source.update(metadata[0].get("source", {}))
                license.update(metadata[0].get("license", {}))
        elif len(collection_paths) == 1:
            source["catalogPath"] = next(iter(collection_paths))
        events.append({"kind": "asset", "path": (target / output).relative_to(root).as_posix(),
                       "origin": "catalog", "sha256": member["sha256"], "source": source, "license": license,
                       "inputs": [{"sha256": receipt["archiveSha256"], "source": {key: value for key, value in source.items() if key != "memberPath"}, "license": license}],
                       **({"transformations": [{"operation": "extract", "tool": "catalog-retrieve",
                            "description": "Nested containers: " + json.dumps(locator["containers"], separators=(",", ":"))}]} if isinstance(locator, dict) else {})})
    return record_provenance(events, root)


def download(entry, cache, opener, source=None):
    identity = {"sha256": entry["sha256"], "sizeBytes": entry["sizeBytes"]}
    base = cache / entry["sha256"]
    partial, record = base.with_suffix(".part"), base.with_suffix(".json")
    for path in (base, partial, record, base.with_suffix(".lock")):
        no_symlinks(path)
    with lease(base.with_suffix(".lock")):
        previous = read_json(record) if record.exists() else {}
        if record.exists() and (not isinstance(previous, dict) or any(previous.get(key) != value for key, value in identity.items())):
            fail("cache_identity_mismatch", "Cache identity differs; choose a clean cache directory.")
        sources = cache_catalog_sources(base, entry["sha256"]) if base.exists() else []
        if source and source not in sources and len(sources) < 64:
            sources.append(source)
        record_identity = {**identity, **({"catalogSources": sorted(sources, key=lambda item: (item["snapshotId"], item["catalogPath"]))} if sources else {})}
        if base.exists():
            if base.stat().st_size != entry["sizeBytes"] or digest(base) != entry["sha256"]:
                fail("cache_integrity_failed", "Cached bytes changed; remove this cache entry and retry.")
            if previous != record_identity:
                try:
                    record.write_text(json.dumps(record_identity, sort_keys=True))
                except OSError:
                    pass  # A provenance update cannot make verified cached bytes unavailable.
            return base, True
        if partial.exists() and not record.exists():
            fail("cache_identity_mismatch", "Partial download has no identity; choose a clean cache directory.")
        record.write_text(json.dumps(record_identity, sort_keys=True))
        offset = partial.stat().st_size if partial.exists() else 0
        if entry["sizeBytes"] == 0 and not partial.exists():
            partial.touch(mode=0o600, exist_ok=False)
        if offset > entry["sizeBytes"]:
            fail("cache_integrity_failed", "Partial download is larger than expected; remove it and retry.")
        if offset < entry["sizeBytes"]:
            headers = {"Accept-Encoding": "identity"}
            if offset:
                headers["Range"] = f"bytes={offset}-"
            try:
                response = opener(urllib.request.Request(entry["url"], headers=headers), timeout=60)
                with response:
                    validate_url(response.geturl())
                    status = response.status
                    end = entry["sizeBytes"]
                    if status == 206:
                        match = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", response.headers.get("Content-Range", ""))
                        if not match or tuple(map(int, match.groups())) != (offset, end - 1, end):
                            fail("invalid_range", "The server returned an inconsistent byte range; retry with a fresh grant.")
                    elif status == 200:
                        offset = 0
                    else:
                        fail("download_failed", "The server did not return the requested object.")
                    length = response.headers.get("Content-Length")
                    if length is not None and (not length.isdigit() or int(length) != end - offset):
                        fail("invalid_range", "The response byte count differs from the requested object.")
                    if response.headers.get("Content-Encoding", "identity") != "identity":
                        fail("invalid_range", "The response transformed the requested bytes.")
                    with open(partial, "ab" if offset else "wb") as output:
                        received = offset
                        while block := response.read(min(CHUNK, end - received + 1)):
                            if len(block) > end - received:
                                fail("size_mismatch", "The download exceeded its declared byte size.")
                            output.write(block)
                            received += len(block)
                    if received != end:
                        fail("download_interrupted", "Download stopped early; request fresh links and retry to resume.")
            except urllib.error.HTTPError as error:
                if error.code in (401, 403):
                    fail("renewal_required", "Request fresh webdev.access_game_assets links for the same catalog paths.")
                fail("download_failed", "Download failed; request a fresh grant and retry.")
            except (OSError, urllib.error.URLError, TimeoutError, http.client.HTTPException):
                fail("download_interrupted", "Transfer interrupted; request fresh links and retry to resume.")
        if partial.stat().st_size != entry["sizeBytes"] or digest(partial) != entry["sha256"]:
            partial.unlink(missing_ok=True)
            fail("integrity_failed", "Downloaded bytes differ from the catalog object; retry with a fresh grant.")
        os.replace(partial, base)
        return base, False


def fetch_grants(value, cache_dir, max_total_bytes, destination=None, opener=None):
    if destination is not None:
        destination_path(destination)
    body = grant_body(value)
    snapshot, entries = grant_items(body)
    access_request = {} if body.get("files") is None and body.get("bootstrap") else {
        "snapshotId": snapshot, "paths": [entry["path"] for entry in entries],
    }
    if sum(e["sizeBytes"] for e in entries) > max_total_bytes:
        fail("download_budget_exceeded", "Selected objects exceed --max-total-bytes.")
    cache = no_symlinks(cache_dir)
    cache.mkdir(parents=True, exist_ok=True, mode=0o700)
    opener = opener or urllib.request.build_opener(HTTPSRedirect()).open
    results = []
    events = []
    try:
        for entry in entries:
            source = catalog_source(snapshot, entry)
            local, reused = download(entry, cache, opener, source=source)
            remember_catalog_metadata(cache, source, local, entry["sha256"])
            results.append({"path": entry["path"], "cachePath": str(local), "sha256": entry["sha256"],
                            "sizeBytes": entry["sizeBytes"], "reused": reused})
            if source:
                events.append({"kind": "download", **source, "sha256": entry["sha256"], "size": entry["sizeBytes"]})
    except CatalogError as error:
        if events:
            record_provenance(events, destination)
        error.result.update(snapshotId=snapshot, paths=[e["path"] for e in entries], accessRequest=access_request, completed=results)
        raise
    return {"ok": True, "snapshotId": snapshot, "files": results,
            "provenance": record_provenance(events, destination)}


def archive_options(max_archive_bytes=None, case_sensitive_members=False):
    if (max_archive_bytes is not None and
            (type(max_archive_bytes) is not int or not 0 < max_archive_bytes <= MAX_ARCHIVE_BYTES)):
        fail("invalid_retrieval_budget", "Use an integer --max-archive-bytes from 1 through 8589934592.")
    if type(case_sensitive_members) is not bool:
        fail("invalid_retrieval_budget", "Case-sensitive member selection must be explicitly enabled or disabled.")


def zip_inventory(archive, *, max_archive_bytes=None, case_sensitive_members=False):
    archive_options(max_archive_bytes, case_sensitive_members)
    members, folded, total = {}, set(), 0
    if len(archive.infolist()) > 100_000:
        fail("unsafe_archive", "Archive has too many members.")
    declared_bytes = sum(info.file_size for info in archive.infolist())
    for info in archive.infolist():
        if info.orig_filename != info.filename:
            fail("unsafe_archive", "Archive member names contain invalid characters.")
        name = relative_name(info.filename[:-1] if info.is_dir() else info.filename)
        fold = unicodedata.normalize("NFC", name).casefold()
        kind = stat.S_IFMT(info.external_attr >> 16)
        if info.flag_bits & 1 or kind not in (0, stat.S_IFREG, stat.S_IFDIR):
            fail("unsafe_archive", "Encrypted or special archive members are unsupported.")
        if name in members or (fold in folded and not case_sensitive_members):
            fail("unsafe_archive", "Archive contains duplicate or case-colliding paths.")
        folded.add(fold)
        total += info.file_size
        if (info.file_size < 0 or info.compress_size < 0 or total > (max_archive_bytes or MAX_ARCHIVE_BYTES)
                or (max_archive_bytes is None and
                    (info.file_size > 512 * CHUNK or info.file_size > max(1, info.compress_size) * 1000))):
            fail("unsafe_archive", "Archive exceeds inspection or decompression bounds.",
                 archiveExpandedBytes=declared_bytes, maxArchiveBytes=MAX_ARCHIVE_BYTES)
        members[name] = info
    for name in members:
        for parent in PurePosixPath(name).parents:
            if str(parent) in members and not members[str(parent)].is_dir():
                fail("unsafe_archive", "Archive contains conflicting file and directory paths.")
    return members


def require_zip(path):
    if not Path(path).is_file():
        fail("input_or_io_error", "The local archive file is unavailable.")
    if not zipfile.is_zipfile(path):
        fail("unsupported_archive", "This command accepts ZIP archives only. Inspect and unpack TAR bootstrap navigation separately with bounded checks.")


def dependency_path(parent, uri):
    if not isinstance(uri, str):
        fail("unsupported_dependencies", "A referenced dependency has an invalid path.")
    if uri.startswith("data:"):
        return None
    try:
        parsed = urllib.parse.urlsplit(uri)
    except ValueError:
        fail("unsupported_dependencies", "A referenced dependency has an invalid URI.")
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        fail("unsupported_dependencies", "External model references must be inspected separately.")
    ref = urllib.parse.unquote(parsed.path)
    if ref.startswith("/") or "\\" in ref or ":" in ref:
        fail("unsafe_archive", "A dependency leaves its archive.")
    parts = list(PurePosixPath(parent).parent.parts)
    for part in ref.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if not parts:
                fail("unsafe_archive", "A dependency leaves its archive.")
            parts.pop()
        else:
            parts.append(part)
    return relative_name("/".join(parts))


def authored_references(text, extension, name):
    def required(value):
        if not isinstance(value, str) or not value.strip():
            fail("unsupported_dependencies", "A descriptor has a missing dependency path.", member=name)
        return value

    def font_pages(common, pages, characters):
        try:
            count = int(common["pages"])
            ids = [int(page["id"]) for page in pages]
            used = [int(char["page"]) for char in characters]
        except (KeyError, ValueError, TypeError):
            fail("unsupported_dependencies", "Bitmap font page coverage is incomplete.", member=name)
        if not 1 <= count <= 1000 or sorted(ids) != list(range(count)) or any(page not in ids for page in used):
            fail("unsupported_dependencies", "Bitmap font page coverage is inconsistent.", member=name)
        return [required(page.get("file")) for page in pages]

    if extension == ".fnt" and not text.lstrip().startswith("<"):
        lines = [shlex.split(line, comments=False) for line in text.splitlines() if line.strip()]
        if not lines or lines[0][0] not in ("info", "common"):
            return None
        pages, common, characters = [], {}, []
        for values in lines:
            attrs = dict(value.split("=", 1) for value in values[1:] if "=" in value)
            if values[0] == "common":
                common = attrs
            elif values[0] == "page":
                pages.append(attrs)
            elif values[0] == "char":
                characters.append(attrs)
        return font_pages(common, pages, characters)
    if extension == ".json":
        try:
            value = json.loads(text)
        except ValueError:
            return None
        if isinstance(value, dict) and isinstance(value.get("meta"), dict) and "frames" in value:
            return [required(value["meta"].get("image"))]
        return None
    if not text.lstrip().startswith("<"):
        if extension in (".tsx", ".tmx"):
            fail("unsupported_dependencies", "Tiled descriptor is malformed.", member=name)
        return None
    if "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper():
        fail("unsupported_dependencies", "Descriptor declarations are unsupported.", member=name)
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        fail("unsupported_dependencies", "XML descriptor is malformed.", member=name)
    nodes = list(root.iter())
    if len(nodes) > 100_000:
        fail("unsupported_dependencies", "Descriptor exceeds the inspection bound.", member=name)
    if root.tag == "TextureAtlas":
        return [required(root.get("imagePath"))]
    if root.tag == "font":
        pages = root.findall("./pages/page")
        common = root.find("common")
        return font_pages(common.attrib if common is not None else {}, [page.attrib for page in pages],
                          [char.attrib for char in root.findall("./chars/char")])
    if root.tag in ("map", "tileset", "template"):
        references = []
        for node in nodes:
            if node.tag == "image" and ("source" in node.attrib or node.find("data") is None):
                references.append(required(node.get("source")))
            elif node.tag == "tileset" and "source" in node.attrib:
                references.append(required(node.get("source")))
            elif node.tag == "object" and "template" in node.attrib:
                references.append(required(node.get("template")))
            elif node.tag == "property" and node.get("type") == "file":
                references.append(required(node.get("value") or node.text))
        return references
    return None


def _member_blocks(archive, info):
    remaining = info.file_size
    with archive.open(info) as stream:
        while data := stream.read(min(CHUNK, remaining + 1)):
            if len(data) > remaining:
                fail("integrity_failed", "Archive member exceeds its declared byte size.")
            remaining -= len(data)
            yield data
    if remaining:
        fail("integrity_failed", "Archive member is shorter than its declared byte size.")


def _case_safe_destinations(target, names):
    # An archive may contain case variants; one output scope may not.
    selected = {}
    for name in names:
        parts = PurePosixPath(name).parts
        for length in range(1, len(parts) + 1):
            path = "/".join(parts[:length])
            fold = unicodedata.normalize("NFC", path).casefold()
            if fold in selected and selected[fold] != path:
                fail("destination_conflict", "Select case-variant members into distinct destination directories.")
            selected[fold] = path
        output = target / name
        while output != target.parent:
            if output.parent.is_dir():
                folded = unicodedata.normalize("NFC", output.name).casefold()
                if any(child.name != output.name and unicodedata.normalize("NFC", child.name).casefold() == folded
                       for child in output.parent.iterdir()):
                    fail("destination_conflict", "An existing output has a case-variant name; use a distinct destination directory.")
            output = output.parent


def gltf_references(raw, name, model_requirements=None):
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeError, ValueError):
        fail("unsupported_dependencies", "glTF dependency data is malformed.", member=name)
    if not isinstance(data, dict):
        fail("unsupported_dependencies", "glTF dependency data must be an object.", member=name)
    required = data.get("extensionsRequired", [])
    if (not isinstance(required, list) or len(required) > 64
            or any(not isinstance(value, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,127}", value)
                   for value in required)):
        fail("unsupported_dependencies", "glTF required extensions must be a bounded array of extension names.", member=name)
    if required and model_requirements is not None:
        model_requirements.append({"member": name, "requiredExtensions": sorted(set(required))})
    references = []
    for field in ("buffers", "images"):
        values = data.get(field, [])
        if not isinstance(values, list) or any(not isinstance(entry, dict) for entry in values):
            fail("unsupported_dependencies", "glTF dependency entries must be object arrays.", member=name)
        for entry in values:
            if "uri" in entry:
                if not isinstance(entry["uri"], str) or not entry["uri"]:
                    fail("unsupported_dependencies", "glTF dependency URIs must be nonempty strings.", member=name)
                references.append(entry["uri"])
    return references


def glb_references(archive, info, name, model_requirements=None):
    # Only decode the first JSON chunk. Geometry may be large; its bytes remain
    # subject to the normal extraction budget, byte count and SHA-256 checks.
    with archive.open(info) as stream:
        header = stream.read(20)
        if len(header) != 20:
            fail("unsupported_dependencies", "GLB header is incomplete.", member=name)
        magic, version, length, json_length, chunk_type = struct.unpack("<4s4I", header)
        if magic != b"glTF" or version != 2 or length != info.file_size:
            fail("unsupported_dependencies", "Expected a GLB version 2 file with its declared byte length.", member=name)
        if chunk_type != 0x4E4F534A or not json_length or json_length % 4 or json_length > length - 20:
            fail("unsupported_dependencies", "GLB must begin with a complete aligned JSON chunk.", member=name)
        if json_length > MAX_JSON:
            fail("unsupported_dependencies", "GLB JSON descriptor exceeds the inspection bound.", member=name)
        raw = stream.read(json_length)
        if len(raw) != json_length:
            fail("unsupported_dependencies", "GLB JSON chunk is incomplete.", member=name)
    return gltf_references(raw, name, model_requirements)


def closure(archive, members, selected, model_requirements=None):
    pending, included, limitations = list(selected), set(), set()
    while pending:
        name = relative_name(pending.pop())
        if name in included:
            continue
        if name not in members or members[name].is_dir():
            fail("missing_member", "An exact selected member or dependency is absent.", member=name)
        included.add(name)
        extension = PurePosixPath(name).suffix.lower()
        if extension == ".glb":
            references = glb_references(archive, members[name], name, model_requirements)
            pending.extend(ref for uri in references if (ref := dependency_path(name, uri)) is not None)
            continue
        if extension not in (".gltf", ".obj", ".mtl", ".xml", ".fnt", ".tsx", ".tmx", ".tx", ".json"):
            if extension in UNINSPECTED_DEPENDENCY_FORMATS:
                limitations.add(extension)
            continue
        if members[name].file_size > MAX_JSON:
            fail("unsupported_dependencies", "Model descriptor exceeds the inspection bound.", member=name)
        raw = b"".join(_member_blocks(archive, members[name]))
        if extension == ".gltf":
            references = gltf_references(raw, name, model_requirements)
            pending.extend(ref for uri in references if (ref := dependency_path(name, uri)) is not None)
            continue
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeError:
            if extension == ".fnt":
                limitations.add(extension)
                continue
            fail("unsupported_dependencies", "Descriptor encoding requires explicit inspection.", member=name)
        references = []
        if extension in (".xml", ".fnt", ".tsx", ".tmx", ".tx", ".json"):
            try:
                references = authored_references(text, extension, name)
            except ValueError:
                fail("unsupported_dependencies", "Descriptor dependency data is malformed.", member=name)
            if references is None:
                limitations.add(extension)
                continue
        else:
            for line in text.splitlines():
                values = shlex.split(line, comments=True)
                if not values:
                    continue
                if extension == ".obj" and values[0].lower() == "mtllib":
                    references.extend(values[1:])
                elif extension == ".mtl" and (values[0].lower().startswith("map_") or values[0].lower() in ("bump", "disp", "decal", "refl", "norm")):
                    if len(values) != 2 or values[1].startswith("-"):
                        fail("unsupported_dependencies", "MTL map options require explicit inspection.", member=name)
                    references.append(values[1])
        pending.extend(ref for uri in references if (ref := dependency_path(name, uri)) is not None)
    return sorted(included), sorted(limitations)


def model_requirements_summary(requirements):
    """Reuse descriptor facts from closure; do not reread models or probe an engine."""
    if not requirements:
        return {}
    result = {"modelsWithRequiredExtensions": len(requirements),
              "modelRequirements": requirements[:8],
              "modelRequirementsInReceipt": len(requirements) > 8,
              "modelImportCompatibility": "not_verified"}
    if any("KHR_mesh_quantization" in row["requiredExtensions"] for row in requirements):
        result["modelCompatibilityNote"] = (
            "Godot 4.7.2.stable.official.ed1daf0bf rejects required KHR_mesh_quantization. "
            "For this engine, choose an unquantized catalog member or procedural geometry before integration. "
            "Other engines are not assessed.")
    return result


def extract(archive_path, selected, destination, expected_sha256, max_bytes, *,
            max_archive_bytes=None, case_sensitive_members=False, _catalog_sources=None, _catalog_metadata_sha256=None):
    archive_options(max_archive_bytes, case_sensitive_members)
    if type(max_bytes) is not int or max_bytes < 0:
        fail("invalid_retrieval_budget", "Use a nonnegative integer extraction byte budget.")
    if isinstance(selected, list) and any(isinstance(member, dict) for member in selected):
        if max_archive_bytes is not None or case_sensitive_members:
            fail("invalid_retrieval_budget", "Archive overrides apply to flat ZIP member paths only.")
        return extract_nested(archive_path, selected, destination, expected_sha256, max_bytes,
                              _catalog_sources=_catalog_sources, _catalog_metadata_sha256=_catalog_metadata_sha256)
    target = destination_path(destination)
    hash_value(expected_sha256)
    require_zip(archive_path)
    if digest(archive_path) != expected_sha256:
        fail("integrity_failed", "Archive bytes differ from the expected catalog object.")
    if not isinstance(selected, list) or not selected or len(selected) > 10_000:
        fail("invalid_members", "Select 1–10,000 exact member paths in a JSON array.")
    if max_archive_bytes is not None or case_sensitive_members:
        _zip_directory_bound(archive_path)
    with zipfile.ZipFile(archive_path) as archive:
        members = zip_inventory(archive, max_archive_bytes=max_archive_bytes, case_sensitive_members=case_sensitive_members)
        model_requirements = []
        names, limitations = closure(archive, members, selected, model_requirements)
        if sum(members[name].file_size for name in names) > max_bytes:
            fail("extraction_budget_exceeded", "Selected files and dependencies exceed --max-bytes.")
        for name in names:
            destination_path(target / name, directory=False)
        if case_sensitive_members:
            _case_safe_destinations(target, names)
        created, records = [], []
        target.mkdir(parents=True, exist_ok=True)
        try:
            for name in names:
                output = no_symlinks(target / name)
                output.parent.mkdir(parents=True, exist_ok=True)
                expected = hashlib.sha256()
                for data in _member_blocks(archive, members[name]):
                    expected.update(data)
                checksum = expected.hexdigest()
                if output.exists():
                    if not output.is_file() or output.stat().st_size != members[name].file_size or digest(output) != checksum:
                        fail("destination_conflict", "An existing file differs; choose a separate destination.", member=name)
                else:
                    with output.open("xb") as writer:
                        created.append(output)
                        for data in _member_blocks(archive, members[name]):
                            writer.write(data)
                    if digest(output) != checksum:
                        fail("integrity_failed", "Extracted bytes failed verification.", member=name)
                records.append({"member": name, "sha256": checksum, "sizeBytes": members[name].file_size})
            if digest(archive_path) != expected_sha256:
                fail("integrity_failed", "Source archive changed during extraction.")
            receipt = {"version": 1, "archiveSha256": expected_sha256, "archiveSizeBytes": Path(archive_path).stat().st_size, "members": records,
                       "dependencyCoverage": DEPENDENCY_COVERAGE,
                       "limitations": limitations}
            if model_requirements:
                receipt["modelRequirements"] = sorted(model_requirements, key=lambda row: row["member"])
            receipt.update(receipt_catalog_sources(archive_path, expected_sha256, _catalog_sources, _catalog_metadata_sha256))
            receipt_key = hashlib.sha256(json.dumps(receipt, sort_keys=True).encode()).hexdigest()[:16]
            receipt_path = no_symlinks(target / f".catalog-retrieval-{receipt_key}.json")
            payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
            if receipt_path.exists():
                if receipt_path.read_text() != payload:
                    fail("destination_conflict", "An existing provenance receipt differs.")
            else:
                with receipt_path.open("x") as writer:
                    created.append(receipt_path)
                    writer.write(payload)
        except BaseException:
            for path in reversed(created):
                path.unlink(missing_ok=True)
            raise
    return {"ok": True, "destination": str(target), "fileCount": len(records),
            "fileBytes": sum(record["sizeBytes"] for record in records), "receipt": str(receipt_path),
            "provenance": record_extracted_provenance(target, receipt),
            "dependencyCoverage": DEPENDENCY_COVERAGE,
            "limitations": receipt["limitations"],
            **model_requirements_summary(receipt.get("modelRequirements", [])),
            "nextAction": "Inspect dependencies for listed formats and explicitly select required files." if receipt["limitations"] else None}


NESTED_MAX_DEPTH = 3
NESTED_MAX_MEMBERS = 100_000
NESTED_MAX_WORK_BYTES = 512 * CHUNK
NESTED_CONVERSION_SECONDS = 30


def _bsdtar():
    return shutil.which("bsdtar") if os.name != "nt" else None


def capabilities():
    external = _bsdtar()
    return {"schema": "game-asset-archive-capabilities/v1", "formats": {
        "zip": {"available": True, "backend": "stdlib"},
        "tar": {"available": True, "backend": "stdlib"},
        "tar.gz": {"available": True, "backend": "stdlib"},
        "tar.bz2": {"available": True, "backend": "stdlib"},
        "tar.xz": {"available": True, "backend": "stdlib"},
        "unitypackage": {"available": True, "backend": "stdlib", "delivery": "raw_guid_files"},
        **{name: {"available": bool(external), "backend": "bsdtar" if external else None}
           for name in ("rar", "7z")}}, "maxNestedDepth": NESTED_MAX_DEPTH,
        "maxMembers": NESTED_MAX_MEMBERS, "maxWorkingBytes": NESTED_MAX_WORK_BYTES,
        "maxSelectedBytes": 256 * CHUNK}


def _container_chain(containers):
    if (not isinstance(containers, list) or not 1 <= len(containers) <= NESTED_MAX_DEPTH + 1
            or containers[0] != "assets.zip"):
        fail("invalid_container_chain", "Use assets.zip followed by at most three exact nested container members.")
    return tuple(relative_name(name) for name in containers)


def normalize_member_scope(selected, *, allow_empty=False):
    if (not isinstance(selected, list) or len(selected) > 10_000
            or (not selected and not allow_empty)):
        fail("invalid_members", "Select 1–10,000 exact member paths or typed locators.")
    if all(isinstance(member, str) for member in selected):
        return sorted({relative_name(member) for member in selected})
    normalized = {}
    for value in selected:
        if isinstance(value, str):
            member = relative_name(value)
        elif isinstance(value, dict) and set(value) == {"containers", "member"}:
            member = {"containers": list(_container_chain(value["containers"])),
                      "member": relative_name(value["member"])}
        else:
            fail("invalid_members", "A typed member needs only containers and member fields.")
        normalized[json.dumps(member, sort_keys=True, ensure_ascii=False)] = member
    return [normalized[key] for key in sorted(normalized)]


def _parts(member):
    return (("assets.zip",), member) if isinstance(member, str) else (tuple(member["containers"]), member["member"])


def _scope_member(chain, name, typed):
    return {"containers": list(chain), "member": name} if typed or len(chain) > 1 else name


def _zip_directory_bound(path):
    with open(path, "rb") as stream:
        end = zipfile._EndRecData(stream)
    if (end is None or end[zipfile._ECD_DISK_NUMBER] or end[zipfile._ECD_DISK_START]
            or end[zipfile._ECD_ENTRIES_TOTAL] > NESTED_MAX_MEMBERS
            or end[zipfile._ECD_SIZE] > 32 * CHUNK):
        fail("unsafe_archive", "ZIP directory exceeds nested inspection bounds or is unsupported.")


def _tar_preflight(path):
    size = path.stat().st_size
    if size > NESTED_MAX_WORK_BYTES:
        fail("nested_budget_exceeded", "The intermediate archive exceeds the working-byte bound.")
    count, consecutive_extensions = 0, 0
    with path.open("rb") as stream:
        while True:
            block = stream.read(512)
            if not block or block == b"\0" * 512:
                break
            if len(block) != 512:
                fail("unsafe_archive", "TAR header is incomplete.")
            try:
                entry = tarfile.TarInfo.frombuf(block, "utf-8", "surrogateescape")
            except tarfile.HeaderError:
                fail("unsafe_archive", "TAR header is invalid.")
            count += 1
            if count > NESTED_MAX_MEMBERS or entry.size < 0 or entry.size > NESTED_MAX_WORK_BYTES:
                fail("nested_budget_exceeded", "TAR entries exceed nested inspection bounds.")
            if entry.type in (tarfile.XHDTYPE, tarfile.XGLTYPE, tarfile.GNUTYPE_LONGNAME, tarfile.GNUTYPE_LONGLINK):
                consecutive_extensions += 1
                if consecutive_extensions > 16:
                    fail("unsafe_archive", "TAR extended metadata exceeds its nesting bound.")
                if entry.size > 64 * 1024:
                    fail("unsafe_archive", "TAR extended metadata exceeds its bound.")
            else:
                consecutive_extensions = 0
                if not (entry.isreg() or entry.isdir()):
                    fail("unsafe_archive", "Links and special TAR entries are unsupported.")
            end = stream.tell() + ((entry.size + 511) // 512) * 512
            if end > size:
                fail("unsafe_archive", "TAR member extends beyond the available archive.")
            stream.seek(end)


class _TarEntry:
    def __init__(self, info):
        self.info, self.filename, self.file_size = info, info.name.rstrip("/") if info.isdir() else info.name, info.size

    def is_dir(self):
        return self.info.isdir()


class _TarView:
    def __init__(self, archive):
        self.archive = archive

    def open(self, entry):
        stream = self.archive.extractfile(entry.info)
        if stream is None:
            fail("invalid_members", "Select a regular file.")
        return stream

    def read(self, entry):
        if entry.file_size > MAX_JSON:
            fail("unsupported_dependencies", "Descriptor exceeds the inspection bound.")
        with self.open(entry) as stream:
            data = stream.read(MAX_JSON + 1)
        if len(data) > MAX_JSON:
            fail("unsupported_dependencies", "Descriptor exceeds the inspection bound.")
        return data


def _tar_inventory(archive):
    members, folded, total = {}, set(), 0
    for info in archive:
        entry = _TarEntry(info)
        name = relative_name(entry.filename)
        fold = unicodedata.normalize("NFC", name).casefold()
        if (fold in folded or not (info.isfile() or info.isdir()) or info.linkname or info.sparse
                or any(key.startswith("GNU.sparse") for key in info.pax_headers)):
            fail("unsafe_archive", "TAR contains links, sparse, special or colliding members.")
        if any(0xD800 <= ord(char) <= 0xDFFF for char in name):
            fail("unsafe_archive", "Archive member names must be valid Unicode.")
        total += info.size
        if len(members) >= NESTED_MAX_MEMBERS or info.size < 0 or total > NESTED_MAX_WORK_BYTES:
            fail("nested_budget_exceeded", "TAR content exceeds nested inspection bounds.")
        folded.add(fold)
        members[name] = entry
    for name in members:
        for parent in PurePosixPath(name).parents:
            if str(parent) in members and not members[str(parent)].is_dir():
                fail("unsafe_archive", "Archive contains conflicting file and directory paths.")
    return members


def _convert_external(path, destination, limit):
    binary = _bsdtar()
    if binary is None:
        fail("unsupported_archive_capability", "RAR/7z inspection requires an available supported bsdtar.")
    process = subprocess.Popen([binary, "-P", "-cf", "-", "@" + str(path)], stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    selector = selectors.DefaultSelector()
    total, warnings = 0, bytearray()
    deadline = time.monotonic() + NESTED_CONVERSION_SECONDS
    try:
        selector.register(process.stdout, selectors.EVENT_READ, "stdout")
        selector.register(process.stderr, selectors.EVENT_READ, "stderr")
        with destination.open("xb") as output:
            while selector.get_map():
                if time.monotonic() >= deadline:
                    fail("archive_timeout", "Nested archive conversion exceeded its time bound.")
                for key, _ in selector.select(min(0.25, max(0, deadline - time.monotonic()))):
                    data = os.read(key.fileobj.fileno(), min(CHUNK, max(1, limit - total + 1)))
                    if not data:
                        selector.unregister(key.fileobj)
                        continue
                    if key.data == "stderr":
                        warnings.extend(data[:8193 - len(warnings)])
                        if len(warnings) > 8192:
                            fail("unsafe_archive", "Archive conversion reported unsupported input.")
                    else:
                        total += len(data)
                        if total > limit:
                            fail("nested_budget_exceeded", "Converted archive exceeds the working-byte bound.")
                        output.write(data)
            process.wait(timeout=max(0.01, deadline - time.monotonic()))
        if process.returncode or warnings:
            fail("unsafe_archive", "Archive conversion reported an error or changed member names.")
        return total
    except subprocess.TimeoutExpired:
        fail("archive_timeout", "Nested archive conversion exceeded its time bound.")
    finally:
        selector.close()
        if process.poll() is None:
            process.kill()
        process.wait()
        process.stdout.close()
        process.stderr.close()


class _NestedSession:
    def __init__(self, archive_path, expected_sha256):
        self.archive_path = Path(archive_path)
        hash_value(expected_sha256)
        require_zip(archive_path)
        if digest(archive_path) != expected_sha256:
            fail("integrity_failed", "Archive bytes differ from the expected catalog object.")
        self.expected_sha256 = expected_sha256
        self.stack = contextlib.ExitStack()
        self.temp = Path(self.stack.enter_context(tempfile.TemporaryDirectory(prefix="catalog-nested-")))
        self.views, self.descriptors, self.used_bytes, self.used_members = {}, {}, 0, 0
        self.next_path = 0

    def close(self):
        self.stack.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()
        if exc_type is not None and issubclass(exc_type, (tarfile.TarError, zipfile.BadZipFile, lzma.LZMAError, EOFError, zlib.error)):
            fail("unsafe_archive", "The nested archive is invalid or incomplete.")

    def _path(self):
        path = self.temp / str(self.next_path)
        self.next_path += 1
        return path

    def _remaining(self):
        return NESTED_MAX_WORK_BYTES - self.used_bytes

    def _copy(self, reader, path, expected=None):
        written = 0
        with path.open("xb") as output:
            while True:
                data = reader.read(min(CHUNK, max(1, self._remaining() + 1)))
                if not data:
                    break
                written += len(data)
                self.used_bytes += len(data)
                if self.used_bytes > NESTED_MAX_WORK_BYTES or (expected is not None and written > expected):
                    fail("nested_budget_exceeded", "Nested container bytes exceed the working bound.")
                output.write(data)
        if expected is not None and expected != written:
            fail("unsafe_archive", "Nested container size differs from its inventory.")

    def open_chain(self, chain):
        chain = _container_chain(list(chain))
        if chain in self.views:
            return self.views[chain]
        name = chain[-1]
        if len(chain) == 1:
            path = self.archive_path
        else:
            view, members, _ = self.open_chain(chain[:-1])
            if name not in members or members[name].is_dir():
                fail("missing_container", "Exact nested container is unavailable.")
            if members[name].file_size > self._remaining():
                fail("nested_budget_exceeded", "Selected container exceeds the working-byte bound.")
            path = self._path()
            with view.open(members[name]) as reader:
                self._copy(reader, path, members[name].file_size)
        with path.open("rb") as stream:
            header = stream.read(512)
        if zipfile.is_zipfile(path):
            kind = "zip"
            _zip_directory_bound(path)
            view = self.stack.enter_context(zipfile.ZipFile(path))
            members = zip_inventory(view)
        else:
            tar_path = path
            if header.startswith((b"Rar!\x1a\x07", b"7z\xbc\xaf\x27\x1c")):
                kind = "rar" if header.startswith(b"Rar!") else "7z"
                tar_path = self._path()
                self.used_bytes += _convert_external(path, tar_path, self._remaining())
            elif header.startswith((b"\x1f\x8b", b"BZh", b"\xfd7zXZ\x00")):
                kind = "unitypackage" if name.lower().endswith(".unitypackage") else "tar.gz" if header.startswith(b"\x1f\x8b") else "tar.bz2" if header.startswith(b"BZh") else "tar.xz"
                opener = gzip.open if header.startswith(b"\x1f\x8b") else bz2.open if header.startswith(b"BZh") else lzma.open
                tar_path = self._path()
                with opener(path, "rb") as reader:
                    self._copy(reader, tar_path)
            elif name.lower().endswith(".tar"):
                kind = "tar"
            else:
                fail("unsupported_archive", "The selected member is not a supported nested archive.")
            _tar_preflight(tar_path)
            archive = self.stack.enter_context(tarfile.open(tar_path, "r:", errorlevel=2))
            view = _TarView(archive)
            members = _tar_inventory(archive)
        self.used_members += len(members)
        if self.used_members > NESTED_MAX_MEMBERS:
            fail("nested_budget_exceeded", "Nested inventories exceed the total member bound.")
        self.views[chain] = view, members, kind
        self.descriptors[chain] = {"locator": {"containers": list(chain[:-1]), "member": name},
                                   "sha256": digest(path), "sizeBytes": path.stat().st_size, "format": kind}
        return self.views[chain]

    def current(self):
        if digest(self.archive_path) != self.expected_sha256:
            fail("integrity_failed", "Source archive changed during nested inspection.")


def _unity_closure(view, members, selected):
    extra = set(selected)
    for name in selected:
        parts = name.split("/")
        if len(parts) == 2 and re.fullmatch(r"[0-9a-fA-F]{32}", parts[0]):
            extra.update(parts[0] + "/" + companion for companion in ("asset", "asset.meta", "pathname")
                         if parts[0] + "/" + companion in members and not members[parts[0] + "/" + companion].is_dir())
    return sorted(extra)


def inspect_nested(archive_path, containers, *, expected_sha256, limit=20, offset=0):
    if type(limit) is not int or not 1 <= limit <= 100 or type(offset) is not int or offset < 0:
        fail("invalid_inspection_options", "Use limit 1–100 and a nonnegative offset.")
    chain = _container_chain(containers)
    with _NestedSession(archive_path, expected_sha256) as session:
        view, members, kind = session.open_chain(chain)
        names = sorted(members)
        if offset > len(names):
            fail("invalid_inspection_options", "Offset exceeds this container inventory.")
        entries = []
        for name in names[offset:offset + limit]:
            row = {"path": name, "sizeBytes": members[name].file_size, "directory": members[name].is_dir(),
                   "locator": {"containers": list(chain), "member": name}}
            if kind == "unitypackage" and name.endswith("/asset"):
                companion = name.rsplit("/", 1)[0] + "/pathname"
                if companion in members and members[companion].file_size <= 4096:
                    try:
                        row["unityPath"] = relative_name(view.read(members[companion]).decode("utf-8").strip())
                    except (UnicodeError, CatalogError):
                        row["unityPathStatus"] = "unresolved"
            entries.append(row)
        session.current()
        return {"ok": True, "schema": "game-asset-nested-inventory/v1", "archiveSha256": expected_sha256,
                "containers": list(chain), "containerIdentities": list(session.descriptors.values()), "format": kind,
                "memberCount": len(names), "members": entries, "offset": offset,
                "nextOffset": offset + len(entries) if offset + len(entries) < len(names) else None,
                "limitations": ["unitypackage_raw_guids_no_project_import", "unity_guid_dependencies_uninspected"] if kind == "unitypackage" else []}


def _nested_plan(session, selected, max_bytes):
    if type(max_bytes) is not int or not 0 < max_bytes <= 256 * CHUNK:
        fail("invalid_byte_budget", "Use a positive nested selection byte budget no larger than 256 MiB.")
    requested = normalize_member_scope(selected)
    groups = {}
    for value in requested:
        chain, name = _parts(value)
        row = groups.setdefault(chain, {"names": set(), "typed": False})
        row["names"].add(name)
        row["typed"] |= isinstance(value, dict)
    records, scope, limitations, total, outputs = [], [], set(), 0, {}
    model_requirements = []
    for chain in sorted(groups):
        view, members, kind = session.open_chain(chain)
        requirements = []
        names, missing = closure(view, members, sorted(groups[chain]["names"]), requirements)
        for row in requirements:
            model_requirements.append({**row, "member": _scope_member(chain, row["member"], groups[chain]["typed"]),
                                       "outputPath": relative_name("/".join((*chain[1:], row["member"])))})
        limitations.update(missing)
        if kind == "unitypackage":
            names = _unity_closure(view, members, names)
            limitations.update(("unitypackage_raw_guids_no_project_import", "unity_guid_dependencies_uninspected"))
        for name in names:
            member = _scope_member(chain, name, groups[chain]["typed"])
            output = relative_name("/".join((*chain[1:], name)))
            folded = unicodedata.normalize("NFC", output).casefold()
            if folded in outputs:
                fail("destination_conflict", "Selected locators map to colliding output paths.")
            outputs[folded] = output
            total += members[name].file_size
            if total > max_bytes:
                fail("extraction_budget_exceeded", "Selected nested members and dependencies exceed --max-bytes.")
            checksum, observed = hashlib.sha256(), 0
            with view.open(members[name]) as stream:
                while data := stream.read(CHUNK):
                    observed += len(data)
                    if observed > members[name].file_size:
                        fail("unsafe_archive", "Nested member exceeded its declared size.")
                    checksum.update(data)
            if observed != members[name].file_size:
                fail("unsafe_archive", "Nested member size differs from its inventory.")
            records.append({"member": member, "sha256": checksum.hexdigest(), "sizeBytes": observed, "outputPath": output})
            scope.append(member)
    for name in outputs:
        if any(str(parent) in outputs for parent in PurePosixPath(name).parents):
            fail("destination_conflict", "Selected output files conflict with parent directories.")
    session.current()
    return {"ok": True, "schema": "game-asset-nested-plan/v1", "archiveSha256": session.expected_sha256,
            "selectedMembers": requested, "scope": normalize_member_scope(scope), "members": records,
            "selectedBytes": total, "containers": [session.descriptors[chain] for chain in sorted(session.descriptors)],
            "dependencyCoverage": DEPENDENCY_COVERAGE, "limitations": sorted(limitations),
            **({"modelRequirements": model_requirements} if model_requirements else {})}


def plan_nested(archive_path, selected, expected_sha256, max_bytes):
    with _NestedSession(archive_path, expected_sha256) as session:
        return _nested_plan(session, selected, max_bytes)


def extract_nested(archive_path, selected, destination, expected_sha256, max_bytes, *,
                   _catalog_sources=None, _catalog_metadata_sha256=None):
    target = destination_path(destination)
    with _NestedSession(archive_path, expected_sha256) as session:
        plan = _nested_plan(session, selected, max_bytes)
        for record in plan["members"]:
            output = destination_path(target / record["outputPath"], directory=False)
            if output.exists() and (not output.is_file() or output.stat().st_size != record["sizeBytes"] or digest(output) != record["sha256"]):
                fail("destination_conflict", "An existing file differs; choose a separate destination.")
        created = []
        try:
            for record in plan["members"]:
                output = no_symlinks(target / record["outputPath"])
                output.parent.mkdir(parents=True, exist_ok=True)
                if output.exists():
                    if not output.is_file() or output.stat().st_size != record["sizeBytes"] or digest(output) != record["sha256"]:
                        fail("destination_conflict", "An existing file changed during nested extraction.")
                    continue
                chain, name = _parts(record["member"])
                view, members, _ = session.open_chain(chain)
                with output.open("xb") as writer:
                    created.append(output)
                    with view.open(members[name]) as reader:
                        written = 0
                        while data := reader.read(CHUNK):
                            written += len(data)
                            if written > record["sizeBytes"]:
                                fail("integrity_failed", "Nested bytes exceeded their planned size.")
                            writer.write(data)
                if output.stat().st_size != record["sizeBytes"] or digest(output) != record["sha256"]:
                    fail("integrity_failed", "Extracted nested bytes failed verification.")
            session.current()
            for record in plan["members"]:
                output = no_symlinks(target / record["outputPath"])
                if not output.is_file() or output.stat().st_size != record["sizeBytes"] or digest(output) != record["sha256"]:
                    fail("integrity_failed", "Selected output bytes changed during nested extraction.")
            receipt = {"version": 2, **{key: plan[key] for key in ("archiveSha256", "selectedMembers", "scope", "members", "containers", "dependencyCoverage", "limitations")}}
            if plan.get("modelRequirements"):
                receipt["modelRequirements"] = plan["modelRequirements"]
            receipt["archiveSizeBytes"] = Path(archive_path).stat().st_size
            receipt.update(receipt_catalog_sources(archive_path, expected_sha256, _catalog_sources, _catalog_metadata_sha256))
            payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
            name = ".catalog-retrieval-" + hashlib.sha256(payload.encode()).hexdigest()[:16] + ".json"
            receipt_path = no_symlinks(target / name)
            if receipt_path.exists():
                if receipt_path.read_text() != payload:
                    fail("destination_conflict", "An existing provenance receipt differs.")
            else:
                with receipt_path.open("x") as writer:
                    created.append(receipt_path)
                    writer.write(payload)
        except BaseException:
            for path in reversed(created):
                path.unlink(missing_ok=True)
            raise
    return {"ok": True, "destination": str(target), "fileCount": len(plan["members"]),
            "fileBytes": sum(record["sizeBytes"] for record in plan["members"]), "receipt": str(receipt_path),
            "provenance": record_extracted_provenance(target, receipt),
            "dependencyCoverage": DEPENDENCY_COVERAGE,
            **model_requirements_summary(plan.get("modelRequirements", [])),
            "limitations": plan["limitations"], "members": plan["members"]}


def metadata_bytes(path, limit):
    path = no_symlinks(path)
    if not stat.S_ISREG(path.stat().st_mode):
        fail("invalid_metadata_input", "Use a local regular file.")
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0)
    with os.fdopen(os.open(path, flags), "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            fail("invalid_metadata_input", "Use a local regular file.")
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        fail("input_too_large", "Read a smaller local input.")
    return raw


def metadata_fields(value, fields):
    value = value if isinstance(value, dict) else {}
    result = {}
    for name, kind in fields.items():
        item = value.get(name)
        valid = ((kind == "number" and type(item) in (int, float) and 0 <= item < 10 ** 15)
                 or (kind == "count" and type(item) is int and 0 <= item < 10 ** 15)
                 or (kind == "bool" and type(item) is bool)
                 or (kind == "text" and isinstance(item, str) and len(item) <= 160))
        result[name] = item if valid else None
    result["unknownFields"] = [name for name in fields if result[name] is None]
    return result


def font_text_coverage(font, text):
    ranges = font.get("unicode_ranges") if isinstance(font, dict) else None
    previous = -1
    valid = isinstance(ranges, list) and bool(ranges)
    for pair in ranges if valid else []:
        if (not isinstance(pair, list) or len(pair) != 2 or any(type(n) is not int for n in pair)
                or not previous < pair[0] <= pair[1] <= 0x10ffff
                or pair[0] <= 0xdfff and pair[1] >= 0xd800):
            valid = False
            break
        previous = pair[1]
    requested = sorted({ord(char) for char in text if char not in "\r\n\t"})
    result = {"status": "known" if valid else "unknown", "requestedCodepoints": len(requested),
              "ignoredLayoutControls": sorted({f"U+{ord(c):04X}" for c in text if c in "\r\n\t"}),
              "allRequestedCovered": None, "renderingChecked": False}
    if not valid:
        result["reason"] = "Missing or malformed measured unicode_ranges."
        return result
    missing = []
    position = 0
    for codepoint in requested:
        while position < len(ranges) and ranges[position][1] < codepoint:
            position += 1
        if position == len(ranges) or codepoint < ranges[position][0]:
            missing.append(codepoint)
    result.update({"allRequestedCovered": not missing, "missingCount": len(missing),
                   "missingCodepoints": [f"U+{n:04X}" for n in missing[:16]],
                   "missingListComplete": len(missing) <= 16})
    return result


def metadata_file(record, text, kind="all"):
    kinds = [kind for kind in ("image", "audio", "font") if kind in record]
    if "atlases" in record:
        kinds.append("atlas")
    if kind != "all":
        kinds = [kind]
    result = {"path": record["path"], "kinds": kinds,
              "sizeBytes": record.get("bytes") if type(record.get("bytes")) is int and record["bytes"] >= 0 else None}
    fields = {
        "image": {"width": "count", "height": "count", "has_transparency": "bool", "animated_frames": "count"},
        "audio": {"duration_seconds": "number", "channels": "count", "sample_rate_hz": "number",
                  "codec": "text", "loopable": "bool", "auditioned": "bool"},
        "font": {"family": "text", "subfamily": "text", "glyph_count": "count",
                 "unicode_codepoint_count": "count", "units_per_em": "count"},
    }
    for kind in kinds:
        if kind in fields:
            result[kind] = metadata_fields(record[kind], fields[kind])
    if "font" in kinds:
        result["font"]["unicodeRangesOmitted"] = True
        if text is not None:
            result["font"]["textCoverage"] = font_text_coverage(record["font"], text)
    if "atlas" in kinds:
        atlases = record["atlases"]
        if not isinstance(atlases, list) or any(not isinstance(a, dict) for a in atlases):
            result["atlases"] = None
            result["atlasStatus"] = "unknown"
        else:
            result["atlasCount"] = len(atlases)
            result["atlasDetailsComplete"] = len(atlases) <= 2
            result["atlases"] = []
            for atlas in atlases[:2]:
                facts = metadata_fields(atlas, {"format": "text", "frame_count": "count", "rectangle_coverage": "text",
                    "tile_width": "number", "tile_height": "number", "spacing_x": "number", "spacing_y": "number",
                    "outer_margin": "number", "columns": "count", "rows": "count", "image_reference": "text"})
                rectangles = atlas.get("frame_rectangles")
                facts["recordedRectangleCount"] = len(rectangles) if isinstance(rectangles, list) else None
                facts["frameRectanglesOmitted"] = True
                result["atlases"].append(facts)
    dependencies = record.get("dependencies")
    result["dependencies"] = ({"recorded": len(dependencies), "statusCounts": {
        status: sum(isinstance(d, dict) and d.get("status") == status for d in dependencies)
        for status in ("present", "missing", "unsafe", "unresolved")},
        "unknownStatusCount": sum(not isinstance(d, dict) or d.get("status") not in ("present", "missing", "unsafe", "unresolved")
                                  for d in dependencies), "pathsOmitted": bool(dependencies)}
        if isinstance(dependencies, list) else None)
    return result


def selection_members(value):
    selection = value.get("selection")
    if selection is None:
        return {}
    if (not isinstance(selection, dict) or selection.get("purpose_coverage") not in ("complete", "partial", "unknown")
            or not isinstance(selection.get("members"), list) or len(selection["members"]) > 128):
        fail("invalid_selection_evidence", "Inspect the sidecar's member-purpose evidence.")
    members = {}
    allowed = {"runtime_asset", "preview", "reference", "support", "source", "unknown"}
    for item in selection["members"]:
        if not isinstance(item, dict):
            fail("invalid_selection_evidence", "Member-purpose records must be objects.")
        name = relative_name(item.get("path"))
        basename = name.rsplit("/", 1)[-1]
        extension = basename.rsplit(".", 1)[-1].lower() if "." in basename else ""
        purposes, evidence = item.get("purposes"), item.get("evidence")
        if (name in members or not isinstance(purposes, list) or not purposes or len(purposes) > len(allowed)
                or any(not isinstance(p, str) or p not in allowed for p in purposes)
                or len(set(purposes)) != len(purposes)
                or ("unknown" in purposes and len(purposes) != 1)
                or item.get("basis") not in ("source_declared", "filename_clue", "measured")
                or not isinstance(item.get("format"), str) or not re.fullmatch(r"(?:[a-z0-9][a-z0-9_-]{0,31})?", item["format"])
                or item["format"] != extension
                or not isinstance(evidence, list) or not evidence or len(evidence) > 8
                or any(not isinstance(e, str) or not e or len(e) > 256 or "://" in e
                       or any(unicodedata.category(c) == "Cc" for c in e) for e in evidence)):
            fail("invalid_selection_evidence", "Inspect the sidecar's exact member-purpose fields.")
        hash_value(item.get("sha256"))
        members[name] = item
    coverage = selection["purpose_coverage"]
    if ((coverage == "complete" and (not members or any("unknown" in item["purposes"] for item in members.values())))
            or (coverage == "unknown" and any(item["purposes"] != ["unknown"] for item in members.values()))):
        fail("invalid_selection_evidence", "Purpose coverage disagrees with its member evidence.")
    for record in value.get("files", []):
        if isinstance(record, dict) and record.get("path") in members and record.get("sha256") is not None:
            if record["sha256"] != members[record["path"]]["sha256"]:
                fail("invalid_selection_evidence", "Member-purpose and measurement content identities disagree.")
    return members


def selection_summary(item):
    if item is None:
        return {"purposes": ["unknown"], "basis": None}
    return {"format": item["format"], "purposes": item["purposes"], "basis": item["basis"],
            "evidence": item["evidence"][:2], "omittedEvidence": max(0, len(item["evidence"]) - 2)}


def runtime_records(value):
    if not isinstance(value, dict) or value.get("schema") != "game-asset-runtime-metadata/v1":
        fail("invalid_metadata_schema", "Use a game-asset-runtime-metadata/v1 sidecar; publisher metadata is a different input.")
    if "files" in value and not isinstance(value["files"], list):
        fail("invalid_metadata_schema", "Runtime metadata files must be an array when present; omit files for summary-only coverage.")
    return value.get("files", [])


SUMMARY_MEMBER_ACTION = ("Use exact member paths and supplied facts from metadata.json or asset-catalog-index.json directly; "
                        "do not inspect archive members to reconfirm them. Only if a required exact path is absent there, "
                        "use a bounded members --archive query. Summary counts do not establish missing member measurements; "
                        "inspect only required technical facts absent from published metadata.")


def inspect_metadata(path, *, kind="all", member=None, text_path=None, limit=5, offset=0):
    if kind not in ("all", "image", "audio", "font", "atlas") or not 1 <= limit <= 20 or offset < 0:
        fail("invalid_metadata_options", "Use limit 1–20, a nonnegative offset and a supported kind.")
    if member is not None:
        relative_name(member)
    value = json.loads(metadata_bytes(path, MAX_METADATA))
    records = runtime_records(value)
    summary_only = "files" not in value
    text = metadata_bytes(text_path, 64 * 1024).decode("utf-8") if text_path is not None else None
    files, names = [], set()
    for record in records:
        if not isinstance(record, dict):
            fail("invalid_metadata_schema", "Measured file records must be objects with exact member paths.")
        name = relative_name(record.get("path"))
        if name in names:
            fail("invalid_metadata_schema", "Measured member paths must be unique.")
        names.add(name)
        if (member is None or name == member) and (kind == "all" or ("atlases" if kind == "atlas" else kind) in record):
            files.append(record)
    selected = selection_members(value)
    if member is not None and member not in names and member in selected and kind == "all":
        files.append({"path": member})
    if member is not None and member not in names and member not in selected and not summary_only:
        fail("member_not_measured", "This sidecar has no record for the selected member. Use its path and supplied facts from "
             "metadata.json or asset-catalog-index.json directly; do not inspect archive members to reconfirm them. "
             "Inspect only required technical facts absent from published metadata. This does not establish archive absence.")
    files.sort(key=lambda record: record["path"])
    coverage = value.get("coverage") if isinstance(value.get("coverage"), dict) else {}
    result = {"ok": True, "schema": value["schema"], "status": "summary_only" if summary_only else "available",
              "measuredFileCount": len(names), "matchingFileCount": len(files),
              "sourceCoverage": {key: metadata_fields(coverage.get(key), {"available": "count", "selected": "count", "inspected": "count"})
                                 for key in ("image", "audio", "font", "descriptor")},
              "coverageNote": "Unmeasured files and missing fields remain unknown.",
              "offset": offset, "nextOffset": None, "pageComplete": True, "outputLimited": False, "files": []}
    if summary_only:
        result["summary"] = metadata_fields(value.get("summary"), {
            "inspected_files": "count", "images": "count", "audio_files": "count", "fonts": "count",
            "authored_atlases": "count", "missing_dependencies": "count", "all_supported_files_inspected": "bool"})
        result["nextAction"] = SUMMARY_MEMBER_ACTION
        if member is not None:
            result["requestedMember"] = member
    limitations = value.get("limitations")
    result["sourceLimitationCount"] = len(limitations) if isinstance(limitations, list) else None
    result["sourceLimitations"] = [s for s in limitations[:2] if isinstance(s, str) and len(s) <= 180] if isinstance(limitations, list) else []
    result["sourceLimitationsComplete"] = isinstance(limitations, list) and len(result["sourceLimitations"]) == len(limitations)

    def output_size(candidate):
        return len(json.dumps(candidate, sort_keys=True, ensure_ascii=False)) + 1

    for record in files[offset:offset + limit]:
        projected = metadata_file(record, text, kind)
        if record["path"] in selected:
            projected["selection"] = selection_summary(selected[record["path"]])
        result["files"].append(projected)
        if output_size(result) > MAX_METADATA_OUTPUT - 100:
            result["files"].pop()
            result["outputLimited"] = True
            if result["files"]:
                break
            result["files"].append({"path": record["path"], "kinds": projected["kinds"], "detailsOmitted": True,
                                    "reason": "Measured detail exceeds the compact output budget."})
    end = offset + len(result["files"])
    result["pageComplete"] = end >= len(files)
    result["nextOffset"] = None if result["pageComplete"] else end
    if output_size(result) > MAX_METADATA_OUTPUT:
        fail("metadata_output_too_large", "The selected metadata cannot fit the compact output budget.")
    return result


def validate_member_query(query, limit, offset):
    if (not isinstance(query, str) or len(query) > 256 or type(limit) is not int or not 1 <= limit <= 100
            or type(offset) is not int or offset < 0 or any(ord(c) < 32 for c in query)):
        fail("invalid_member_query", "Use a query of at most 256 characters, limit 1–100 and a nonnegative offset.")


def find_members(path=None, *, archive_path=None, expected_sha256=None, query="", limit=5, offset=0, _retrieval=None,
                 max_archive_bytes=None, case_sensitive_members=False):
    archive_options(max_archive_bytes, case_sensitive_members)
    if archive_path is None and (max_archive_bytes is not None or case_sensitive_members):
        fail("invalid_member_query", "Archive overrides require a hash-verified local or granted ZIP.")
    validate_member_query(query, limit, offset)
    normalize = lambda text: unicodedata.normalize("NFKC", text).casefold()
    terms = list(dict.fromkeys(normalize(query).split()))
    if (path is None) == (archive_path is None) or (archive_path is None and expected_sha256 is not None):
        fail("invalid_member_query", "Use one runtime/inventory --file, or --archive with its catalog --sha256.")
    if archive_path is not None:
        hash_value(expected_sha256)
        archive_path = no_symlinks(archive_path)
        require_zip(archive_path)
        if digest(archive_path) != expected_sha256:
            fail("integrity_failed", "Archive bytes differ from the expected catalog object.")
        _zip_directory_bound(archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            value = [{"path": name, "sizeBytes": entry.file_size, "directory": entry.is_dir()}
                     for name, entry in zip_inventory(archive, max_archive_bytes=max_archive_bytes,
                                                      case_sensitive_members=case_sensitive_members).items()]
        if digest(archive_path) != expected_sha256:
            fail("integrity_failed", "Source archive changed during member inspection.")
    else:
        value = json.loads(metadata_bytes(path, MAX_METADATA))
    selected, records, names = {}, {}, set()
    if isinstance(value, dict) and value.get("schema") == "game-asset-runtime-metadata/v1":
        scope = "sidecar_members"
        measured = runtime_records(value)
        selected = selection_members(value)
        for record in measured:
            if not isinstance(record, dict):
                fail("invalid_metadata_schema", "Measured member records must be objects.")
            name = relative_name(record.get("path"))
            if name in names:
                fail("invalid_metadata_schema", "Measured member paths must be unique.")
            names.add(name)
            records[name] = record
        measured_count = len(names)
        for name in selected:
            records.setdefault(name, {"path": name})
        coverage = {"scope": scope, "measuredFileCount": measured_count, "selectionMemberCount": len(selected),
                    "purposeCoverage": (value.get("selection") or {}).get("purpose_coverage", "unknown"),
                    "measurementStatus": "summary_only" if "files" not in value else "available",
                    "note": "Only listed measured or declared members are searched; a miss does not establish archive absence."}
    elif isinstance(value, list) and len(value) <= 100_000:
        scope = "supplied_archive_inventory"
        for record in value:
            if (not isinstance(record, dict) or type(record.get("directory")) is not bool
                    or type(record.get("sizeBytes")) is not int or not 0 <= record["sizeBytes"] < 10 ** 15):
                fail("invalid_member_inventory", "Use the full JSON array saved by inspect --output, not its stdout sample.")
            name = relative_name(record.get("path"))
            if name in names:
                fail("invalid_member_inventory", "Saved member paths must be unique.")
            names.add(name)
            if not record["directory"]:
                records[name] = {"path": name, "bytes": record["sizeBytes"]}
        coverage = {"scope": scope, "inventoryEntryCount": len(names), "purposeCoverage": "unknown",
                    "measurementStatus": "not_supplied",
                    "note": "Searches the supplied saved array, not the archive; completeness depends on using inspect's full output."}
        if archive_path is not None:
            coverage.update(scope="verified_archive_inventory", archiveSha256=expected_sha256,
                            note="Searches every safe member name in the hash-verified ZIP; geometry and visual facing remain unmeasured.")
    else:
        fail("invalid_member_inventory", "Use a runtime sidecar or the full JSON array saved by inspect --output, not stdout.")
    matches = [record for name, record in sorted(records.items()) if all(term in normalize(name) for term in terms)]
    if offset > len(matches):
        fail("invalid_member_query", "The offset exceeds matching members; restart with the same input and query.")
    result = {"ok": True, "query": query, "matchMode": "literal_path_terms", "coverage": coverage,
              "inputFileCount": len(records), "matchingFileCount": len(matches), "offset": offset,
              "nextOffset": None, "pageComplete": True, "outputLimited": False, "files": []}
    if _retrieval is not None:
        result.update(_retrieval)
    if coverage.get("measurementStatus") == "summary_only" and not matches:
        result["nextAction"] = SUMMARY_MEMBER_ACTION
    def size():
        return len(json.dumps(result, sort_keys=True, ensure_ascii=False)) + 1
    for record in matches[offset:offset + limit]:
        if coverage["scope"] == "sidecar_members":
            projected = metadata_file(record, None)
            projected["selection"] = selection_summary(selected.get(record["path"]))
        else:
            projected = {"path": record["path"], "sizeBytes": record["bytes"]}
        result["files"].append(projected)
        if size() > MAX_METADATA_OUTPUT - 100:
            result["files"].pop()
            result["outputLimited"] = True
            if result["files"]:
                break
            result["files"].append({"path": record["path"], "detailsOmitted": True,
                                    "nextAction": "Inspect this exact member in the supplied local metadata."})
    end = offset + len(result["files"])
    result["pageComplete"] = end >= len(matches)
    result["nextOffset"] = None if result["pageComplete"] else end
    if size() > MAX_METADATA_OUTPUT:
        fail("metadata_output_too_large", "Shorten the query or inspect the exact local member.")
    return result


def inspect_batch(request, grant, cache_dir, max_total_bytes, opener=None):
    candidates = request.get("candidates") if isinstance(request, dict) else None
    if not isinstance(candidates, list) or not 1 <= len(candidates) <= 8:
        fail("invalid_inspection_request", "Inspect 1–8 candidates in one request.")
    body = grant_body(grant)
    snapshot, entries = grant_items(body)
    if not snapshot or len(snapshot) > 128:
        fail("invalid_inspection_request", "Use the current catalog snapshot identifier.")
    descriptors = {entry["path"]: entry for entry in entries}
    if len(descriptors) != len(entries):
        fail("invalid_inspection_request", "The access response contains duplicate paths.")
    needed, prepared, seen, archives = set(), [], set(), set()
    for item in candidates:
        if not isinstance(item, dict):
            fail("invalid_inspection_request", "Each candidate must be an object.")
        metadata_path = relative_name(item.get("metadataPath"))
        archive_path = relative_name(item.get("archivePath"))
        pack = str(PurePosixPath(metadata_path).parent)
        if (PurePosixPath(metadata_path).name != "metadata.json" or pack == "."
                or archive_path != pack + "/assets.zip" or metadata_path in seen):
            fail("invalid_inspection_request", "Use distinct canonical collection metadata and archive paths.")
        seen.add(metadata_path)
        archives.add(archive_path)
        if item.get("member") is not None:
            relative_name(item["member"])
        runtime_path = item.get("runtimeMetadataPath")
        if runtime_path is not None:
            relative_name(runtime_path)
            if not re.fullmatch(re.escape(pack) + r"/runtime-metadata(?:\.[0-9a-f]{64})?\.json", runtime_path):
                fail("invalid_inspection_request", "Use the runtime sidecar returned for this collection.")
        selected = [metadata_path, *([runtime_path] if runtime_path is not None else [])]
        if any(path not in descriptors for path in [*selected, archive_path]):
            fail("missing_inspection_file", "Request selected metadata paths and the archive descriptor through access.")
        if any(descriptors[path]["sizeBytes"] > MAX_METADATA for path in selected):
            fail("input_too_large", "An inspection object exceeds the local input bound.")
        if item.get("kind", "all") not in ("all", "image", "audio", "font", "atlas"):
            fail("invalid_inspection_request", "Use kind all (default), image, audio, font or atlas.")
        needed.update(selected)
        prepared.append((item, pack, metadata_path, archive_path, runtime_path))
    if needed & archives:
        fail("invalid_inspection_request", "Inspection cannot transfer candidate archives.")
    if sum(descriptors[path]["sizeBytes"] for path in needed) > max_total_bytes:
        fail("download_budget_exceeded", "Selected inspection files exceed --max-total-bytes.")
    # Legacy evidencePaths, reviewFile and members inputs are accepted but unused.
    # Catalog admission is complete; this command inspects only technical facts.
    try:
        fetched = fetch_grants({**body, "files": [descriptors[path] for path in sorted(needed)]},
                               cache_dir, max_total_bytes, opener=opener)
    except CatalogError as error:
        if error.result["code"] == "renewal_required":
            # A retry also needs archive descriptors for source binding, even
            # though inspection never downloads their bytes.
            error.result["accessRequest"] = {"snapshotId": snapshot, "paths": sorted(needed | archives)}
        raise
    local = {entry["path"]: entry["cachePath"] for entry in fetched["files"]}
    results = []
    for index, (item, pack, metadata_path, archive_path, runtime_path) in enumerate(prepared):
        result = {"candidate": index, "metadataPath": metadata_path, "metadataCachePath": local[metadata_path]}
        try:
            metadata = json.loads(metadata_bytes(local[metadata_path], MAX_METADATA))
            if not isinstance(metadata, dict):
                fail("invalid_inspection_input", "Collection metadata must be a JSON object.")
            result["source"] = {key: metadata[key] for key in ("id", "name")
                                if isinstance(metadata.get(key), str) and len(metadata[key]) <= 160}
            if runtime_path is not None:
                result["runtimeCachePath"] = local[runtime_path]
                runtime = json.loads(metadata_bytes(local[runtime_path], MAX_METADATA))
                source = runtime.get("source") if isinstance(runtime, dict) else None
                semantic_metadata = {key: value for key, value in metadata.items() if key != "runtime_metadata"}
                semantic_hash = hashlib.sha256(json.dumps(semantic_metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
                if (not isinstance(source, dict) or runtime.get("collection_path") != pack
                        or runtime.get("path_basis") != "archive-relative"
                        or source.get("metadata_content_sha256") != semantic_hash
                        or source.get("archive_sha256") != descriptors[archive_path]["sha256"]
                        or source.get("archive_bytes") != descriptors[archive_path]["sizeBytes"]):
                    result["runtime"] = {"status": "source_mismatch", "files": []}
                else:
                    result["runtime"] = inspect_metadata(local[runtime_path], kind=item.get("kind", "all"),
                                                          member=item.get("member"), text_path=item.get("textFile"), limit=1)
            else:
                result["runtime"] = {"status": "unavailable", "files": []}
        except CatalogError as error:
            result["error"] = {key: error.result[key] for key in ("code", "message")}
        except (ValueError, TypeError, KeyError, OSError):
            result["error"] = {"code": "invalid_inspection_input", "message": "Inspect this candidate's local metadata and runtime files."}
        results.append(result)
    return {"ok": True, "snapshotId": snapshot, "results": results,
            "downloads": {"objects": len(fetched["files"]), "reused": sum(entry["reused"] for entry in fetched["files"]),
                          "transferredBytes": sum(entry["sizeBytes"] for entry in fetched["files"] if not entry["reused"])}}


def compact_batch(report, output=None):
    result = {key: report[key] for key in ("ok", "snapshotId", "downloads")}
    result.update(resultCount=len(report["results"]), results=[], detailsOmitted=False, outputPath=output)
    def length(value):
        return len(json.dumps(value, sort_keys=True, ensure_ascii=False)) + 1
    for item in report["results"]:
        compact = {key: item[key] for key in ("candidate", "error") if key in item}
        if "runtime" in item and "status" in item["runtime"]:
            compact["runtime"] = {"status": item["runtime"]["status"]}
        result["results"].append(compact)
    for item, compact in zip(report["results"], result["results"]):
        additions = {key: item[key] for key in ("metadataPath", "metadataCachePath", "runtimeCachePath", "source") if key in item}
        if "runtime" in item:
            runtime = item["runtime"]
            additions["runtime"] = {key: runtime[key] for key in ("status", "files", "nextOffset", "matchingFileCount", "sourceCoverage", "summary", "requestedMember", "nextAction") if key in runtime}
        for key, value in additions.items():
            previous = compact.get(key)
            compact[key] = value
            if length(result) > MAX_METADATA_OUTPUT - 200:
                if previous is None:
                    compact.pop(key)
                else:
                    compact[key] = previous
                compact["detailsOmitted"] = True
                result["detailsOmitted"] = True
    result["omittedResults"] = 0
    if length(result) > MAX_METADATA_OUTPUT:
        fail("inspection_output_too_large", "Use a shorter output path or a smaller inspection batch.")
    return result


def compact_inspection_error(value):
    result = {key: value[key] for key in ("ok", "code", "message")}
    if value["code"] != "renewal_required":
        return result
    request = value.get("accessRequest")
    valid = (isinstance(request, dict) and isinstance(request.get("snapshotId"), str)
             and 0 < len(request["snapshotId"]) <= 128 and isinstance(request.get("paths"), list)
             and 1 <= len(request["paths"]) <= 32)
    if valid:
        try:
            paths = [relative_name(path) for path in request["paths"]]
            valid = len(set(paths)) == len(paths)
        except CatalogError:
            valid = False
    if valid:
        retry = {**result, "accessRequest": {"snapshotId": request["snapshotId"], "paths": paths}}
        if len(json.dumps(retry, sort_keys=True)) + 1 <= MAX_METADATA_OUTPUT:
            return retry
        result["snapshotId"] = request["snapshotId"]
    result.update(accessRequestOmitted=True,
        nextAction="Repeat the original inspection access request with the same snapshot and paths. Rerun inspect-batch with the new saved grant and existing cache.")
    return result


def nested_cli_report(report, output=None):
    if output:
        payload = json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n"
        path = no_symlinks(output)
        if path.exists():
            if not path.is_file() or path.stat().st_size != len(payload.encode("utf-8")) or path.read_bytes() != payload.encode("utf-8"):
                fail("destination_conflict", "An existing nested report differs; choose a fresh output path.")
        else:
            with path.open("x", encoding="utf-8") as writer:
                writer.write(payload)
    compact = {key: report[key] for key in ("ok", "schema", "archiveSha256", "format", "memberCount",
                "offset", "nextOffset", "selectedBytes", "limitations") if key in report}
    compact.update({"members": [], "detailsPath": str(output) if output else None,
                    "returnedMembers": len(report["members"]), "detailsOmitted": True})
    size = lambda value: len(json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    if size(compact) > 3000:
        fail("inspection_output_too_large", "Use a shorter nested report output path.")
    for member in report["members"]:
        if size({**compact, "members": compact["members"] + [member]}) > 3500:
            break
        compact["members"].append(member)
    compact["omittedMembers"] = len(report["members"]) - len(compact["members"])
    compact["nextAction"] = "Read the full report at detailsPath." if output else "Use --output to retain complete locators, dependency scope and container identities."
    return compact


def fetch_selected_archive(grant, archive_path, cache_dir, max_total_bytes=256 * CHUNK, *, destination=None, opener=None):
    archive_path = relative_name(archive_path)
    if not archive_path.endswith("/assets.zip"):
        fail("invalid_archive_path", "Use the exact collection archivePath returned by catalog search.")
    if type(max_total_bytes) is not int or max_total_bytes < 0:
        fail("invalid_retrieval_budget", "Use a nonnegative integer download byte budget.")
    if cache_dir is None:
        fail("invalid_member_query", "Grant-driven member discovery requires --cache-dir.")
    body = grant_body(grant)
    snapshot, entries = grant_items(body)
    descriptors = {entry["path"]: entry for entry in entries}
    if len(descriptors) != len(entries):
        fail("invalid_grant", "The access response contains duplicate paths.")
    if archive_path not in descriptors:
        fail("missing_archive_grant", "Request this exact archivePath with webdev.access_game_assets.")
    archive = descriptors[archive_path]
    metadata_path = archive_path.rsplit("/", 1)[0] + "/metadata.json"
    metadata = descriptors.get(metadata_path)
    if archive.get("metadata") is not None:
        # The optional descriptor is part of the private, manifest-bound access result.
        # Never fetch a neighboring collection or copy its grant into project evidence.
        nested = archive["metadata"]
        if not isinstance(nested, dict) or nested.get("path") != metadata_path:
            fail("invalid_grant", "Archive metadata must name the same collection's metadata.json.")
        grant_items({"snapshotId": snapshot, "files": [nested]})
        if metadata and any(metadata[key] != nested[key] for key in ("sha256", "sizeBytes")):
            fail("invalid_grant", "The access response contains conflicting metadata identities.")
        metadata = nested
    fetched = fetch_grants({**body, "files": [archive]}, cache_dir, max_total_bytes,
                           destination=destination, opener=opener)
    if metadata is not None:
        # Enrichment is optional: retain the archive's existing availability and budget.
        # Binding the selected digest also prevents fallback to stale cached facts.
        fetched["_catalogMetadataSha256"] = metadata["sha256"]
        remaining = max_total_bytes - archive["sizeBytes"]
        if metadata["sizeBytes"] <= remaining:
            try:
                fetch_grants({**body, "files": [metadata]}, cache_dir, remaining,
                             destination=destination, opener=opener)
            except CatalogError as error:
                if error.result["code"] not in ("download_failed", "download_interrupted", "renewal_required", "cache_busy"):
                    raise
                # Only transport, expired-grant and cache-contention failures are optional. Invalid paths,
                # conflicting identities and byte-integrity failures remain errors.
    return fetched


def retrieval_summary(fetched):
    local = fetched["files"][0]
    return {"snapshotId": fetched["snapshotId"], "archivePath": local["path"],
            "download": {"cachePath": local["cachePath"], "sha256": local["sha256"],
                         "sizeBytes": local["sizeBytes"], "reused": local["reused"]}}


def find_granted_members(grant, archive_path, cache_dir, *, query="", limit=5, offset=0,
                         max_total_bytes=256 * CHUNK, opener=None, max_archive_bytes=None, case_sensitive_members=False):
    archive_options(max_archive_bytes, case_sensitive_members)
    validate_member_query(query, limit, offset)
    fetched = fetch_selected_archive(grant, archive_path, cache_dir, max_total_bytes, opener=opener)
    local = fetched["files"][0]
    return find_members(archive_path=local["cachePath"], expected_sha256=local["sha256"],
                        query=query, limit=limit, offset=offset, _retrieval=retrieval_summary(fetched),
                        max_archive_bytes=max_archive_bytes, case_sensitive_members=case_sensitive_members)


def retrieve_selected(grant, archive_path, selected, cache_dir, destination,
                      max_total_bytes=256 * CHUNK, max_bytes=256 * CHUNK, opener=None, *,
                      max_archive_bytes=None, case_sensitive_members=False):
    """Compose existing destination, download and extraction checks for one selected pack."""
    archive_options(max_archive_bytes, case_sensitive_members)
    if (isinstance(selected, list) and any(isinstance(member, dict) for member in selected)
            and (max_archive_bytes is not None or case_sensitive_members)):
        fail("invalid_retrieval_budget", "Archive overrides apply to flat ZIP member paths only.")
    destination_path(destination)
    selected = normalize_member_scope(selected)
    if type(max_bytes) is not int or max_bytes < 0:
        fail("invalid_retrieval_budget", "Use a nonnegative integer extraction byte budget.")
    fetched = fetch_selected_archive(grant, archive_path, cache_dir, max_total_bytes, destination=destination, opener=opener)
    local = fetched["files"][0]
    result = extract(local["cachePath"], selected, destination, local["sha256"], max_bytes,
                     max_archive_bytes=max_archive_bytes, case_sensitive_members=case_sensitive_members,
                     _catalog_sources=[catalog_source(fetched["snapshotId"], {"path": local["path"]})],
                     _catalog_metadata_sha256=fetched.get("_catalogMetadataSha256"))
    # Nested extraction keeps its full scope in the durable receipt, like extract's CLI.
    if "members" in result:
        result.pop("members")
        result["membersInReceipt"] = True
    result.update(retrieval_summary(fetched))
    return result


def main():
    parser = argparse.ArgumentParser(description="Retrieve selected Manus catalog files on the current execution target.")
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch")
    fetch.add_argument("--grant-file", required=True)
    fetch.add_argument("--cache-dir", required=True)
    fetch.add_argument("--destination")
    fetch.add_argument("--max-total-bytes", type=int, default=256 * CHUNK)
    retrieve = sub.add_parser("retrieve", help="Validate the destination, fetch one granted archive and extract exact selected members.")
    for flag in ("grant-file", "archive-path", "members-file", "cache-dir", "destination"):
        retrieve.add_argument(f"--{flag}", required=True)
    retrieve.add_argument("--max-total-bytes", type=int, default=256 * CHUNK)
    retrieve.add_argument("--max-bytes", type=int, default=256 * CHUNK)
    sub.add_parser("capabilities", help="Report nested archive parser availability and bounds.")
    nested = sub.add_parser("inspect-nested", help="Inspect one exact container chain; --output retains the complete page.")
    for flag in ("archive", "containers-file", "sha256"):
        nested.add_argument(f"--{flag}", required=True)
    nested.add_argument("--limit", type=int, default=20)
    nested.add_argument("--offset", type=int, default=0)
    nested.add_argument("--output")
    planned = sub.add_parser("plan-nested", help="Plan exact nested members and dependency scope without extracting.")
    for flag in ("archive", "members-file", "sha256"):
        planned.add_argument(f"--{flag}", required=True)
    planned.add_argument("--max-bytes", type=int, default=256 * CHUNK)
    planned.add_argument("--output")
    inspect = sub.add_parser("inspect")
    inspect.add_argument("--archive", required=True)
    inspect.add_argument("--output")
    inspect.add_argument("--sha256", help="Required catalog digest when using archive overrides.")
    metadata = sub.add_parser("metadata")
    metadata.add_argument("--file", required=True)
    metadata.add_argument("--kind", choices=("all", "image", "audio", "font", "atlas"), default="all")
    metadata.add_argument("--member")
    metadata.add_argument("--text-file")
    metadata.add_argument("--limit", type=int, default=5)
    metadata.add_argument("--offset", type=int, default=0)
    members = sub.add_parser("members")
    member_input = members.add_mutually_exclusive_group(required=True)
    member_input.add_argument("--file")
    member_input.add_argument("--archive")
    member_input.add_argument("--grant-file")
    members.add_argument("--sha256")
    members.add_argument("--archive-path")
    members.add_argument("--cache-dir")
    members.add_argument("--max-total-bytes", type=int)
    members.add_argument("--query", default="")
    members.add_argument("--limit", type=int, default=5)
    members.add_argument("--offset", type=int, default=0)
    batch = sub.add_parser("inspect-batch")
    batch.add_argument("--request-file", required=True,
                       help="JSON request with candidates[].kind: all (default), image, audio, font or atlas.")
    for flag in ("grant-file", "cache-dir"):
        batch.add_argument(f"--{flag}", required=True)
    batch.add_argument("--max-total-bytes", type=int, default=32 * CHUNK)
    batch.add_argument("--output")
    check = sub.add_parser("check-destination")
    check.add_argument("--destination", required=True)
    unpack = sub.add_parser("extract")
    for flag in ("archive", "members-file", "destination", "sha256"):
        unpack.add_argument(f"--{flag}", required=True)
    unpack.add_argument("--max-bytes", type=int, default=256 * CHUNK)
    for command in (retrieve, inspect, members, unpack):
        command.add_argument("--max-archive-bytes", type=int,
                             help="Explicit total expanded ZIP byte bound, at most 8 GiB; replaces default member/ratio heuristics for a verified archive.")
        command.add_argument("--case-sensitive-members", action="store_true",
                             help="Allow exact case-variant ZIP names; output paths must remain collision-free.")
    args = parser.parse_args()
    try:
        if args.command == "capabilities":
            result = {"ok": True, **capabilities()}
        elif args.command == "inspect-nested":
            report = inspect_nested(args.archive, read_json(args.containers_file), expected_sha256=args.sha256,
                                    limit=args.limit, offset=args.offset)
            result = nested_cli_report(report, args.output)
        elif args.command == "plan-nested":
            result = nested_cli_report(plan_nested(args.archive, read_json(args.members_file), args.sha256, args.max_bytes), args.output)
        elif args.command == "fetch":
            result = fetch_grants(read_json(args.grant_file), args.cache_dir, args.max_total_bytes, args.destination)
        elif args.command == "retrieve":
            result = retrieve_selected(read_json(args.grant_file), args.archive_path, read_json(args.members_file),
                                       args.cache_dir, args.destination, args.max_total_bytes, args.max_bytes,
                                       max_archive_bytes=args.max_archive_bytes, case_sensitive_members=args.case_sensitive_members)
        elif args.command == "check-destination":
            result = {"ok": True, "destination": str(destination_path(args.destination))}
        elif args.command == "extract":
            result = extract(args.archive, read_json(args.members_file), args.destination, args.sha256, args.max_bytes,
                             max_archive_bytes=args.max_archive_bytes, case_sensitive_members=args.case_sensitive_members)
            if "members" in result:
                result.pop("members")
                result["membersInReceipt"] = True
        elif args.command == "metadata":
            result = inspect_metadata(args.file, kind=args.kind, member=args.member, text_path=args.text_file,
                                      limit=args.limit, offset=args.offset)
        elif args.command == "members":
            if args.grant_file:
                if args.sha256 is not None or args.archive_path is None or args.cache_dir is None:
                    fail("invalid_member_query", "Use --grant-file with --archive-path and --cache-dir; its grant supplies the archive digest.")
                result = find_granted_members(read_json(args.grant_file), args.archive_path, args.cache_dir,
                    query=args.query, limit=args.limit, offset=args.offset,
                    max_total_bytes=args.max_total_bytes if args.max_total_bytes is not None else 256 * CHUNK,
                    max_archive_bytes=args.max_archive_bytes, case_sensitive_members=args.case_sensitive_members)
            else:
                if args.archive_path is not None or args.cache_dir is not None or args.max_total_bytes is not None:
                    fail("invalid_member_query", "Grant/cache options require --grant-file; use --archive with --sha256 for a local ZIP.")
                result = find_members(args.file, archive_path=args.archive, expected_sha256=args.sha256,
                                      query=args.query, limit=args.limit, offset=args.offset,
                                      max_archive_bytes=args.max_archive_bytes, case_sensitive_members=args.case_sensitive_members)
        elif args.command == "inspect-batch":
            report = inspect_batch(read_json(args.request_file), read_json(args.grant_file), args.cache_dir, args.max_total_bytes)
            if args.output:
                payload = json.dumps(report, sort_keys=True, ensure_ascii=False) + "\n"
                path = no_symlinks(args.output)
                if path.exists():
                    if metadata_bytes(path, MAX_METADATA).decode("utf-8") != payload:
                        fail("destination_conflict", "An existing inspection output differs; choose a fresh output path.")
                else:
                    with path.open("x") as writer:
                        writer.write(payload)
            result = compact_batch(report, args.output)
        else:
            archive_options(args.max_archive_bytes, args.case_sensitive_members)
            require_zip(args.archive)
            if args.max_archive_bytes is not None or args.case_sensitive_members or args.sha256 is not None:
                hash_value(args.sha256)
                if digest(args.archive) != args.sha256:
                    fail("integrity_failed", "Archive bytes differ from the expected catalog object.")
                _zip_directory_bound(args.archive)
            with zipfile.ZipFile(args.archive) as archive:
                entries = [{"path": n, "sizeBytes": i.file_size, "directory": i.is_dir()}
                           for n, i in zip_inventory(archive, max_archive_bytes=args.max_archive_bytes,
                                                     case_sensitive_members=args.case_sensitive_members).items()]
            if args.sha256 is not None and digest(args.archive) != args.sha256:
                fail("integrity_failed", "Source archive changed during member inspection.")
            if args.output:
                with no_symlinks(args.output).open("x") as output:
                    json.dump(entries, output)
            sample = []
            for entry in entries[:20]:
                if len(json.dumps(sample + [entry])) > 2500:
                    break
                sample.append(entry)
            result = {"ok": True, "memberCount": len(entries), "members": sample, "complete": len(entries) == len(sample),
                      "inventoryPath": args.output}
        print(json.dumps(result, sort_keys=True, ensure_ascii=args.command not in ("metadata", "inspect-batch", "members", "inspect-nested", "plan-nested")))
        return 0
    except CatalogError as error:
        value = error.result
        if args.command == "inspect-batch":
            value = compact_inspection_error(value)
        elif args.command in ("inspect-nested", "plan-nested"):
            value = {key: value[key] for key in ("ok", "code", "message")}
        print(json.dumps(value, sort_keys=True))
    except (OSError, ValueError, TypeError, KeyError, zipfile.BadZipFile, RuntimeError):
        print(json.dumps({"ok": False, "code": "input_or_io_error", "message": "Inspect local inputs, file permissions and archive integrity, then retry."}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
