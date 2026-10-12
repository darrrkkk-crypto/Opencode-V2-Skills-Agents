# API hub

The API hub calls Manus-managed external data APIs without separate provider credentials. It uses the [shared runtime API contract](service-api.md#calling-the-platform-api-surface).

## Calling convention

`POST $MANUS_API_URL/webdevtoken.v1.WebDevService/CallApi` (Connect RPC).

| JSON field | Meaning |
| --- | --- |
| `apiId` | Required API identifier, such as `Youtube/search` |
| `query` | Optional upstream query parameters |
| `body` | Optional upstream request body |
| `path_params` | Optional upstream path parameters |
| `multipart_form_data` | Optional upstream multipart fields |

The available API IDs and upstream fields depend on the registered API.
A registered session API-search capability, when present, provides discovery; it is not a guarantee that every session exposes that tool.

## Response

The response contains the upstream object. When a `jsonData` field is present, its value is a JSON-encoded string; otherwise the response object itself is the result.

## Provider selection

Before wiring a separate third-party API and collecting its key, look for a suitable built-in API. Use the registered search capability when the session provides one; an external caller can use IDs already discovered by a Manus session or present in the project. Use a provider with its own key only when no suitable built-in API exists, unless the user explicitly selected that provider. Keep its keys in the protected-secret flow.
