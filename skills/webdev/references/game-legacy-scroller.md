# Historical side-scroller projects

This guide applies to recognized `game-scroller-v1` through `game-scroller-v61` projects. These revisions precede the current grappling game and include earlier robot implementations; their content, upgrades, controls, persistence and test entrypoints differ. The three-stage grappling game begins at `game-scroller-v62` and uses [the current Side Scroller guide](game-scroller.md). Do not apply its implementation paths, STYLE/FURY system or stage progression to an older project.

## Read the installed revision

Before changing gameplay, read the installed project's root `README.md` together with its `.manus-game-template.json` and, when present, `template-provenance.json`. Use that README for revision-specific mechanics, content, save ownership and verification commands. Inspect `project.godot` and the actual owners of the affected behavior to account for changes already made in the project. The installed source is authoritative when it differs from its README.

Preserve the project's existing movement, combat, destruction, progression, audio and delivery paths. For robot revisions, inspect the installed owners of contextual melee, damage attribution, structural support, streaming restoration, upgrades, score and salvage checkout before changing those systems. Retain their actual event wiring and gameplay authority; a later guide's different game is not a reason to remove or transplant them. Do not infer a stage count, enabled upgrade roster, leaderboard service, shortcut, save schema or local tuning UI from another revision.

If the README or provenance is missing, inspect the installed source and meaningful verification hooks before editing. Do not initialize over the project or substitute the current starter to recover documentation. A guide route preserves access to existing-project guidance; it does not promise that the retired starter remains packaged for fresh materialization.

## Apply current shared policy

[Game workflow](game-workflow.md) owns scope and implementation workflow; [Game assets](game-assets.md) owns current art/audio policy; [Game runtime](game-runtime.md) and [Game delivery](game-delivery.md) own current Preview, build, release and publishing behavior. These policies take precedence over frozen README lifecycle or production instructions. Use the executable and runtime commands from the current receipt, with the installed revision's relevant tests.

Developer tuning follows the current [Preview tuning handoff](game-runtime.md#preview-tuning-handoff), including Addon-hosted Tweak ownership. An older README's native tweak panel or local draft storage is historical implementation detail, not a requirement to recreate it. Inspect the installed adapter and consumers before changing tuning; preserve gameplay boundaries and ordinary player settings.

Verify the affected behavior with the installed revision's meaningful checks and current finite verifier. Preserve current asset locks, case-sensitive paths, media and existing saves. An intentional source upgrade is separate work with an explicit migration scope, not a side effect of reading this guide.
