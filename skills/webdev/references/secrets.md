# Protected values and secret declarations

This page owns per-key declarations, values, revisions, and environment delivery. General
card completion, waiting, locks, and response envelopes belong to
[configuration](configuration.md). Follow its first-use and operation prerequisites;
when the current complete contract is already in context, do not reread it unnecessarily.

## Value boundary

A declaration contains key metadata, never a protected value. Values are supplied directly
through the registered user input surface and are not returned in model-visible config
responses.
Do not ask users to disclose values in chat or copy them into source/config files, Git,
logs, screenshots, or tool output.
Platform injection does not create `.env` or `.env.example` files.

The registered `webdev.request_secrets` tool requests new or replacement values and chooses
each key's declaration revision from current state. Its optional per-key `value` prefills the
card only when the user has already explicitly supplied that value in chat. The user must
confirm before it is saved; never retrieve stored credentials to fill this argument. `value`
does not replace an existing stored value: also set `replace_existing=true` when the user
supplies a new value to replace it. `GET env`
inside the sandbox provides redacted key names, not values.
Actual values are available to application processes through their environment.

Only pass top-level `environment` when the user explicitly specifies Development (`dev`) or
Production (`production`). Otherwise omit it so the user can choose in the input card; do not
pass `all` or `null`. A call requests at most 12 keys for one user-selected or explicitly
requested environment; the project still permits at most 64 declared keys. When the user
explicitly requests different development and production values, use sequential calls,
waiting for each card to settle. Existing secure Connector candidates are
available within the card for keys without a supplied `value`. Omit `value` when it is unknown;
never ask the user to paste a credential in chat. Do not repeat the value in messages, files,
logs, or other tool arguments.

## Declaration schema

`PUT <config-plane>/secrets/<NAME>` takes a strict metadata object:

| Field | Contract |
| --- | --- |
| Key in the path/map | Matches `^[A-Z][A-Z0-9_]{0,127}$`; at most 64 declared keys per project. |
| `description` | Optional; if supplied, trimmed nonempty string of at most 500 characters. |
| `revision` | Optional positive integer; omission has the effective value `1`. This is a per-key revision, not the config envelope's revision. |

No `value` field is accepted in a declaration. A description containing a credential literal
(an `sk-` token followed by at least 16 `[A-Za-z0-9_-]` characters, or a PEM private-key header)
is rejected. The protected input value itself must be nonempty and at most **16 KiB**.

Every declared key is required: publishing with an unavailable declared value fails with
`409 required_secret_missing`. Exceeding the key cap rejects the whole declaration.
A new secret-input candidate cannot be combined with unrelated non-secret changes in a
whole-config import (`secret input candidate must be saved separately`).

## Target environments

Values have independent `all`, `dev`, and `production` target rows. An `all` row supplies either
environment only when that environment has no exact row; saving `all` never removes a scoped
override. `replace_existing: true` applies only to an existing row for the requested target, so
an `all` fallback must not suppress a request for an explicit `dev` or `production` value. A
production-only card can complete without a development value, including when the user chooses
Production in the dropdown. With no explicit environment and no replacement intent, an existing
`all` value satisfies the request; a scoped value alone does not imply the user
wants that scope. Replacing a stored value in the user-selected environment still requires
`replace_existing: true`.

`GET config` leaves the declaration metadata in `config.secrets` unchanged. Its separate
top-level `secrets` metadata map never contains values. `configured_environments` is the only
value-presence field: it lists the stored `all`/`dev`/`production` rows, or `[]` when none exists.
Development can use `all` or `dev`; production can use `all` or `production`. Neither implies
that a requested override already exists: check the exact target scope for that.

## Per-key replacement and withdrawal

- A new key's effective declaration revision must be `1`.
- Keeping its revision retains the stored value; changing description alone does not open
  value input.
- Replacing a value requires exactly the previous revision **plus one**. Other jumps are
  rejected as `secret_revision_invalid`.
- Values are not overwritten in place. Submitting the already-stored value is a 200 no-op;
  submitting a different value for that same declaration returns
  `409 secret_value_already_set`. A fresh config read does not change that per-key condition.
- `DELETE <config-plane>/secrets/<NAME>` withdraws the declaration. For a key present only
  in pending input, a 200 with unchanged config revision means that pending declaration was
  withdrawn, not that nothing happened. The general pending-card unlock behavior is in
  [configuration](configuration.md).

Repeating a completed `webdev.request_secrets` replacement in the same target environment
(`replace_existing: true`) requests another per-key replacement and can open another card.

## Names that interact with platform supply

`DATABASE_URL` cannot be newly declared while the managed database is enabled, and enabling
that database over a declared `DATABASE_URL` is also rejected (`database_url_reserved`).
A server project explicitly configured without the managed database can supply its own DSN;
[database](database.md) owns that capability's data and enablement contract.

`STRIPE_SECRET_KEY`, `VITE_STRIPE_PUBLISHABLE_KEY`, and `STRIPE_WEBHOOK_SECRET` are provided by
the platform Stripe integration. Adding or revising those fixed declarations without Stripe
enablement is rejected as `stripe_integration_required`; [payments](payments.md) owns their
managed lifecycle. Old stored declarations do not make manual replacement the supported route.

Other injected names are not generally rejected as reserved names. A user-declared value can
shadow a platform-injected value for the application, while the declared key is excluded from
the platform's own environment reads. The application may therefore run with the override
while a platform feature that reads that variable no longer receives it; a successful save
has no separate warning for this condition. [Service API](service-api.md) and individual
capability pages identify the variables they supply.

## Environment delivery

Declared keys become environment variables under exactly their declared names; they are not
written into the project workspace.

They resolve for the development environment and published runtime according to their target
rows. Saving a value does not publish or republish, and does not establish that any process has
loaded it. Loading a stored revision and the environment retained by an already-running process
are distinct; [configuration](configuration.md#stored-and-active-state) owns that general
behavior.

## Configuration and input sequence

Before the first configuration call, read the [configuration transport contract](configuration.md). Declare capabilities from [features](features.md), not memory; before writing Manus login code, read [authentication](authentication.md). Use your own names for application secrets instead of shadowing platform-supplied variables, even when the config plane accepts the name.

Use `webdev.request_secrets` for new or replacement protected values. If the next command after input completion needs the new development
values immediately, call `webdev.config` with `GET config` once to synchronize the runtime, and
use its load receipt. Never replay a completed request with `replace_existing: true`; that
requests another replacement for its target and can open another card.

## After changing a value

Restart processes that were already running with the old value when they need the replacement. If the old value may have leaked, restart them immediately after the replacement is available rather than leaving the old credential active in the process.
Synchronize the runtime before a dependent command when required above; old and new terminals receive subsequent environment updates, but an already-running dev server or worker does not refresh itself.
After a secret revision, rerun validation appropriate to the affected application behavior. There is no blanket requirement to add a test or make a fresh provider call after every change, but the change must be checked where it affects the project.
