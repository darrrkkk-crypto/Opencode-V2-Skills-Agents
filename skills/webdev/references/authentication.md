# Default login and project access

When adding login, sign-up, user accounts, or authentication without a specified provider, use Manus OAuth by default. The user does not need to mention Manus. Do not build a separate email/password authentication system or choose another provider unless the user explicitly requests it. Preserve an existing application's authentication unless the user requests a change.

Application login is separate from project visibility. Manus OAuth requires `features.server: true`, without a separate auth feature key; the declaration schema is in [features](features.md). Provider-specific third-party credentials use [secrets](secrets.md).

## "Who can open this URL" is not your login

Project visibility is a Dashboard sharing control, not application configuration. The platform checks non-public access after Manus authentication, before a request reaches the application. `owner` visibility admits the owner, the project's session collaborators, and invited users, subject to team policy. `team_only` admits the owner and current accepted members of the owner's team permitted by team policy; invitations and session collaboration do not widen that audience. Effective public visibility has no such platform access gate. None of these settings creates an application session.

## Manus account login: the wire contract

The following values are platform-provided for application authentication.
Managed Cloud development injects them into the application environment; the published deployment receives them too. [Local](../worklocally/SKILL.md) owns Local Host loading. The internal config tool's `GET env` shows redacted names, not usable values.

| Value | Meaning |
| --- | --- |
| `MANUS_PROJECT_ID` | OAuth client ID; public |
| `MANUS_OAUTH_PORTAL_URL` | Browser authorization base; public |
| `MANUS_OAUTH_API_URL` | Token exchange and identity API base |

The browser authorization endpoint is `$MANUS_OAUTH_PORTAL_URL/app-auth` with query fields `appId`, `redirectUri` (absolute callback URL), `state` (base64-encoded JSON containing `redirectUri` and `nonce`), and `responseType=code`.

Token exchange is server-side HTTP POST, JSON:

```text
$MANUS_OAUTH_API_URL/webdev.v1.WebDevAuthPublicService/ExchangeToken
{"clientId":"<MANUS_PROJECT_ID>","grantType":"authorization_code","code":"...","redirectUri":"..."}
```

Successful exchange returns the following camelCase JSON fields:

| Field | Meaning |
| --- | --- |
| `accessToken` | Access token supplied to the subsequent identity lookup |
| `tokenType` | `Bearer` |
| `expiresIn` | Lifetime value in seconds; the current service returns `2147483647` and stores no time-based expiry |
| `refreshToken` | Optional in the response schema; the current exchange supplies one |
| `scope` | The scope stored with the authorization code |
| `idToken` | Current service's opaque ID-token value, not a signed OIDC JWT |

The current exchange implementation accepts only `grantType: "authorization_code"`. A `refreshToken` field does not imply a supported refresh-token grant on this endpoint.

Identity lookup is HTTP POST, JSON:

```text
$MANUS_OAUTH_API_URL/webdev.v1.WebDevAuthPublicService/GetUserInfo
{"accessToken":"..."}
→ {openId, name, email, platforms}
```

The callback is the application's actual frontend URL. Its acceptance is governed by the platform redirect policy; a loopback URL is not automatically permitted. The browser-visible frontend origin can differ from the server's internal host. The platform OAuth exchange does not create an application's own login implementation or session handling.

## Reserved names the platform occupies

`app_session_id` is a platform-owned cookie. On non-public projects the gateway verifies it with the project's signing secret; an application cookie using that name can be rejected by the gateway before application code runs.

The [platform environment contract](service-api.md#platform-owned-compatibility-names) owns
signing-secret names and publication-only compatibility aliases. Use that contract when
choosing environment names for an application's separate session implementation.

The [routing contract](routing-and-responses.md#published-routes) owns reserved path prefixes and interception. Platform OAuth endpoints include `/manus-oauth/callback` and `/manus-oauth/logout`. The storage namespace is owned by [assets and storage](storage.md#stable-asset-addresses), not an application OAuth callback namespace.

## Preview and application sessions

For Web applications using Manus account login, preserve the exact application session cookie name `webdev_app_session` to remain compatible with Preview auto-login. This applies to the default starter and `template: "flexible"`, regardless of framework or backend language. Preview injects a cookie with this fixed name; it does not discover a renamed cookie or read the application's `COOKIE_NAME` variable. Use the same name when setting the normal OAuth session cookie, reading authenticated requests, and clearing the session on logout.

The cookie name alone is insufficient: validate the project JWT using `MANUS_JWT_SECRET` and HS256, check expiry and that `appId` matches `MANUS_PROJECT_ID`, and resolve the authenticated `openId` through the application's user and permission logic. Preserve the starter's validation when adapting it to another stack. Preview auto-login requires support from the Preview host; if no valid session is supplied, keep normal login and the logged-out state. Platform OAuth and the platform access gate alone do not establish the application's own session.

Cloud Preview forwards the application's `Authorization` and `Cookie` headers to the development
server. An application may use its own Bearer token through Preview; forwarding a header does not
authenticate a user or grant a role. Browser cookie delivery still follows the rules below.

Cloud Dashboard embeds the application's public Preview in a cross-site iframe. The public connection is HTTPS even when the development server receives HTTP internally. Browser cookies marked `SameSite=Lax` or `SameSite=Strict` are not sent on that cross-site iframe request. `SameSite=None; Secure` makes a cookie eligible for that context, but browser third-party-cookie restrictions can still block it.

For application-owned login, do not choose `Secure`/`SameSite` from the internal `req.secure` value
or `NODE_ENV`: the HTTPS Preview may reach the app over HTTP while running in development mode.

Partitioned cookies have separate storage contexts for the embedded Preview and a standalone tab. Login in one context therefore does not establish a session in the other. The internal request scheme alone does not describe the browser's HTTPS cookie context. [Runtime](runtime.md) owns the platform proxy and embedding-header contract.

## Authentication implementation

For a new application using Manus OAuth, declare its server capability at creation, before implementing login. Implement application sessions and permissions around the returned Manus identity. Credentials for an explicitly requested third-party provider use the protected-secret declaration path.

Bind OAuth `state` to the initiating browser using a single-use nonce in a short-lived cookie. On callback, verify that state/nonce binding before exchanging the code and fail closed on mismatch. After login, redirect only to a fixed in-application path, never to an arbitrary URL supplied in the request. Preserve the actual frontend callback origin and the platform's redirect-acceptance rules.

Use real login and validated application sessions in Cloud Preview, Manus Studio and the published site. Show logged-out state until it succeeds; do not invent a Preview user, bypass authentication under `NODE_ENV`/another development switch, or defer real login until publishing. If cookies, callback policy or authorization prevent the flow, keep the real implementation and report the specific observed failure.
