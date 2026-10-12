<!-- Generated from skill-src/internal/game-sources; run generate:game-guides. -->

# Generic Multiplayer Template

Use [Game workflow](game-workflow.md) for scope/delivery; mobile/touch/portrait work and checks require a user request. Read only for changed code. For online multiplayer, read [the shared service guide](game-multiplayer.md).



## Playable foundation

This is the fallback for online multiplayer games without a matching specialized gameplay starter.
It includes a Godot client and a standalone Node + `ws` authoritative server. The paddle game is the runnable
example used to demonstrate the connection and deployment contract, not a restriction on the genre.

For a different requested game, replace paddle-game rules, court and in-game UI with that game's mechanics.
Reuse room/seat lifecycle, validated messages, reconnect handling, endpoint discovery and deployment
plumbing where applicable. Implement authority in the Node server and adapt the client's input and
snapshot presentation together; do not replace the service with headless Godot just to reuse GDScript.
The sample has two seats and paddle-game packets. Adapt player limits, rules and both protocol ends
with focused tests; renaming the template does not provide arbitrary player counts or game rules.
For a paddle-game request, extend the shipped simulation and client directly. Purely offline requests use
`generic` instead and do not need this server.

Existing projects marked `game-pong-online-v1` through `game-pong-online-v7` keep their installed
source, Pong protocol and user edits. The new catalog name alone does not authorize a gameplay rewrite,
reinitialization or migration of an existing project.

