# Scheduled work (Heartbeat)

Heartbeat is a platform-owned scheduler. Its HTTP trigger targets the published application, independently of the application's process lifetime. Container process lifetime is defined by [container publishing](build-contracts.md#container-build).

When a requirement includes scheduled work, read this contract before implementing its
callback. Include the handler, authentication support, and any required application schema in
the first published code. Deployment-dependent registration and storing a returned task
identity can follow publication; those steps do not inherently require another code build.

## Callback and run lifecycle

The callback is HTTP `POST` to a published URL whose path starts with `/api/scheduled/`. Unlike an intercepted platform route, this prefix reaches the application's handler; [routes](routing-and-responses.md#published-routes) owns routing restrictions.

Cron expressions have six fields (`sec min hour dom mon dow`), use UTC, and have a minimum interval of 60 seconds. Timeout and attempt limits are schedule configuration. A 2xx response denotes success; transport failures and any non-2xx, including 4xx, may be retried when attempts remain. The Dashboard Investigate panel exposes a 500 response body.

A trigger receives a platform cookie only when project deployment status is `DEPLOY_STATUS_SUCCESS` and ticket-issuance prerequisites are satisfied. Otherwise the run can still fire without the cookie; authentication then fails and the run becomes `FAILED`. A scheduled invocation is therefore distinct from an authenticated successful callback.

## Callback identity

The scheduler sends `Cookie: app_session_id=<JWT>`. This is a platform credential, not the application's session format. It is an HS256 JWT signed with the project's `MANUS_JWT_SECRET`. Claims are `openId` prefixed `cron_`, `appId` equal to `MANUS_PROJECT_ID`, `name`, and a two-hour expiry; the standard `sub` claim is unset. Signature, project ID and expiry establish the ticket's authenticity.

`MANUS_JWT_SECRET`, `MANUS_PROJECT_ID`, and `MANUS_OAUTH_API_URL` are platform-provided runtime values. The signing secret remains server-side.
Managed Cloud development and the published deployment receive these values through environment injection; [Local](../worklocally/SKILL.md) owns Local Host loading. Internal `GET env` lists redacted names rather than returning values.

The following identity lookup is HTTP POST with `Content-Type: application/json`:

```text
$MANUS_OAUTH_API_URL/webdev.v1.WebDevAuthPublicService/GetUserInfoWithJwt
{"jwt_token":"<app_session_id>","project_id":"<MANUS_PROJECT_ID>"}
→ {openId, projectId, name, taskUid}
```

Both request fields are required. CamelCase `jwtToken` / `projectId` is also accepted; responses use camelCase. Missing `project_id` yields `400 invalid_argument: project_id is required`; missing JSON content type yields 415. The returned `taskUid` is the authenticated schedule identity. `openId` is the cron identity, not a task UID; callback body fields do not establish that identity.

## Creation and management surfaces

All surfaces manage the same schedule collection:

- Sandbox CLI `manus-heartbeat`: `create`, `update`, `pause`, `resume`, `delete`, `list`, `logs`; it reads its credentials from the sandbox environment.
- Application runtime Connect RPCs on `$MANUS_API_URL/webdevtoken.v1.WebDevService/`: `CreateHeartbeatJob`, `UpdateHeartbeatJob`, `DeleteHeartbeatJob`, `ListHeartbeatJobs`, using [shared API authentication](service-api.md#calling-the-platform-api-surface).
- Project Dashboard: schedule list, run history, pause/resume, and Investigate.

Runtime RPCs accept `x-manus-user-session` carrying the requesting end user's decoded session token. It attributes the schedule to that end user; without it the schedule belongs to the project owner. `created_by` / `created_by_user_id` distinguish creation identity. A schedule created through one surface appears in the others.

Create is subject to per-user and per-project quotas based on the owner's plan; numeric limits are not published in this contract. Over-quota creation returns Connect `ResourceExhausted`. Creation by a cron identity (`openId` prefixed `cron_`) is rejected; that rejection does not apply to ordinary end-user identities.

## Agent schedules

The session scheduling tool can create a schedule that spawns a fresh agent. For authenticated HTTP calls back to the site, that agent receives `SCHEDULED_TASK_ENDPOINT_BASE` and `SCHEDULED_TASK_COOKIE`; the cookie uses the same issuance conditions and identity contract above. This does not grant direct access to application memory or an application database connection.


## Run inspection

Stored run-response bodies are capped at 8 KB. List surfaces have a hard cap of 200 items per page.

`manus-heartbeat logs` omits response bodies unless `--with-body` is used; `--run-uid` details have the same body cap. `list` and `logs` clamp larger `--page-size` values. The CLI does not auto-paginate: `--page` selects the page and `total` reports the collection size. Over-quota create adds `(heartbeat quota for this project / user reached)` to the CLI error.

## Handler implementation and rollout

For a scheduled-handler change, arrange the saved checkpoint, publication and schedule against the version that actually contains the handler. In Cloud this requires publication through the user's Dashboard action or enabled automatic publishing; an unpublished local change does not update an existing production schedule target.

Implement the callback in this order: verify the platform JWT, resolve identity with `GetUserInfoWithJwt`, look up the application's business row by returned `taskUid`, then perform the work and reply 2xx. Persist that task UID on the business row when creating the schedule. Do not select another business record from untrusted callback-body identifiers.

Make the handler idempotent because configured retries can repeat work after transport or non-2xx failures. Return 2xx for an accepted successful invocation, and preserve enough application state to avoid repeated side effects.
Spawn a scheduled agent only when the task needs agentic capabilities such as browsing, research or multi-step work. A one-shot LLM call belongs directly in the handler through the platform LLM API. When a spawned agent must write back, use the site's authenticated HTTP API with its injected scheduling endpoint/cookie pair.
