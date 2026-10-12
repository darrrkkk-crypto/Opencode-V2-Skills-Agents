# Catalog retrieval and recovery

Read only for a concrete missing path/fact or retrieval failure. Ordinary known-member retrieval is in
[SKILL.md](../SKILL.md#select-and-retrieve). Published facts need no remeasurement or new admission/license audit.
Use existing verified cache, preserve snapshot/source identity and exact paths, and never execute archive content.

## Missing member paths

Reuse metadata/index and available sidecar/inventory first. Summary-only runtime metadata or omitted search samples
do not invalidate canonical member paths. Only if an essential exact path remains missing, query bounded literal terms:
```sh
node "$SKILL_DIR/scripts/retrieve.mjs" members --grant-file "$ACCESS_RESULT" --archive-path "$ARCHIVE_PATH" --cache-dir "$CACHE" --query "craft .png" --limit 100 --max-total-bytes 268435456
```
Already local: members --archive "$ARCHIVE" --sha256 "$ARCHIVE_HASH", no new access/download. Terms are case-insensitive
substrings in the same path, not Boolean/negation/fuzzy expressions. Limit 1–100, stdout ≤4,000 characters; follow
nextOffset with same input/query only as needed. Never infer N/E/S/W filenames from NE/NW/SE/SW members. Preserve actual facings/wrappers/Unicode; names/sizes prove no geometry.
Use download.cachePath/sha256 for extraction; once path is supplied, extract directly without inspecting it again.

Only when a complete inventory is genuinely needed and absent, Python `retrieve.py inspect --output` saves the full JSON ARRAY of
{path,sizeBytes,directory}. Stdout's ≤20 samples/complete:false describes display, not the saved array.
Legacy inventory_snapshot/inventory_record_index need both valid fields. Python `retrieve.py members --file "$MEMBER_INVENTORY"`
accepts that array or member-bearing sidecar; stdout samples are rejected. supplied_archive_inventory excludes
directories; sidecar_members covers measured plus declared members. No ZIP re-verification, transfer or extraction
in --file/local archive modes. pageComplete is page scope; nextOffset advances returned rows.
A verified_archive_inventory establishes safe ZIP names/sizes, not purpose/geometry/full catalog coverage.

## Missing technical facts

Publisher metadata is heterogeneous. Runtime game-asset-runtime-metadata/v1 sidecars may contain measured files or
summary_only; summaries cannot answer per-file geometry/facing, but canonical paths remain valid. A malformed files
field is an error. `metadata` takes runtime sidecars, not publisher metadata. Previews can omit variants; inspect
only a missing fit question. delivery.loose_paths identifies actual separately published files; never guess URLs.

For up to eight candidates needing missing technical facts, access exact metadata/archive descriptor/optional runtime
sidecar paths, then save INSPECTION_REQUEST:
```json
{"candidates":[{"metadataPath":"<published path>","archivePath":"<archive path>","runtimeMetadataPath":"<optional runtime sidecar>","kind":"font"}]}
```
Omit absent runtime path. kind is all/image/audio/font/atlas (all for models); optional member narrows selection,
textFile tests needed font text. No archive downloads are performed by this metadata operation:
```sh
python3 "$SKILL_DIR/scripts/retrieve.py" inspect-batch --request-file "$INSPECTION_REQUEST" --grant-file "$INSPECTION_ACCESS_RESULT" --cache-dir "$CACHE" --max-total-bytes 16777216
```
Read bounded stdout, detailsOmitted/omittedResults and runtime status; optional --output only for needed omitted facts.
metadataCachePath/runtimeCachePath are actual local locators. On renewal_required use exact accessRequest including
archive identity descriptors; accessRequestOmitted:true means reuse original access request/snapshot/paths, never a
truncated list. Preserve cache. Missing optional runtime enrichment is not an empty catalog or invalid canonical path.
For separately needed previews/files, request only those paths (not archivePath), then:
```sh
node "$SKILL_DIR/scripts/retrieve.mjs" fetch --grant-file "$INSPECTION_FILES_ACCESS_RESULT" --cache-dir "$CACHE" --max-total-bytes 16777216
python3 "$SKILL_DIR/scripts/retrieve.py" metadata --file "$RUNTIME_METADATA" --member "$MEMBER_PATH" --limit 1
```
fetch transfers every granted file; use returned cachePath. metadata supports kind/limit/offset and font --text-file.
Declared selection members can have purpose but no measurements; member_not_measured proves only sidecar absence.
An authoredSetRef resolves matching selection.authored_sets[].id with exact root/members/relationships; arbitrary
pack members aren't a compatible authored set. Keep long frame arrays on disk and read only missing details.

## Bounded archive overrides

Only verified flat ZIPs support these flags on members/retrieve/extract/inspect; local modes require --sha256.
Saved --file inventories and nested operations do not accept them. Inspect declared size before increasing budgets:
- --max-total-bytes bounds compressed transfer, --max-bytes selected output plus dependencies.
- --max-archive-bytes is finite expanded-all-members budget, 1..8,589,934,592 bytes. It replaces default 512MiB/member
  and 1000:1 heuristics but retains 100,000 entries, bounded directory, safe path/type, whole hash and streamed sizes.
  archiveExpandedBytes is declared size, not extraction proof; unselected members are not extracted.
- --case-sensitive-members allows distinct exact variants like _AO/_Ao, not exact duplicates/traversal/special files
  or selected/output case collisions. Retrieve conflicting variants/dependencies into separate destinations, no renames.
```sh
node "$SKILL_DIR/scripts/retrieve.mjs" extract --archive "$ARCHIVE" --sha256 "$ARCHIVE_HASH" --members-file "$SELECTED_MEMBERS" --destination "$DESTINATION" --max-archive-bytes "$ARCHIVE_EXPANDED_BUDGET" --max-bytes "$SELECTED_OUTPUT_BUDGET"
```
Apply only the needed override; do not bypass other bounds/integrity checks.

## Nested containers

The standalone Node helper currently supports flat ZIP members; nested containers and the advanced metadata/inspection
commands require the existing Python helper. Do not silently skip these paths on Windows without Python;
report the unsupported operation and preserve the verified download for a capable environment. For known typed locators:
```sh
python3 "$SKILL_DIR/scripts/retrieve.py" retrieve --grant-file "$ACCESS_RESULT" --archive-path "$ARCHIVE_PATH" --members-file "$SELECTED_MEMBERS" --cache-dir "$CACHE" --destination "$DESTINATION"
```

Known typed members extract directly, no capabilities/inventory/plan preflight. Helper supports nested ZIP/TAR/
tar.gz/tar.bz2/tar.xz/Unitypackage; optional RAR/7z needs available bsdtar, capabilities only if unknown/needed.
Outer archive retains catalog SHA. Container chain is ["assets.zip","source/pack.7z"], each exact member of its
parent, at most three nested containers. SELECTED_MEMBERS mixes flat strings and
`{containers:["assets.zip","source/pack.7z"],member:"images/hero.png"}`. These are local locators, not access paths.
Only unresolved leaves/dependencies require:
```sh
python3 "$SKILL_DIR/scripts/retrieve.py" capabilities
python3 "$SKILL_DIR/scripts/retrieve.py" inspect-nested --archive "$ARCHIVE" --sha256 "$ARCHIVE_HASH" --containers-file "$CONTAINER_CHAIN" --limit 20 --output "$NESTED_PAGE"
python3 "$SKILL_DIR/scripts/retrieve.py" plan-nested --archive "$ARCHIVE" --sha256 "$ARCHIVE_HASH" --members-file "$SELECTED_MEMBERS" --output "$NESTED_PLAN"
```
Normal extract dispatches typed locators, retains chain directories and records container/leaf hashes. Plan scope
includes supported dependencies. Limits: 100,000 cumulative members, 512MiB intermediate archives, 256MiB selected
extraction. Reports stay private/outside project; omittedMembers counts display omissions, nextOffset advances saved
full page, not samples. Matching outputs reused, conflicts rejected. Unitypackage keeps raw GUID asset/asset.meta/
pathname companions; unityPath is evidence only, GUID dependencies/import remain uninspected. Never invent conversion.

## Deeper navigation

Start characters at 2d-sprites/characters or 3d-models/characters; scenery at architecture/environment/
tiles/vegetation; objects at props; interfaces at ui, fonts at ui/fonts and sounds at sfx.
When a subcategory misses, follow its association manifest, canonical cross-category collections,
then nearby subcategories. Query synonyms separately, e.g. tree/forest/foliage, click/select/confirm,
footstep/walk/run; preserve required runtime representation and user filters.

Use for an actual association/offline-index lead, not ordinary search. Preserve user filters; mixed-category packs
may have fitting formats. Association coverage is partial: absent/empty is not absence. associated_cross_category_packs
relative_path is root-relative, files[].path is a ZIP member. Deduplicate canonical collection/member identity.
Root asset-catalog-index.json may itself be full inventory or contain full_index:{path,sha256}. In the latter case,
require `discovery/_cache/full-index.<sha256>.json` with identical lowercase 64-character hash. Never normalize a
malformed locator, turn it into a URL or silently substitute compact root. Access exact path in the same snapshot;
verify returned snapshot/path/hash/size and bytes against grant and locator before reading. Bootstrap's same logical
path requires the same checks. Missing full index is not an empty catalog; changed snapshot re-resolves root.

Set CATALOG_INDEX to verified full inventory (legacy root if no full_index). Keep JSON on target, project only needed
fields. Source-matched search runtimeMetadata precedes record runtime_metadata; local fields include metadata_path,
archive_path, inventory, sample_asset_paths. IDs are not file paths:
```sh
jq --arg pack "$PACK_PATH" '. as $i | .lookup.by_path[$pack] as $p | if $p == null then error("Collection not indexed") else $i.records[$p] | {path,metadata_path,archive_path,inventory,runtime_metadata,sample_asset_paths} end' "$CATALOG_INDEX"
```
coverage.readViewStatus active/absent/unavailable refers to optional enrichment. Continue canonical paths if absent/
unavailable; retry only when required measured detail is missing. Bootstrap access {} is optional deeper/offline
navigation; its bundle is TAR, safely unpacked separately from helper outer ZIP packs. No credential/backend bypass.
Expired grants renew via returned request, retired snapshots re-resolve; report persistent authorization/integrity/
availability errors rather than fabricating approval. Missing historical reviewer annotations need no new audit.
