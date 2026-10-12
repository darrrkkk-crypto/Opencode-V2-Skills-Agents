# Error handling and recovery

Use the concrete action for the returned code, including its retry limit and stop condition.
A code definition or a linked schema alone does not complete failure handling. Shapes and transport are owned by [the config plane guide](configuration.md);
per-domain rules live on the domain pages this catalog links.

A rejected call stores no configuration unless a row below says otherwise. **"Stored
nothing" is not the same as "changed nothing":** a `secret_values_required` rejection leaves
a pending input card behind that can block conflicting writes — read that row before you conclude a
refused call was a no-op. Codes appear on two
levels of the error envelope — `error.code` (the envelope code) and
`error.field_errors[].code` (one entry per offending field, with its `path`).

**How complete `field_errors` is depends on which kind of call was rejected**, and the
difference decides whether one round trip is enough:

- **Query parameters** (`GET <config-plane>/logs`) — every offending parameter of that call
  is listed. Fix them all in one edit; a second rejection means you introduced something new.
- **Request bodies** (the config writes) — the list is capped at the first few offending
  fields. Fixing exactly what was named can still be rejected again with a different field,
  which is normal progress, not a loop: each round names real work. Re-read the whole
  declaration against the domain page when the second rejection surprises you, rather than
  fixing one field at a time.

## Before retrying

For an external HTTP call, branch on non-2xx status before `ok`; an omitted `ok` is not success.
Read `reason_code` before applying a generic revision-conflict recipe. Use only bounded retry:
follow a returned retry window, and where this table says once, stop after that one retry and
report the exact requestId and safe diagnostic. Do not retry a permission, unsupported-route,
or terminal-version error unchanged. Never distribute requests across keys/processes to evade
rate limits. Keep credentials and user data out of reported errors.

