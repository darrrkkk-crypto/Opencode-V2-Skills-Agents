<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Horizontal Platformer Game Template (Godot 4.7 → Web/WASM)

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


This complete current recipe overrides conflicting frozen README instructions, including genre-specific policy. Read historical README sections only for unchanged implementation details; use the receipt's GODOT_BIN and current Game delivery commands, never placeholder executable paths or retired hosting scripts.

## Playable reference and controls
`game-platformer-v58` is Yarn Platformer, a Godot 4.7.2 felt-cat platformer. Its loop is Title → Sunlit Nook → stage clear → Lofty Lounge → Victory; timer expiry produces Defeat. Stage 1 teaches traversal; Stage 2 requires 12 fish before its exit opens. Each course starts with 180 seconds. Falling or enemy contact returns the cat to its checkpoint and costs 10 seconds. Stage changes retain run score and reset actors, checkpoint, objective and timer; Restart starts a new run at Stage 1. Preserve terminal guards and once-only results when adding events.

| Course data | Authored content | Objective |
|---|---|---|
| `data/stages/sunlit_nook.json` | 7,800 px; 19 platforms, 3 trees, 7 reward blocks, 33 placed fish | Reach exit |
| `data/stages/lofty_lounge.json` | 8,500 px; 18 platforms, 3 trees, 10 reward blocks, 47 placed fish | Collect 12 fish and reach exit |

Default enemy budget is 11 per course. Actual-physics deterministic traversal takes roughly 61 seconds of simulated active play across both courses; this compact reference does not establish 10–15-minute content. Extend authored content when requested pacing requires it.

| Action | Keyboard | Gamepad | Touch |
|---|---|---|---|
| Move | A/D or Left/Right | Left stick / D-pad | Floating joystick horizontal drag |
| Jump / short hop | Space or Up; release early | South button | Joystick upward drag |
| Yarn attack | J or X | West button | YARN button |
| Pause | Esc | Start | HUD pause |
| Skip tutorial | K | Back/View | Skip callout button |

W does not jump. Yarn uses cooldown, swept collisions, lifetime and count limits; missed shots disappear on their third ground rebound, while walls/robots consume them. Preserve coyote time, jump buffer, variable height, stomp and checkpoint recovery. Menus suppress gameplay input. Pause has Resume, Restart, Settings and Return to Title; destructive routes confirm progress loss. Modals restore prior pause/focus. Title provides profile/name, EN/CN, local standings, settings and tutorial replay.

## Implementation owners
| Owner | Responsibility |
|---|---|
| `scripts/game.gd`, `scenes/game.tscn` | Run/stage routing, construction, objective, timer, checkpoint, HUD, victory/defeat and retry/title routes |
| `scripts/stage_catalog.gd`, `data/stages/*.json` | Ordered stage IDs and validated geometry/spawn/objective definitions; add courses here, preserving one router |
| `scripts/player.gd`, `scripts/touch_input.gd` | Movement, buffered/coyote jumps, animation, attacks and touch state |
| `scripts/entities.gd`, `scripts/yarn_ball.gd` | Fish, robots, reward blocks, exit and bounded swept projectiles |
| `scripts/run_score.gd`, `scripts/save_store.gd` | Typed awards, finalized result snapshots, profile/local top ten, safe persistence and tutorial version |
| `scripts/tutorial_director.gd` | Event-driven, input-aware callouts; Skip, completion and replay |
| `scripts/title_screen.gd`, `scripts/pause_menu.gd` | Title and pause navigation |
| `scripts/menu_style.gd`, `scripts/menu_modal.gd`, `scripts/settings_panel.gd`, `scripts/leaderboard_panel.gd` | Shared styles, modal ownership, ordinary player settings and standings |
| `scripts/game_audio.gd`, `scripts/audio_catalog.gd` | Central music/cue mapping, eight one-shot voices and persistent category controls |
| `scripts/visual_effects.gd` | Bounded bursts/run dust, reduced motion, warm filter and screen feedback |
| `scripts/world_art.gd`, `scripts/viewport_policy.gd` | Camera-relative scenery and bounded responsive game surface |
| `scripts/surface_finish.gd`, `scripts/brick_surface.gd`, `scripts/sprite_grounding.gd` | Continuous terrain edges and alpha-aware foot/physics alignment |
| `config/tuning.json`, `scripts/tuning_store.gd`, `scripts/tuning_panel.gd` | Typed descriptors, validation, requested/active values, application timing, persistence and integrity |
| `autoload/i18n.gd`, `localization/en.json`, `localization/zh-CN.json` | `I18n.t`, complete EN/CN copy and persisted locale |

