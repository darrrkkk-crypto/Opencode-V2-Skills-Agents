# Custom diagnostics, recovery and published logs

Read this page for custom server registration, native settings, missing/stale checks,
recovery, published logs or the live version.

## Two different configurations

| Configuration | Purpose | How to change it |
| --- | --- | --- |
| Post-edit registration and routing | Which project files go to which running server connection | Preset startup registers automatically. For your own server, use `webdev.config` at `runtime/post-edit`. Manus stores the registration; do not edit its private storage files. |
| Native server settings file | The server's initialization options and configurable checking behavior | Edit the file reported by startup or referenced by `settings_file`. The client reads it and forwards its values using standard LSP. |

`connection` is the server address. `files` maps exact file names/extensions to LSP language IDs. These belong to routing, not to the native settings file. `settings_file` in the registration is a path pointing to the native settings file. `runtime/post-edit` names the Manus registration/config entry; it is not an HTTP endpoint or an LSP protocol method.

For example, a routing entry with `"files": {".py":"python"}` selects that server for Python file changes and supplies `python` as the document language ID. It does not configure Python's type-checking rules.

Native project files such as `tsconfig.json` are separate: the server/toolchain reads them according to its own documentation. Do not copy their contents into the client settings file unless the server's native protocol configuration requires it.

## Start your own server and register it

Install and start the server in the same execution environment as the MCP client. Expose standard LSP on a loopback TCP connection. If the native server only supports stdio, the generic launcher can provide the transport:

```sh
manus-webdev-lsp start --command /absolute/path/to/server --args '["native argument"]' --project /home/ubuntu/app
```

The custom-command flow starts the process and returns the connection; it does not infer file mappings or native settings and does not auto-register.

Call `webdev.config` with `method: "PUT"`, `path: "runtime/post-edit"`, and a body such as:

```json
{
  "server_id": "my-typescript",
  "connection": {"host": "127.0.0.1", "port": 43821},
  "files": {".ts": "typescript", ".tsx": "typescriptreact", ".js": "javascript"},
  "settings_file": "/home/ubuntu/app/my-typescript.settings.json"
}
```

Use the actual connection returned by your process. When using `manus-webdev-lsp`, preserve its `launch_state_file` in the registration template; this binds automatic recovery to that launcher and canonical project directory. A missing or expired receipt does not invalidate an otherwise usable connection; the result reports reconnect-only recovery instead. Omit `settings_file` when native defaults, launch parameters and project files suffice. The current project supplies the project root. Registration performs the same connection and initialization as preset startup; after registration presets and custom servers use the same client and configuration behavior. PUT creates or updates only the named `server_id`; other registrations remain. DELETE requires `body: {"server_id":"..."}` and removes only that entry. Identical PUT reuses the existing connection.

GET returns `{ "ok": true, "project_dir": "...", "servers": [...] }`. Each server includes its registration plus `registered`, `connection_status` (`ready` or `disconnected`), `configuration_status` (`loaded`, `restart_required`, or `error`), `settings_hash`, and an optional `error`. PUT returns the updated entry directly alongside `ok`. A configuration status of `loaded` describes the client, not an acknowledgement from the language server.

## Native settings and reload

A protocol settings file has two payloads:

```json
{
  "initializationOptions": {},
  "settings": {"implicitProjectConfiguration": {"checkJs": true}}
}
```

This example is for TypeScript's inferred JavaScript projects. Use the selected server's own keys and values. Manus does not translate settings between languages or expand dotted keys. The file wrapper is a Manus storage convention for standard LSP payloads, not a standard LSP configuration-file format.

| Change | Behavior |
| --- | --- |
| `settings` in the referenced file | The client loads valid JSON, notifies the server with `workspace/didChangeConfiguration`, and answers later `workspace/configuration` requests with the new values. Whether a native option takes effect dynamically depends on that server. |
| `initializationOptions` | The client detects the change and reports `restart_required` in explicit status. Restart the server and register its current address; initialization is not repeated on the same connection. |
| `files` through the config interface | Routing changes for subsequent edits; existing document associations/diagnostics are updated accordingly. No server restart is required solely for routing. |
| `connection` | A new connection and initialization are required. |
| Native project files | Follow the native server's reload behavior. |

Presets and custom servers share these rules. File parse errors retain the last valid client configuration and are available through logs/status. A successfully sent configuration notification is not a server acknowledgement that an option was applied.

## Diagnose and recover

Webdev automatically recovers existing diagnostic registrations when a replacement MCP receives the owning project context. It first reconnects; when a launcher-owned session ended with the old MCP, it uses the matching launch receipt to restart the same command and arguments, preserves the settings file, registers the new address, and initializes the client. Do not start a duplicate server merely because the Addon updated. Unscoped installation/health probes do not start project services.

