# Platformer Game Template (Godot 4.7.2 → Web/WASM)

Legacy-only gameplay contract: keep the installed project and protocol; new initialization selects newer revisions. Read the selected starter's matching guide; paths below are relative to its project root. [Game workflow](game-workflow.md) owns initialization, Preview, release preparation and deployment. Source-specific test/export commands are diagnostics only, not lifecycle replacements; serialize them with active Game builds. [Shared game rules](game-workflow.md) take precedence for gameplay/art/audio policy. First-checkpoint completion means the first completed-game deliverable, excluding bootstrap and intermediate version saves.


The current playable theme is **Calico Yarn Adventure**: a wool-felt calico exotic shorthair cat collects dried fish, defeats robot vacuums, and traverses felt terrain. Press **J/X** (or the on-screen YARN button) to fire a yarn ball in the facing direction. Missed yarn makes three ground rebounds and disappears when the third rebound lands; hits and walls consume it immediately. Shots have cooldown, swept wall/enemy collision, a lifetime and a hard count limit; tree pause freezes them and scene teardown frees them. `attack_cooldown`, `yarn_speed` and `yarn_lifetime` live in the existing Tweak schema. `pnpm verify-export` includes `test/yarn_combat.gd`. Cat standing/running sprites share one reference, continuous-video-derived frames, a 192×192 canvas and a common foot baseline.
A **complete, playable browser platformer reference** originally authored with Godot 4.7.1 and GDScript; use the Addon-required Godot 4.7.2 stable and verify compatibility. It includes a title screen, pause and main-menu navigation, keyboard and touch controls, checkpoint-ready Tweak controls, a reachable-jump reference route, enemies, collectibles, generated art, animation frames, reusable particle feedback, score persistence, deterministic tests, and the Web/WASM publishing path.
## Definition of done: complete game delivery
**A game is not complete merely because it boots, shows the reference level, or demonstrates one mechanic. Do not claim completion or publish until every requirement below is satisfied with observable evidence.** Once the deterministic requirements pass, follow the shared verification and handoff workflow. These requirements apply by default; omit one only when the user explicitly excludes that part of the game, and state the exclusion in the final response.
Also satisfy the shared completion evidence. The table below adds this template’s requirements.
| Required part | Completion evidence |
|---|---|
| Bounded viewport | The actual game surface stays between 1:1 and 16:6, with centered letterboxing outside that range; UI and touch coordinates follow the game surface rather than the outer preview. |
| Game-specific start screen | The first checkpoint meets the title-screen art requirements; its title, instructions, and Start action are readable and usable. |
| CJK-safe UI typography | Follow the current typography contract, including user-uploaded fonts. Every runtime string has bundled glyph coverage; Godot Web never relies on a system CJK font. Smoke and exported-PCK tests prove representative Chinese, Latin, numbers, punctuation, and arrows exist, and the user confirms the delivered checkpoint has no tofu boxes or missing glyphs in a real browser. |
| Pause and navigation | `Esc` and the touch pause button stop gameplay and open a real pause menu. Resume returns to the same state, **Tuning** opens the debug panel when available, and **Return to Main Menu** reaches the title screen without reloading the page. |
| Complete purpose-built scene art | By the **first user-facing checkpoint**, replace irrelevant template art and every visible prototype shape with a coherent, game-specific asset set. Unless the user explicitly requests a geometric, abstract, or procedural style, ground and platforms, backgrounds, trees, rocks, buildings, vegetation, major props, characters, and items must use purpose-built generated or user-provided art; native Godot UI is acceptable when deliberately styled to the same direction. Plain rectangles, circles, polygons, debug drawing, and unstyled primitives are allowed for collision, navigation, prototypes, and effects—not as final scene art. |
| Gameplay feedback and visual effects | Keep or replace the working particle feedback for jumping, landing, collecting, stomping, death, checkpoints, and completion. Every important action must have immediate visual confirmation that matches the new art direction; removing `VisualEffects` without an equivalent is incomplete. |
| Audio when needed | Follow shared optional audio production; reuse fitting cues and check changed routing. |
| Tuning and debug support | Preserve `config/tuning.json`, `TuningStore`, and `TuningPanel` as working infrastructure, not prose-only guidance. Every gameplay-feel value—including jump power, gravity, short-hop cutoff, movement, enemies, camera, and timing—must be adjustable in the panel. Changes auto-save in the browser; Manus applies approved values to source defaults and re-exports the game. The debug Preview exposes the panel, while checkpoint and published release players do not see it. |
| Persistence where required | Player-facing progress or scores that should survive a reload are saved, loaded, versioned, and covered by deterministic tests. Browser acceptance happens from the delivered checkpoint. |
| Automated and visual verification | Resource import, gameplay smoke, Godot-native viewport screenshots, and exported-pack checks pass. Tests prove `Esc` pause/resume, main-menu wiring, the Tweak entry point, and that the default full-jump envelope clears every required platform rise with margin. New mechanics add assertions and representative Godot capture coverage. Browser acceptance follows the shared verification workflow. |
| Checkpoint-ready delivery | The Web export matches current sources, contains every runtime asset, excludes test outputs, respects size limits, and uses the intended title and instructions. A normal checkpoint is saved and handed to the user for browser acceptance. |
## Development loop
1. Start from the running reference. Keep `PauseMenu`, `VisualEffects`, `TuningStore`, `TuningPanel`, their event wiring, and their tests alive while replacing the theme and mechanics; a wholesale rewrite that drops them is incomplete.
2. Read the relevant implementation in `scripts/`, then make the smallest playable change. Before the first checkpoint, finish the environment, character, prop, item, and UI asset pass; do not checkpoint a gameplay-complete scene whose visible world is still built from prototype geometry.
3. After a coherent edit batch, use the packaged preview-build.mjs described in [Game workflow](game-workflow.md). Keep the resident preview running.
4. Run the Godot smoke and native capture tests. Use their failures to correct the implementation directly.
5. Run the exported-pack check, save a normal checkpoint, and complete the shared verification and browser-acceptance handoff.
6. Ask the user to press `F1` or choose **Tuning** from the pause menu and tune the gameplay values. Slider changes auto-save locally.
7. Ask Manus to apply approved values to `config/tuning.json`, request a preview build, and verify the result.
8. Rerun the deterministic checks and save the updated checkpoint.
## Native capture implementation
Follow the shared verification and handoff workflow. This template’s native harness is `test/debug_capture.gd`: arrange representative deterministic states, capture the live viewport with `get_viewport().get_texture().get_image()`, and save PNGs with `Image.save_png()`. Pair each capture with state assertions and use the commands below.
## Playable reference map
| Path | Working reference included in the template |
|---|---|
| `scenes/title_screen.tscn` + `scripts/title_screen.gd` | Styled title screen, score display, keyboard and button start flow |
| `scenes/game.tscn` + `scripts/game.gd` | Full level construction, HUD, score, timer, checkpoints, respawn, camera, and finish flow |
| `scripts/pause_menu.gd` | `Esc` and touch pause flow with Resume, debug Tuning, and Return to Main Menu actions |
| `scripts/player.gd` | `CharacterBody2D` platforming with acceleration, friction, gravity, coyote time, jump buffering, variable jump height, stomping, and animation |
| `scripts/entities.gd` | Reusable coins, walking enemies, question blocks, and goal flag |
| `scripts/game_audio.gd` + `scripts/audio_catalog.gd` | Persistent streamed BGM, bounded SFX pool, pause/menu cleanup, and replaceable static asset mapping |
| `scripts/visual_effects.gd` | Web-compatible `CPUParticles2D` presets for jump and landing dust, collection sparkles, stomp impact, death burst, checkpoint feedback, and finish confetti |
| `config/tuning.json` | Single schema for tuning keys, source defaults, ranges, steps, labels, precision, and units |
| `scripts/tuning_store.gd` + `scripts/tuning_panel.gd` | Schema-driven live editing, automatic browser persistence, reset, and debug-only UI |
| `scripts/world_art.gd` | Dimmed screen-space felt scenery, independent of camera zoom |
| `scripts/touch_input.gd` | Floating touch joystick; horizontal drag moves and upward drag jumps |
| `scripts/save_store.gd` | Versioned score persistence in `user://` |
| `assets/template/backgrounds/`, `collectibles/`, `enemies/`, `audio/` | User-supplied title background, coin/enemy artwork, one BGM and eight SFX cues |
| `assets/template/cat/` | Current calico character and run frames, robot, dried fish, yarn, felt terrain, cat tree, warm scenery and game-specific title art |
| `assets/template/generated/` | Retained original reference assets |
| `fonts/fusion-pixel-12px-proportional-zh_hans.woff2` | Historical font path; replace through the current typography contract |
| `tools/art_pipeline/` + `tools/font_pipeline/` | Parameterized media processing plus reproducible runtime-text collection and `pyftsubset` font generation |
| `test/smoke.gd` | Boots both scenes and verifies keyboard/touch movement, particle presets and jump/landing wiring, pause/menu flow, reachable jumping, stomping, live tuning, and checkpoint respawn |
| `test/debug_capture.tscn` | Drives the game into representative states and saves title, particle-enhanced gameplay, pause, and tuning screenshots |
| `test/exported_pack_boot.gd` | Boots the exported PCK main scene to catch omitted resources |
| Game runtime | Local Web export/preview, asset sync, and published-site assembly; the platform manages this runtime outside the project scaffold |
## How to adapt the reference
Keep the infrastructure that already works: input actions, touch input, `ViewportPolicy`, `GameAudio`, `PauseMenu`, `VisualEffects`, `SaveStore`, `TuningStore`, `TuningPanel`, debug gating, tests, Web preset, preview, and publishing. Replace the level layout, copy, art, rules, scoring, and effect styling required by the new game. **Before checkpoint delivery, explicitly prove that `Esc`, the touch pause button, Resume, Return to Main Menu, `F1`, the pause-menu Tuning button, and the required gameplay feedback still work.**
Follow the shared ownership boundaries, with these additional owners:
- `pause_menu.gd` owns pause presentation and navigation actions; `game.gd` coordinates it with Tuning and scene changes.
- `visual_effects.gd` owns reusable particle construction and styling; gameplay scripts emit semantic events instead of duplicating particle setup.
For platformer-specific supplements, read `docs/GAME_PRODUCTION_PLAYBOOK.md`: level reachability and route constants, optional action-design examples, audio prompt skeletons, and ffmpeg conversion examples. The shared rules and this template's media/font/audio integration sections remain the primary guidance for those topics.
## Bounded game viewport: 1:1 to 16:6
The game surface must keep a **width/height ratio between 1:1 and 16:6**, independently of the preview panel or browser window. `ViewportPolicy` (`scripts/viewport_policy.gd`) clamps the logical viewport, while Godot's `canvas_items` + `keep` stretch mode uniformly scales and centers it. In **adaptive mode**, a host within the range is filled; a taller host gets top/bottom letterboxing and a wider host gets left/right pillarboxing. In that adaptive mode, a 400×800 preview displays a centered 400×400 game surface; a 2400×600 preview displays 1600×600. Do not distort the canvas, crop the scene, or restore unrestricted `expand` to fill these margins.
**Display defaults to locked 16:9** (`display_mode = 0`), using the 1280×720 design area with centered letterboxing/pillarboxing and no stretching. In debug Tweak, **Display → 自适应画面比例** (`display_mode = 1`) restores the bounded adaptive mode described below. Both choices apply while paused, survive scene changes, and use the existing local draft save/reset path. The release debug-UI gate remains unchanged.
In adaptive mode, keep the existing 1280×720 design area: the logical viewport can grow to 1280×1280 at the square limit or 1920×720 at the wide limit. Design backgrounds, camera bounds, HUD, pause menu, and Tweak layout for that bounded range—not the outer page dimensions. The autoload survives scene transitions and applies changes even while paused. Keep the Web canvas resize policy unchanged: Godot, rather than a second CSS transform, owns the viewport and input mapping in both preview and exported PCK.
Touch and mouse joystick presses must originate inside the game surface; presses in the bars are ignored, and releasing outside still clears an active drag. Transparent full-rect HUD containers must ignore mouse input without disabling their interactive children. Preserve the policy when adapting the template. Run `pnpm test:responsive` after layout changes; it covers portrait, square, normal landscape, 16:6, ultrawide, resize while paused, background coverage, and input boundaries. A different aspect policy requires an explicit user request.
**Layout acceptance:** backgrounds cover the visible game surface after camera movement and resizing throughout 1:1–16:6; tiled terrain has no transparent seams or artwork beyond collision bounds; passages remain traversable without bump animations trapping the player. Implementation safeguards live beside the relevant code. `pnpm verify-export` runs the box/camera regression; `pnpm test:terrain-render` checks actual rendered coverage and tile pixels using a real renderer or Xvfb.
## Visual effects and particles
`scripts/visual_effects.gd` is a working, asset-free particle reference built with `CPUParticles2D`, which stays compatible with the Godot Web renderer. The template already wires the following cues:
| Gameplay event | Included particle feedback |
|---|---|
| Jump / landing | Small takeoff dust and a wider landing dust puff |
| Coin or block reward | Bright collection sparkles at the world position |
| Enemy stomp | A fast impact burst at the player/enemy contact point |
| Player death | A larger warm-colored radial burst before respawn |
| Checkpoint | A cool-colored confirmation burst, emitted only on first activation |
| Course clear | A long-lived confetti burst behind the completion message |
Keep event meaning separate from rendering: `player.gd` emits jump and landing signals, entities emit world positions, `game.gd` maps gameplay events to feedback, and `visual_effects.gd` builds the particle nodes. When changing genre or art direction, preserve that flow and adjust particle colors, amount, velocity, gravity, lifetime, spread, texture, and scale in one place. Add a named preset and deterministic assertion for every new high-value action; do not scatter one-off `CPUParticles2D` configuration across gameplay files.
The generated particle textures are tiny runtime shapes, so the baseline has no additional image dependency. Replace them with approved textures only when the visual direction requires it. Keep one-shot effects bounded and self-cleaning, and prefer `CPUParticles2D` for these lightweight cues unless the target Web build has explicitly verified another implementation.
`test/smoke.gd` verifies every included preset creates an emitting particle node and verifies real player jump/landing signals reach the system. `test/debug_capture.gd` adds visible sparkle and confetti to the gameplay viewport capture, while the exported-pack test ensures the effect script and node are present in the PCK.
## Tuning and debug builds
`config/tuning.json` is the single owner of every tunable key, source default, range, slider step, display label, precision, and unit. `TuningStore` loads that schema and the current browser-local values; `TuningPanel` builds its controls from the same entries. Add or change tuning metadata there instead of duplicating constants across GDScript, UI, and server code. Increment its `version` when stored browser values are no longer compatible.
**Do not replace gameplay-feel values with constants and do not remove the panel while adapting the template.** Wire every new feel-sensitive mechanic through the schema before calling the game playable. At minimum, platformers must expose horizontal speed and response, full-jump power, short-hop cutoff, gravity, coyote time, jump buffer, bounce behavior, enemy motion, camera response, and timing. Other genres must provide the equivalent controls for their core loop.
Click the **TWEAK / F1** button, press `F1` or `P`, or choose **Tuning** from the pause menu, to pause the debug Preview and edit values live. Every slider change is debounced and saved to `user://platformer_tuning.json`, so refreshing the same browser preserves the experiment without modifying source. Reset restores the current source defaults.
The panel displays the derived full-jump apex. For the reference route, the default `jump_power` and `gravity` must produce at least `REFERENCE_MAX_PLATFORM_RISE + MIN_JUMP_CLEARANCE`; the smoke test checks both the calculated envelope and an actual held jump. When changing a level, measure the largest required vertical rise on the intended route, update the route constant, keep a deliberate clearance margin, and test the real jump. A platform visible on screen is not valid level content until the default controls can reach it.
After values have been tested, ask Manus to update the matching defaults in `config/tuning.json`, request a preview build, and verify the same feel before saving a checkpoint.
Debug UI is only instantiated in debug builds. Use the live Game Dev preview for tuning; checkpoint and published release builds do not expose the panel. When serving a local exported build for playtesting, use `--export-debug Web`; do not remove `OS.is_debug_build()` to make a release export show the panel.
The debug template includes jump power/gravity and movement, enemy speed/count, camera zoom/smoothing, and yarn speed/cooldown/lifetime/upward speed/gravity. Enemy-count edits rebuild the population; camera zoom updates immediately, including while paused, without shrinking the screen-space background. `test/tweak_regression.gd` covers the build gate, panel entry, local autosave/reload and reset. Browser storage restrictions can prevent persistence; show the save result, never report a local draft as a source update.
## Art workflow
The reference art is deliberately included so new games start with a visually complete sample. Replace assets gradually during implementation, but complete the game-specific scene-art pass before the first user-facing checkpoint.
### Scene art completeness: no prototype geometry in the first checkpoint
Unless the user explicitly asks for a geometric, abstract, minimalist, vector-primitive, or procedural visual style, generated or user-provided assets must carry the final appearance of the scene. Rectangles, circles, polygons, lines, gradients, and Godot draw calls may define collision, navigation, debug overlays, masks, particles, or temporary blockout geometry, but they must not remain visible as the final ground, platforms, scenery, vegetation, structures, characters, enemies, collectibles, or major props.
Before generating art, inventory every visible category required by the actual level. At minimum inspect the ground and platform surfaces, far/mid/near backgrounds, trees and vegetation, rocks or terrain features, buildings or structures, major interactive props, characters and enemies, collectibles, and UI. Generate only categories the game needs, but do not omit a needed category merely because a colored shape already makes the mechanic playable. Call `generate_image` (or the currently available equivalent image-generation tool) for the full required set during the first implementation pass; do not postpone environment art as optional polish after showing a checkpoint. The first checkpoint should look like an authored game scene, not a mechanics prototype with one finished hero.
Define one compact art-direction contract before generating the set: camera/view angle, world scale, horizon and perspective, silhouette language, outline weight, palette, material rendering, light direction, contrast, texture density, and target display dimensions. Repeat those constraints across environment and prop prompts. A single attractive image is not enough if the ground, trees, rocks, buildings, and character appear to come from different games.
Process each accepted environment asset at its actual maximum display size, remove accidental backgrounds or halos, preserve intentional transparency, and export a clean-edged WebP. Use tileable or modular pieces for repeated ground and structures, separate far/mid/near layers for depth, and keep collision shapes independent from the visible texture so art can change without changing gameplay.
Before the first checkpoint, use the existing Godot-native capture flow to render representative gameplay. Confirm that the scene no longer exposes prototype geometry as finished art and that the environment, character, props, items, particles, and UI share the intended perspective, scale, outlines, palette, and lighting. Fix the asset set or presentation before checkpoint delivery; follow the shared browser-acceptance workflow after the native checks.
### Title-screen art must communicate the actual game
The **first user-facing checkpoint** must include purpose-built title-screen/key art that visibly represents the playable protagonist, the main enemy or hazard when applicable, and recognizable gameplay elements (for example collectibles, abilities, props, or traversal). A generic scenic background alone is not sufficient. Match the game’s character identities, material style and setting; reserve a text-safe region, give the title/instructions adequate contrast, and keep the key cast visible in every supported Display mode. Render typography and buttons as live Godot UI, not baked into the illustration.
Do **not** regenerate title art after every gameplay change. When a substantial character, enemy, core-mechanic, setting or art-direction change makes the existing title misleading—or at a natural visual-review/checkpoint milestone—ask the user whether they want it refreshed before doing extra title-art work. Minor balance, bug-fix and parameter changes do not require a refresh or repeated prompts.
Follow the shared video-first animation workflow before processing or integrating character frames.
### Character size and anchor consistency
Idle, run, jump, attack, hit, death, and any other state must look like the same character occupying the same world-space scale. Use the approved character reference for every source clip, keep the camera framing and character scale fixed, and process every state to the same transparent canvas. `tools/art_pipeline/process_animation_frames.py` demonstrates the required pattern: inspect Alpha bounds, compute one union crop, apply one resize, center horizontally, and align the result to a shared bottom padding that acts as the foot baseline.
Before wiring frames into Godot, inspect the non-transparent bounding box of every frame. Width and height may change naturally with a pose, but a whole state becoming consistently larger, smaller, higher, or lower usually means its source framing, crop, scale, or baseline differs. Do not directly mix independently generated poses, different source resolutions, per-action tight crops, or frames processed with different canvas/content settings.
At runtime, keep a single scale and drawing origin across all states. Follow the reference in `scripts/player.gd`: both `HERO_TEXTURE` and `RUN_FRAMES` use the same square canvas, `draw_scale`, and centered `draw_texture()` origin. State selection should change only the texture unless an intentional gameplay effect such as death squash is explicitly designed. Do not add idle-only, run-only, or jump-only offsets to hide an asset-pipeline defect.
If the user reports that a character changes size, floats, drifts, or has a shaking foot position when its state changes:
1. Compare the affected files' pixel dimensions and Alpha bounding boxes; identify whether the mismatch is canvas size, occupied size, crop position, or foot baseline.
2. If anatomy, camera distance, or source character scale changed, regenerate or re-extract that action from the approved reference; cropping cannot repair a different character scale.
3. Otherwise, reprocess every affected character state in **one invocation** with repeated `--state SOURCE_DIR TARGET_DIR PREFIX` arguments and the same `--canvas` and `--content`. The tool scans every source frame once, derives one union crop and scale, and applies that exact geometry to every output state; do not run one command per action or omit a state from the batch.
4. Remove any per-state runtime scale or offset workaround, reimport the assets, and confirm that every state still uses the shared Godot scale and origin. Preserve clearly intentional motion such as the reference run bob or death squash; remove only compensation added to disguise inconsistent source assets.
5. Give the updated checkpoint to the user to verify the transition. A Godot-native comparison capture can help diagnose or demonstrate a reported mismatch, but it is not a mandatory completion artifact by default.
Follow the shared asset storage and import rules.
Check FFmpeg in the current execution environment before video extraction. The image-processing tools require Pillow:
```bash
# Keep raw video and extracted PNGs outside the Godot project.
uv run python tools/art_pipeline/extract_video_frames.py ../game-art-sources/run.mp4 ../game-art-sources/run_frames/ --fps 12 --start 0.4 --duration 1.4
uv run --with-requirements tools/art_pipeline/requirements.txt python tools/art_pipeline/remove_image_background.py input.webp output.webp
uv run --with-requirements tools/art_pipeline/requirements.txt python tools/art_pipeline/process_animation_frames.py \
  --state ../game-art-sources/idle_frames/ assets/characters/hero/idle/ idle \
  --state ../game-art-sources/run_frames/ assets/characters/hero/run/ run \
  --state ../game-art-sources/jump_frames/ assets/characters/hero/jump/ jump \
  --pattern 'frame_*.png' --report-bounds
```
After adding or replacing art, run an import before other tests:
```bash
godot --headless --path . --import
```
## CJK-safe game UI font
Follow the [current typography contract](game-workflow.md#default-typography): default to bundled ManusCC0 with ManusCC0 Sans CJK SC fallback, and allow unrestricted user-uploaded fonts. For font changes, update theme overrides, hydration pins, loader sources and project-local checks together; preserve gameplay and protocol. Check chosen-font rendering, Chinese player names and actual Web font resolution; diagnostics do not block uploaded-font choices. Keep system fallback disabled; update the project theme, fallback resources, imports and export tests together. The original per-copy subset commands are retired. Check line height and clipping with the replacement fonts.
## Audio integration
Follow the current shared optional audio workflow: reuse fitting permitted audio, and generate only for a concrete need. No separate cue sheet is required. The generation recipes below apply only when new audio is needed.
- **Preferred Manus Max Mode BGM:** use `generate_music` for loopable music.
- Follow the live tool contract for arguments; do not guess parameter names in project code or documentation.
Use [audio production as needed](game-workflow.md#audio-production-as-needed). Reuse fitting permitted reference BGM/SFX. Consult `docs/GAME_PRODUCTION_PLAYBOOK.md` only for a missing conversion or wiring detail; its cue-sheet and mandatory replacement instructions do not apply.
**Design for sustained browser play, not just successful boot.** Reuse resources, bound concurrent SFX, and never unconditionally restart audio, reassign streams, or allocate resources every frame. Compare pause state before assigning `stream_paused`: repeated `false` assignments have caused Web audio buffer reallocation and freezes. Long BGM must use `AudioServer.PLAYBACK_TYPE_STREAM`; `.ogg` alone does not select streaming. Pause/resume, respawn, and scene changes must not accumulate players, timers, or signal connections.
The included `test/audio_idle_regression.gd` runs through `pnpm test:audio` and is mandatory in `pnpm verify-export` against the actual PCK. It checks: 10,000 idle updates produce zero pause-state writes; 10,000 paused and 10,000 resumed updates produce exactly one write per transition, with streaming BGM asserted. This catches the setter loop, not Web memory leaks. For browser-only failures, request targeted user acceptance on the exported checkpoint: sustained idle play, repeated pause/resume, respawn and menu return, checking freezes, audio errors and growing resource usage. Native/headless success is not proof of Web stability; use the shared verification workflow for the remaining browser acceptance.
### Reuse GameAudio; replace the catalog, not the lifecycle
`GameAudio` is an autoload with one streaming music player and **eight SFX voices total**, each limited to one playback. When full, the pool reuses a voice instead of allocating a new player. `scripts/audio_catalog.gd` is the single asset mapping: when changing a cue, update its entry with static `preload("res://assets/audio/...")` references to generated or user-supplied BGM and cues. Null entries are valid for optional absent audio; explicitly requested audio must still be fulfilled or reported missing; the reference catalog now supplies one BGM and eight SFX files under `assets/template/audio/`. Use looping Ogg Vorbis for BGM and short non-looping clips for SFX.
The Start button/key calls `GameAudio.begin_game()` within the user gesture; do not autoplay from scene `_ready()`. Existing gameplay handlers call `GameAudio.play(&"jump")`, `&"land"`, `&"coin"`, `&"stomp"`, `&"checkpoint"`, `&"death"`, and `&"success"`. Tree pause is synchronized with guarded assignments. Respawn keeps the same music player and playback; returning to the title or removing the game scene stops all voices. Do not create another manager on respawn or bypass it with per-entity audio players. `set_muted()` / `set_volume()` are available for UI controls; `M` and `-` / `+` are reference keyboard controls.
Keep the regression test when adapting the game. Besides idle/pause transitions, it exercises real title/game/menu and respawn paths, checks player and bus counts, SFX bounds, idempotent starts, and muted/volume controls. Its silent test streams are created only by the excluded test script, not shipped as final audio. The runner requires an explicit `[AUDIO_IDLE_PASS]`, rejects script errors even on exit code zero, and times out instead of silently passing or hanging. These checks cover the manager contract; validate game-specific cue mappings and final browser sound separately.
## Template-specific diagnostics
Use the shared log guide for export, runtime, network, and replay errors.
| Symptom | Where the answer is |
| --- | --- |
| Whether the screen looks right | Godot `test/debug_capture.tscn` output |
| Character changes size, drifts, floats, or has a shaking foot position between states | Compare canvas dimensions and Alpha bounds, then follow **Character size and anchor consistency**; repair the shared asset-processing batch instead of adding per-state runtime offsets |
| Whether approved tuning reached the source and preview | `config/tuning.json` plus the later `[export] done` line in `.manus-logs/devserver.log` |
## Verification commands
Run these from the generated game project directory:
```bash
# Audio lifecycle, idle/pause, bounded voices and scene reuse
pnpm test:audio

# Scene, world, movement, and tuning smoke test
godot --headless --path . -s test/smoke.gd

# Render deterministic title, gameplay, and tuning screenshots with Godot APIs
GAME_CAPTURE_DIR=../game-captures xvfb-run -a godot --audio-driver Dummy \
  --path . --resolution 1280x720 res://test/debug_capture.tscn

# Export, then verify its contents and configured main scene from an isolated directory
pnpm export
pnpm verify-export
```
The smoke test must print `[SMOKE_PASS]`, the capture test must print `[DEBUG_CAPTURE_PASS]`, and the PCK checks must print `[PCK_CONTENTS_PASS]` and `[PCK_BOOT_PASS]`; the audio regression must also print `[AUDIO_IDLE_PASS]`.
The capture requires a rendering display so the viewport texture exists. Use the Xvfb command above in Sandbox; do not add `--headless` to the capture command.
If `godot` is not on `PATH`, set `GODOT_BIN` to the executable before running `pnpm verify-export`.
## Template-specific constraints
Apply the shared export constraints, plus:
- Keep `config/*.json` in the Web preset's `include_filter`; the tuning schema must be present in the exported PCK.
- Never depend on system CJK fonts. Keep the supported glyph repertoire, `gui/theme/custom_font`, and PCK glyph assertions in sync.
- Run the native capture and exported-pack checks below, then follow the shared browser-acceptance handoff.
## Publishing
**Finish deterministic checks, save a checkpoint, and give it to the user.** Publishing can follow after user acceptance. Follow the shared checkpoint artifact and publishing workflow.
## Template-specific failures
Check the shared common failures first.
- **Chinese text becomes boxes or disappears in Web:** rebuild the Fusion Pixel subset from all runtime text, confirm `gui/theme/custom_font`, reimport, and rerun the exported-pack check. Add omitted dynamic text through `--text-file` or `--characters`; do not add a system-font fallback.
- **Movement feels wrong:** tune it in the F1 panel before changing defaults.
- **Approved tuning is missing after restart:** update the matching defaults in `config/tuning.json`, then request one preview build and verify the updated game again.
- **Generated BGM does not fit:** regenerate it with tighter duration, arrangement, sonic-palette, and negative instructions; do not keep an unrelated result merely because a file was produced.
- **An SFX cue does not fit:** regenerate only that cue with a tighter event, duration, material, intensity, perspective, and negative description, then audition and integrate it yourself. Do not switch to `generate_music` or accept a poor result.
