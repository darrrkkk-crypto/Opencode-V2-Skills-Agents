# Godot backend publication

Use these rules for a Godot game's project-hosted login/OAuth, Stripe Checkout/webhooks,
leaderboards or other backend APIs. Keep `applicationKind: game` and the `true`/`site` build;
publish the backend and static game as hybrid. Offline/static Godot games need no declaration.
Three.js uses the normal Web deployment/checkpoint flow. An external payment link alone does not
require a game backend.

## Use Webdev configuration for publication

Configure the actual build, Dockerfile/health paths and complete ordered routes through Webdev config.
Read back the applied config before online deployment; unresolved provisioning remains a blocker.
Godot backend publication uses the same config and secret preflight as Webdev, plus its prepared
`true`/`site` export checks. Login, payment and generic API backends do not need a separate
`game-backend-contract.json` merely to publish. Historical checkpoints without a declaration use
the current validated Webdev config; no new checkpoint is needed solely to add this file.

Use the capability's installer/reference first. The [login installer](game-authentication.md)
returns Webdev configuration without creating a declaration; [leaderboards](game-leaderboards.md#publish-history-and-persistence)
require their board/rules declaration. Preserve existing backend code and declarations when adding
another capability to the same game.

Only when an explicit checkpoint-bound deployment declaration is needed for a backend with no
leaderboard-specific requirements, read the current config and run from the project root:

`node <runtime-directory>/scripts/prepare-backend-contract.mjs --dockerfile <deploy.dockerfilePath> --health-path <deploy.healthPath> --routes '<routes JSON>'`

The config must use a project-relative Dockerfile, a concrete `/api/...` health path without wildcards,
uncached `/api/*` server routing and a final `/*` static fallback. If the helper reports incompatible
config, reconcile the config and actual backend first; this does not mean an existing declaration is invalid.

The helper validates the Dockerfile and creates the existing auth-backend release schema. It
preserves a matching login/leaderboard declaration byte-for-byte, including boards and rules,
and rejects a mismatching or invalid declaration. Reconcile those explicitly; never overwrite them,
invent board rules, or use the helper's generic schema to replace a required leaderboard declaration.

## Prepare, verify and recover

An existing declaration is a bounded, strictly parsed release input, not another editable Webdev config.
Never put secrets in the declaration.
Prepare-release validates and hashes it with the frozen source. Hybrid publication compares the
selected checkpoint's declaration, when present, with the current deployment binding. Invalid
declarations, mismatches and static-only publication of a declared backend are still rejected;
do not remove an existing declaration to bypass them. History reads do not require the declaration.

Follow [Game delivery](game-delivery.md): prepare-release, save-release, push, then verify
`gamePublishReady:true` for that exact SHA before requesting publication. The public error
`publish_contract_missing` with `reasonCode: game_backend_contract_missing` is a legacy server
requirement: verify the active Addon version and refresh readiness after its update. If the server
still requires the file, use the capability-specific declaration and save a new checkpoint; a
workspace-only edit cannot fix an immutable version. For a binding mismatch, restore
compatible current config or prepare a new checkpoint. Never edit old checkpoints or change
applicationKind to bypass validation. Preserve credentials, payment logic and existing game data.

A declaration or ready release does not prove live OAuth, payment fulfillment or leaderboard/database
compatibility. Complete the capability's own checks and report any unobserved online acceptance.