[Configuration](configuration.md#handling-a-rejected-operation) owns common field-error and
write-state handling. An actual user-input card requires waiting; a non-blocking Stripe claim
status does not. Do not infer either solely from the presence of action_url.

## 1. Envelope codes (`error.code`)

### Platform-wide codes

| Code | Fix |
| --- | --- |
| `unauthenticated` | the call carried no usable credential; authenticate and repeat |
| `reauthorization_required` | the authorization expired mid-flight; refresh it (in a session this is automatic on the next call), then repeat |
| `permission_denied` | this identity cannot do this on this project; do not retry — use the owner path the `note` names |
| `resource_not_found` | Check the actual project/resource identifier and caller access. First distinguish an external `endpoint_not_available` reason; do not change project ids to work around an unserved route. |
| `validation_failed` | the body broke the typed contract; fix exactly what `field_errors` names and resubmit |
| `revision_conflict` | the config moved under you; `GET <config-plane>/config`, reapply only the intended change to the fresh `revision`, preserving concurrent fields, resubmit — **but check `error.reason_code` first and follow §1c when it is present**: with `secret_input_in_progress` nothing moved under you at all and rebasing can never succeed |
| `database_record_conflict` | a database row write hit an existing row on a unique or primary key. Its own code, never a `revision_conflict`: nothing moved under you and re-reading changes nothing, so do not loop. Send a different value for the taken column, or update the existing row instead |
| `secret_input_pending` | a secure value input card is open. When `pending_secret_input.blocks_config_writes` is false, unrelated Web domain updates can proceed; conflicting keys, dependent changes and whole-document replacement must wait. True means a legacy candidate blocks all config writes. Rebasing and resubmitting can never clear it, so do not loop: the `note` names the keys the card is collecting. Use the appropriate owner input surface; an external operation URI is not a public link. Two exits — the user completes (or cancels) the card, or you drop the half-finished declaration with `DELETE <config-plane>/secrets/<NAME>` for one of those keys ([config/secrets](secrets.md)) |
| `secret_value_already_set` | the key already holds a value and values are never overwritten in place. Its own code, never a `revision_conflict`: rebasing and resubmitting can never clear it, so do not loop. Redeclare the key with `revision + 1`, then submit the new value for that declaration ([config/secrets](secrets.md)). Storing the value already stored is a no-op answering `200`, so this code always means the value you sent differs |
| `idempotency_conflict` | For an independent operation whose contract permits a new request, use a fresh operation identity instead of reusing a key with different input. For project initialization, keep the original Session/name and frozen input: changing the key/name cannot bypass that execution or binding. Follow its typed recovery or report the conflict. |
| `publish_contract_missing` + `reasonCode: game_backend_contract_missing` | The selected Godot hybrid checkpoint has no backend declaration. Follow the [Godot backend recovery](game-backend.md#prepare-verify-and-recover), then prepare and save a new checkpoint. Do not change credentials or retry the old version. |
| `publish_contract_missing` | Read the applicable [static](build-contracts.md#static-build) or [container](build-contracts.md#container-build) contract, declare the missing build/deploy fields, then publish again. A server with build output still needs deploy for hybrid publication. |
| `required_secret_missing` | publish is blocked until every declared secret has a value; collect the named keys, then publish again |
| `no_checkpoint` | nothing has ever been pushed; create a checkpoint (accepted push) before publishing |
| `git_state_conflict` | the checkpoint does not match canonical main; refresh project state before retrying |
| `publish_confirmation_required` | the current canonical main commit has no checkpoint; the Dashboard must ask the user to confirm before saving and publishing that exact commit — never confirm on the user's behalf |
| `publish_unavailable` | Make the project repository usable through its permitted initialization/recovery path before publishing; retrying the unchanged publish cannot repair it. Report when recovery is unavailable. |
| `local_first_mobile_unsupported` | managed Mobile requires Cloud; disclose the Cloud move and obtain the user's choice before switching. A plain-local choice skips Addon init/attach |
| `binding_replaced` | Do not re-init or re-attach. After the next runtime reconcile, retry the failing operation once; if it persists, report the failure and returned requestId. |
| `not_attached` | First use the currently registered project entry appropriate to a new or existing project, only in an unbound execution environment. Respect withdrawn entry tools and the current binding; do not invent another attach/init route. |
| `runtime_not_ready` | the project runtime is not ready yet (initialization or attach still in progress); continue the task and retry the same operation shortly — never re-attach |
| `project_init_failed` | Stop retrying the ordinary failing operation. In the creating Session, the unchanged original project name/request may recover the same failed/expired execution only when its registered entry remains available and the current recovery permits it. Otherwise report the failure; never change the name/key or bind again to bypass it. |
| `attachment_required` | Bind through the correct available new/existing-project entry first; do not use attachment as a switch or repair of an already-bound environment. |
| `resource_session_conflict` | this session already has its one project; keep working in it or ask for or use a separately authorized new session |
| `canonical_changed` | Refresh current canonical/binding facts and restart the intended Git operation against them. Do not re-attach an active project or push to the obsolete repository. |
| `checkpoint_restore_required` | Keep GitHub connected and report that the latest accepted checkpoint must first be restored to Manus. Do not substitute an older session copy or copy GitHub history to bypass the block. |
| `history_diverged` | the canonical GitHub repository diverged from project history; resolve manually before retrying |
| `unsupported_branch` | only `main` is supported as the canonical branch |
| `unrelated_history` / `github_repository_not_empty` | the target repository has content that cannot be adopted; pick an unused name and start a new Create request |
| `github_connector_required` / `github_installation_required` | the owner must connect GitHub / grant the Manus GitHub App first |
| `github_repository_forbidden` / `github_unauthorized` / `github_repository_detached` | access to the canonical repository broke; the owner restores access to the original repository, then retry |
| `github_repository_conflict` | the repository name is taken; pick another |
| `github_unreachable` | GitHub is temporarily down; retry later |
| `self_config_not_managed` | this project has no managed config plane; nothing to declare against |
| `config_revision_required` | an applied config revision is required and none exists; declare the config first, then retry |
| `cursor_expired` | the event cursor aged out; resume from a fresh resource snapshot |
| `lease_expired` | a pending browser-side confirmation expired before submission; calls through this API do not normally produce it — if ever seen, report the failure instead of retrying |
| `filesystem_rebind_required` | the filesystem binding predates the current contract; continue the project in a new task |
| `owner_unavailable` | the platform side is temporarily unavailable; retry later (bounded), report the `requestId` when it persists |
| `rate_limited` | slow down; retry after the reported window |
| `internal_error` | an internal operation failed; use any returned safe diagnostic, retry once, then report the failure with its `requestId` verbatim when one is provided |
| `legacy_project` | the project predates the managed config plane, so managed-plane operations refuse it — do not retry; manage it through its legacy Dashboard surfaces |
| `managed_project` | the project is managed by the config plane, so the legacy save surface refuses it — do not retry; operate through the managed plane (this API or the Dashboard managed surface) |

### Config-plane routed codes

| Code | Fix |
| --- | --- |
| `secret_values_required` | not an error to fix: the write waits on the user — the secure value input card is already open; stop and wait ([config/secrets](secrets.md)). Completing the card applies the pending declaration. Repeating a completed replacement request may open another card; follow the replacement rules in [config/secrets](secrets.md). **This rejection is not a no-op**: the declaration is not stored, but the card can block conflicting writes with `secret_input_pending`; `blocks_config_writes: false` allows unrelated Web domain updates — the response's `pending_secret_input` carries the card and its `unblock` action ([config/secrets](secrets.md)) |
| `confirmation_required` | not an error to fix: the write waits on the user's confirmation card (GitHub repository creation); stop and wait. Completing the card applies the original request; read the current configuration rather than submitting it again |
| `live_apply_failed` | the `apply: "live"` request failed and **nothing was stored**; repeat the request to retry, or drop `apply: "live"` to store for the next publish |
| `not_applicable` | this endpoint does not serve this caller or this project state (e.g. the `runtime` domain outside a sandbox, or `GET logs` on a project with no live server deployment); use the path the `note` names |
| `requires_membership` | the declared capability is a membership feature. On a `hosting` save: nothing was stored — keep the default or suggest the plan upgrade ([hosting](hosting.md)). On a publish (top resources tier): the tier **is** stored and only the publish was refused — re-`PUT` a lower `resources` tier to roll back, or suggest the upgrade |
| `github_canonical_active` | the canonical repository is on GitHub, so this Manus-hosted-only endpoint refuses; publish from the Dashboard / push to GitHub instead |
| `version_not_found` | the requested version anchor is not in this project's version history — terminal for that id; list the published versions first, then retry with an existing one |
| `version_source_unavailable` | this version's source can no longer be rebuilt — terminal for that version; roll back to a different version from the history |

### 1c. `reason_code` on a 409

A 409 envelope may carry `error.reason_code`, turning it actionable:

| reason_code | Meaning / move |
| --- | --- |
| `secret_input_in_progress` | a secure value input card is open. On config writes it rides the `secret_input_pending` envelope above. **One surface still pairs it with `revision_conflict`: enabling the Stripe integration.** There the envelope code is misleading and the generic `revision_conflict` move — re-read, rebase, resubmit — cannot work, because nothing moved under you: branch on this `reason_code` before the envelope code, and take the card's two exits instead |
| `feature_reconcile_in_progress` | a features provisioning pass is mid-flight; repeat shortly |
| `confirmation_cancelled` / `confirmation_expired` | the card ended without applying; re-declare only if still wanted |
| `integration_not_available` | the integration cannot be enabled (disabled on the platform); do not retry |
| `provider_unavailable` | the provider side is down; retry later |
| `publish_required` | external Stripe enable needs a successful Published URL for the sandbox webhook. Implement `/api/stripe/webhook`, checkpoint and publish, then retry enable ([Stripe](payments.md)) |
| `publish_state_unavailable` | external Stripe enable could not read the deployment facts; retry the lookup later. Do not translate it into `publish_required` or publish again blindly ([Stripe](payments.md)) |
| `runtime_apply_failed` | Inspect the stated apply cause and correct it. If the desired revision is already stored, GET config to retry loading it; otherwise repeat the failed operation only as its typed recovery permits. Do not replay a completed replacement or continue against unapplied new values. |


## 2. Field codes (`error.field_errors[].code`)

Almost always under a `422 validation_failed` envelope. `requires_membership` above answers at
the envelope level instead.
Groups by origin:

### Schema codes (declaration rules)

- `routes_*` — 8 codes owned by [routes](routing-and-responses.md#published-routes) (rule count, reserved/duplicate/
  unreachable paths, lane prerequisites, and server-cache bounds and static-only SPA fallback).
- `hosting_empty`, `hosting_idle_minutes_conflicts_always_on` — owned by
  [hosting](hosting.md); a `hosting` declaration without `mode` answers the plain
  `required` field code on `hosting.mode`.
- `diagnostics_language_required` / `diagnostics_language_unknown` /
  `diagnostics_server_redefines_builtin` / `diagnostics_servers_too_many` /
  `diagnostics_languages_too_many` / `diagnostics_settings_too_many_keys` /
  `diagnostics_settings_too_large` — the `runtime.diagnostics` rules; use the complete [runtime](runtime.md) schema and correct the named declaration.
- `resources_needs_deploy` / `resources_tier_invalid` — declare `deploy` first / use one of
  the exact tiers ([hosting/resources](hosting.md)).
- `build_cache_needs_container` — the top-level `buildCache` controls the container image
  build cache; it needs a `deploy` contract (container or hybrid shape) to act on.
- `build_output_directory_not_canonical` / `deploy_dockerfile_path_not_canonical` — spell
  the path canonically (no `./`, `//`, trailing `/`).


- `endpoint_name_reserved` / `endpoint_name_duplicate` / `endpoint_port_reserved` /
  `endpoint_port_duplicate` / `endpoint_port_conflicts_runtime` — the `runtime.endpoints`
  rules: names are unique lowercase slugs (`preview` and `primary` are built-ins you cannot
  claim), ports are unique, stay off the platform ports (5900, 5901, 8328, 8330, 8340, 8350, 9222, 9330, 19780, 50031),
  and must not repeat `runtime.port` — the main port already has the built-in
  `{url:primary}`; declare only extra ports.
- `device_connect_template_invalid` / `device_connect_placeholder_required` /
  `device_connect_unknown_endpoint` — `preview.device.connect` accepts only
  `{host:NAME}`, `{url:NAME}`, and `{url_encoded:NAME}` placeholders, requires at least
  one, and each name must be a declared runtime endpoint or the built-in `preview` or `primary`.
- `needs_server_true` — store [features.server](features.md) as true before the dependent domain write, or include both in a valid whole-document update; do not retry the unchanged dependent write.
- `phase1_domain_not_available` — a stored pre-GoLive declaration still carries a retired
  domain, feature flag, or redirect/headers route. Reads stay available so it can be removed,
  but publish answers `409 publish_contract_missing` until the retired field is gone; do not
  retry unchanged.
- `integrations_mutually_exclusive` — Shopify/Stripe integration conflict.
- `stripe_integration_required` — never hand-write the three fixed Stripe keys; declare
  `integrations: ["stripe"]` instead ([Stripe](payments.md)).
- `database_url_reserved` — `DATABASE_URL` belongs to the managed database: for a server project that has not enabled its managed database, explicitly keep
  `database: false` before declaring your own DSN; otherwise remove the conflicting secret
  declaration and use the managed database. Do not try to disable an already-enabled database
  ([managed database](database.md)).

### Transport codes (request shape, checked before the engine)

`required`, `unknown_field`, `invalid_json`, `invalid_format` (malformed secret name),
`invalid_value` (e.g. `apply` other than `"live"`) — fix the body/path literally and
resubmit.

### Settlement codes (secrets and features)

- `secret_revision_invalid` — new declarations carry `revision: 1`; a replacement is exactly
  `+1` ([config/secrets](secrets.md)).
- `value_too_large` / `required` — the submitted value is over the size cap / empty.
- `managed_feature_disable_unsupported` / `invalid_value` on `features.*` — a managed
  capability cannot be turned off; keep it declared or, when the user wants a separate project, create one through its supported new-project entry. Do not rename/re-init inside an already-bound Session to bypass the refusal.
- `stripe_key_shape_invalid` / `stripe_key_rejected` / `stripe_key_check_unavailable` — the
  owner-supplied Stripe key is malformed / rejected by Stripe / unverifiable right now
  ([Stripe](payments.md)).
- `database_url_reserved` — the BYO `DATABASE_URL` declaration and the managed database are
  mutually exclusive; the save is rejected whichever side arrived second
  ([managed database](database.md)).

### Zod-native codes

`invalid_type`, `invalid_literal`, `invalid_enum_value`, `invalid_string`, `invalid_union`,
`unrecognized_keys`, `too_small`, `too_big`, `required` (a missing required field), and
`custom` (a rule without its own code). The `path` names the field; compare it against the
domain page's shape and fix the literal value.

## 3. Model-only codes (MCP tool results)

These appear only in a session's `webdev_error` tool-result facts, never on the HTTP
envelope:

| Code | Move |
| --- | --- |
| `runtime_step_failed` | Use `failedStage` and the typed recovery. `retryable: true` resumes with the same registered tool. `false` releases that attempt; original-execution init recovery is conditional, not a fresh-name workaround. Do not probe ports to bypass the failed operation or report success |
| `sandbox_already_bound` | this sandbox already hosts a webdev project; continue on it, never retry init |
| `attach_unavailable` | the entry tools are withdrawn because a project is already hosted here; keep working on it — re-attaching degrades the binding |
| `managed_feature_disable_unsupported` | same meaning as the field code above, surfaced as its own code on the tool result |

An attach `internal_error` may also include `failedStage` and fixed text containing a
finite system error code, process exit code, or signal. This does not change its error
code, `retryable`, `recoveryAction`, or one-retry limit, and does not imply that an attempt
is held or released. Retry the same registered operation once with unchanged arguments;
if it fails again, report the failure instead of starting a new operation or improvising
a workaround. Unknown details remain omitted; a stage or errno alone is not a root cause.

Only if the current error guidance leaves the operation state unresolved, consult
[project background](project.md#failure-codes-and-retry-state) for the complete `failedStage`
vocabulary and initialization-state conditions. A stage/errno alone does not authorize a new binding.

## 4. Platform-local (Biz) surfaces

Some endpoints are answered by the platform locally and use its own error grammar, not the
config-plane envelope: the file-storage object endpoints (`storage/objects` / `storage/presign` /
`storage/delete` — their rejections answer `object_not_found` for a missing object, and
`storage_key_invalid` for a malformed key; [assets and storage](storage.md)),
the schedules group (its code table lives in [scheduled work](scheduled-work.md)),
project custom-domain management, and publish
progress (`failure_stage` values on the deploy status). Their rejections name the fix in
the response itself; this catalog does not duplicate them.
