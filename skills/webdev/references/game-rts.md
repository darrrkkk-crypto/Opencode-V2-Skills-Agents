<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Game Template — Real-Time Strategy

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


This current recipe overrides conflicting frozen README instructions; current shared rules and receipt commands take precedence.

**Campus Hero Defense** is a Godot 4.7.2 isometric campus-defense RTS. Choose Rookie, Varsity or Legend, watch or skip the comic intro, rescue classmates, secure four classrooms, train five hero types and defend Maplecrest High through eight Grimsby invasion waves. The Main Hall must survive. Yearbook results offer rematch, difficulty and a local Hall of Fame. English only; local play and scores.

For other isometric requests, reuse suitable projection, picking, camera and presentation code; the requested gameplay decides which campus systems remain. Update obsolete commands, assets, tests and guidance together.

## Authoritative owners

| Owner | Scope |
| --- | --- |
| `scripts/main.gd`, `scenes/main.tscn` | Title, difficulty, intro, match, pause, results and event fan-out. |
| `scripts/sim/rts_simulation.gd`, `scripts/sim/invader_ai.gd` | Gameplay, pathing, combat, economy, rooms, waves, outcomes and enemy squad decisions. |
| `scripts/data/hero_catalog.gd`, `scripts/data/campus_map.gd` | Hero/enemy stats, room labels/help, wave composition and the 36×36 campus with classroom production mappings. |
| `scripts/core/iso_projection.gd`, `scripts/view/battlefield.gd`, `scripts/view/campus_minimap.gd` | Projection, selection, commands, camera, rendering and minimap. |
| `scripts/view/unit_animator.gd`, `scripts/data/unit_anim_data.gd`, `scripts/view/fx_layer.gd` | Animation atlas frames, grounding, particles and comic effects. |
| `scripts/ui/hud.gd`, `scripts/ui/hero_theme.gd`, `scripts/ui/results_screen.gd` | Notebook HUD, hero cards, room controls, themed UI and yearbook results. |
| `scripts/data/comic_script.gd`, `scripts/ui/comic_intro.gd` | Two-page, six-panel story and its playback. |
| `scripts/audio/audio_director.gd`, `default_bus_layout.tres` | Music, SFX, voices and bus routing. |
| `scripts/services/high_score_store.gd`, `scripts/services/localization.gd`, `localization/en-US.json` | Local standings and presentation text. |
| `config/tweaks/catalog.gd`, `scripts/tuning/tweak_service.gd`, `scripts/manus/preview/tuning_adapter.gd` | Tweak descriptors, apply boundaries, settings and ranking eligibility. |

Change balance in these owners and update consumers together; only simulation decides damage, capture, rewards and outcomes.

Classroom production comes from `campus_map.gd`'s `CLASSROOMS[].trains`; `hero_catalog.gd`'s `ROOMS[].trains` also supplies UI/help lookups. Keep both mappings aligned when changing which hero a room trains. Main Hall production is initialized separately in `RtsSimulation._create_buildings()`.

## Gameplay invariants

`advance()` caps incoming time at 0.25 seconds and advances fixed 1/30-second ticks, at most eight per call. Preserve tick ordering, seeded behavior, walkable spawn placement, A* obstacle rules and simulation-owned separation. Pause and terminal results stop normal advancement; the match controller also blocks commands during pause/results. `main.gd` drains events once and distributes them to the battlefield, audio and HUD.

A match starts with three Hall Monitors, one Stretch, five trapped civilians and four enemy-held classrooms. The base squad cap is six; each secured classroom adds three. Queued heroes count toward population. Training validates room ownership, capacity, queue limit and Reputation before charging; it is FIFO, while cancel removes and refunds the last queued hero. Losing a classroom refunds and clears its remaining queue. Spawned heroes follow that room's rally point.

| Training room | Hero | Power |
| --- | --- | --- |
| Main Hall | Hall Monitor | Hall Pass Dash |
| Gymnasium | Stretch | Rubber Slam |
| Chemistry Lab | Blaze | Fireball |
| Cafeteria | Frost | Glacier Shield |
| Library | Psi | Mind Lift |