## Scores, onboarding and presentation
Awards are fish 100, robot 250, reward-block activation 50, and 10 per whole remaining second at stage clear; blocks also release fish. The default arithmetic ceiling is 19,650, including theoretical maximum time bonuses, not an attainable-score promise. `RunScore.finalize()` snapshots ID, score, stage, outcome, duration, timestamp, configuration hash and eligibility once. `SaveStore` keeps ten offline records ordered by score descending, then duration/timestamp/run ID ascending, rejecting malformed/duplicate records. There is no remote/global leaderboard. `user://save.json` owns profile, records and versioned tutorial state.

Names support at most 24 characters / 96 UTF-8 bytes, preserving supported mixed Latin/Simplified-Chinese text. Reject markup/control characters and unsupported glyphs without system-font substitution. The six tutorial steps react to movement, jump, yarn, hazard, checkpoint and pause, with an 18-second fallback. Skip never acquires an input lock or releases another modal's pause; completed tutorials stay completed across retry unless title replay is requested.

For user-uploaded fonts, apply the [shared typography policy](game-workflow.md#default-typography) and update project-local font checks accordingly. EN/CN selection persists through runs and title return in `user://language.cfg` and Web storage; fresh profiles follow the system/browser language (`zh*` selects Chinese). Retain the template fonts with the bundled 6,547-codepoint Noto Sans SC fallback and separate loader subset. Rare Chinese names and Traditional Chinese are not guaranteed. Theme, loader, input validation and PCK font checks must agree.

`ViewportPolicy` defaults to centered 16:9 and offers adaptive 1:1–16:6 in player Settings. Small windows use physical-sized logical UI pixels; camera `world_scale()` preserves authored world framing and jump visibility. Menus reflow/scroll, and modal close controls stay outside scroll bodies. Touch starts inside the game surface and releases cleanly outside. Preserve shared foot pivots, flat walkable tops, seam-free tile joins and rounded whole-platform perimeters. Background/foreground camera factors are 0.08/0.16.

The 41 locked media files total 3,997,506 bytes. `assets/template/cat/` holds the calico/18 run frames, robots/fish/yarn/terrain/tree/scenery/title; `generated/foliage_near.webp` is the only retained original generated asset. Audio contains the supplied soundtrack and eight SFX; fonts are OFL subsets, each with its license file. The 24 superseded theme assets and restore/import entries are removed. Preserve retained provenance; unavailable original prompts, generator facts and editable media inputs are not newly produced evidence.

## Audio, effects and tuning
This sample retains its supplied 64.4-second Vorbis BGM and eight final SFX; reuse fitting supplied audio under its recorded permissions and the shared optional-production rules; do not describe it as newly generated custom BGM. `GameAudio` owns gesture unlock, idempotent title/game transitions, pause/UI handling, fade/duck and bounded voices through the browser BGM adapter/native fallback. Respawn reuses music; retry cleans up then restarts gameplay. `audio_catalog.gd` owns semantic cues/gains/cooldowns; controllers never allocate separate players. Player Master/Music/SFX/UI volumes and mutes persist in `user://audio.cfg`; debug multipliers do not overwrite them. Actual listening and browser acceptance remain separate from native/bridge checks.

`VisualEffects` caps 12 bursts / 48 particles per burst. Reduced motion replaces moving bursts with static feedback and suppresses trails. Feedback cannot alter physics/score and resets with stage/retry.

`config/tuning.json` and `scripts/tuning_store.gd` own the typed catalog, including display-mode enum choices.
`scripts/manus/preview/tuning_adapter.gd` translates it for the Addon. Camera/display/HUD/audio/filter/particles
apply live; attack cooldown at NEXT_ACTION; yarn at NEXT_SPAWN; enemies at NEXT_STAGE; movement/jump/time at NEXT_RUN.
Validate the whole patch against the authored jump envelope. Preserve sticky gameplay taint and the separate normal
player Settings whitelist/persistence; Addon Apply does not save debug overrides.


## Relevant verification hooks
Follow current Game delivery for finite checks, Preview, export, save and publication; these source hooks do not establish another export pipeline. Select meaningful affected hooks: `test/gameplay_contract.gd` covers stages/results/local records/tutorial; `test/traversal.gd` drives actual movement/jumps/attacks through both courses; `test/ui_contract.gd` covers menu input and modal ownership; `test/tweak_regression.gd` covers boundaries/integrity/release gates. Use existing audio, combat, VFX, terrain/grounding, responsive/framing and localization checks for changes in those owners. `test/acceptance_capture.gd` provides native EN/CN desktop/fixed-phone/adaptive-phone evidence; use representative affected states, not a mandatory fresh matrix. Tests that write saves need isolated temporary player storage; localization expects a `PlatformerLocalizationTests-` directory.

Keep `localization/*.json`, `config/*.json` and `data/stages/*.json` in export inclusion, and tests/authoring evidence outside the player pack. `scripts/check-exported-pack.mjs` checks the receipt-selected isolated PCK; its `--release-profile` mode applies only to the stripped release artifact. Relevant imported/exported checks and native captures do not prove deployed adoption, final listening or user Web acceptance. Preserve those distinctions at handoff.
