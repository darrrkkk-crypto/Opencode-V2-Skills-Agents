# Platform runtime API

This is the shared HTTP contract for application calls to the platform's AI and utility services. It does not define database connections, OAuth, Stripe configuration, or browser analytics. Each capability has its own contract and can be read directly when needed.

## Runtime credentials and scope

| Variable | Meaning |
| --- | --- |
| `MANUS_API_URL` | Runtime API base URL |
| `MANUS_API_KEY` | Project's server-side API credential |
| `MANUS_API_BROWSER_KEY` | Different, browser-safe credential for supported browser surfaces |

Calls use the project's service identity and resources, not an application's independently authenticated user identity. An endpoint that accepts user attribution defines it in that endpoint's contract. The server key is not a browser credential or an operator's config-plane key.

Managed Cloud development supplies these values to the sandbox shell and dev process. Local Host environment loading is governed by [Local](../worklocally/SKILL.md); an arbitrary local shell does not receive them automatically. The sandbox retains `BUILT_IN_FORGE_API_URL` and `BUILT_IN_FORGE_API_KEY` for platform CLIs.

Development and published application calls use the same platform API credentials. Empty platform values are omitted rather than supplied as empty strings. Published deployments retain pre-rename aliases, but an old alias is not guaranteed in a development environment.

### Platform-owned compatibility names

Published containers also receive `JWT_SECRET` as a compatibility alias of the platform's
`MANUS_JWT_SECRET`; the managed development environment supplies the canonical name, not this
alias. Neither name is an application-owned setting, and the platform does not promise the
length or format an application's independently chosen signing library might require.
For a separate application session/signing secret, use an application-specific name through
[protected secret configuration](secrets.md), rather than shadowing either platform name.
Platform callback authentication is defined in [scheduled work](scheduled-work.md#callback-identity).

Build-time availability is a different contract: [static build](build-contracts.md#static-build) and [container placement](build-contracts.md#container-build) own it. A variable available to a build is not necessarily safe to embed in browser output.

## Calling the platform API surface

The base URL is `MANUS_API_URL`. Server calls authenticate with `Authorization: Bearer <MANUS_API_KEY>`. No application source helper or SDK is injected by this HTTP contract.

| Surface | Request contract |
| --- | --- |
| OpenAI-compatible `/v1/...` | Endpoint-specific verb; JSON or multipart body |
| `<package>.<Service>/<Method>` Connect RPC | `POST`, JSON body, `Content-Type: application/json`, `connect-protocol-version: 1` |
| Maps proxy | Google-style `key=` authentication; [Maps](maps.md#calling-convention) owns the browser/server distinction |

## Results and errors

Non-2xx responses carry an error body. A service can also return an `error` object with HTTP 200 instead of its result payload. Missing result fields, empty results, and explicit errors are different outcomes. `retry_able` and `Retry-After`, when returned, are retry hints; they do not make an invalid parameter combination valid.

## Capability contracts

[LLM](llm.md), [images](images.md), [speech](speech.md), [API hub](api-hub.md), and [owner notifications](owner-notifications.md) use this shared API contract. [Storage](storage.md) uses it for runtime uploads; merely consuming an already-returned storage URL does not require API credentials. [Scheduled work](scheduled-work.md) uses it for management RPCs; callback authentication is self-contained on that page.

## Using the supplied platform services

Before designing around a built-in service, check its capability page's environment availability and current project Resource/configuration or supplied variables. Use a provider capability only when the current project advertises it or its required environment is actually present. Read the relevant database, authentication, or payments contract before writing code or changing configuration for that capability; this is not a requirement to read unrelated services.

Use the real supplied service during development rather than substituting a local fake and assuming the platform path works. Read endpoints and credentials from their documented environment variables at call time; do not hardcode values already supplied there. Use application-specific names and the [protected secret flow](secrets.md) for any separate provider credential.

Implement and verify real application login in Preview/development as well as in the published application; the [authentication practice](authentication.md#authentication-implementation) defines the checks. Do not use a simulated Preview user, skip authentication based on a development flag, or infer that all Preview login is unsupported from one failed callback.

Use the actual browser-visible application origin for redirects. Pass that origin from the frontend when the server needs it; in browser JavaScript this is `window.location.origin`. Do not derive it from an internal `req.host` or a guessed deployment URL. Preserve this origin across the actual authorization/callback flow.

## Failure and retry practice

Read a failed call's response body before deciding what to do. For transient 429/5xx failures, use exponential backoff and honor `Retry-After` when present. Do not treat every non-2xx as transient: malformed input, unsupported combinations and authorization failures need the appropriate correction.

Check the body's `error` before indexing a result, then distinguish a missing/empty result from a usable one. If retrying yields the same error message, stop repeating that unchanged request and correct it or report the failure. [LLM structured-output handling](llm.md#reliable-structured-output) adds the model-specific recovery sequence.
