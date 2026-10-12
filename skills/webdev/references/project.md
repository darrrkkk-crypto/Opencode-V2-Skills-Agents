# Project background for exceptional troubleshooting

Rarely needed background about Manus project internals and historical compatibility. Read only
when a concrete initialization, binding, Sandbox restoration, file-display or compatibility failure
remains unresolved after the current tool's recovery guidance. Read the relevant
section for that failure; do not preload this page for normal development, initialization, environment
inspection or routine successful attach. These facts do not authorize another init/attach operation.

## Initialization and attachment internals

A new Cloud Web project normally uses [web-db-user](../templates/web-db-user/README.md): complete editable application files, initial configuration and installed dependencies. The base users-table migration runs only when a database was selected during initialization. An explicit `template: "flexible"` starts empty without those preparations. Neither flow starts an application process. A Mobile
project has the separate fixed-product contract in [Mobile](../templates/expo/README.md). Local Host binding is
specified in [Local](../worklocally/SKILL.md).

The registered `webdev.init_project` and `webdev.attach_project` tool schemas own their accepted
arguments. Init creates a project; attach binds an existing editable Resource into the current
execution environment. Cloud attach can establish it in a fresh Sandbox. Success returns a
ready project Resource; it does not itself prove an application listener is serving.

In Cloud, an active project withdraws the entry tools. Local may re-attach the same resource
after an authorized directory recovery, as specified in webdev-worklocally. Attach is not an
automatic switch to another website or a generic Git/Preview retry.

Initialization execution identity is derived from the creating Session and original project
name. The recorded request and execution identity constrain replay:

- A valid active or workspace-ready attempt can be reused.
- Completing or completed attempts continue finalization or replay their result.
- The same execution can replace a failed or expired attempt on its original Resource.
- A different name creates a different execution and cannot bypass the Session's existing
  failed-project boundary. Other argument changes can conflict with the recorded request body.
- An active binding separately prevents entry, even if a caller is considering an init retry.

The initialization state and the availability of the registered entry tool are separate facts.

## Sandbox restoration and delayed file views

The returned Resource and absolute `project_dir` identify the active local workspace in the
Cloud Sandbox. Edit the project in that directory. Frontend code and asset views use an
asynchronous display mirror; their update can lag behind a successful local file write.
Save changes to the canonical Git remote through the existing checkpoint workflow. Sandbox
replacement can restore the saved Git version and recorded external assets, but not local
changes that were never saved remotely.

Keep source code and project-defining files in `project_dir`. Dependencies, build outputs,
and caches use ordinary local filesystem behavior. Keep installed dependencies and secrets
out of Git. The platform manages frontend display synchronization; do not upload files or
change storage configuration merely because the Code or Assets view has not refreshed yet.
A display synchronization failure does not require moving the project or stopping local edits.

After a Sandbox reset, continue in the restored project directory. The saved Git version is
the code recovery source; frontend mirror contents are not a backup to copy over local work.

## Cloud image provenance for tool/version failures

The Cloud image definition provides outbound development tooling and passwordless `sudo`.
Its current declared toolchain inventory is below; an existing Session's actual selected image
and executable versions are authoritative for that Session, not a version inferred from this
page. The inventory does not describe a Local computer or a published build machine.

| Toolchain | Image-definition supply |
| --- | --- |
| Node.js | Default `NODE_VERSION=v22.13.0`; `npm`/`npx`; globally installed `pnpm` and `yarn` whose versions are resolved at image build |
| Python | Python 3.12 default; `pip` and `uv`/`uvx` |
| Go | Go toolchain copied from the Go 1.26 build image |
| Java | Base image installs the `default-jre` package |
| Rust | Rustup-managed toolchain, currently pinned to 1.97.1 with `rust-src`, `clippy`, and `rustfmt` |
| MySQL | Base-image client package |

This is a positive inventory, not an assertion that every unlisted runtime or a JDK is absent.
A populated package cache does not mean the project has installed dependencies. Application
listeners, Preview, and runtime configuration belong to [runtime](runtime.md) when those facts
are needed; the inventory selects no application language or framework.

When supplied, `MANUS_APP_TITLE` and `MANUS_APP_LOGO` are the project's public title/logo
metadata. They are not authentication credentials. Their presence is distinct from application
code choosing to display them.

## Initialization, attach, and restoration

The registered `webdev.init_project` and `webdev.attach_project` tool schemas own their accepted
arguments. Init creates a project; attach binds an existing editable Resource into the current
execution environment. Cloud attach can establish it in a fresh Sandbox. Success returns a
ready project Resource; it does not itself prove an application listener is serving.

In Cloud, an active project withdraws the entry tools, except that legacy migration keeps same-project attach retry available until its runtime handover is confirmed. Local may re-attach the same resource
after an authorized directory recovery, as specified in webdev-worklocally. Attach is not an
automatic switch to another website or a generic Git/Preview retry.

Initialization execution identity is derived from the creating Session and original project
name. The recorded request and execution identity constrain replay:

- A valid active or workspace-ready attempt can be reused.
- Completing or completed attempts continue finalization or replay their result.
- The same execution can replace a failed or expired attempt on its original Resource.
- A different name creates a different execution and cannot bypass the Session's existing
  failed-project boundary. Other argument changes can conflict with the recorded request body.
