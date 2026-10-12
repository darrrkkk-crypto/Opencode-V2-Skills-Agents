<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Pinball Game Template

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


## Reference identity and playable loop
`game-pinball` is a Godot 4.7.2 pinball foundation. Its reference game, **Space Pinball**, uses a configurable observatory table with physical flippers, a charged plunger, bumpers, rollover lanes, a target bank, timed missions, multiball and jackpots. Retain the contact-driven table simulation when adapting its theme, targets, missions or scoring.

The title starts a timed stage. Launch, keep the ball in play, complete the mission sequence to earn multiball, and score the stage's required jackpots. Victory occurs when that multiball window finishes after the jackpot requirement is met. Running out of the stage's time or final ball ends the run in defeat. Results offer retry, title navigation and a local score entry; a completed stage exposes Next Stage when another registry entry exists. Pause offers resume, confirmed restart and confirmed return to title.

The initial registry contains one `observatory` stage with a 240-second limit and one required jackpot. Adding a stage means adding a configuration and registry entry, not another controller. A table with no mission sequence can remain a standalone customization fixture, but it is not a valid campaign stage: stage completion requires missions plus enabled multiball and jackpots.

## Source owners and customization
```text
game-pinball/
├── project.godot                         # main scene, autoloads, viewport and font
├── scenes/main.tscn                      # pinball_template.gd entry
├── config/
│   ├── stages.json                      # stage IDs, configuration, jackpot/time goals
│   ├── pinball-template.json            # table, physics, targets, missions and scoring
│   ├── pinball-template.schema.json     # authoring schema
│   └── tuning.json                      # typed tuning catalog and apply boundaries
├── scripts/
│   ├── pinball_template.gd              # routes, results, dialogs, input, tuning/filter
│   ├── pinball_stages.gd                # validated stage registry and configuration
│   ├── pinball_run.gd                   # bounded typed score events and final results
│   ├── pinball_leaderboard.gd           # name validation and local top-ten records
│   ├── pinball_tutorial.gd              # event-driven versioned onboarding
│   ├── pinball_locale.gd                # English/Chinese lookup and mission copy
│   ├── comet_main.gd                    # base table presentation, input and preferences
│   ├── comet_observatory.gd             # table HUD, multiball and mission presentation
│   ├── comet_physics.gd                 # ball, plunger, flipper and contact simulation
│   ├── comet_rules.gd                   # missions, chains, multipliers and jackpots
│   ├── comet_juice.gd, comet_effects.gd  # bounded cosmetic feedback
│   ├── manus/preview/tuning_adapter.gd # Addon preview adapter
│   └── manus/browser_bgm_*.gd           # shared browser music transport
├── autoload/
│   ├── audio_director.gd                # semantic cues, buses and bounded voices
│   ├── tuning_store.gd                  # validated requested/active values and integrity
│   └── manus_font_theme.gd              # approved primary/fallback font binding
├── localization/{en,zh_CN}.json
├── assets/template/                     # managed artwork, audio, fonts and provenance
├── web/loading.html                     # editable game loading shell
├── assets.lock.json                     # portable managed media restoration
├── asset-provenance.json                 # retained source/generation facts
├── game-verification.json                # source and packed outcome checks
├── docs/{configuration,development}.md   # detailed source customization and checks
├── docs/examples/four-bumper-table.json  # alternative validated table fixture
└── tools/                               # game checks, capture and bounded font tools
```

Read `docs/configuration.md` before editing table data and `docs/development.md` for the supplied validators. `docs/source-game.md` preserves the supplied game's README; use this version's generated README and installed Addon workflow for template routing and delivery. `template-provenance.json` pins the original repository/commit and distinguishes original Git blob identities from locally adapted input hashes.

Table geometry, bumper and target positions, board bounds, launcher/flipper values, scoring and mission targets belong in `config/pinball-template.json`. `scripts/template_config.gd` validates a configuration before play. Keep `config/pinball-template.schema.json` and the validator aligned, and exercise the supplied four-bumper fixture when target count or configuration structure changes. Mission labels belong in localized configuration data. Avoid hardcoding target counts, point values or English-only mission labels into rendering.

`scripts/pinball_stages.gd` rejects duplicate IDs, configurations outside `res://config/`, non-string title keys, jackpot counts below one and time limits outside 60–900 seconds. The router owns stage transitions and clears run, tutorial, input, effect and multiball state on restart. A new stage must work after a preceding victory as well as from a fresh boot.

## Input, menus and onboarding
| Action | Keyboard | Gamepad | Pointer/touch |
| --- | --- | --- | --- |
| Left/right flippers | Left/right arrows | Left/right shoulder | Separate flipper pads |
| Charge/release launcher | Hold/release Space or Down | Hold/release primary action | Hold/release Launch |
| Pause/resume | Escape or P | Start | Pause / Resume |
| Start from title | Enter or focused Start | Focused Start | Start |
| Mute | M | Settings | Settings |

