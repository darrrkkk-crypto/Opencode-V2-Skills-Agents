# Catalog adaptation and integration

Read only for unresolved fit, actual transformation or a missing integration fact. Ordinary direct retrieval
requires neither this page nor a new review. [Main Skill](../SKILL.md) owns source permissions and scope;
[retrieval](retrieval.md) owns missing metadata/member paths. Preserve existing approved assets while testing replacements.

## Adaptive search

Keep each unresolved role's subject/style/perspective/actions/facings/runtime representation/constraints in the
existing plan. Change wording/function/structure/material/component search hypotheses, not user requirements.
Synonyms are separate queries; examine diagnostics/recoveryQueries and carry omittedTerms into selection. Negation
is not enforced. Use observed filters, broaden only your own exploratory categories. Follow promising associations/
authored sets, not exhaustive catalog scans; a mixed-category pack can contain the required representation.

For a difficult role compare a few credible reuse/adaptation/composition routes internally; no per-asset approval
menu. Search-only returns candidates, not unsolicited downloads. Preserve geometry/perspective/motion/style/dependencies
before minimizing size. Recolor cannot fix anatomy/gait/perspective. A representative sample is justified only for a
missing fit question (one facing/transition/tile/material/cue), not a routine production gate. Reject implausible routes
before multiplying variants. Supplied facts need no remeasurement. A preview isn't a usable animated sequence.

Budget per unresolved role: start with a direct query and up to two focused reformulations, stop sooner on fit.
Continue only for a concrete new lead, such as an uninspected authored set/association, not repeated synonyms of the
same packs. Follow useful cursors even on short budget-limited pages. Deduplicate snapshot/collection/member identities,
reuse downloads/measurements and integrate selected inputs into actual gameplay. Catalog absence claims are bounded
to checked coverage; outages/partial inventories/missing measurements stay explicit. Stop when a viable route covers
scope; don't await a separate enrichment request or add unselected optional content.

Permitted adaptations slice/recolor/compose/transform actual inputs and retain lineage/parameters/output hashes.
For 2D catalog/Hybrid gaps, apply main Skill's explicit-placeholder/AI permission boundary; a catalog image used only
as a reference for newly drawn art is not adaptation. Preserve catalog-only/supplied-only/silence/search-only limits.
Access failures are not gaps. Audio SFX can trim/fade/pitch/filter/layer suitable catalog bases before permitted
synthesis; music is optional and follows its recorded source restrictions. Reuse fitting permitted title/loading backgrounds
or adapt existing art without mandatory new generation. Favicon may adapt recognizable
permitted game art at small size; Share OG follows Game delivery's separate AI workflow, not catalog composition.

## XML slicing and palette substitution

Known XML/palette tasks use installed scripts/adapt.py directly with verified selected inputs and existing Python/
Pillow. Missing dependency reports image_dependency_unavailable; do not silently install or substitute AI. Helper
preserves sources and writes separate PNGs under game-owned lowercase assets/. It is not arbitrary editing, animation
production, GLB processing or catalog publication. archiveSha256 is recorded source identity; input/descriptor hashes
are checked, not the archive itself. Example recipe:
```json
{"schemaVersion":1,"operation":"slice","source":{"collection":"<canonical collection>","member":"<PNG member>","sha256":"<member hash>","archiveSha256":"<archive hash>"},"atlas":{"member":"<XML member>","sha256":"<descriptor hash>"},"frames":["<authored frame name>"]}
```
```sh
python3 "$SKILL_DIR/scripts/adapt.py" --source-file "$SOURCE_PNG" --atlas-file "$ATLAS_XML" --recipe-file "$RECIPE" --destination "$VARIANT_DESTINATION"
```
XML imagePath must identify supplied source member. Selected rectangles are untrimmed/unrotated authored integers
inside PNG; unsupported pivots/trim/rotation require engine importer preservation, not discarded metadata. Frame order/
alpha are preserved; no guessed grid/recentering. Max 64 frames/4M output pixels. Palette operation retains source,
uses operation:palette and mapping:{"#ff0000":"#00ff00"} instead of atlas/frames, omits --atlas-file. Actual colors
must exist in nontransparent pixels; mappings are simultaneous, ≤64 colors, preserve alpha/transparent RGB, not
perceptual recoloring/quantization. Input single-frame PNG ≤16MiB/4M pixels/8 bits per channel, recipe ≤64KiB, outputs
≤32MiB. Different existing outputs fail; repeat recipes verify/reuse files and compact provenance with source/recipe/
rectangles/hashes/Pillow version. Exact bytes depend on that version. Review changed result at display scale when needed;
a crop does not supply missing action/pivot/timing facts. Reference local output, never catalog URLs at runtime.

