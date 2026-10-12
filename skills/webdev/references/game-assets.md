# Game asset operations

Read for import/generation/adaptation/grouping, deletion, restoration, animation, models/textures or user-attached asset edits; do not audit unchanged assets.
Catalog sourcing uses the enrolled `game-asset-catalog` Skill from `webdev-mcp`, including
its helpers and recovery. Respect recorded methods and published facts without publisher/licensing re-review. Use
the project's layout and local runtime media that survives grant expiry. The [delivery](game-delivery.md)
save/prepare path reconciles receipts and syncs assets automatically; do not add a separate sync before it unless
a new batch needs grouping before the release snapshot.

## Deletion and restoration

For a requested deletion run `node "$GAME_RUNTIME/scripts/delete-asset.mjs" "assets/<exact-media-path>"` from the
project; disk-only deletion is restored by sync, and lock storage facts are never hand-edited. For missing files,
reuse verified copies and restore known managed assets first, then diagnose actual path, import or config errors.
Search only unresolved roles within source permission, and get agreement before changing restrictions; an access
failure is not a catalog gap. Keep originals until replacements work, and verify integration before claiming
recovery.

From the project, `node "$GAME_RUNTIME/scripts/hydrate-assets.mjs"` restores genuinely missing managed assets, and
`node "$GAME_RUNTIME/sync-assets.mjs"` registers a coherent changed batch when early registration is needed. Keep
existing `asset-provenance.json`, supplied license notices, lock entries, groups and sidecars; never fake preloads or
delete dependencies because they are marked `used:false`.

## Asset browser groups

Choose groups by the game's browsing purpose, not media type, source pack, production method or directory depth.
`assetType` describes the media; `groupId` describes its purpose in the game. Type directories such as
`models`, `images` or `audio` are not useful purpose groups. Keep files in their existing paths; classify
subjects by their actual role rather than imposing a fixed taxonomy or a group for every folder.
Preserve existing user-defined IDs, names, memberships and order unless regrouping is requested;
reserved `assets/template/` media stays in `template`. Automatically inferred directory groups are defaults,
not user-defined categories: assign meaningful groups to the new batch even when sync already supplied one.

After the engine-specific sync has registered the new batch, edit only complete `assets.lock.json` entries.
Never prewrite partial entries with just `groupId` or invent storage facts. Already registered assets need
no extra sync for grouping alone. Assign `groupId` and matching `groups` declarations with human-readable
`name` and `order`. Normalize IDs to lowercase, replace runs of non-letter/non-number characters with `-`,
and trim edge hyphens. Keep recolored/adapted variants with their subject.

Runtime fallback uses the first directory below `assets/`, so `assets/models/` becomes `models` regardless
of content. This is registration fallback, not completed grouping. Change only membership and group
metadata, never storage paths, hashes, sizes, asset types or provenance; no file move or upload is needed.
Check the batch's entries and declarations before saving, then confirm the saved version retains the groups.
A post-save grouping edit needs a new checkpoint. No browser session is required.

For new Godot assets, run `node "$GAME_RUNTIME/sync-assets.mjs"` after the coherent batch lands and
before save/prepare, then apply the grouping rules above. Set the group on every animation frame,
including alternate formats; sync rebuilds bundle membership from the first frame. Never edit generated
bundle membership directly. Confirm saved assets and bundles retain their intended groups before pushing.
The Godot Assets tab displays Animations → Images → Audio → Others; group order applies within each
media category. Mixed groups are split for display only; preserve their manifest membership.

## Animation bundles

Animation frames share size/anchor and consecutive names in one
clip directory or prefix. Authored `<prefix>.animation.json` needs `type:"frame-animation"`, `name`, `fps`,
`loop` and project-relative `coverFrame`, without `managed:true`. Mixed-directory clips need descriptors rather
than moves. Sync builds ordered bundles; loose images are not an Animation entry and generated bundles are not
hand-edited.

## Models and textures

Preserve case, relative URIs and GLB/glTF dependencies; move dependencies together and update model URIs, material
bindings and consumers. New layouts use assets/models/<asset>, materials/<material> and textures/<material>, keeping
existing model-relative Textures directories. The lock covers images, audio, video, fonts and GLB/glTF/OBJ/FBX/Blend/
DAE models; loose textures register separately and embedded ones stay in models. Buffers, material resources and
unsupported HDR/EXR/TGA stay versioned source; only GLB/glTF dependencies are automatic. Keep the runtime-managed
.gitignore rules so hydrated media stays out of Git.
`node "$GAME_RUNTIME/check-textures.mjs" --strict` is read-only: a nonzero exit includes oversized *or uninspected*
resources and resizes nothing. It covers GLB/glTF images and identifiable Godot material or scene bindings; other
formats, binary resources and dynamic or default shader textures need explicit inspection, so never claim strict
coverage for them. Optional versioned `game-texture-budgets.json` (excluded from player export) is
`{version:1,textures:{"assets/models/hero.glb":{maxSize:2048,reason:"Closest camera fills face"}}}`, keyed by exact
image, model, material or scene path or `model.glb#image/0`. Allowed sizes are 256/512/1024/2048/4096, and above
1024 needs a concrete reason.

