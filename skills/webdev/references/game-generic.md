<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Generic Game Template

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


## Reference identity and purpose
`game-generic` is the Godot 4.7.2 fallback scaffold for Manus GameDev. Its reference game is **Generic Game Template**, a two-stage collection/chase game with a minimalist graphite, porcelain, and brushed-metal presentation. The title action is **START GAME**. Collect every energy node and power-up while avoiding sentinels; complete both circuits to win.

Select it only without a matching specialized genre; follow the [game-generic exception](game-workflow.md#preserve-the-selected-template) for non-maze gameplay/UI.

The template intentionally contains **no default audio media**. Its silent baseline is an explicit template-owner choice; future adaptations follow the shared audio requirements and their user's choices.

## Source architecture
For an explicitly requested Godot 3D game, initialization selects `scenes/manus_world_3d.tscn` with `scripts/manus/world_3d.gd`: this single owner supplies the Node3D world, camera and movement. Read those actual paths first. The layout below describes the original 2D reference, whose maze owners are not the active 3D scene. The 3D overlay is a starting scaffold; replace its primitive world and scaffold checks with the requested game and meaningful outcomes.
```text
game-generic/
├── project.godot                  # identity, input, autoloads, font, viewport
├── template.json                 # stable game-generic catalog identity
├── assets.lock.json              # Runtime v2 permanent CDN mappings
├── assets/template/
│   ├── environment/              # studio backdrop and sparse foreground
│   ├── characters/               # porcelain runner and metal sentinel
│   ├── powerups/                 # energy, overdrive, shield, slow field, magnet
│   ├── ui/                       # text-free title and pause glass artwork
│   ├── fonts/                    # Template display/body fonts, Noto Sans SC + OFL licenses
│   └── provenance/               # generation prompts and optional audio contract
├── autoload/
│   ├── audio_director.gd         # optional cues, buses, streaming, bounded voices
│   ├── i18n.gd                   # catalogs and fallback/interpolation
│   ├── save_store.gd             # local scores, player/locale/tutorial state
│   └── tuning_store.gd           # authoritative values and apply boundaries
├── scripts/
│   ├── main.gd                   # title, session, HUD, menus, tutorial routing
│   ├── manus/preview/            # Addon-only tuning transport and adapter
│   ├── game/{stage_catalog,maze_world}.gd
│   ├── entities/{runner,sentinel}.gd
│   ├── ui/{screen_factory,tutorial_callout}.gd
│   ├── effects/effects_director.gd
│   └── score/run_score_service.gd
├── config/tuning.json            # typed six-category tuning catalog
├── localization/{en,zh-CN}.json
├── docs/minimalist-redesign.md   # concept, implementation plan, evidence
├── test/test_suite.gd
└── tools/                       # finite verification adapters, native capture, bounded font installation
```

`MazeWorld` owns simulation, `RunScoreService` owns score/finalization, and `TuningStore` owns configuration and run integrity. UI, art, shaders, particles and audio present that state. Save keys, stage IDs and tuning IDs remain compatible with earlier template runs; creative runtime IDs have been renamed to neutral terms.

## Game Addon tweaks
Reuse `config/tuning.json`, `TuningStore` and `scripts/manus/preview/tuning_adapter.gd`. The Addon generates its floating frosted-glass popover from game descriptors without resizing the preview; game code supplies parameters, not panel styling. Adapt or extend the examples for the requested game, with real consumers, stable IDs, localized labels/categories/descriptions, defaults, bounds/steps, integrity and honest LIVE/NEXT_ACTION/NEXT_STAGE/NEXT_RUN timing. Generic currently supports up to 128 number/boolean controls; other types need game-side support.

Keep one store and existing run-eligibility rules. Edits and resets change only the panel draft; unchanged or invalid drafts cannot Apply. Apply validates/commits the whole patch without persistence or reload; deferred values activate at their declared gameplay boundaries. Unchanged values emit nothing, and gameplay events never push catalogs. Do not add numeric tuning revisions.

After Apply, Save with Manus reads a snapshot and sends it to the task for source edits and normal build/checkpoint, never auto-publish. Release excludes the debug bridge and overrides while retaining source defaults and gameplay consumers.

These rules override frozen README tuning instructions: do not recreate a native panel, launcher, F10 shortcut or native Tweak capture. Preserve existing protocol/runtime guards; ordinary game generation needs no Addon transport implementation reading.

## Run and verify
```bash
npm run check                   # finite import, boot and game-owned outcome hooks
npm run build                   # current standalone export through the shared runtime
npm run check -- --pack          # verify that current export and applicable outcome hooks
```
Use the runtime directory returned by init/attach and the installed Game workflow. Keep meaningful game-specific hooks in optional `game-verification.json`; an absent hook file is normal before one is needed. Fresh compatibility aliases delegate to this same finite verifier. Older READMEs and `tools/verify.sh` may hardcode the maze scene, obsolete resource-audit assumptions or a different `dist/index.pck`; adapt relevant outcome hooks instead of repairing that separate pipeline. Asset sync/build own dependency, hash and current-export checks. The Web preset uses `thread_support=false`; developer tools and fixtures stay outside the playable export.

The original 2D reference's native capture uses the actual viewport and renderer; adapt its scene/state selectors for another game and run without `--editor`:
```bash
GENERIC2D_CAPTURE_PATH=/absolute/path/title.png "$GODOT_BIN" --path . --script tools/capture_native.gd
GENERIC2D_CAPTURE_PATH=/absolute/path/game.png GENERIC2D_CAPTURE_GAME=1 "$GODOT_BIN" --path . --script tools/capture_native.gd
GENERIC2D_CAPTURE_PATH=/absolute/path/pause.png GENERIC2D_CAPTURE_PAUSE=1 "$GODOT_BIN" --path . --script tools/capture_native.gd
```
`GENERIC2D_CAPTURE_ZH=1` selects Chinese; `GENERIC2D_CAPTURE_TUTORIAL=1` with the game flag captures onboarding. Use a real renderer; headless Dummy output is not visual evidence. Browser acceptance belongs to the user under the shared workflow.

## Controls and playable loop
| Action | Keyboard | Gamepad | Pointer/touch |
| --- | --- | --- | --- |
| Move | WASD / arrows | Left stick / D-pad | Direction pad |
| Pause/resume | Escape | Start | Pause / Resume |
| Activate focused UI | Enter / Space | Primary action | Click / tap |

Title → Start → Stage 1 → Stage 2 → Result → Retry / Title. Pause supports resume, confirmed stage restart and confirmed return to title. Local results persist through `SaveStore`. Developer tuning is rendered by the Addon outside the game. Both EN and zh-CN are bundled.

Event-driven callouts teach movement, collection and power-ups; title arms replay. Preserve [shared skip/dismissal and developer-control separation](game-workflow.md#tutorial-content-boundary).

## Stage and score contracts
`StageCatalog.STAGES` stores 21×17 layouts, palette, spawn positions and speed multipliers. Validation checks legal symbols, rectangular rows, exactly one player spawn, enemies, collectibles and connected walkable cells. Add stages through catalog data rather than duplicating the controller.

| Symbol | Meaning | Score/event |
| --- | --- | --- |
| `#` | Connected solid wall | None |
| `.` | Energy node | `energy`: 10 |
| `o` | Overdrive; permits disabling sentinels | `overdrive`: 50 |
| `s` | Shield; collision protection | `powerup`: 75 |
| `t` | Slow field; enemy slowdown | `powerup`: 75 |
| `m` | Magnet; nearby connected-node collection | `powerup`: 75 |
| `P` | Player spawn | None |
| `E` | Sentinel spawn | `sentinel_disable`: 200 when overdriven |

Clearing a stage awards `stage_clear`: 500. `RunScoreService.authored_collectible_maximum()` excludes repeatable sentinel disables. Score is bounded to 999,999,999; `finalize()` produces an immutable once-only result containing score, stage, outcome, duration, tutorial status and integrity marker.

## Minimalist presentation
`ScreenFactory` owns graphite panels, hairlines, cool blue focus states, neutral secondary buttons and the light primary action. Real Godot text renders every label. The HUD uses separate status and wrapping effect rows; power-up timers remain visible in portrait. World scaling fits below the HUD and leaves touch-control space. Actor sprites remain centered on their grid positions without vertical bobbing.

The reference uses eleven separately generated original raster assets. Prompt/source/runtime mappings are recorded in `assets/template/provenance/IMAGEGEN.md`. Original generated outputs remain in generation history; shipped media is restored from permanent CDN mappings. No old picnic art or default sound assets are part of the current payload. Connected maze walls and path-facing borders remain code-native.

The effects director owns twelve recycled burst emitters and one ambient emitter. Reduced Motion disables ambient movement and uses restrained feedback. The default particle density is 0.4 and studio filter strength is 0.18. There is no continuous player trail.

## Optional audio engine
`AudioDirector.CUES` retains semantic IDs for logical title/gameplay music, confirm/cancel, action, impact, reward, pause, victory and defeat. All default paths are empty. Master/Music/SFX/UI buses, two music channels through the [shared browser BGM adapter/native fallback](game-runtime.md#browser-safe-lifecycle), eight effect voices, two UI voices, crossfade, looping, pause ducking and mute/volume remain intact.
Apply [shared audio sourcing](game-workflow.md#audio-production-as-needed): music routes remain empty for silent BGM or share one approved track; required SFX are independent.

```gdscript
# After importing project-owned audio:
AudioDirector.register_cue("score.reward", "res://assets/template/audio/reward.ogg")
# Only when BGM is implemented under the shared audio workflow:
AudioDirector.register_cue("music.title", "res://assets/template/audio/music.ogg")
AudioDirector.register_cue("music.gameplay", "res://assets/template/audio/music.ogg")
```
`register_stream()` accepts an existing AudioStream; `unregister_cue()` clears it. Empty/missing resources, wrong resource types, null streams and unknown IDs return `false` safely. A missing music route stops previous music. There are no synthetic fallback tones or automatic downloads. A real button/input gesture unlocks playback. Tests use an in-memory fixture, never a shipped placeholder file. See `assets/template/provenance/AUDIO.md`.

## Local standings
Local top-ten standings persist scores and configuration provenance. No dormant global-leaderboard adapter or hidden network UI ships. Add global integration only when explicitly requested.

## Localization and fonts
Uploads follow [shared typography](game-workflow.md#default-typography); update project-local checks. Visible copy uses `I18n.t(key, replacements)`. By default `assets/template/fonts/ui_regular.tres` binds the template body face with `assets/template/fonts/NotoSansSC-VF.subset.woff2` fallback. Verify its full common-character repertoire:
```bash
python3 tools/install_cjk_font.py --check
```
Checks cover key parity, Chinese/player-name glyphs and the primary font. Default runtime/loader fonts are OFL; keep each `<Family>-OFL.txt` beside its font. `tools/build_cjk_font_subset.py` launches the default-font installer; fixed loader text uses a separately pinned subset.
