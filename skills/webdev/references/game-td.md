<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Game Template — Elemental Tower Defense

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).


**Seed Defense** uses `junnyboi/game-td-elemental` art.
Follow the installed Game workflow; do not restore predecessor roster, traps or campaign.

## Playable loop

Defend the Last Seed across three eight-wave chapters. Place guardians on raised platforms, earn
gold, upgrade three tiers and merge elements. Clears improve stars/unlocks. Replays, tutorials,
pause/settings, durable results and standings are integrated. Normal/Hard is fixed at battle start.

`scripts/fablewood/tuning_catalog.gd` starts gold at 300 (200–800/25) and health at 20 (5–20/1).
On launch, `screen.gd::_apply_tuning()` overrides model `dp/base_hp`; align its fallbacks with
`sim/fablewood_battle.gd::create_fablewood()` and test chapter launches. For health above 20,
raise `_check_terminal()`'s `mini(20, base_hp + 1)` cap too.

| Element | Combat role |
|---|---|
| Fire | Ground splash and burning; suppresses troll regeneration. |
| Frost | Slows ground and flying enemies. |
| Storm | Chains lightning with aerial priority. |
| Earth | Ground-only armor-piercing physical damage and stagger; bypasses Prismback’s Arts shell. |

Invaders: Goblin, Orc, Troll, Dragon, Prismback, Harrier and Broodmother. Prismback's shell regenerates;
slow/stagger interrupts Harrier bursts; Broodmother spawns bounded children. Hard strengthens/compresses
late schedules. Counter feedback adds no damage bonuses.
Basic hits use `ceil(attack_rating * 0.25)` at every tier. Base enemy HP uses
`floor(authored_hp * 1.5)` before chapter/wave/difficulty multipliers. Preserve rounding, costs
and rewards. The Chapter 3 regression proves one eight-wave clear using starting and earned gold.

## Source owners and extension seams

| Owner | Responsibility |
|---|---|
| `autoloads/game.gd` | Routes, tickets, results, score retry, data clearing. |
| `sim/fablewood_battle.gd` | Fixed-tick combat, upgrades, waves, merges, terminal metadata. |
| `sim/fablewood_ultimates.gd` | Recharge, targets, delayed pulses and Convergence Meteor. |
| `sim/battle_model.gd`, `sim/campaign_*`, `sim/battle_ticket*` | Combat, campaign commands, recovery and launch validation. |
| `data/{stages,operators,enemies}/` | Grids, paths, schedules, base definitions. |
| `scripts/fablewood/screen.gd` | Title/chapter/battle/result/settings/tutorial UI and input. |
| `scripts/fablewood/world.gd`, animation/effect helpers | Projection, actors, camera, bounded effects. |
| `autoloads/{music,sfx}.gd` | Playback and routing. |
| `scripts/fablewood/tuning{,_catalog}.gd` | Typed parameters, requested/active state, integrity. |
| `scripts/manus/preview/tuning_{adapter,transport}.gd` | Addon Tweak bridge, excluded from player builds. |
| `scripts/fablewood/screen_filter.gd{,shader}` | Optional static presentation filter. |

The model owns combat, RNG, ticks and rewards; views cannot mutate simulation or saves.
`Game` owns routes and campaign saves.
Launch commits before battle. Failed results retain their ticket/outcome; pending-attempt recovery
restarts the chapter. Clear data through `Game.clear_player_data()`.

Only `s1`–`s3` are playable; retained `s4`–`s10` still affect campaign identity.
`sim/campaign_runtime_context.gd` and `sim/campaign_v3_codec.gd` include **every stage with
`campaign_index >= 1`** in stage order, rewards and combat binding; do not delete them.
Schedules use `wave_index * 30000 + within_wave_tick` with zero-based waves. More waves/chapters
require coordinated launch, navigation, clear rules, rewards and tests.
`CampaignV3Codec.derive_environment_sha256()` binds operator resource bytes/combat fields, classes,
skill/target policy, campaign/reward rules, traps and campaign stage IDs/order. Its
`sim/combat_content_binding.gd` projection also binds the enemy IDs referenced by waves across
all those stages and each enemy's `defense`, `resistance_permille` and `attack_damage_kind`.
Stage/enemy resources contribute this projection, not all their bytes. After editing identity inputs, run
`tools/run_godot_test.sh res://test/fablewood_context.gd`. Synchronize its derived hash in
`data/campaigns/p16_v3.tres` and `data/campaign_def.gd` (`P16_V3_ENVIRONMENT_SHA256`), then verify
launch/result commit. Preserve old saves through explicit migration or a new fork save identity.
Runtime Tweak does not edit these authored files.

