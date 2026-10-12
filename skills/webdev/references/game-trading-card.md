<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Game Template — Godot Browser Card Battler

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


This complete current recipe overrides conflicting frozen README instructions, including genre-specific policy. Read historical README sections only for unchanged implementation details; use the receipt's GODOT_BIN and current Game delivery commands, never placeholder executable paths or retired hosting scripts.

The boot scene is a lightweight loader; card_game.gd remains the authoritative run/battle/UI owner, card_database static content and battle_layout the sole safe-canvas/HUD geometry owner. Classify the actual changed mechanic/art/UI/data boundary, then read the corresponding README Core Card-Game Mechanics or Required UI and Alignment Contract section. Preserve run/intermission/rewards/cooking/enemy AI and actual card legality/targeting when retained.
Static art stays text-free and separate from procedural effects/shadows/logos/cursors. Read Complete Reskin Asset Matrix only for a full reskin and affected rows otherwise. Apply updates preview memory; Save with Manus requests source changes through the existing task.
PvP uses the separately deployed matching server-v4, public multiplayer/config.json endpoint and version/room protocol; native service tests use GAME_CARD_SERVER_SOURCE. No old pnpm host aliases or standalone reference leaderboard service are shipped. Online rankings use the installed opt-in contract.
Existing native checks include scripts/smoke_test.gd, test/boot_loading_test.gd, multiplayer_ui_test.gd and applicable test/*_test.gd; node --test test/multiplayer_rules.test.mjs and test/multiplayer_native_test.mjs cover actual multiplayer changes. Use real-renderer test/debug_capture.tscn and matching prepared PCK; no separate legacy host audit.

## Source owners
| Path | Authority |
| --- | --- |
| `scenes/boot.tscn`, `scripts/boot.gd` | Lightweight startup artwork, preparation indicator, failure/retry, and title handoff. |
| `scenes/card_game.tscn` | Minimal full-screen root scene. The scene is intentionally thin. |
| `scripts/card_game.gd` | Main run/battle state machine, combat, enemy AI, cooking, rewards, title/battle/intermission/result UI, input, saves, scoring, tutorial integration, and semantic presentation events. |
| `scripts/card_database.gd` | Static art registry, card definitions, starter deck, recipes, legendary rewards, encounters, and enemy decks. |
| `scripts/battle_layout.gd` | Sole authority for battle HUD zones, 1280×720 reference geometry, safe-canvas projection, and compact profile. |
| `scripts/localization.gd` | Locale detection/preference, paired-catalog loading, fallback behavior, placeholder validation, and shared EN/CN font application. |
| `scripts/pause_input_router.gd` | Always-processing Escape input while the scene tree is paused. |
| `scripts/juice_director.gd` | Procedural particles, overlays, shakes, flashes, card ghosts, ingredient flights, BGM, voiceover, and SFX playback. |
| `scripts/card_battle_juice_profiles.gd` | Effect tiers, mechanic kits, motion scaling, and concurrency budgets in v54 and later. In v53 and earlier, follow the existing `PROFILES` preload in `scripts/juice_director.gd` to its historical filename; edit that owner instead of creating a second profile file. |
| `scripts/juice_target_line.gd` | Curved source-to-pointer targeting line and arrowhead above elevated cards. |
| `scripts/sleep_particle_emitter.gd` | Animated or static localized Sleep-state feedback. |
| `scripts/cursor_director.gd` | Semantic custom cursors, trails, halos, blocked/valid feedback, and touch hiding. |
| `scripts/tutorial_callout.gd` | Tutorial dimmer, live spotlight, guide, pointer, callout placement, and input containment. |
| `scripts/runtime_tweak_controls.gd` | Game-owned descriptors, values, validation and rank-affecting classification. |
| `scripts/atomic_json_file.gd` | Validated temporary write, backup rotation, and corrupt/missing-primary recovery. |
| `scripts/leaderboard_client.gd` | Local/global score contract, same-origin HTTP, retries, fallbacks, diagnostics, and sorting. |
| `localization/en.json`, `localization/zh-CN.json` | Paired English and Simplified Chinese catalogs. |
| `test/` and `scripts/smoke_test.gd` | Executable specification. Preserve behavioral intent when renaming theme-bound tests. |
| `web/` | **Generated output. Never treat it as source.** |
`ScreenLayer` is the authored HUD canvas. `JuiceLayer`, tutorial, cursor, are separate presentation spaces. Cross-layer effects must use live `CanvasItem` transforms; raw local positions drift under HUD scale, shake, responsive projection, and entrance animation.

## Runtime tweak controls
`scripts/runtime_tweak_controls.gd` owns descriptors and values; the Addon renders them through
`scripts/manus/preview/tuning_adapter.gd`. Preserve run/battle/turn consumer timing and multiplayer authority.
`_start_battle` snapshots NEXT BATTLE values; board-capacity checks and enrage logic keep that snapshot until the
next battle. Other parameters are consumed at their named actions. Addon Apply never writes local tuning drafts.
