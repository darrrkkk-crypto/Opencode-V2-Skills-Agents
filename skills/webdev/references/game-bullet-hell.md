<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Horizontal Bullet-Hell Shooter — Godot Web

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).



`game-bullet-hell` is a playable horizontal shooter; **Space Dogfighter** is its sample theme. Preserve tuned pacing and working systems while adapting characters, setting and mechanics.

## English and Chinese UI
`autoload/i18n.gd` owns the active locale and `user://language.cfg` preference; `localization/en.json` and `localization/zh-CN.json` own all player-facing copy, including debug tuning. A fresh launch follows the system language (the browser language on Web): Chinese for `zh*`, otherwise English; a valid saved EN/CN choice wins on later launches. The title-screen **EN/CN** selector changes copy immediately and retains the choice through play, retry and returning to the title. Preserve its active indication and pointer, touch, keyboard and controller access without starting the game as a side effect. Keep catalog keys/placeholders in parity and use the template fonts with the bundled Noto Sans SC fallback for both locales. Run the locale test only from a hydrated temporary project copy: it deliberately refuses real player storage. In that copy, use this `override.cfg`, then run `"$GODOT_BIN" --headless --path . --script test/localization.gd` and capture representative title, gameplay, results and pause/tuning states in both languages before export. Keep the override and captures outside the delivered source.

```ini
[application]
config/use_custom_user_dir=true
config/custom_user_dir_name="ManusLocaleAcceptance-locale-check"
```

## Reference and completion contract