## Media integration

Inspect only absent facts or behavior changed by processing/import: 2D alpha/dimensions/layout/pivot/hotspot/nine-slice;
3D axes/scale/mesh/material/rig/animations; exact font format/weight/glyphs; SFX event/format/mix/clipping/loops.
Published facts are authoritative; extension/name alone does not imply unstated properties. Keep unknowns explicit.

For missing atlas/font facts, use bounded metadata --kind atlas, or metadata --kind font --member "$FONT_MEMBER_PATH"
--text-file "$REQUESTED_TEXT_FILE". Coverage comes from that exact face's unicode_ranges, not sample counts or a combined
family; missing measurements stay unknown. Engine text needs a supported binary TTF/OTF, not an alphabet image.
The Game workflow owns font defaults, unrestricted uploaded-font choices and CJK coverage; font decoration cannot fix missing glyphs.

Preserve published descriptor/image links. Helper follows glTF/OBJ/MTL, supported TextureAtlas XML/JSON meta.image,
BMFont pages and Tiled TMX/TSX/template/images, validates paths/dependencies and terminates cycles. Unsupported descriptor
features need their real importer; extraction does not prove rendering. Tile stride does not reveal unstated margins,
actions or pivots. Keep long frame arrays on disk and use exact authored-set relationships.

### Sprite geometry and animation

Use supplied rectangles/canvas/margins/spacing/trim/rotation/alpha bounds/pivots directly. Preserve source/member,
coordinate convention/frame order/intended scale/engine pivot in existing asset data. Distinguish authored values from
measured corrections. Inspect only missing geometry or changed mapping, not every unchanged frame. Preserve jumps,
bobbing and asymmetry; never independently recenter alpha bounds. Map semantic anchor once, restore trim offsets and
separate crop/placement/reflection. Mirroring keeps positive placement rectangles and explicit anchor via renderer flip,
not negative sizes/compensating gameplay offsets. Inspect drift/clipping/pops at fixed world/camera/scale/support and
fix the reusable mapping. Reuse representative native captures; no catalog-specific acceptance matrix.
When a humanoid motion reference is genuinely missing, locate live `2d-sprites/characters/manus-humanoid-walk-reference`.
Its final-centered wrapper contains eight-direction walk videos/frames/sheets/source-speed manifests, not other actions
or a skeletal rig. Target character remains appearance authority. Authorized generation uses one continuous video per
character containing required facings, guided by matching references, preserving extracted directional loops/timing/
contact anchors. Separate reference files do not require separate generated clips. Report unavailable dependencies,
never invent paths/claim inspection. Supplied verified references can be reused within source permission.

### 3D model textures

Use the Game assets page's 3D texture budgets for project-local derivatives including embedded images; keep catalog masters
outside initialized project/export. Import size settings alone do not reduce source. Preserve structure, UVs, map-aware
processing, bindings, source identity/parameters and output hashes. XML/palette helper does not resize GLB textures;
use suitable installed tooling, report missing capability and retain working assets rather than installing silently
or substituting generation. Store model/image under existing assets groups, synchronize supported lock entries;
buffers/material resources stay versioned. Reimport/inspect changed model/native/PCK use and actual byte reductions.

## Project handoff

Standalone retrieval stops without sync/checkpoint. Authorized integration uses the current owner's project/runtime
and loaded lifecycle, including legacy-owned games; no guessed commands from another template. For Addon games,
normal save-release.mjs/prepare-release.mjs already syncs. Only early registration/restoration needs
`node "$GAME_RUNTIME/sync-assets.mjs"` once per coherent batch. It skips unchanged files, returns bounded counts and
saves no checkpoint. Follow redacted configuration diagnostics; don't unset credentials/mix URL-key pairs/wrap internals.
Portable exports don't require platform sync. Generated lock owns storage paths/hashes/sizes/bundles, never hand-edit.

Retrieval and adaptation retain available source/license/derivative metadata automatically. Preserve existing
records and supplied notices; run game workers in project cwd with receipt GAME_RUNTIME. Do not manually import
provenance receipts, fill source/use/visual-role records or produce asset-count reports. Save/export updates
matching inventory automatically. Missing metadata does not block integration or delivery; never pass private
grants/signed URLs as source records.
Verify only affected integration and requested delivery: dependencies/animation/texture/font/data resolve locally,
restorable without temporary grants. Retain required support files even if used:false; default asset cleanup is absent.
Report download, Assets registration, working checkpoint and export as separate outcomes actually established.
