# Development runtime and Preview

This page owns the development runtime and Preview connection contract. These settings do
not select a language, framework, or published deployment shape. General configuration
responses are described in [the configuration API](configuration.md) when needed.

## Runtime behavior

The Preview window targets an HTTP process on the active development port. A ready project
Resource does not mean a process is listening. The platform does not start or restart the
application after a runtime declaration; a resident application process remains running until
it exits or its execution environment stops. Its running job state is not a completed check.
There is no `runtime.devCommand` field. Choose the port for the actual application, rather
than forcing 3000. Start the process yourself; after changing its port, restart it with the new
listener settings so Preview can reach it.

In Cloud, the process must listen on `0.0.0.0` at the declared port so the platform ingress
can reach it. In [Studio](../worklocally/SKILL.md), use the same `webdev.config` GET config and
PUT config/runtime calls; only `runtime.port` is overridden in Session-local state. Other runtime
fields remain project-owned and cannot be modified by this Studio call. Listen on `127.0.0.1`
at the declared port. Other configuration domains remain project-wide.
The fixed Mobile starter uses its [Expo README](../templates/expo/README.md); current returned state is authoritative.

## `runtime` schema

`PUT <config-plane>/config/runtime` takes `{"runtime": {...}}` and replaces the complete
runtime domain. `port` must remain present; in Cloud, omitted optional fields are removed.

| Field | Contract |
| --- | --- |
| `port` | Required integer, 1024–65535; the primary development HTTP port. It is independent of the published container's port, which follows the Dockerfile/hosting platform convention. |
| `endpoints` | Optional array of 1–4 named extra ports, with the entry rules below. Omit the array when there are none. |
| `post_edit` | Managed by LSP registration. Preserve its stored value when replacing runtime configuration. |

The reserved ports for both `port` and `endpoints[].port` are **5900, 5901, 8328, 8330,
8340, 8350, 9222, 9330, 19780, 50031**. Validation and runtime loading enforce this boundary.

Each endpoint has only `name` and `port`:

- `name`: `^[a-z](?:[a-z0-9-]{0,30}[a-z0-9])?$`; unique within the array.
- `port`: integer 1024–65535; unique within the array, not reserved, and different from
  `runtime.port`.
- `preview` and `primary` are built-in names and cannot be declared. `preview` resolves to
  the stable Web Preview origin; `primary` resolves directly to the current main dev port.
- Named endpoints resolve their current public origins; they do not allocate another stable
  Preview proxy slot. Runtime replacement may change the resolved origin.

If a write reports `runtime_sync: failed`, do not start against the new values yet. Inspect the
stated cause, correct it when specific, then make one `GET config` call to retry loading the
stored revision. Require `applied` or `noop` before continuing with that new runtime contract;
if it still fails, report the unresolved cause instead of claiming the new values are active.
Previous active values remain in effect until loading succeeds.
The complete receipt semantics are in [configuration](configuration.md#stored-and-active-state).

### Vite arguments through pnpm

When pnpm forwards flags to a Vite script, pass them directly, for example
`pnpm dev --host 0.0.0.0 --port 3000 --strictPort` with the actual declared port. Do not insert
a standalone `--`: Vite can ignore the following host/port flags and fall back to 5173.
Confirm the actual listener against the configured port rather than assuming the command
line selected it. This is a Vite/pnpm invocation pitfall, not a requirement to choose Vite.

## LSP diagnostics

In Sandbox, the host manages language-server processes for registered project directories.
Use `webdev.config` at `runtime/post-edit` to inspect or select project languages; do not start
another server. Local Device execution retains agent-managed native servers and settings.
[Diagnostics](diagnostics.md) owns custom routing, native settings and recovery.
Registration manages `runtime.post_edit` internally; preserve it when replacing an existing runtime domain.



## `preview` schema and current connections

`PUT <config-plane>/config/preview` takes `{"preview": {"device": {...}}}`. A declared
`preview` requires `device`; an empty object is invalid. Omitting the optional domain clears
its custom connection metadata, not the ordinary Web Preview.

| Field | Contract |
| --- | --- |
| `device.connect` | Required string, 1–500 characters, containing at least one supported endpoint placeholder. |
| `device.openWith` | Optional display metadata. |
| `device.openWith.name` | Required when `openWith` is present; trimmed nonempty string, at most 50 characters. |
| `device.openWith.ios` / `android` | Optional HTTPS URLs, at most 500 characters each. |

Supported placeholders are `{host:NAME}`, `{url:NAME}`, and `{url_encoded:NAME}`: respectively
the current origin's host, full origin, or URL-encoded origin. `NAME` must be a declared
runtime endpoint or the built-in `preview` / `primary`. Braces outside a valid placeholder,
unknown names, and a literal-only connection string are rejected. `openWith` is display
metadata; the platform does not interpret the target application's protocol.

`GET config` can include derived `runtime_endpoints`, `preview_origin`, and `preview_device`
fields. They describe the current binding and are not stored config fields or values to copy
back into a declaration. Endpoint templates are resolved again after runtime replacement.

## Public Preview versus direct development access

Cloud Preview embeds the application in a cross-site iframe. `X-Frame-Options: DENY` or
`SAMEORIGIN`, and a Content-Security-Policy `frame-ancestors` restricted to `none` or `self`,
reject that embedding. An explicit ancestor allowlist must include the actual Dashboard
ancestors; the application and Dashboard do not share an origin.

The public browser origin differs
from the internal Host delivered to the application, which can be `127.0.0.1:<port>`.
The 8328 Preview ingress forwards the application's `Authorization` and `Cookie` headers, while
rebasing Host to the internal listener. A request-derived server origin is therefore not a
reliable public application origin; published ingress has its own forwarding behavior too.

Root-relative application URLs do not depend on that internal Host. The browser's actual
origin is available as `window.location.origin`; server-generated public URLs need an explicit
public origin. A direct request to the dev port bypasses the Preview ingress. Sandbox screenshots
also cannot establish the browser-facing public origin or its header behavior. Embedded login
and application identity constraints belong to [authentication](authentication.md).