Hero contact makes a trapped classmate follow. Escort them to the Main Hall **or any secured classroom** to receive Reputation, score, Hype and escort XP. A lost escort leaves the classmate trapped again. Trapped classmates are excluded from enemy targeting and splash damage; escorted classmates are vulnerable. New trapped classmates spawn during play. Secured buildings heal nearby living heroes and classrooms add passive Reputation income.

Classroom control progresses only when one side's living units occupy the capture ring; opposing occupants contest it. Securing and losing rooms changes production, population capacity and income without deleting existing heroes. Powers keep their individual cooldowns. Knockouts grant XP and shared nearby XP to living heroes; heroes reach level three, gaining health and damage and healing on level-up. Dead records must not act, occupy rooms, heal or revive through delayed XP. Knockouts within the combo window earn combo score and Hype. Full Hype enables an eight-second Spirit Surge with increased hero damage and movement speed. Pep Rally separately spends Reputation to heal heroes, repair the Main Hall and temporarily boost damage.

Eight catalog waves enter from the parking lot, sports field and loading dock; Mecha-Mascot appears in waves five and eight. Ringing the bell advances the next wave and awards Reputation based on time skipped. Preserve staggered spawning, lane assignments, the Principal's Bulletin and ground telegraphs for Brute slams and Mecha-Mascot attacks. Victory requires the final wave to finish spawning and all wave invaders to be defeated; classroom guards are not an extra victory condition. Main Hall destruction takes precedence and causes defeat.

Stars: one for victory, one more for at least 60% Main Hall health, and one more for holding all four classrooms or rescuing at least ten classmates. Defeat earns no stars. `compute_stars()` owns this rule; results must not invent a second formula.

Difficulty applies enemy health/speed, starting Reputation and AI level together. Rookie squads mass before attacking, score objectives and raise guard alarms; Varsity adds focus fire, kiting, pincers and retreats; Legend adds regrouping, a low-health Main Hall rush and predictive rockets. Keep intent arrows, room threat notices and alarm/regroup cues consistent with actual squad state. The simulation test requires Rookie and Varsity autopilot victories; Legend is a completion/balance comparison, not a guaranteed win.

## Controls and presentation

| Input | Action |
| --- | --- |
| Left-click / drag | Select heroes; Shift adds or toggles selection. Double-click a hero selects its type on screen. |
| Hero cards | Select that type across the campus; double-click focuses it. |
| Right-click | Attack an enemy or move; with only an owned room selected, set its rally point. |
| E, then left-click | Issue one attack-move. Right-click or Esc cancels the armed mode. |
| C / Q / G | Stop / selected heroes' powers / Spirit Surge. |
| F / H / I or period | Select all heroes / focus Main Hall / select and focus an idle hero. |
| T / X | Queue training in the selected room (Main Hall by default) / cancel the selected room's last queued hero. |
| R / B | Pep Rally / call the next wave early. |
| Ctrl or Command + 1–5 / 1–5 | Assign / recall a squad. |
| WASD letters, arrows, edges, middle-drag | Pan; keys override edge scrolling. |
| Wheel, trackpad magnify, + / − | Zoom without modifier keys; base zoom is bounded from 0.5 to 1.5. |
| Space / Esc / M | Focus selection / close help, cancel attack-move or toggle pause / mute. |

Shift changes selection, not an order queue. Keep commands filtered to heroes, UI hit blocking, camera bounds and selection/room context coherent. The minimap can focus the camera and command the selected squad. Keep the 1280×720 `canvas_items`/`expand` layout, readable telegraphs and HUD, stable sprite grounding and reduced-motion option.

Opening Help during a match pauses gameplay and hides the pause menu beneath it. Closing Help returns to the paused menu for explicit Resume. Pause requests during the outcome delay or results must not re-enable commands or change outcome music; entering results clears pause/help overlays.

The inherited touch layout supports landscape: tap a hero to select; with a squad selected, tap an enemy to attack or ground to attack-move; drag to pan and pinch to zoom. Portrait shows a rotate-device prompt. Preserve this behavior; additional mobile work follows the shared workflow's scope rule. No gamepad mapping is supplied.

## Story, media and persistence

First Play, including Play from the Hall of Fame, opens the comic unless `user://story.cfg` records `intro_seen`. Click, tap, Space or Enter completes the current panel then advances; Skip/Esc exits. Finishing or skipping the first-run intro starts a match; both finishing and skipping Story replay return to the title. Keep narration cancellation, voice ducking and the transition guard when leaving the intro.

