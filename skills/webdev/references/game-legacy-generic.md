# Generic Game Template

Legacy-only gameplay contract: keep the installed project and protocol; new initialization selects newer revisions. Read the selected starter's matching guide; paths below are relative to its project root. [Game workflow](game-workflow.md) owns initialization, Preview, release preparation and deployment. Source-specific test/export commands are diagnostics only, not lifecycle replacements; serialize them with active Game builds. [Shared game rules](game-workflow.md) take precedence for gameplay/art/audio policy. First-checkpoint completion means the first completed-game deliverable, excluding bootstrap and intermediate version saves.


## Reference identity and purpose
`game-generic` is the Godot 4.7.2 fallback scaffold for Manus GameDev. Its reference game is **Generic Game Template**, a two-stage collection/chase game with a minimalist graphite, porcelain, and brushed-metal presentation. The title action is **START GAME**. Collect every energy node and power-up while avoiding sentinels; complete both circuits to win.

The reference proves movement, AI, stages, scoring, persistence, onboarding, tuning, effects, optional audio, localization, and Web transport. It does not define the genre of games created from this scaffold. It is the currently installed Addon scaffold for all Game projects. When adapting it: preserve genre-independent infrastructure and replace gameplay/in-game UI for a non-maze request.

Built-in reference media lives under `assets/template/` with `groupId: "template"` in `assets.lock.json`. Keep new project assets outside this reserved directory and choose their groups according to the game.

The template intentionally contains **no default audio media**. Its silent baseline is an explicit template-owner choice; future adaptations follow the shared audio requirements and their user's choices.

## Source architecture
```text
game-generic/
├── project.godot                  # identity, input, autoloads, font, viewport
├── .manus-game-template.json      # installed starter identity and provenance
├── assets.lock.json              # Runtime v2 permanent CDN mappings
├── assets/template/              # built-in reference assets only
│   ├── environment/              # studio backdrop and sparse foreground
│   ├── characters/               # porcelain runner and metal sentinel
│   ├── powerups/                 # energy, overdrive, shield, slow field, magnet
│   ├── ui/                       # text-free title and pause glass artwork
│   ├── fonts/                    # bundled fonts; migrate using current typography contract
│   └── provenance/               # generation prompts and optional audio contract
├── autoload/
│   ├── audio_director.gd         # optional cues, buses, streaming, bounded voices
│   ├── i18n.gd                   # catalogs and fallback/interpolation
│   ├── save_store.gd             # local scores, player/locale/tutorial state
│   ├── tuning_store.gd           # validated deltas and apply boundaries
│   └── sandbox_bridge.gd         # local tuning envelope and optional parent message
├── scripts/
│   ├── main.gd                   # title, session, HUD, menus, tutorial routing
│   ├── game/{stage_catalog,maze_world}.gd
│   ├── entities/{runner,sentinel}.gd
│   ├── ui/{screen_factory,tutorial_callout,tuning_panel}.gd
│   ├── effects/effects_director.gd
│   └── score/run_score_service.gd
├── config/tuning.json            # typed six-category tuning catalog
├── localization/{en,zh-CN}.json
├── test/test_suite.gd
└── tools/                       # resource audit, native capture, verification, font subsetting
```

`MazeWorld` owns simulation, `RunScoreService` owns score/finalization, and `TuningStore` owns configuration and run integrity. UI, art, shaders, particles and audio present that state. Save keys, stage IDs and tuning IDs remain compatible with earlier template runs; creative runtime IDs have been renamed to neutral terms.

## Run and verify
```bash
./tools/verify.sh                 # resource audit, import, deterministic suite, bounded boot
./tools/verify.sh --export        # also builds and verifies an isolated Web pack
./tools/verify_clean_scaffold.sh  # isolated copy, fresh Godot import cache
```
Set `GODOT_BIN` when Godot is not on PATH or at the standard macOS application path. Node.js runs the resource audit: every runtime source must be reachable from the project, every asset must have a live reference and matching manifest hash, and import/UID sidecars must have owners. The Web preset uses `thread_support=false`; tools, test fixtures and provenance are excluded from the playable export. Managed Manus sessions use the existing Game Dev runtime for serving, asset hydration, exports and checkpoint artifacts.