## Apply asset edits without overwriting newer work

Preserve the attachment's baseDigest, resource URI and path; resized thumbnails never establish original hashes, and
missing bases require inspecting the actual targets. Generate candidates under dist/asset-edit-candidates, keeping
originals, and prepare the matching candidate lock with the changed bytes and hash. Batch originals, derivatives and
the lock with `node "$GAME_RUNTIME/asset-edit.mjs" --prepare request.json`, then `--apply ID`:
```json
{"resourceId":"wdp_PROJECT_ID","changes":[{"path":"assets/hero.png","baseDigest":"sha256:ORIGINAL_HASH","candidate":"dist/asset-edit-candidates/hero.png"},{"path":"assets.lock.json","baseDigest":"sha256:LOCK_HASH","candidate":"dist/asset-edit-candidates/assets.lock.json"}]}
```
Derive identity from the attachment URI, current runtime or Local declaration, never a fabricated init marker; attach
on mismatch. Use a null base only for explicitly new targets. Prepare freezes candidates; apply rechecks bases and
backs up originals, and only phase:complete succeeds. A conflict keeps candidates and newer files: report it and ask
which to keep, never silently refresh the base. Interrupted edits use `--recover ID`; remove an exact stale lock only
after confirming its owner PID exited. Bundle frame edits keep timing, groups and annotation coordinates.
Keep `.manus-asset-history/` in source checkpoints and outside the player export. To restore, read its ID.json,
choose before or after, capture the current digest, run `--restore request.json` with
`{resourceId,id,path,side,baseDigest}`, then `--apply` the NEW returned ID; restore related animation sets together.
Before-creation means deletion, not image restoration. Keep the last successful Preview if rebuilding fails.

## Model generation and presentation

### 3D model generation
For all GameDev 3D model generation, default to the Manus built-in `generate_3d_model` tool in Cloud and Local,
for new games and additions to existing games. Discover its active schema and use only supported arguments.
Do not write custom scripts to submit or poll Tripo/provider jobs, or use the Data API as a generation shortcut.
A Fast/Hybrid/AI mode, a provider name or an enabled connector does not select an external entry point.
Only an explicit user request for a connector selects that route; use its registered tools, never a custom API
client. If the selected tool or required method is unavailable, report the blocker and defer those models; do not
switch routes, invent parameters or probe with paid calls. Preserve generation consent and narrower source
restrictions. Recover completed outputs after delivery failures instead of generating them again.
When retrying `generate_3d_model`, reuse the previous call's `brief` verbatim; do not prefix it with "Retry"
or replace it with a description of the retry.

### 3D texture budgets
Budget the project's stored textures, including bytes embedded in GLB/glTF, not catalog masters or import limits.
Longest edge: 256–512 for small or distant props, 1024 by default, 2048 for close main actors or shared atlases,
4096 only for a justified visible difference. Never upscale, and keep UVs, channel packing and material bindings
intact. Remove replaced embedded bytes, keep ancestry and sync the changed files. If suitable tools are missing,
report it rather than replacing working assets. Claim only measured savings.

### Continuous animation and alignment
Use the approved animation method. AI continuous motion goes from approved static references to a guided
fixed-camera, in-place video to fixed-FPS extracted loops; independent poses need an approved stepped style. Keep a
shared canvas, scale, pivot and contact anchor across states and facings instead of per-state placement patches, and
keep raw masters outside the game. Check representative movement, reversal and ground contact with the native
renderer.
For 3D models, author and import locomotion clips in place: walking or running animates the pose while the model
stays at its local origin. For in-place playback, remove baked locomotion displacement from model/rig roots and
root/hip tracks while preserving limb motion and bounded body bob. Gameplay code owns world movement; clip playback
must not accumulate root displacement. Preserve an existing controller's root-motion data and extraction contract
while keeping the visual model anchored. With gameplay movement disabled, verify the imported animation across repeated loops and
idle/walk/run transitions: no drift from the origin or position snaps at loop boundaries.

### Seamless parallax backgrounds
Repeating layers must tile left and right without mirroring; check the joins between adjacent copies at the intended
scale after any crop, import or scale change. Side-scrollers keep a low scenic foreground above world actors and
below the HUD without hiding combat.
