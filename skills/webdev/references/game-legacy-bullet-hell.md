# Horizontal Bullet-Hell Shooter — Godot Web

Legacy-only gameplay contract: keep the installed project and protocol; new initialization selects newer revisions. Read the selected starter's matching guide; paths below are relative to its project root. [Game workflow](game-workflow.md) owns initialization, Preview, release preparation and deployment. Source-specific test/export commands are diagnostics only, not lifecycle replacements; serialize them with active Game builds. [Shared game rules](game-workflow.md) take precedence for gameplay/art/audio policy. First-checkpoint completion means the first completed-game deliverable, excluding bootstrap and intermediate version saves.



This is a **playable horizontal bullet-hell reference**, not an empty starter. `game-bullet-hell` names the game type; **Stargrave Dogfighter** is only its sample theme. Preserve the supplied game's tuned pacing and working systems while adapting its characters, setting and mechanics to the user's request.

## Reference and completion contract

| Area | Working reference and adaptation requirement |
|---|---|
| Game loop | Three scrolling combat segments, five formation waves per segment, three elite encounters and a final boss; intro, transitions, victory, defeat and replay are implemented. Adapt the progression deliberately rather than dropping the complete loop. |
| Player and attacks | Keyboard/touch movement, automatic fire, three weapon upgrades, visible upgrade feedback, energy, a five-second laser and a three-hit shield. Keep the small central hit radius distinct from the ship artwork. |
| Enemies and feedback | Line/V/W formations, aimed fans, curved projectiles, telegraphed lasers, pickups, particles, shake, dialogue and score feedback. Attack warnings must remain readable and leave a feasible dodge route. |
| Presentation | A content-specific title, live HUD, three scrolling background layers, player and enemy artwork, English UI with an embedded pixel font and a fixed 1280×720 / 16:9 canvas. Use centered letterboxing outside 16:9, never stretch or expose uncovered canvas. |
| Audio | Looping reference BGM and shot/hit/explosion cues. One streaming BGM player and three bounded SFX players; pause state changes are idempotent. Replace the catalog as needed, not the lifecycle guarantees. |
| Pause and navigation | `Esc` or the on-screen PAUSE control pauses/resumes. While paused, `M` or the central menu hint returns to the title. Victory/defeat can be replayed; `M` also returns to the title. |
| Tweak | Debug Preview retains twelve live parameters, reset and local autosave. Release builds hide the panel and do not load browser tuning overrides. Manus applies approved values to source defaults and re-exports; local saving is not source synchronization. |
| Persistence and delivery | Versioned local best score, all referenced assets restored and included in the PCK, source/pack tests passed, and a current checkpoint delivered for user browser acceptance. |

A complete adapted game needs every relevant row, not merely a booting scene. Do not replace final environment art with prototype geometry or leave the audio, pause menu or tuning workflow as prose-only promises.

## Source map and controls

| File | Responsibility |
|---|---|
| `project.godot`, `export_presets.cfg` | Fixed 16:9 viewport, bundled global font, main scene and Web export. |
| `scripts/title_screen.gd` | Title artwork, input gesture, start flow and best-score display. |
| `scripts/game.gd` | Phase machine, movement, projectiles, enemy formations, four bosses, abilities, particles, audio, HUD, pause and debug tuning. |
| `scripts/tuning_defaults.gd` | The twelve source defaults; keep this the default-value owner. |
| `assets.lock.json`, `assets/template/` | Published reference artwork, audio and font. Hydrate through the shared asset runtime; use the current typography contract. |
| `test/smoke.gd`, `test/template_contract.gd` | Tuned gameplay, weapon/boss progression, CJK, viewport, bounded audio, pause and tuning contracts. |
| `test/debug_capture.gd` | Deterministic Godot-native title, gameplay, boss and debug captures. |

Move with **WASD/arrows** or the left-side touch drag area; ordinary fire is automatic. At full energy, **K** activates the laser and **L** activates the shield; the right-side touch controls mirror them. **Esc / PAUSE** controls pause. **R** retries victory/defeat; touching the end screen also retries.

## Debug tuning and saving

In a **debug Preview**, use **F1 / P** to open SYSTEM TWEAK. Up/down selects a row, left/right adjusts it, Shift makes a larger adjustment, and the row's minus/plus controls work with pointer/touch. **R** resets; **F1/P/Esc** closes. Changes save to `user://stargrave_tuning.cfg`; errors or unavailable persistent browser storage must not be reported as a durable save.

| Parameter | Meaning |
|---|---|
| `player_speed`, `fire_delay` | Ship movement and automatic fire interval. |
| `enemy_count`, `enemy_health`, `enemy_speed` | Formation-density, health and movement multipliers; `enemy_count` is not an absolute count. |
| `enemy_bullet_speed`, `boss_health` | Hostile projectile speed and boss-health multipliers. |
| `hit_radius` | Player's central damage radius, independent of rendered ship size. |
| `energy_rate`, `bone_drop` | Energy recharge and upgrade-drop probability. |
| `bgm_volume_db`, `sfx_volume_db` | Music and effect levels. |

**Enter saves the local draft and prints `[TUNING_DRAFT]` with the current values; it does not write remotely.** When the user approves the balance, read that draft or their requested values, edit the corresponding constants in `scripts/tuning_defaults.gd`, rebuild through the managed runtime, verify, and save a new checkpoint. Never restore a previous session's preview URL, add a custom public write endpoint, or claim browser-local settings were applied to source. Keep release builds free of Tweak UI and browser draft overrides.

## Bullet-hell asset and font wiring

The sample's title, layered space scenery, ships, pickups and audio live under `assets/template/` and are restored through `assets.lock.json`. Its ships use motion/transforms rather than character walk cycles. Preserve the small central damage radius and readable attack warnings independently of sprite size.

Follow the [current typography contract](game-workflow.md#default-typography): default to bundled ManusCC0 with ManusCC0 Sans CJK SC fallback, and allow unrestricted user-uploaded fonts. For font changes, update theme overrides, hydration pins, loader sources and project-local checks together; preserve gameplay and protocol. Check chosen-font rendering, Chinese player names and actual Web font resolution; diagnostics do not block uploaded-font choices.

The audio implementation in `scripts/game.gd` has one streaming BGM player and three fixed SFX players. `_sync_audio_pause()` guards transition writes. `test/template_contract.gd` checks 10,000 idle/paused updates, font glyphs, fixed viewport and local tuning. Keep these contracts while adapting cues.

## Focused validation and checkpoint

```bash
# GODOT_BIN can point at the current installed Godot binary.
godot --headless --path . --editor --import
pnpm test

# Use a real renderer, not the headless Dummy renderer, for visual captures.
godot --path . test/debug_capture.tscn

# Source-specific offline export validation; the Addon preview updates only on an explicit build.
pnpm export
pnpm verify-export
```

`pnpm verify-export` mounts the generated PCK and checks its contents, title boot, gameplay and template contracts. The runner requires explicit pass markers, rejects script errors even when Godot exits zero, and has a timeout. `pnpm check` is only the shared watcher's keep-alive shim, not a gameplay test. Do not hand-edit `dist/` or `site/`, include test outputs in the release pack, or copy the attachment's already-built WASM/PCK as proof of current-source correctness.