## Merging and ultimates

Two living, different-element tier-III guardians produce six dual guardians: Fire/Frost → Rimeflame;
Fire/Storm → Thunderpyre; Fire/Earth → Cinderroot; Frost/Storm → Tempestquill;
Frost/Earth → Winterbark; Storm/Earth → Thornvolt. The model owns donor eligibility, reversible
removal and legal placement. Pending placement holds preparation and blocks conflicting actions.
Cancel, Escape and teardown restore donors, counters and ultimates. Execute cancellation outside
`assert()`. Merging costs no currency.
Dual guardians retain independent attack channels and the larger donor range; ordinary upgrades end.

Complementary duals with no shared element summon **Worldheart, the Fourfold Warden**:
Rimeflame + Thornvolt, Thunderpyre + Winterbark, or Cinderroot + Tempestquill. It inherits four
channels and summed donor ranges, then cannot upgrade/merge. Reject mixed basic/dual, same-element,
overlapping-element or dead donors without losing units or spending gold.
Dual ultimates recharge in active waves with living enemies, wait for eligible targets and retain
charge between waves. Preserve integer-tick periods and masks.
Worldheart’s meteor charges for 600 combat ticks and flies for 30 ticks to a locked position.
Removal, cancellation and terminal states clear/restore pending work in the model;
meters, localized inspectors and effects only display it.

## Results and recovery

Score remains `clamp(win * 2,000,000 + chapter * 100,000 + stars * 20,000 + kills * 50 -
leaks * 500, 0, 4,000,000)`. Duration is terminal combat ticks divided by tick rate, excluding
wall-clock pauses. The model seals mode, terminal tick, tick rate, duration, run hash and tuning
provenance. Fatal damage wins over simultaneous final-wave completion. Preferences/resets cannot
relabel finished attempts; hashes prove local consistency, not server-certified anti-cheat.

Standings retain 50 rows/group, filter before showing eight, and break ties deterministically.
**Normal/Hard** contain eligible runs; **Practice** contains
applied gameplay tuning; **Legacy** preserves records without sufficient provenance. Pending
NEXT_STAGE edits do not taint a current run. Applied gameplay changes remain marked through Reset;
cosmetic/audio changes remain eligible. No remote leaderboard is configured.

Failed campaign saves retain their mutation behind Retry Save, which survives resize/language changes
and cannot be dismissed. Failed launches retain the screen with retry feedback. After campaign commit,
score-only retries retain submission ID/time without repeating progression. Corrupt scores recover
from a valid backup.

## Controls, onboarding and localization

Pointer/touch controls place, select, upgrade, merge, pan and zoom. Preserve inverse picking,
platform contacts, bounds and single touch ownership; ignore emulated mouse events in the world.
Keyboard: 1–4 select; U upgrades; Enter/keypad Enter starts a wave; Space opens Pause;
Q/E changes 1×–4× speed; WASD pans; Escape cancels placement/merge or follows the active modal.
Ignore repeated/modifier gameplay shortcuts and focused text input. Keep speed across pause/relayout.

Each wave has 30 seconds of preparation independent of speed; Pause, modals, tutorials and pending
merges hold it. Manual start/expiry share one action without duplicate waves. Preserve ready pulse/bar,
upgrade shortfalls, affordability and reduced motion. Modals own focus/input; Settings returns to
Pause, Resume works after Threats/How to Play, and resize/language changes retain state and camera.

The six-step tutorial offers Skip. Selection, placement, upgrade and wave steps require successful
actions; informational pages allow Next. Hints follow input method. Persist versioned completion/skip,
migrate old seen flags once and respect completion on Retry. How to Play replays it; omit developer controls.
All copy uses matching keys and whole-message placeholders in `localization/{en-US,zh-CN}.json`,
including narrow guardian labels, inspectors, rankings and Tweak. Figtree regular/medium/bold use
the full approved Noto Sans SC fallback; retain OFL notices and the loader’s embedded subset.

## Art, audio and player settings

For new TD games, theme towers and raised pads within the complete brief, saved Blueprint roles,
accepted asset source and permissions. Preserve approved reuse/exclusions and empty coverage;
generate only when authorized, else adapt suitable supplied/catalog art.
Backgrounds alone are insufficient; report retained art.
For selected roles, replace four elements at all tiers, six merges and Worldheart: static and
basic idle/merged idle/cast sheets (48 frames, 8×6), plus pads. Use new paths outside
`assets/template/` and update
preloads in `presentation.gd`, `guardian_animation.gd`, `merged_art.gd` and
`merged_animation_layout.gd`. Align logical cells, trim, pivots, anchors and pad contact/picking
with art. Atlas metadata is path-keyed; do not overwrite packed paths with
raw sheets or run `pack_atlas_padding.py --apply` while packing is enabled. Save/prepare syncs
media; never hand-edit lock facts. Check atlas; render idle/cast, reduced motion and placement.

