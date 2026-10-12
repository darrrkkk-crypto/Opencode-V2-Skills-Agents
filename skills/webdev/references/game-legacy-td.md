# Historical isometric tower-defense projects

This guide applies to recognized `game-td-v1` through `game-td-v56` projects. These revisions share the older isometric lineage, but their stage counts, campaign rules, UI and developer controls differ. Fablewood begins at `game-td-v57` and uses [the Fablewood guide](game-td.md); do not apply its implementation paths or mechanics to an older project.

## Read the installed revision

Before changing gameplay, read the installed project's root `README.md` together with its `.manus-game-template.json` and, when present, `template-provenance.json`. Use that README for revision-specific stages, controls, content, persistence and test entrypoints. Inspect `project.godot` and the actual owners of the affected behavior to account for changes already made in the project. The installed source is authoritative when it differs from its README.

Do not infer a stage count, local/global leaderboard service, tweak catalog, shortcut, save schema or campaign contract from another TD revision. In particular, later isometric revisions must not receive the v1 gameplay description merely because they share a template family. Preserve the project's existing routes, authored content and save ownership; extend the existing implementation instead of transplanting a different revision's systems.

If the README or provenance is missing, inspect the installed source and existing verification hooks before editing. Do not initialize over the project or substitute the current starter to recover documentation. A guide route preserves access to existing-project guidance; it does not promise that the retired starter is still packaged for fresh materialization.

## Apply current shared policy

[Game workflow](game-workflow.md) owns scope and implementation workflow; [Game assets](game-assets.md) owns current art/audio policy; [Game runtime](game-runtime.md) and [Game delivery](game-delivery.md) own current Preview, build, release and publishing behavior. These policies take precedence over frozen README lifecycle or production instructions. Use the executable and runtime commands from the current receipt, with the installed revision's relevant test hooks.

Developer tuning follows the current [Preview tuning handoff](game-runtime.md#preview-tuning-handoff), including Addon-hosted Tweak ownership. An older README's in-game F10 panel or local config-file draft is historical implementation detail, not a requirement to recreate it. Inspect the installed adapter and consumers before changing tuning; preserve their gameplay boundaries and ordinary player settings.

Verify only the affected behavior with the installed revision's meaningful checks and current finite verifier. Keep gameplay/result/save authority in the actual owning code; views, audio and presentation remain consumers. An intentional source upgrade is separate work with an explicit migration scope, not a side effect of reading this guide.
