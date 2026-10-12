<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Physics Merge Puzzle Template — Local Multiplayer

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


This complete current recipe overrides conflicting frozen README instructions, including genre-specific policy. Read historical README sections only for unchanged implementation details; use the receipt's GODOT_BIN and current Game delivery commands, never placeholder executable paths or retired hosting scripts.

Retain Plushie Merge solo plus same-device split-screen unless excluded; recommend local friendly competition without provisioning online services. Two actual independent physics worlds share round timing/results/rematch. Read README Local multiplayer contract for input ownership, names and round lifecycle before changing duel behavior; do not replace simulated boards with decorative views.
Title How To Play is read-only; play stays unobstructed. Read Title-screen instructions and unobstructed play and Responsive results and mobile sheets when changing those surfaces: keyboard-safe sheets, one active edge scrollbar, readable results and preserved pause/focus/input boundaries.
Use existing physics/merge/bomb/score/settings/localization/tuning owners; preserve merge anchors, supported names and offline standings. Debug owner_preview and release checkpoint exports have distinct markers; never expose developer controls in release. Shared font and no-cleanup rules override historical font/asset housekeeping text.
README Focused verification lists revision-specific hooks for affected solo/duel/physics/input/mobile/results behaviors. Use the finite verifier and matching candidate plus representative native captures; do not duplicate the entire historical acceptance matrix.

## Current resize and onboarding rules
Changing size during solo play (including pause) or local duel countdown/round ends the run.
Let the implementing agent choose the banner wording; no historical exact phrase is required.
Freeze gameplay/input before layout rebuild, keep the banner through further resizes until a new
round/title, and exclude resize losses from standings. Initial/title/lobby layout and visibility
notifications without size changes are exempt. Keep title-only read-only How To Play: no in-game
tutorial popups, reserved footer, replay/completion dependency or pause-menu help shortcut unless requested.
Do not remove rescue-bomb gameplay when removing teaching copy.

## Source owners
| Path | Responsibility |
|---|---|
| `scenes/main.tscn`, `scripts/plushie_main.gd` | Entry, routing, input, viewport and pause lifecycle |
| `scripts/plushie_hud.gd` | Responsive title, read-only How To Play, HUD, menus, settings and results |
| `scripts/ui/mobile_sheet.gd`, `mobile_scroll_edge.gd` | Keyboard-safe mobile sheets and the active sheet's single edge scrollbar |
| `scripts/core/session.gd`, `data/stages/registry.gd` | Solo goal/timer progression and starting presets |
| `scripts/plushie_body.gd`, `scripts/bomb_plushie.gd` | Collision silhouettes, merge presentation and contact bombs |
| `scripts/game/board_simulation.gd` | Actual physics simulation reused by local duel boards |
| `scripts/multiplayer/local_match.gd` | Two independent physics worlds, shared round timer, results and rematch |
| `scripts/multiplayer/multiplayer_screen.gd`, `board_view.gd` | Same-device match configuration, two cabinet views and input routing |
| `scripts/multiplayer/protocol.gd` | Shared local round constants and name normalization; no transport |
| `scripts/core/settings.gd`, `storage_migration.gd`, `username_input.gd` | Saved preferences/profile and reusable name input |
| `scripts/score/` | Score integrity and bounded offline local standings |
| `scripts/core/localization.gd`, `localization/` | English/Chinese lookup and locale persistence |
| `scripts/game_audio.gd`, `sound_bank.gd`, `default_bus_layout.tres` | Semantic cues, single BGM, bounded voices and buses |
| `scripts/vfx/`, `config/tweaks/catalog.gd`, `scripts/tuning/` | Cosmetic feedback, typed tuning defaults and debug controls |
| `addons/mushies_export/` | Debug `owner_preview` and release `checkpoint` export markers |
| `ui/mobile/`, `ui/web/`, `tools/build_web_shell.py` | Device lifecycle and localized managed Godot loading shell |
| `assets/template/`, `assets.lock.json` | Retained media, fonts/licenses, provenance and permanent restoration |

## Tweak controls
`config/tweaks/catalog.gd` and `scripts/tuning/tweak_service.gd` own bounds, requested/active values, application
boundaries and sticky practice status. `scripts/manus/preview/tuning_adapter.gd` exposes that manager to the Addon.
Keep normal Settings, leaderboard persistence, multiplayer authority and route-stack pause ownership intact.