## Shipped paddle-game example
The reference uses geometric graphics, one generated pulse loop and short synthesized cues; this does not set adaptation preferences. Follow [shared production-choice routing](game-blueprint-godot.md#asset-production-choice-wording) and [audio sourcing](game-workflow.md#audio-production-as-needed). `assets.lock.json` restores the template fonts and `NotoSansSC-VF.subset.woff2`, including editable-name coverage, under [shared typography](game-workflow.md#default-typography).

The title screen exposes EN/CN, a room code, Join/create and audio settings. W/S and Up/Down move the
assigned paddle; press the upper/lower court half on touch. UI and court input stay separate. The
server assigns two seats; additional clients spectate. Both players must be connected for simulation.
There is no local pause of the other player's match. Leaving closes this client's connection; its
seat remains reserved for the server's grace period. Spectators do not automatically take vacant seats;
use **Retry connection** after grace expires to try joining an available seat. This minimal reference has endless points,
not ranked matchmaking, accounts, match completion or durable scores.

## Source owners

| Owner | Responsibility |
| --- | --- |
| `scripts/main.gd` | Title/HUD, room/seat protocol adapter, input and procedural audio |
| `scripts/net/connection.gd` | Reusable discovery, socket lifecycle, cancellation, bounded retry and timeout |
| `scripts/net/protocol.gd` | Bounded packet validation, room/build identity and snapshot fields |
| `scripts/game/local_paddle.gd` | Owned-paddle anticipation, bounded correction and stale-state reset; no input history |
| `scripts/game/pong_board.gd` | Local-paddle presentation and remote snapshot smoothing; never collision or scores |
| `autoload/i18n.gd`, `localization/*.json` | Complete EN/CN copy and title toggle |
| `autoload/save_store.gd` | Locale preference only; not authoritative match storage |
| `autoload/tuning_store.gd`, `config/tuning.json` | Debug presentation drafts and audio mix |
| `server/authoritative_server.mjs` | Fixed-step simulation, rooms, seats, inputs and lifecycle bounds |
| `server/e2e_clients.mjs`, `server/server.test.mjs` | Two-client integration and authority regressions |

## Reusable connection component

Use `scripts/net/connection.gd` with its `main.gd` adapter when adding multiplayer to another game.
The init/attach **Multiplayer reference source** points to these files in the installed Addon;
read them before copying the component into the existing project. Keep that game's scenes and UI.

Add one connection Node under the game owner. Call `start(build, native_env, make_url)` to read the
Web discovery descriptor or the explicit native environment/config endpoint. `make_url(endpoint)`
adds only the game's room/resume parameters to the verified endpoint. In this example it restores
the tab's endpoint-scoped seat token before each handshake. The component never owns room codes,
seat tokens, packet schemas, input, simulation or UI; keep those in the matching client/server adapter.

Call `poll(delta)` each frame, forward `text_received` to the game's bounded protocol decoder,
and call `confirm_activity()` only for accepted welcome/state messages. Use `send_text()` for
validated outbound packets. Map `state_changed` and `disconnected(code, was_open)` to the game's
status and recovery UI. This sample stops after close code 4001 (seat replaced); another protocol
must apply its own terminal-close policy. `stop()` cancels discovery and socket work; retry calls
`start()` again, while `reconnect()` retries the current endpoint without rereading configuration.

During `DISCOVERING`, no socket polling, timeout or reconnect runs. Cancel/restart invalidates late
HTTP callbacks, and stopping from a packet callback drops the remaining queued packets. Invalid
configuration stays `UNAVAILABLE` until an explicit retry. `discover(url, build, make_url)` and
`connect_endpoint(endpoint, make_url)` are explicit entry points for an alternate trusted discovery
source or isolated tests; do not source either address from an invitation. The component keeps the
sample's bounded packets and retry timings; adapt limits alongside protocol tests when required.

## Multiplayer contract

The shared service guide owns deployment, permissions, public HTTPS/WSS, operations and **Responsive controls with minimal client logic**. Its v26 implementation is `scripts/game/local_paddle.gd`: `set_input` responds locally, `accept` records authority, `advance` moves/corrects; `main.gd` feeds input and `pong_board.gd` renders. Reuse these owners. This recipe and the service README supply protocol, concrete defaults and local checks.
Set the verified public endpoint in `multiplayer/config.json`; the installed Game runtime supplies
`multiplayer/bootstrap.json` for Web Preview/publication. For this starter, keep build `pong-online-v2` aligned across
client and server. Native tests use `PONG_WS_URL` and optionally `PONG_ROOM`. No endpoint comes from
an invitation, and no cloud computer or domain is preselected in this template.

Clients send `input` with `value` -1/0/1, increasing `seq` and monotonic `sent_msec`. The server produces
`welcome` with authoritative movement bounds/speed and sequenced `state` packets,
including room, marker, roles, paddles, ball, score, phase and audio event. Resume tokens stay in tab-scoped
storage; invitations contain only the room. Reset snapshot sequence tracking on a new welcome, including
after server restart. Stop automatic reconnect after another socket has resumed the seat. Missing service
shows a configuration/retry state rather than claiming the game is online.

The server echoes the **applied** input's `ack_seq` and `sent_msec` plus paddle `vy` in each snapshot.
Client timestamps are echoed only; they never control server simulation time or movement. The local
paddle estimates one-way latency from that echo, projects at most 150 ms and corrects small errors
with a 100 ms blend time. Its dead zone is 0.002 court-heights; errors over 0.20 reset immediately.
A pending direction change suppresses older corrections for at most 500 ms without storing input
history. Snapshots missing for 500 ms, disconnect, seat loss and waiting stop anticipation; welcome
and a fresh snapshot reset it. The server also releases input after 500 ms without a new valid input.
Only the owned paddle anticipates; the ball, opponent, scores and audio events remain server-driven.
This improves simple controls but does not implement ball-contact prediction or competitive rollback.

Existing projects retain the protocol declared in their client and matching service. Template revision
numbers alone do not identify the protocol: upstream v23/v25 use `pong-online-v1`, while v26 and the
earlier anticipation candidate v22 use `pong-online-v2`. Do not change only one protocol end. Apply an
explicit client/service adaptation to update snapshot-only games; incompatible service builds are rejected.

`config/tuning.json` and `TuningStore` own local UI/audio descriptors, exposed to the Addon by
`scripts/manus/preview/tuning_adapter.gd`. Preserve interpolation, reduced motion and audio consumers. Do not
expose client controls for server-owned movement, collisions, tick rate or reconnect rules. Such rule changes
belong in `server/authoritative_server.mjs` and require both-client validation before redeployment. The Addon
popover does not pause or restart the match; ordinary player audio/language settings remain independent.

## Verification

Hydrate assets in a clean disposable project first. Run `tools/verify.sh --export` for source tests,
Godot import, current Web export and isolated PCK validation. Keep the `ManusFontTheme` autoload:
it binds the bundled composite after import and covers Controls outside the main scene as well as
world labels. Do not restore an early project font load or replace it with a main-scene-only theme. Run `pnpm --dir server install
--frozen-lockfile` then `pnpm --dir server test` for isolated two-client/server checks. The service uses
an OS-assigned port in automated tests; it must not bind another project's listener. Native visual
captures use `tools/capture_native.gd` with `PONG_CAPTURE_PATH` and a real renderer. Run `node test/native_network.mjs` for two real Godot clients against an isolated service,
including immediate input/stop/reverse, authoritative scores and seat recovery through a TCP proxy
with 200 ms simulated RTT and ordered jitter. Set `PONG_TEST_LATENCY_MS=50` for 100 ms RTT (the value
is delay per direction). No cloud deployment is involved. Run the standard
Addon Preview/release workflow after a coherent batch; test output and server source stay outside PCK.
Local tests do not prove a public cloud deployment. Ask the user for normal Web acceptance after delivery.
