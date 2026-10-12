# Platformer Game Template (Godot 4.7.2 → Web/WASM)

Legacy-only gameplay contract: keep the installed project and protocol; new initialization selects newer revisions. Read the selected starter's matching guide; paths below are relative to its project root. [Game workflow](game-workflow.md) owns initialization, Preview, release preparation and deployment. Source-specific test/export commands are diagnostics only, not lifecycle replacements; serialize them with active Game builds. [Shared game rules](game-workflow.md) take precedence for gameplay/art/audio policy. First-checkpoint completion means the first completed-game deliverable, excluding bootstrap and intermediate version saves.


A **complete, playable browser platformer reference** originally authored with Godot 4.7.1 and GDScript; use the Addon-required Godot 4.7.2 stable and verify compatibility. It includes a title screen, a long side-scrolling level, keyboard and touch controls, tunable movement, enemies, coins, question blocks, checkpoints, generated art, animation frames, score persistence, deterministic tests, and the Web/WASM publishing path.
## Definition of done: complete game delivery
**A game is not complete merely because it boots, shows the reference level, or demonstrates one mechanic. Do not claim completion, create the final checkpoint, or publish until every requirement below is satisfied with observable evidence.** These requirements apply by default; omit one only when the user explicitly excludes that part of the game, and state the exclusion in the final response.
Also satisfy the shared completion evidence. The table below adds this template’s requirements.
| Required part | Completion evidence |
|---|---|
| Purpose-built art | Replace irrelevant template art and copy with a coherent visual set at production sizes. Include the backgrounds, world pieces, characters, items, and UI needed by the finished game; do not present placeholders as final assets. |
| Audio when needed | Follow shared optional audio production; reuse fitting cues and check changed routing. |
| Tuning and debug support | Gameplay-feel values are adjustable through `TuningStore` and the debug-only panel. Debug drafts can be saved in the browser; approved source defaults are updated in `scripts/tuning_store.gd`. Add deterministic debug states or captures for new mechanics, and keep debug UI hidden from normal release players. |
| Persistence where required | Player-facing progress or scores that should survive a reload are saved, loaded, versioned, and exercised in the real Web build. |
| Automated and visual verification | Resource import, gameplay smoke, representative screenshots, exported-pack checks, and the actual Web preview all pass. New mechanics add assertions and representative visual coverage. |
| Release-ready delivery | The final Web export matches current sources, contains every runtime asset, excludes test outputs, respects size limits, starts without console errors, and uses the intended title and instructions. |
## Development loop
1. Read the relevant implementation in `scripts/`, then make the smallest playable change.
2. After a coherent edit batch, use the packaged preview-build.mjs described in [Game workflow](game-workflow.md). Keep the resident preview running.
3. Run deterministic smoke, Godot-native captures, and exported-pack checks, then save a checkpoint for user browser acceptance under the shared verification workflow. Read `.manus-logs/browserConsole.log` to diagnose reported Web failures.
4. Use `F1` in a debug build to tune gameplay values. Save a browser-local debug draft when useful, then copy approved values into `scripts/tuning_store.gd` and request a preview build.
5. Run the smoke, visual, and audio checks after gameplay, scene, or asset changes.
6. Save a checkpoint only after the game is playable. Satisfy the definition of done before the final checkpoint or completion claim.
## Playable reference map
| Path | Working reference included in the template |
|---|---|
| `scenes/title_screen.tscn` + `scripts/title_screen.gd` | Styled title screen, score display, keyboard and button start flow |
| `scenes/game.tscn` + `scripts/game.gd` | Full level construction, HUD, score, timer, checkpoints, respawn, camera, and finish flow |
| `scripts/player.gd` | `CharacterBody2D` platforming with acceleration, friction, gravity, coyote time, jump buffering, variable jump height, stomping, and animation |
| `scripts/entities.gd` | Reusable coins, walking enemies, question blocks, and goal flag |
| `scripts/tuning_store.gd` + `scripts/tuning_panel.gd` | Source defaults, live editing, optional browser-local debug drafts, reset, and debug-only UI |
| `scripts/world_art.gd` | Three generated parallax layers with different scroll speeds |
| `scripts/touch_input.gd` | Floating touch joystick; horizontal drag moves and upward drag jumps |
| `scripts/save_store.gd` | Versioned score persistence in `user://` |
| `assets/template/generated/` | Complete background, foreground, tile, hero, and running animation assets |
| `tools/art_pipeline/` | Parameterized video-frame extraction, background removal, and aligned animation-frame processing tools |
| `test/smoke.gd` | Boots both scenes and verifies keyboard/touch movement, stomping, live tuning, and checkpoint respawn |
| `test/debug_capture.tscn` | Drives the game into representative states and saves title/gameplay/tuning screenshots |
| `test/exported_pack_boot.gd` | Boots the exported PCK main scene to catch omitted resources |
| Game runtime | Local Web export/preview, asset sync, and published-site assembly; the platform manages this runtime outside the project scaffold |
## How to adapt the reference
Keep the infrastructure that already works: input actions, touch input, `SaveStore`, `TuningStore`, debug gating, tests, Web preset, preview, and publishing. Replace the level layout, copy, art, rules, and scoring required by the new game.
Follow the shared ownership boundaries.
For the broader production workflow, read `docs/GAME_PRODUCTION_PLAYBOOK.md` before tasks involving game feel, generated character animation, layered backgrounds, generated audio, visual capture tests, or release preparation.
## Tuning and debug builds
`TuningStore.DEFAULTS` owns the gameplay defaults. `TuningPanel.RANGES` owns the debug control ranges and labels. Press `F1` in a debug build to edit values live. The **下次继续（调试）** button stores the current values in the browser profile; **恢复默认** restores `TuningStore.DEFAULTS`.
After approving a tuning pass, update the matching values in `scripts/tuning_store.gd`, request a preview build, and verify the real Web build. The Game Dev preview enables the panel for the owner; normal published URLs do not expose its controls.
## Art workflow
The reference art is deliberately included so new games start with a visually complete sample. Replace assets gradually and verify each replacement in the running game.
Follow the shared video-first animation workflow before processing or integrating character frames. Verify the animation in motion and in Debug captures.
Follow the shared asset storage and import rules.
Check FFmpeg in the current execution environment before video extraction. The image-processing tools require Pillow:
```bash
# Keep raw video and extracted PNGs outside the Godot project.
uv run python tools/art_pipeline/extract_video_frames.py ../game-art-sources/run.mp4 ../game-art-sources/run_frames/ --fps 12 --start 0.4 --duration 1.4
uv run --with-requirements tools/art_pipeline/requirements.txt python tools/art_pipeline/remove_image_background.py input.webp output.webp
uv run --with-requirements tools/art_pipeline/requirements.txt python tools/art_pipeline/process_animation_frames.py ../game-art-sources/run_frames/ assets/characters/hero/run/ --pattern 'frame_*.png' --prefix run
```
After adding or replacing art, run an import before other tests:
```bash
godot --headless --path . --import
```
## Audio integration
Follow the current shared optional audio workflow: reuse fitting permitted audio, and generate only for a concrete need. No separate cue sheet is required. The generation recipes below apply only when new audio is needed.
For the preferred Manus Max Mode BGM workflow, use one `generate_music` call for the single BGM track of 180 seconds or shorter. Follow [audio production as needed](game-workflow.md#audio-production-as-needed) for effects; never use the BGM workflow as an SFX generator. Only plan multiple source clips for a requested BGM duration beyond that limit, then assemble one final track. Each call writes one `.wav` or `.mp3` file and supports up to about 184 seconds. Set its `path` to an absolute source path outside the Godot project, then convert only the selected final result into `assets/generated/audio/` as OGG.
| Deliverable | Prompt requirements |
|---|---|
| Gameplay BGM | Begin with `Instrumental only, no vocals`, then state exact duration and BPM. Specify genre, mood, key or scale, instrumentation, density, arrangement, space, and production quality. Ask for a stable loop-friendly body with no long intro, final cadence, or fade-out. Do not name an artist, song, or album. A normal game loop should fit in one call of 180 seconds or less. |
| One-shot sound effect | Generate each cue separately. State the target duration, game event, material and motion, intensity, tonal palette, and perspective. Require an immediate onset, short clean tail, and no vocals, speech, music bed, unrelated ambience, or extra events. If the result is longer than the clean cue, trim it before import. |
Adapt these as single continuous prompts and replace every bracketed field:
```text
Instrumental only, no vocals. Create a [duration]-second loop-friendly game BGM at [BPM] in [key or scale]. [Genre and mood]. Use [instrumentation] with [density and brightness]. [Arrangement with optional timestamp cues whose final timestamp equals the requested duration]. [Soundscape and stereo space]. Clean high-quality game mix. Keep a stable loop-friendly body with no long intro, final cadence, or fade-out. Avoid [unwanted instruments, moods, or behaviors].  Create a [duration]-second standalone game sound effect for [exact event]: [material, motion, intensity, tonal palette, and listening perspective]. Immediate onset, one clearly isolated event, short clean tail, dry high-quality game mix. No vocals, no speech, no music bed, no unrelated ambience, and no additional events.
```
After generation:
1. Audition every result and reject cues with speech, unwanted music, excessive silence, clipping, or an incorrect event.
2. Trim the selected region and convert it to OGG. Do not ship generated WAV files in the game package.
3. Register the loop and one-shot effects in the centralized audio engine required by the shared baseline. Its bounded players route BGM and SFX through separate buses; gameplay emits semantic cues rather than allocating scene-local players.
4. Start Web BGM only after the player presses the start button or provides another user gesture. Provide mute and volume controls when audio is present, and persist player-facing settings when appropriate.
5. Add smoke assertions that required streams load and important events trigger the intended players. After checkpoint delivery, ask the user to test the real Web preview with audio enabled: listen through a full loop, exercise every cue, check repeated and overlapping effects, and confirm that mute, volume, scene changes, restart, failure, and success behave correctly.
Example conversion after selecting the generated source files:
```bash
mkdir -p assets/generated/audio
ffmpeg -y -i ../game-audio-sources/level-theme.wav -c:a libvorbis -q:a 5 assets/generated/audio/bgm_level.ogg
ffmpeg -y -i ../game-audio-sources/coin.wav -c:a libvorbis -q:a 5 assets/generated/audio/sfx_coin.ogg
```
The starter has empty audio routes. Preserve safe silence unless audio is requested or needed; reuse or produce fitting audio under the current shared workflow. Empty optional BGM does not make delivery incomplete.
## Template-specific diagnostics
Use the shared log guide for export, runtime, network, and replay errors.
| Symptom | Where the answer is |
| --- | --- |
| Whether the screen looks right | the registered screenshot or browser capability |
## Verification commands
Run these from the generated game project directory:
```bash
# Scene, world, movement, and tuning smoke test
godot --headless --path . -s test/smoke.gd

# Render deterministic title, gameplay, and tuning screenshots
GAME_CAPTURE_DIR=../game-captures xvfb-run -a godot --audio-driver Dummy \
  --path . --resolution 1280x720 res://test/debug_capture.tscn

# Export, then verify its contents and configured main scene from an isolated directory
pnpm export
pnpm verify-export
```
The smoke test must print `[SMOKE_PASS]`, the capture test must print `[DEBUG_CAPTURE_PASS]`, and the PCK checks must print `[PCK_CONTENTS_PASS]` and `[PCK_BOOT_PASS]`.
If `godot` is not on `PATH`, set `GODOT_BIN` to the executable before running `pnpm verify-export`.
## Template-specific constraints
Apply the shared export constraints, plus:
- Follow the shared native-capture and checkpoint handoff workflow. Ask the user to accept the actual Web preview; headless success does not prove rendering success.
## Publishing
**Save a checkpoint, then publish** once this template’s definition of done is satisfied. Follow the shared checkpoint artifact and publishing workflow.
## Template-specific failures
Check the shared common failures first.
- **Movement feels wrong:** tune it in the F1 panel, copy approved values into `scripts/tuning_store.gd`, then request one preview build and verify the updated game.
- **Generated audio does not fit:** regenerate the specific BGM or cue with a tighter duration, event, sonic-palette, and negative description; do not keep an unrelated result merely because a file was produced.