- An active binding separately prevents entry, even if a caller is considering an init retry.

The initialization state and the availability of the registered entry tool are separate facts.

## Blueprint records and plan-file provenance

The compact Cloud Blueprint route stores structured content in platform operation state
(`operation.requiredInput.plan`), then the confirmed `blueprintResult`, and wakes the Agent.
That branch itself has no file-submission step; it must not be represented as an automatically
created project `plan.md`.

When a request's main features do not fit in the card's 10 items, no card or Blueprint record is
created: there is no confirmed feature list, design style or power-up selection. Scope then comes
from the user's request and what is agreed in the conversation.

Local initialization and attachment do not precreate a plan file. Keep design decisions in
the actual implementation plan when one exists; reuse approved requirements and design for
small changes without introducing a separate design document.

## Failure codes and retry state

MCP-specific failures are carried in `structuredContent.webdev_error`. The exact `code`,
`retryable`, optional `recoveryAction`, and optional `failedStage` describe the failed operation;
these are not the config-plane's `error.field_errors` rows.

| Code or state | Meaning |
| --- | --- |
| `runtime_step_failed`, `retryable: true` | The attempt is held; the same registered operation can resume it. `recoveryAction` is `retry`. |
| `runtime_step_failed`, `retryable: false` | That attempt has been released, not merely classified as a transient service error. For init, the unchanged original request can recover the same execution through a replacement attempt; the current tool result supplies its bounded recovery text. |
| `sandbox_already_bound` | The environment is already bound to another Webdev project. No new project was created; the rejected init attempt is released. |
| `attach_unavailable` | Active binding has withdrawn the named entry operation. `unavailableTool` can identify init or attach. |
| `project_init_failed` | The Resource is currently failed and unavailable to ordinary project operations. This alone does not rule out same-execution initialization recovery. |
| `resource_session_conflict` | The requested operation conflicts with the Session's existing project/execution boundary. |
| `binding_replaced` | The binding used by the operation is no longer current; it is not a request to re-attach that active environment. |
| `runtime_not_ready` | Initialization or attachment has not established a ready runtime for that operation. |
| `managed_feature_disable_unsupported` | The capability transition is refused by the [feature contract](features.md). |

`failedStage: workspace_directory_conflict` means the requested new-project directory is occupied.
Preserve and move that directory aside, then retry with the original init/attach arguments;
do not change the project name or keep retrying before resolving the directory conflict.

A valid `boundResourceUri` may identify the existing project for a binding rejection. It is an
optional, validated result field, not an identifier inferred from an error string. Other public
codes are indexed in [errors](errors.md).

An attach `internal_error` can include `failedStage` and bounded system-error, process-exit,
or signal details. Unknown details are omitted; the raw exception is not an instruction or a
root-cause finding. Those details do not change `retryable`/`recoveryAction` or establish that an
init attempt was held or released. Its registered recovery text allows one retry of the same
operation with unchanged arguments; it does not authorize replacing the binding or starting an
unrelated operation. A failed operation has not become successful because a separately probed
local port answers.

`failedStage` uses this closed vocabulary; it does not mean every operation runs every step:

```text
mount, workspace_directory_conflict, materialize_template, install_dependencies, sync_database_schema,
sync_code_snapshot, git_credentials, git_push, reuse_initial_version,
start_dev_server, register_endpoint, preview_port_mismatch, ingress_health_check,
screenshot, bind_runtime_project, bind_workspace_runtime_project, window_init,
local_init, workspace_init, validate_request, begin_attach, mount_workspace,
hydrate_workspace, read_workspace_head, record_workspace_binding, complete_attach,
build_receipt
```

## Legacy configuration and version mismatches

Older stored declarations may still expose retired fields so they can be removed. `deploy.port` is retired. Old overrides are omitted from the active configuration view; publishing uses the existing Dockerfile/platform port behavior. New writes
cannot add or preserve `gateway`, `workers`, `queues`, `kv`, `mobileBuild`, `storage`, `email`,
or `alerts`; retired feature names include `kv`, `devDatabase`, and `mobileBuild`. Redirects
and per-route response-header declarations are also retired. Their presence can block publish
with `publish_contract_missing` / `phase1_domain_not_available`. A readable old field is not a
currently supported capability.

There is no local `webdev.json`, `webdev.config_save`, or `webdev.config_view` mechanism.
The external HTTP `_list` catalog is not an internal MCP endpoint. Old names found in a project or historical response do not re-enable removed interfaces.

`upgrade_info` means the serving contract is newer than the supplied skill version. Its absence
is not a health result: versions may match, or the caller may be newer during rollout.
On `upgrade_info`, prefer the serving result's guidance and tell the user this skill needs an
update. Check the version signal; absence alone is not a success or health check.

## Why an attach summary omits a configured command

`command_configured` without `command` means arbitrary shell text was omitted from the attach
summary for safe display, not that the build is missing. The summary includes only selected
configuration fields and existing file locators, not full file contents. Use the current config
or project scripts if the operation needs a missing value; do not reinitialize or invent configuration
because a summary omitted it. Build commands describe publication builds, not development startup.