Use `assets/template/game/` for authored runtime media, `assets/template/catalog/` for retrieved catalog media and `assets/template/share/` for sharing art. `assets/template/runtime/audio/sfx/` contains twelve cues preloaded by `AudioDirector`; these are active consumers, not obsolete media. Keep `assets.lock.json` paths, hashes, sizes and provenance aligned with consumers. Bangers and Nunito are the game's bundled display/body fonts, with adjacent OFL notices and weighted Noto Sans SC fallbacks for Chinese player names. Preserve these bindings and the portable font verifier under `tools/`; system fonts must not hide missing glyphs.

English is the only shipped locale. Keyed UI and comic text use `I18n.t` and `localization/en-US.json`, but unit/room names, role text and room blurbs also live in `hero_catalog.gd`, while `invader_ai.gd` supplies raw lane names for notice placeholders. Retheming or adding a locale must cover these owners and the spoken English voice assets, not just the JSON catalog. `comic_script.gd` links localization keys and narration voice IDs; keep captions, narration and displayed names consistent.

Nine combat characters have idle/walk/attack atlases. `unit_anim_data.gd` records trimmed rectangles, full-cell margins, anchors and frame rates; `UnitAnimator` caches `AtlasTexture` frames. Preserve the shared ground anchor, facing overrides, stunned-frame freeze and slowed playback. Civilians retain static sprites. Animation source videos and full-cell masters are not packaged; do not claim they can be regenerated by inherited asset-processing scripts.

`AudioDirector` owns title/battle/boss tracks through the browser BGM adapter, a bounded 20-voice SFX pool and prioritized voice playback with cooldowns. Keep gesture unlock, music state changes, voice ducking, mute and world-event filtering; preserve the delivered mix. Playable releases exclude preview-only tuning modules.

`HighScoreStore` stores the top ten scores per difficulty in `user://high_scores.json`; names are sanitized and limited to 12 characters. Results capture eligibility before ending the run. Gameplay/score tweaks taint the current run even if reset; cosmetic tweaks do not. Preserve LIVE/NEXT_ACTION/NEXT_SPAWN/NEXT_RUN boundaries: spawn and training boundaries apply pending values before their first read, and `TweakService.begin_run()` activates all pending modes before eligibility and fresh simulation setup. Keep ordinary mute/reduced-motion preferences separate from temporary preview patches.

## Verification

Use receipt-resolved `GODOT_BIN`/`GAME_RUNTIME` and matching 4.7.2 Web templates. Restore the lock into a disposable copy before importing; never create `.godot`, exports or captures inside a frozen starter.

For UI/input tests, use a custom user directory containing `Tests` in the disposable project. `RTS_UI_CAPTURE_DIR` enables screenshots.

```bash
"$GODOT_BIN" --headless --editor --path . --import
"$GODOT_BIN" --headless --path . --script res://tests/simulation_test.gd
# Rendered captures as relevant to the change; use a real display or xvfb on Linux:
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/visual_capture.gd
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/anim_capture.gd
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/comic_capture.gd
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/ai_capture.gd
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/drag_select_probe.gd
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/ui_flow_test.gd
"$GODOT_BIN" --rendering-method gl_compatibility --path . --script res://tests/camera_input_test.gd
# After Addon initialization installs canonical runtime scripts:
npm run check
npm run preview:build
npm run build
```

The simulation suite covers setup, rescue, capture/training, powers, levels, combos/Surge, telegraphs, stars, local standings, defeat, AI and full-match autopilot. `AI_PROBE=1` selects the autopilot timeline only; it is not a substitute for the full suite. Captures write to `/tmp/hallhero_captures` and require visual review; the comic capture resets its test profile's story preference. Use an isolated test profile. Check camera/selection, first Play, Story replay, Help/Resume, outcome input blocking, results/rematch, animation anchors and AI intent. Native checks do not establish browser audio/input acceptance. Debug Preview must retain its tuning bridge and connect to Tweak; the canonical release projection removes the bridge and its autoload. Canonical Web build remains single-threaded and excludes docs, tests and generated QA artifacts.
