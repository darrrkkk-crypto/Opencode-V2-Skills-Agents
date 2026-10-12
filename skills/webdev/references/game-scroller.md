<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Side Scroller — Operation: Dust Fang

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


This recipe describes the current `game-scroller` template: a complete, English-language arcade run-and-gun with a grappling claw. Its three connected stages are Dust Fang Town, Rustline Canyon and Jackal Fortress. Four locked combat arenas lead to the two-phase Rhino Crawler boss, followed by the mission results. Preserve the supplied gameplay, stage transitions, art, soundtrack and editable Godot sources when reskinning or extending it.

## Play and controls

Run and jump through the mission, shoot at range or slash nearby enemies, grapple light enemies and props into your hands, carry enemies as bullet shields, and throw them into other targets. Heavy enemies pull the hero into a grapple strike; overhead rings support swinging across gaps. Explosive barrels and fuel tanks create chain reactions. Rescue captives, collect weapons and supplies, and mount machine-gun nests with an overheat meter.

| Input | Action |
| --- | --- |
| A/D or left/right arrows | Run |
| W/S or up/down arrows | Aim up; crouch or aim down in the air |
| Space/Z | Jump; hold down to drop through a platform |
| J/X | Shoot; close-range knife; throw a carried target |
| K/C | Grapple; combine with up for overhead targets |
| L/V | Grab, throw, or mount/dismount a machine-gun nest |
| E | Use the selected item |
| Q | Switch item |
| F/R | Activate FURY when its meter is full |
| Escape/P | Pause or resume |
| Enter | Start from the title screen |

Keyboard is the supported gameplay input. Do not describe the inherited engine input events as a complete controller or touch implementation. The title contains the field manual and credits; pause offers audio controls, restart and return to title.

## Mission, scoring and feedback

`scripts/level_data.gd` owns the continuous level strip, stage boundaries, terrain, encounters, props, captives, checkpoints and boss arena. `scripts/game.gd` owns camera locks, encounter completion, stage tally, streaming gates, respawn, victory/defeat and local best score. Preserve the four arena locks, continuation gates and boss activation when changing geometry or spawn placement.

`scripts/style.gd` owns D/C/B/A/S STYLE ranks, score multipliers from 1× to 3×, varied-kill rewards, repeat-method penalties, decay and FURY. Taking a hit drops a rank. FURY fills from stylish play and enables a timed overdrive, eight seconds with the bundled defaults. Preserve the distinction between mission combo, STYLE rank, chain explosions and stage tally bonuses.

The Rhino Crawler uses cannon volleys and ground rams, then adds lasers, missile rain and drones below half health. Platforms and a swing ring support dodging. Keep telegraphs, damage windows and defeat flow synchronized with its presentation.

The current game saves its local best score and audio/player preferences. It does not ship the previous template's robot upgrade shop, Calico stages, player-name entry or leaderboard. Menus and authored game text are English; `localization/en.json` supports the owner tuning labels.

## Source owners

```text
game-scroller/
├── project.godot, scenes/{title_screen,game}.tscn
├── scripts/
│   ├── game.gd, level_data.gd           mission and authored encounters
│   ├── hero.gd, actor.gd               player movement, grappling and carrying
│   ├── enemy_*.gd, boss.gd             enemy and boss behavior
│   ├── prop.gd, world_object.gd        throws, explosives, captives and nests
│   ├── projectiles.gd, pickup.gd       projectile combat and inventory
│   ├── style.gd, hud.gd, title_screen.gd, ui_kit.gd
│   ├── terrain.gd, background.gd, decor.gd, fx.gd, post.gd
│   ├── sprite_db.gd, sprite_lib.gd     generated sprite pivots and rendering
│   ├── segments.gd, segment_manifest.gd
│   ├── game_audio.gd, audio_catalog.gd
│   └── tuning_store.gd, manus/preview/tuning_adapter.gd
├── config/tuning.json                 typed owner tuning schema
├── assets/template/{game,share,audio,fonts}/
├── web/
│   ├── export.json                   same-origin auxiliary media manifest
│   └── loading.template.html, manus-fonts.css, build-shell.mjs
├── tools/{build_segments.py,art/}     reproducible media manifests and tools
└── test/{smoke,progress,bot,capture}.gd
```

## Assets, audio and Web streaming

