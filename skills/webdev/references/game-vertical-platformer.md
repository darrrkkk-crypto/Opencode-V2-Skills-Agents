<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Vertical Platformer Game Template (Godot 4.7 → Web/WASM)

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


This complete current recipe overrides conflicting frozen README instructions, including genre-specific policy. Read historical README sections only for unchanged implementation details; use the receipt's GODOT_BIN and current Game delivery commands, never placeholder executable paths or retired hosting scripts.

Preserve automatic jumping, horizontal steering, four stage types/endless progression, monsters/pickups, skins/purchases and real portrait/landscape traversal when retained. SessionOwner/SessionUI own modal pause/focus and transitions; saves, once-only standings, tutorial skip/replay and typed requested/active tuning have separate owners. Adapt names/assets without losing those connections.
Read README Local score and tutorial ownership, Tuning and debug builds or Art workflow for a change to those systems. Four skins/directions are supported content, not a mandate to recapture every unchanged combination. Preserve authored anchors across facing/motion; reused representative evidence covers unchanged variants.
Use applicable `test/smoke.gd`, leaderboard_tutorial, tuning_contract, audio, localization, responsive_layout, production_scaling and exported_pack_boot hooks; source debug helpers may be disabled in release. Capture representative affected states with existing debug_capture/localization_capture scenes, not a new capture matrix.

## Source owners
| Path | Working reference included in the template |
|---|---|
| `scenes/title_screen.tscn` + `scripts/title_screen.gd` | Title, EN/CN selector, best height, star balance, skin purchases/selection, tutorial replay and start flow |
| `scenes/game.tscn` + `scripts/game.gd` | Automatic jumping, horizontal steering, four stage types, endless region progression, monsters/pickups, score, HUD, failure/results and retry |
| `scripts/session_owner.gd` + `scripts/session_ui.gd` | Shared modal/pause/focus ownership, real portrait/landscape layout selection, pause/help/settings, restart/title confirmation, standings entry points and result actions |
| `autoload/i18n.gd` + `localization/` | Complete English/Chinese catalogs, live locale changes, placeholders and saved language choice |
| `scripts/leaderboard_store.gd` + `scripts/leaderboard_panel.gd` | Validated offline top-10 snapshots, name entry, persisted standings and duplicate-result protection |
| `scripts/tutorial_director.gd` | Gameplay-triggered, input-aware tutorial cards, persistent completion, Skip and replay |
| `scripts/tweak_catalog.gd` + `scripts/tuning_store.gd` | Typed descriptors, authored defaults, requested/active values and application boundaries |
| `scripts/audio_director.gd` | Semantic cue registry, bounded Music/SFX/UI voices, browser gesture unlock and persistent player volume/mute |
| `scripts/save_store.gd` | Versioned best score/height, star balance, unlocked skins and selected skin in `user://` |
| `assets/template/characters/` | Four preserved hero skins with aligned animation frames |
| `test/smoke.gd`, `test/leaderboard_tutorial.gd`, `test/tuning_contract.gd`, `test/audio.gd` | Climb/progression, score/records, tutorial, tuning integrity and audio ownership regressions |
| `test/localization.gd`, `test/responsive_layout.gd`, `test/production_scaling.gd`, `test/loader_locale.test.mjs` | Paired keys/placeholder/font coverage, language controls, actual project stretch/portrait traversal/rotation preservation and Web-loader checks |
| `test/debug_capture.tscn`, `test/localization_capture.gd`, `test/leaderboard_tutorial_capture.gd` | Real-renderer title/gameplay/menu/tutorial/standings and EN/CN landscape/portrait evidence |
| `test/exported_pack_boot.gd` | Boots the exported PCK main scene to catch omitted resources and release-only regressions |
| Game runtime | Local Web export/preview, asset sync and published-site assembly; managed outside the project scaffold |

## Tweak controls
`scripts/tweak_catalog.gd` owns descriptors; `scripts/tuning_store.gd` owns validation, requested/active values,
application boundaries and sticky practice eligibility. The Addon renders these through
`scripts/manus/preview/tuning_adapter.gd`. Preserve real LIVE/action/spawn/stage timing and normal player saves.