Native visual capture uses the actual viewport and renderer:
```bash
GENERIC2D_CAPTURE_PATH=/absolute/path/title.png godot --path . --script tools/capture_native.gd
GENERIC2D_CAPTURE_PATH=/absolute/path/game.png GENERIC2D_CAPTURE_GAME=1 godot --path . --script tools/capture_native.gd
GENERIC2D_CAPTURE_PATH=/absolute/path/pause.png GENERIC2D_CAPTURE_PAUSE=1 godot --path . --script tools/capture_native.gd
```
`GENERIC2D_CAPTURE_ZH=1` selects Chinese; `GENERIC2D_CAPTURE_TUTORIAL=1` with the game flag captures onboarding; `GENERIC2D_CAPTURE_TWEAK=1` captures developer controls. Use a real renderer; headless Dummy output is not visual evidence. Use [Game workflow](game-workflow.md) for Web verification and remaining user acceptance.

## Controls and playable loop
| Action | Keyboard | Gamepad | Pointer/touch |
| --- | --- | --- | --- |
| Move | WASD / arrows | Left stick / D-pad | Direction pad |
| Pause/resume | Escape | Start | Pause / Resume |
| Activate focused UI | Enter / Space | Primary action | Click / tap |
| Developer controls | F10 in debug | Focus launcher | Tweak Controls in debug |

Title → Start → Stage 1 → Stage 2 → Result → Retry / Title. Pause supports resume, confirmed stage restart, confirmed return to title and developer tuning in debug. Local results persist through `SaveStore`. Tuning overlays preserve previous simulation and focus state. Both EN and zh-CN are bundled.

Tutorial callouts teach movement, collection and power-ups through real events. **Skip tutorial** remains visible during prompts and action-waiting steps. Skipping dismisses the overlay, releases input/simulation and records completion. Replaying is armed from the title. Developer controls are excluded from tutorial content.

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
`AudioDirector.CUES` retains semantic IDs for logical title/gameplay music, confirm/cancel, action, impact, reward, pause, victory and defeat. All default paths are empty. Master/Music/SFX/UI buses, two streaming music players, eight effect voices, two UI voices, crossfade, looping, pause ducking and mute/volume remain intact.

```gdscript
# After importing project-owned audio:
AudioDirector.register_cue("score.reward", "res://assets/audio/reward.ogg")
AudioDirector.register_cue("music.title", "res://assets/audio/music.ogg")
AudioDirector.register_cue("music.gameplay", "res://assets/audio/music.ogg")
```
`register_stream()` accepts an existing AudioStream; `unregister_cue()` clears it. Empty/missing resources, wrong resource types, null streams and unknown IDs return `false` safely. A missing music route stops previous music. There are no synthetic fallback tones or automatic downloads. A real button/input gesture unlocks playback. Tests use an in-memory fixture, never a shipped placeholder file. See `assets/template/provenance/AUDIO.md`.

## Tuning and persistence
`config/tuning.json` drives UI, Gameplay, Audio, Player, Enemies and Environment categories. It defines stable IDs, type/default/bounds, labels, descriptions, integrity class and LIVE/NEXT_ACTION/NEXT_STAGE/NEXT_RUN boundaries. Requested and active values are distinct; validation is transactional. Persisted values are versioned non-default deltas; gameplay changes make local practice eligibility sticky for the run, while cosmetic values preserve it.

The bottom-right Tweak Controls launcher rests at 50% opacity and reaches full opacity on hover/focus. The launcher, F10 and tuning panel are gated to debug builds. Release builds ignore saved developer overrides. Browser-local drafts and the emitted tuning envelope are separate from source defaults. The installed Addon does not consume the reference's same-origin tuning message as a source write; inspect the draft and apply approved values to config/tuning.json explicitly.

Local top-ten standings persist scores and configuration provenance. No dormant global-leaderboard adapter or hidden network UI ships. Add global integration only when explicitly requested.

## Localization and fonts
Visible copy resolves through `I18n.t(key, replacements)`. Follow the [current typography contract](game-workflow.md#default-typography): default to bundled ManusCC0 with ManusCC0 Sans CJK SC fallback, and allow unrestricted user-uploaded fonts. For font changes, update theme overrides, hydration pins, loader sources and project-local checks together; preserve gameplay and protocol. Check chosen-font rendering, Chinese player names and actual Web font resolution; diagnostics do not block uploaded-font choices.
The deterministic tests check key parity, Chinese/runtime glyph coverage and primary font selection.