Input release, menus, confirmation dialogs and tuning must not leave a flipper or launcher held. Preserve independent pointer IDs for simultaneous touch flippers, accessible menu focus and portrait controls below the playfield. Use native captures for both orientations and include resizing in user Web acceptance; keep scores, missions, balls and timer visible.

First-run onboarding advances from actual launch, flipper, target and pause events. It supports skip, a bounded wait per step and a saved tutorial version; the title's tutorial action starts a replay. Tutorial copy follows the current input method and locale. Keep developer tuning separate from player onboarding.

## Scoring, results and local standings
`scripts/pinball_run.gd` accepts defined gameplay event types, clamps scores to 999,999,999, measures active run time and finalizes once. The returned result is a copy containing score, stage, outcome, duration, timestamp, configuration hash and eligibility. Physics/rules emit score events; cosmetic bursts, sound and UI never invent score. Do not create a second score owner when adding targets.

`scripts/pinball_leaderboard.gd` stores a versioned top ten in `user://pinball_records_v1.json`, writes through a temporary file and uses deterministic ordering. Player names are 1–20 characters and at most 80 UTF-8 bytes, reject control/markup characters, and must exist in the actual bound font. Preserve each record's original name and configuration identity when settings change. Invalid files or records must fail safely without corrupting the next valid save.

Standings are local to the browser profile/device. No remote ranking service, account identity, network leaderboard or multiplayer transport ships in this reference. Add these only under an explicit requirement and the relevant installed guidance.

## Runtime tuning and presentation
`config/tuning.json` defines typed settings with bounds, localized labels/descriptions, integrity class and `LIVE`, `NEXT_ACTION`, `NEXT_SPAWN`, `NEXT_STAGE` or `NEXT_RUN` application. `autoload/tuning_store.gd` separates requested values from active values, validates changes, exposes non-default source overrides and makes gameplay tuning ineligibility sticky for the current run. Preserve cosmetic changes without unnecessary score penalties.

`scripts/manus/preview/tuning_adapter.gd` exposes the existing store to the Addon. Retain the source configuration,
stage routing, physics, run eligibility and input/pause ownership; do not recreate a native Tweak panel or launcher.

The background is a static managed image. `comet_juice.gd` and `comet_effects.gd` provide bounded collision feedback, trails, flashes and impact presentation; reduced motion and intensity settings constrain their output. `shaders/arcade_filter.gdshader` is the adjustable full-screen filter. Preserve readable table silhouettes and real contact positions when changing art or effects.

## Audio, media and localization
Keep semantic cue ownership in `autoload/audio_director.gd` and its supplied callers. Preserve the shared browser BGM adapter, one logical soundtrack across title/gameplay routing, user-gesture unlock, native fallback, mute/volume, pause behavior and bounded UI/SFX voices. Follow the shared native/export checks and user Web acceptance workflow for lifecycle changes. Source and transformation evidence for the supplied soundtrack, cues and artwork is recorded in `asset-provenance.json` and `assets/template/provenance/`.

All reusable media keys and resource references belong under `assets/template/`. Restore media through `assets.lock.json` and verify hashes; source-session private locations are not a reusable publication. Update the lock only after permanent public bytes have been verified. Keep sprite-sheet frame dimensions and source regions aligned with their rendering code.

`scripts/pinball_locale.gd` loads `localization/en.json` and `localization/zh_CN.json`, interpolates values and supplies English fallback. It also registers localized mission text from configuration. Keep title, HUD, tutorial, settings, dialogs, results, names and tuning labels bilingual. Language changes persist and must update currently visible controls.

Follow [shared typography](game-workflow.md#default-typography) for user-uploaded fonts. The template's bundled display/body fonts are the default; Noto Sans SC supplies the approved 6,547-codepoint Simplified Chinese repertoire. Verify actual font binding, both locales and player-name validation, including rejection of unsupported characters; this font does not promise arbitrary Unicode or Traditional Chinese coverage. The fixed loader subset is separate from the full runtime fallback.

## Required verification
After restoring managed media, use the installed Addon Game workflow and its runtime directory:
```bash
npm run check
npm run build
npm run check -- --pack
"$GODOT_BIN" --headless --path . --script tools/validate_template.gd
"$GODOT_BIN" --headless --path . --script tools/template_config_check.gd
"$GODOT_BIN" --headless --path . --script tools/pinball_services_check.gd
"$GODOT_BIN" --headless --path . --script tools/tuning_acceptance.gd
python3 tools/install_cjk_font.py --check
```

Keep relevant source/pack hooks in `game-verification.json`. Exercise victory through real mission/jackpot progress, defeat from timeout and last-ball drain, retry, confirmed exits, stage continuation, score finalization, tutorial skip/completion, local save/reload and invalid configuration handling. Verify the export from clean source, with no cache or previous PCK masking missing media or resources.

Use a real renderer for title, play, pause, results, tutorial and tuning captures in English/Chinese and landscape/portrait. Include audio unlock, visibility/pause transitions and release exclusion of tuning in user Web acceptance. A headless pass validates logic; it does not establish visual or browser acceptance.