Keep runtime media under `assets/template/`, pinned in `assets.lock.json` with the Template group. The supplied art, fonts, soundtrack, voice and SFX are part of the template; preserve their bytes and resource paths unless the requested change replaces them. `asset-provenance.json` retains source and license evidence. Kenney particle/smoke packs and sfxmint impacts are CC0; Black Ops One, Chakra Petch, Nunito and the Noto Sans SC fallback carry adjacent SIL OFL notices. Keep the canonical `scripts/manus/open_source_licenses.gd` and browser BGM helpers.

`game_audio.gd` owns one music player, a fixed pool of 16 one-shot voices, separate music/SFX/UI levels, first-gesture activation, pause and transitions. `audio_catalog.gd` owns cue paths, gains, repeat limits and pitch variation. Stage music and boss/victory tracks use the same canonical browser BGM backend as the title music; do not introduce a second independent soundtrack controller.

The boot PCK includes the title, engine scripts, fonts, HUD, common combat audio and stage-one visuals. The title starts background streaming. Stage-one music and stage-two/three media are separate same-origin files, queued by `segments.gd`; stage gates wait for the required segment before continuation. Native play loads the same resources directly. Preserve flat exported filenames and the correspondence between the resource manifest, Web asset map and export exclusions.

Run `python3 tools/build_segments.py` after changing streamed file membership or bytes. It regenerates `scripts/segment_manifest.gd`, `web/export.json` assets and the Web export exclusions. Keep auxiliary files within the managed Web export limit of 64. Use the current managed `npm run build` workflow so the exported media are staged beside `index.html`; copying only the PCK loses later-stage media.

The loading shell is generated from `web/loading.template.html` and `web/manus-fonts.css` by `web/build-shell.mjs`. `web/export.json` declares that builder and the same-origin `loading-background.webp` asset. The font CSS embeds the approved loader face; `web/loader-cjk.json` records its coverage and provenance. Run `npm run loader:check` to validate without writing generated output. Do not restore a generated `web/loading.html` to the starter or inline the loading artwork as base64.

`tools/art/` retains the original sprite/background processing tools. `npm run art:rebuild` requires `ART_RAW` and `ART_RAW_V2` pointing to the original generated masters, plus Pillow and NumPy. These masters are optional authoring inputs and are not required to play or export the supplied assets. Audio regeneration additionally needs FFmpeg. Rebuilding requires reviewing and repinning changed asset hashes before delivery. `frames.json` files own sprite pivots; regenerate `scripts/sprite_db.gd` after edits rather than adjusting its generated entries by hand.

## Tuning and runtime boundaries

`config/tuning.json` describes movement, grapple, health, lives, enemies, STYLE/FURY, feedback, camera and audio controls. `tuning_store.gd` validates values and cross-field movement constraints, keeps requested and active values separate, applies next-run gameplay settings, and applies live cosmetic/audio settings. `scripts/manus/preview/tuning_adapter.gd` exposes those existing owners to Addon Tweak Controls; it does not own a second set of values. The managed release projection removes the preview adapter and its autoload. Keep production gameplay independent of that preview-only path.

Bound transient effects in `fx.gd`, preserve one-shot audio limits and maintain segment decode scheduling. Pause, hit-stop, FURY and stage tally must restore normal speed and input correctly. Keep reduced-motion and effect-density settings wired to the existing systems.

## Verification

Use the receipt's `GODOT_BIN` with the current Game delivery commands. After importing the project, `npm test` runs the finite smoke test for title/game startup, movement, jump, shooting, grapple, grab/throw, item use, enemy carry/throw and pause. `npm run test:progress` walks the entire mission in god mode, clears all four arenas, defeats the boss and requires victory/results; it catches progression softlocks, not difficulty balance. `npm run test:checks` checks that native test failures and Godot script errors are not mistaken for success. `npm run test:bot` is an optional simple play bot that reports its outcome.

`npm run capture -- /absolute/new-output-directory title,start,town,canyon,outpost,boss` creates native screenshots in a fresh directory. Review the title, all stage themes, HUD, FURY/chain feedback, tally and boss presentation as affected by the change. For final Web delivery, verify the generated export in a real browser: title/first-gesture music, keyboard input, pause/resume, stage segment requests, transitions into canyon and fortress, boss/victory music and restart. A native run alone cannot establish that streamed Web files are served correctly.