Use `webdev.config` GET `runtime/post-edit` to inspect registrations, connections, loaded configuration state, restart requirements, and errors. To stop intentionally, DELETE the registration or use `manus-webdev-lsp stop --state FILE` with the current `launch_state_file` from GET `runtime/post-edit`. An explicit stop marker or a failed launcher prevents automatic restart; platform SIGTERM/SIGINT and socket loss remain recoverable disconnects. Deleted registrations stay deleted. An external TCP server without a matching launch receipt can only be reconnected. Automatic edits wait at most two seconds for recovery, then report that checking is still pending while recovery continues in the background. A transient recovery failure can be retried by GET `runtime/post-edit`; if recovery cannot complete, inspect status, then start and register the required server. The platform does not install another server or change your native settings.

A newly selected server/setup is verified by an actionable diagnostic on a real source file and its removal after correction. Process startup or protocol readiness alone does not establish checking coverage. When setup validation is needed, use a naturally occurring error or a disposable probe and remove the probe afterward; this is not an extra whole-project acceptance pass. Preserve useful missing-dependency and source-code diagnostics; fix the dependency or code instead of suppressing the diagnostic mechanism.

Act on `check:` findings only when their locations still match the current source. Re-read stale
locations before editing. Duplicate notices are one finding, not a reason for another full run.
Widen the investigation when the same diagnostic persists after a fix or an actual runtime,
build or Preview failure supplies a reason.

Automatic checks return useful Error/Warning diagnostics in the original edit result. No registration, uncovered files, timeouts, busy checks, stale results or other ordinary check failures add no failure reminder; a failed MCP-replacement recovery reports one explicit recovery reminder and do not undo the edit. Absence of a reminder is not proof that checking completed or that the application works. Active start/config/status operations report their actual result.


## Production logs

`webdev.config` with `GET logs` reads the **published deployment**, not the development
process. Query fields are carried in the tool's `query` object:

| Query | Contract |
| --- | --- |
| `type` | `console` (default) or `system`. |
| `limit` | Integer 1–200; default 100. |
| `end_time` | Returned cursor for paging toward older records; supplied separately from the path. |

`console` is application stdout/stderr for the current production deployment. `system` is
build/deploy-phase output, not a runtime lifecycle stream: later restarts, crashes, health
changes, and idle reclamation need not produce system entries.

A response includes `logs`, `has_more`, `truncated`, and a config `revision`; `next_end_time`
appears when an older page is available. Each log entry has `timestamp`, `level`, `text`, and
`truncated`, ordered oldest-to-newest within the returned page. The config revision does not
identify a successfully executed application request or replace the published version.

Entry text is bounded to 2048 UTF-8 bytes and the page text budget is 65536 bytes. The page's
`truncated` flag means text was shortened or older entries were dropped by that budget.
Equal timestamps at a count-limit boundary can make a page exceed the requested count rather
than discard part of that timestamp group. Byte truncation can still lose material at such a
boundary. The supplied `next_end_time` is the paging reference; a guessed timestamp is not an
equivalent cursor, and timestamp plus text distinguishes overlapping records.

A successful empty response can mean the project has no deployment target or no log data.
`not_applicable` identifies a surface unsupported for that deployment/caller, not an
application exception. Availability and response meanings belong to
[configuration](configuration.md); specific codes are indexed in [errors](errors.md).

### Sandbox terminal log interface

The Cloud sandbox also supplies `manus-webdev-logs`. It reads published **console** logs,
not build/system logs, authenticating with the sandbox's platform token and identifying the active project from
`MANUS_WEBDEV_PROJECT_ID` (process environment, then the platform-managed environment file).
It has no project or credential argument. This is a different transport from `webdev.config`:
its default page size is 200, `--limit` changes the count, and the returned `oldest_time`
is passed verbatim to `--end-time` for older records. Its JSON output includes `project_id`, `count`, `entries`,
`has_more`, and `oldest_time`; it does not use the MCP `next_end_time` cursor.
The CLI's presence in a Cloud sandbox does not imply it is installed on a Local computer.

## Identify the live version

When you suspect that published behavior doesn't match the expected checkpoint, ask the platform what is serving: `curl -sS -X POST https://<domain>/__system__/metadata`.
A JSON `{"v","t"}` response gives the full commit hash now live and the time it went live.
Only a POST to the domain root works. GET, HEAD, or any other path fall through to the app (often its HTML with a 200); that is not evidence. A JSON 404 means the domain has no recorded version.
