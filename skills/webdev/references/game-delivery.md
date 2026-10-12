# Game preview, verification and delivery

Keep Open Source Licenses unless asked otherwise.

Godot workflow. Three.js uses the Web build/checkpoint flow and [Game sharing](game-sharing.md).

Use the init/attach project, GAME_RUNTIME, GODOT_BIN, HOST and PORT; export GAME_RUNTIME only in the local shell.
Reuse checks/artifacts; distinguish preview, checkpoint and publication.

On the user's computer, mute agent-launched Godot runs with `--audio-driver Dummy`; `--headless` already uses Dummy.
Omit Dummy only for SFX/music checks, then restore it for subsequent runs. For requested browser debugging,
launch the test browser muted (e.g. Chromium `--mute-audio`), except during SFX/music checks. Keep muting process-scoped:
never change OS volume, in-game/saved settings or the user's Host Preview; leave user acceptance audible.

## Game publishing configuration

After init or attach, use webdev.config GET config. Game defaults are build.command="true" and
build.outputDirectory="site". If either is missing or different, read [configuration](configuration.md),
[deployment](deployment.md) and its [static build](build-contracts.md#static-build)
contract. Keep Game's true/site contract without reselecting its architecture, then set the build domain:
```json
{"method":"PUT","path":"config/build","body":{"build":{"command":"true","outputDirectory":"site"}}}
```
Require write success and GET config readback before release preparation. Preserve other domains, especially
server/database and backend deployment; retain this build domain in whole-config replacements. Online Games
keep site/ alongside their backend. Do not wait for the user to supply these settings at Publish time.

save-release.mjs prepares and commits site/; true serves that verified output without rebuilding Godot.
dist/ is local export/cache output, not the publish directory. If publishing requests dist/ despite confirmed
true/site, report the selected SHA and returned error as a publish/config mismatch; do not change this contract
or copy site/ into dist/ to hide it.

## Project commands

| Command | Purpose |
| --- | --- |
| npm run check | Finite import/boot and configured gameplay checks |
| npm run check -- --pack | Check matching prepared release PCK/current export, without another export |
| npm run dev | Resident server with explicit receipt HOST/PORT |
| npm run preview:build / preview:status | Build one coherent batch / inspect current build |
| npm run doctor | Only for missing/mismatched toolchain |
| npm run build | Requested portable WASM/PCK export to dist/standalone, not a platform checkpoint |

Aliases need GAME_RUNTIME; older projects can call runtime entries directly. Windows uses Node/npm and
`$env:GAME_RUNTIME`, `$env:HOST`, `$env:PORT`, not POSIX exports/.sh. Portable export uses present assets without
Manus credentials, uploads, commits, publication or site/ replacement; online services still need configuration.

## Godot command environment

Reuse the receipt's GODOT_BIN in each native shell. Only if it is missing or unavailable:
```sh
GODOT_BIN="$(node "$GAME_RUNTIME/doctor.mjs" --executable)" && export GODOT_BIN
```
Stop on failure; native calls use `"$GODOT_BIN" --path .` despite older READMEs. Doctor is read-only. Failed init may
retry original arguments for missing macOS dependencies; fix invalid custom paths, versions or presets without
overwriting them or changing PATH globally.

## Delivery scope and stopping boundary

Default managed delivery requires a verified saved checkpoint. Only when the user explicitly limits delivery to
local play, Preview or source files and does not request a saved version may it stop with accessible artifacts and
sufficient behavior evidence, with platform limits disclosed. Asking to see or play a game during ordinary creation
does not waive its checkpoint; Local First selects the execution environment, not the delivery scope. Checkpoint,
portable export, release-ready and live-publication requests need their matching pipeline, and publication needs
authorization. Fix failures that block the requested result; do not pursue unrequested publication or auxiliary
records as new goals. A blocked requested result remains partial, not complete. Never bypass guards, forge receipts,
patch installed helpers or turn delivery into framework, exporter or validator development. Repeat checks, builds or saves only after relevant changes, a transient failure or a new diagnostic
hypothesis, and read back uncertain operations before replaying them. Keep diagnostics and usable artifacts; without a
supported next step, report the blocker instead of inspecting tool internals. Costly recovery follows the approval rule in
the [workflow](game-workflow.md).

## Resident preview

Check `node "$GAME_RUNTIME/preview-build.mjs" --status` and reuse a healthy server. In Local First, get the verified
`git_dir`/`project_dir` and Managed base from webdev.manus_git status and [Local](../worklocally/SKILL.md). Only a new
Game with unborn Managed HEAD and no remote refs may create an empty initialization commit; never start new history
for an existing resource. The local server and prepare-release set only GIT_DIR/GIT_WORK_TREE to the returned paths,
and saves and pushes use manus_git. Never copy credential env/helpers/remotes into services or source.
Start a server only when none is running, as a resident process with the receipt numeric PORT and HOST
(127.0.0.1 Local, 0.0.0.0 Cloud; Local needs a narrow network grant):
```sh
HOST="${HOST:?Set receipt HOST}" PORT="${PORT:?Set receipt PORT}" node "$GAME_RUNTIME/server.mjs"
```
Use this Session's declared port; never hardcode ports, kill unrelated processes, wait for the resident process to
exit or replace it with a static server. Startup does not build. Implement the requested game before first build,
then run `node "$GAME_RUNTIME/preview-build.mjs"` in another exec per coherent batch (only no arguments or --status,
never --project/--out). A successful build activates an isolated candidate and may reset play; a failure keeps the
last success. Init/Preview already hydrate assets; hydrate manually only for missing media. Diagnose errors before
rebuilding.

## Develop and validate

Reuse applicable checks, real runs through existing entry points and native captures. Run finite npm run check for
changed gameplay; boot or export success and clean logs alone do not prove player behavior. Add no tests when
existing evidence suffices; add the smallest bounded check only on explicit request, or when a critical required
behavior lacks evidence and cannot be exercised through existing entry points. Existing or new assertions must
drive real actions, not assigned outcomes or unrelated rejected actions. Do not build or repair test frameworks to
satisfy an acceptance format; an unsuitable source hook is an
evidence limitation, not an automatic porting task, and the same applies to new checks. An absent
`game-verification.json` or zero outcomeChecks is not a task to fill. Source and pack evidence are distinct: pack checks use existing
SceneTree `kind:"script"` hooks: --pack skips `kind:"scene"` checks and respects release-disabled debug hooks. Reuse
the matching PCK without re-export. Inspect affected native output and concrete devserver.log errors, and reuse
browserConsole.log, networkRequests.log and sessionReplay.log under .manus-logs. No proactive browser screenshots,
automation or loading tests; browser debugging needs an explicit request, otherwise report pending user Web
acceptance. Never claim unobserved behavior passed.

## Wire the game's loading screen

Apply the shared [game-specific loading screen](game-sharing.md#game-specific-loading-screen) requirement to new
games and remixes, including Fast prototype. Inspect the active Web preset's `html/custom_html_shell` and any
`web/export.json` shell builder; edit the authored shell/style/data inputs, not generated HTML or helpers.
If no shell exists, copy runtime loading-shell.html once to web/loading.html and set
html/custom_html_shell="res://web/loading.html". Use `npm run inspect -- <shell-source>` to avoid dumping embedded fonts.
Set application boot_splash/show_image=false (or use this game's own splash) with a matching solid bg_color.
Keep shell, preset and loading data together in source. Preserve the game's customized loader on resume, not
inherited template artwork. Preserve
Engine.startGame({onProgress}), the engine placeholders and canvas, and
`<meta name="manus-game-loading-screen" content="1">`. Use lightweight localized HTML/CSS/JS with live progress,
status, Retry, reduced motion and usable desktop resizing; loading behavior details are in
[runtime](game-runtime.md#fast-recoverable-startup). Loader art must load before the PCK: embed small art or upload
it through [project storage](storage.md) and use its returned immutable /manus-storage/<key> path, never res://,
PCK-only assets, expiring URLs or uncopied siblings. This includes the minimum loader's game-specific favicon.
If using this game's own OG/title art, keep controls clear of the title and subject, and retain the solid-color fallback.

## Sharing metadata

Read [Game sharing](game-sharing.md) before metadata/artwork changes or `game/sharing` writes; it owns
the shared file format, image requirements and authorization rules. Every first complete Godot game, including
Fast prototype, follows its [favicon and sharing text requirements](game-sharing.md#favicon). Standard effort also
prepares game-specific OG; Fast prototype skips unrequested OG production. Routine changes preserve existing edits.
Godot title fallback: project.godot config/name, then Game.
Godot registers the sharing images in the asset lock.

### OG cover and favicon

For Standard effort, the OG cover is a separately AI-generated promotional image in every production mode, including catalog and
procedural, under the [generation gate](game-workflow.md#asset-generation-mode-gate). Honor explicit supplied-cover
or no-AI restrictions and report limits rather than substituting a screenshot, local render or catalog composite.
Generate initially or on request, following the shared [artwork guidance](game-sharing.md#og-cover-and-favicon).
The favicon follows the recorded game-art choice and the shared prototype guidance. Set `project.godot`
`config/icon` to the same game-specific PNG recorded in `game-sharing.json`; do not leave the engine's default icon.
These Godot production rules do not apply to Three.js.

If game-sharing.json exists, call webdev.config POST game/sharing/prepare with {} before release. It records the
trusted publication origin in ignored state only, not images, a checkpoint or publication. The build validates the
bytes, produces immutable site/share/<sha256>.png and site/game-sharing.json and decorates the index; invalid or
missing sharing warns without blocking basic game readiness. Lost preparation context repeats prepare before
rebuilding. File edits alone are not publication. Source drafts never change old checkpoints, and version 1
metadata stays readable. A domain change does not block game publication: afterwards prepare, rebuild, checkpoint
and publish when authorized, reusing images; preparation alone does not update live cards.

## Prepare a version

Skip release preparation only when the user explicitly limits delivery to local play, Preview or source files
without requesting a saved version. Intermediate progress saves are allowed when labeled incomplete; first-complete
standards do not forbid them. For a checkpoint or release, the Host integrates canonical main
per [Git/checkpoints](git-checkpoints.md) before freezing; save never pushes, merges or chooses destinations.
Cloud terminal:
```sh
node "$GAME_RUNTIME/save-release.mjs" --message "Update"
```
Local webdev.manus_git (adapt POSIX process-scoped env to your shell):
```sh
GIT_AUTHOR_NAME=Manus GIT_AUTHOR_EMAIL=dev-agent@manus.ai GIT_COMMITTER_NAME=Manus GIT_COMMITTER_EMAIL=dev-agent@manus.ai node "$GAME_RUNTIME/save-release.mjs" --message "Update"
```
Keep Host GIT_CONFIG_* intact and never use the user's Git. Save syncs assets, prepares or reuses the snapshot and
commits the frozen candidate with normal hooks; later edits stay in the working tree. It rejects staged indices and hook-altered commits; inspect these errors. Unchanged commits are skipped. No extra sync/standalone export or
wrapper commit, except the [assets guide's pre-save grouping sync](game-assets.md#asset-browser-groups).
Run applicable npm run check -- --pack on this candidate before pushing.
Push the receipt's exact SHA to canonical main through Cloud Git or Local manus_git, never later HEAD/extra
merge/force push. checkpoint:not_recorded means unconfirmed: verify with the readback below. Retry transport failures
with that SHA without rebuilding; a moved main requires integration and a new save even with an unchanged tree.
Registration-only failure uses reconciliation, not another save/push. A source-only push cannot replace release
preparation. Release-candidate internals and developer-UI exclusion are in [runtime](game-runtime.md#release-candidates-and-developer-ui-exclusion).

### Checkpoint readback

GET game/sharing/releases/<exact pushed sha>: 200 ok:true confirms registration, not card delivery;
404 is absent/inaccessible/unconfirmed. preparation is sharing status; publish needs gamePublishReady:true.
checking waits without rebuilding. gamePublishCheckUnavailable retries this read once, never save/push.
gamePublishBlocker: required_secret_missing or publish_contract_missing need webdev.config repair.
game_backend_contract_missing: [backend recovery](game-backend.md#prepare-verify-and-recover).
Other failures need diagnostics/source/config fixes before saving; report blockers.
Sharing alone proves no readiness; absent sharing does not block a basic release.

## Publishing

Publish an authorized, verified checkpoint through the Dashboard or the supported corridor under Git/checkpoints.
Verify the [Game publishing configuration](#game-publishing-configuration) before release preparation;
requested online services keep the static client plus API hybrid contract. Historical artifacts are immutable,
version Preview disables external services, and Local First rollback is unavailable. Fix stale releases with a new
prepared version, never forged hashes. Report only the actual publish result and returned project domain, not
invented titles or storage URLs. Preview, checkpoint and publication are distinct results.

## Export inputs

### Export constraints
Use discoverable literal resources, tracked import/UID sidecars and `include_filter` for runtime JSON/CSV/TXT.
Web presets keep `thread_support=false`, `export_filter="all_resources"`, engine placeholders and template export
budgets. Keep tests, captures, tooling, provenance and raw masters out of player exports. Change identity in
project.godot or the editable shell, never generated site/ or dist/. Use installed delivery commands and receipt
ports, not historical Sandbox scripts, cached PCKs or template-local servers.