Starter maintenance keeps imported art/effects. `assets.lock.json` restores `assets/template/`
by path/size/hash with matching imports. `asset-provenance.json` and `THIRD_PARTY_NOTICES.md`
retain known source/license facts; unknown historical models stay unknown. Exclude obsolete
`refined_animation/` from exports. Preserve animation states, bounded caches, culling and teardown.

Music cue `fablewood` uses `Audio/illuminated_theme.ogg`, a 138-second loop across title, chapters,
battle and results. SFX keys map to `Audio/illuminated_<cue>.ogg`: `hover/confirm/back/invalid`,
`build/upgrade`, `fire/frost/storm/earth` and `_hit`, `enemy/breach/wave/merge_success`,
`enemy_shell_break/enemy_harrier_dash/enemy_brood_spawn`, `meteor_impact`, `victory/defeat`.
Check `bundled/{music,sfx}/catalog.tres` and event routing before altering the map. Reuse supplied media.

Routing: Music → Master; UI → SFX → Master. Master/UI default to unity. Preserve Music/SFX gains,
eight SFX voices, cooldowns, deduplication and spatial checks. Settings persist four volumes, reduced
motion and a default-off static filter: intensity zero disables rendering; it ignores input/simulation.
Pause preserves music/existing SFX without new combat events. SceneTree pause suspends/resumes the
same native voice. Stage pitch updates a playing cue without restarting; the browser BGM adapter owns unlock/Master gain.

## Tweak boundaries and player exports

The Addon popover reads 15 localized descriptors in six categories via `TuningBridge`.
The game has no panel/launcher/shortcut. The Addon owns drafts, Reset and Save with Manus.
Apply validates one atomic patch without persistence/reload; unchanged values emit nothing.
Requested/active state stays distinct; schema identity is locale-independent.

| Boundary | Controls |
|---|---|
| LIVE, cosmetic | Guardian/enemy visual scale, effect opacity. |
| NEXT_ACTION, cosmetic | SFX pitch, acknowledged when a cue starts. |
| NEXT_STAGE, cosmetic | Text scale, initial camera zoom, music pitch. |
| NEXT_STAGE, gameplay | Starting gold, reward scale, town health, attack damage/speed, range bonus, enemy health/speed. |

Validate numeric types, finite bounds and steps before consumption. UI rebuilds retain active chapter
values. The bridge checks leases, schema, membership and values. Only the adapter/transport live in
`scripts/manus/preview/`; common release preparation removes that directory and its autoload. The
production manager starts at canonical defaults with no draft-file reads/writes; old debug config
cannot affect release. Player Settings, audio and filter remain available.

Web exports use `web/loading.html` and include locale/atlas metadata and font notices;
exclude tests/tools, obsolete media, locks/provenance and generated output.

## Verification

`game-verification.json` registers twelve bounded checks: base loop, merges, ultimates, Worldheart,
late enemies/old saves, interpolation, particles, endpoints, atlases, results/retries and a source suite.
The suite covers music markers, real Tweak consumers/bridge, audio/filter, modal/tutorial recovery,
Hard standings, placement/touch, isolated test guards and a Chapter 3 earned-gold clear.
Children require clean markers, isolated saves and frame limits. Packed hooks run externally against
the exact PCK; fixtures are not shipped. Launch checks cover repeated Play/Replay/Continue and failed-launch retries.

Run `npm run check`, the installed release preparation workflow, then `npm run check -- --pack`.
Focused `SceneTree` scripts use
`tools/run_godot_test.sh res://test/<check>.gd` with resolved `GODOT_BIN`; Node fixtures use their
`.tscn` scenes (attach the script to a Node in a disposable wrapper if needed). Render-capture
fixtures need native Godot scenes, not headless `--script`. Use disposable copies.
`FABLEWOOD_UI_CAPTURES` captures the integrated UI with a real renderer; Dummy audio cannot prove
audibility. Use registered tower-defense checks; predecessor `tests/` UI fixtures are historical.
Shared workflow controls native screenshots and requested browser/mobile checks.
Source/native/PCK checks do not prove browser acceptance, deployment or session adoption.