| Area | Working reference and adaptation requirement |
|---|---|
| Game loop | Three scrolling combat segments, five formation waves per segment, three elite encounters and a final boss; intro, transitions, victory, defeat and replay are implemented. Adapt the progression deliberately rather than dropping the complete loop. |
| Player and attacks | Keyboard/touch movement, automatic fire, three weapon upgrades, visible upgrade feedback, energy, a five-second laser and a three-hit shield. Keep the small central hit radius distinct from the ship artwork. |
| Enemies and feedback | Line/V/W formations, aimed fans, curved projectiles, telegraphed lasers, pickups, particles, shake, dialogue and score feedback. Attack warnings must remain readable and leave a feasible dodge route. |
| Presentation | A content-specific title, live HUD, three scrolling background layers, player and enemy artwork, English/Chinese UI with the template display/body fonts and the bundled Noto Sans SC fallback and a fixed 1280×720 / 16:9 canvas. Use centered letterboxing outside 16:9, never stretch or expose uncovered canvas. |
| Audio | Looping reference BGM and shot/hit/explosion cues. One BGM channel through the [shared browser adapter/native fallback](game-runtime.md#browser-safe-lifecycle) and three bounded SFX players; pause state changes are idempotent. Replace the catalog as needed, not the lifecycle guarantees. |
| Pause and navigation | `Esc` or the on-screen PAUSE control pauses/resumes. While paused, `M` or the central menu hint returns to the title. Victory/defeat can be replayed; `M` also returns to the title. |
| Tweak | The Addon renders the game-owned catalog with explicit Apply and consumer boundaries. Release builds hide the panel and do not load browser tuning overrides. Manus applies approved values to source defaults and re-exports; local saving is not source synchronization. |
| Persistence and delivery | Versioned local best score, all referenced assets restored and included in the PCK, source/pack tests passed, and a current checkpoint delivered for user browser acceptance. |

Implement every applicable row under the [shared completion contract](game-workflow.md#first-checkpoint-completion-contract).

## Source map and controls

| File | Responsibility |
|---|---|
| `project.godot`, `export_presets.cfg` | Fixed 16:9 viewport, bundled global font, main scene and Web export. |
| `scripts/title_screen.gd` | Title artwork, input gesture, start flow and best-score display. |
| `scripts/game.gd` | Phase machine, movement, projectiles, enemy formations, four bosses, abilities, particles, audio, HUD and pause; tuning values come from the active store. |
| `scripts/tuning_defaults.gd` | The twelve source defaults and typed descriptors; keep this the catalog/default-value owner. |
| `autoload/tuning_store.gd`, `scripts/manus/preview/tuning_adapter.gd` | Validated requested/active values and the Addon adapter. |
| `assets.lock.json`, `assets/template/` | Published reference artwork, audio and font. Hydrate through the shared asset runtime; apply [shared typography](game-workflow.md#default-typography). |
| `test/smoke.gd`, `test/template_contract.gd`, `test/tweak_controls.gd` | Tuned gameplay, weapon/boss progression, CJK, viewport, bounded audio, pause and tuning contracts. |
| `test/debug_capture.gd` | Deterministic Godot-native title, gameplay, boss and debug captures. |

Move with **WASD/arrows** or the left-side touch drag area; ordinary fire is automatic. At full energy, **K** activates the laser and **L** activates the shield; the right-side touch controls mirror them. **Esc / PAUSE** controls pause. **R** retries victory/defeat; touching the end screen also retries.

## Debug tuning and saving

`scripts/tuning_defaults.gd` owns descriptors and source defaults; `autoload/tuning_store.gd` owns validation,
requested/active values and sticky custom-run status. `scripts/manus/preview/tuning_adapter.gd` exposes them to the
Addon. Apply changes the running preview without local autosave; Save with Manus is the explicit source-edit path.

| Parameter | Meaning |
|---|---|
| `player_speed`, `fire_delay` | Ship movement and automatic fire interval. |
| `enemy_count`, `enemy_health`, `enemy_speed` | Formation-density, health and movement multipliers; `enemy_count` is not an absolute count. |
| `enemy_bullet_speed`, `boss_health` | Hostile projectile speed and boss-health multipliers. |
| `hit_radius` | Player's central damage radius, independent of rendered ship size. |
| `energy_rate`, `bone_drop` | Energy recharge and upgrade-drop probability. |
| `bgm_volume_db`, `sfx_volume_db` | Music and effect levels. |

Fire interval applies at the next player volley; enemy projectile speed at the next hostile volley; density at the next formation; enemy/boss health at the next corresponding spawn. Movement, hit radius, recharge, drop probability and audio apply live. These boundaries are called by the actual gameplay owners, not by panel rendering. Apply approved draft/requested values to `scripts/tuning_defaults.gd`, rebuild through the managed runtime, verify and checkpoint under [honest saving](game-runtime.md#development-tweak-when-needed). Release excludes Tweak UI and browser overrides.

## Bullet-hell asset and font wiring

The sample's title, layered space scenery, ships, pickups and audio live under `assets/template/` and are restored through `assets.lock.json`. Its ships use motion/transforms rather than character walk cycles. Preserve the small central damage radius and readable attack warnings independently of sprite size.

For user-uploaded fonts, apply the [shared typography policy](game-workflow.md#default-typography) and update project-local font checks accordingly. `assets/template/fonts/ui_regular.tres` selects the project-wide body face in both locales. Its fallback is the bundled `assets/template/fonts/NotoSansSC-VF.subset.woff2` (OFL, license beside it) with system fallback disabled. Run `python3 tools/install_cjk_font.py --check` after hydration and verify the bundled default font in the PCK. Preserve the small loader-only subset independently of this runtime font.

The audio implementation in `scripts/game.gd` has one BGM channel through the [shared browser adapter/native fallback](game-runtime.md#browser-safe-lifecycle) and three fixed SFX players. `_sync_audio_pause()` guards transition writes. `test/template_contract.gd` checks 10,000 idle/paused updates, font glyphs, fixed viewport and local tuning. Keep these contracts while adapting cues.

## Focused validation and checkpoint

```bash
# GODOT_BIN can point at the current installed Godot binary.
"$GODOT_BIN" --headless --path . --editor --import
pnpm test

# Use a real renderer, not the headless Dummy renderer, for visual captures.
"$GODOT_BIN" --path . test/debug_capture.tscn

# Managed runtime normally exports automatically; this is a local validation command.
pnpm export
pnpm verify-export
```

`pnpm verify-export` mounts the generated PCK and checks contents, title boot, gameplay and contracts; it requires pass markers, rejects script errors even with exit zero and enforces a timeout. `pnpm check` is only the watcher keep-alive shim. Follow [current-source artifact delivery](game-delivery.md#export-constraints).
