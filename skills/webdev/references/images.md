# Image generation

Runtime image generation uses the [shared platform API contract](service-api.md#calling-the-platform-api-surface).

## Generate or edit an image

`POST $MANUS_API_URL/images.v1.ImageService/GenerateImage` (Connect RPC).

| JSON field | Meaning |
| --- | --- |
| `prompt` | Text describing the requested image or edit |
| `originalImages` | Optional input array; each entry supplies `url` or `b64Json`, with `mimeType` |
| `model` | Optional model enum from the catalog; omitted selects the platform default |
| `quality` | Model-specific quality parameter |

Input URLs must be publicly fetchable; local file paths and browser blob URLs are not fetchable inputs. The response contains one image: `{ "image": { "url": "...", "b64Json": "...", "mimeType": "..." } }`.

[Storage owns the persistence difference](storage.md#generated-image-assets) between these runtime results and already-managed Agent image URLs.

## Model catalog

`POST $MANUS_API_URL/images.v1.ImageService/ListModels` with `{}` returns `models`, whose entries contain `model` (the API enum) and `id` (the model ID). Discover available models from this response; do not hardcode an enum or ID from a README, example or historical generation record.

## Model selection and failure handling

Use a `model` enum returned by ListModels when selecting explicitly, preserving the user's choice when available. If an explicitly requested model is unavailable, report that limitation instead of silently substituting another. Omit `quality` unless the selected model's current contract supports the value; do not carry another model's setting over blindly.

Treat a non-2xx generation as a failed attempt, read its response body, and expose a useful retry action to the user. Do not promote a failed or temporary result to a durable asset; the complete transfer sequence is in [application storage practice](storage.md#application-storage-practice).
