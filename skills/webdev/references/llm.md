# LLM (chat completions)

Calls use the [shared platform API contract](service-api.md#calling-the-platform-api-surface) and deduct from the project's credit balance. No separate model-provider account or key is required.

## Endpoint and clients

`POST $MANUS_API_URL/v1/chat/completions`, JSON body, OpenAI-compatible chat-completions surface. `messages` carries the conversation. `model` is optional; omission selects the platform default. Completion text, when returned, is in `choices[0].message.content`.

## Message shapes

`messages[].role` is `system`, `user`, `assistant`, or `tool`. `content` is a string or an array of typed parts:

```json
{ "type": "text", "text": "..." }
{ "type": "image_url", "image_url": { "url": "https://...", "detail": "auto" } }
{ "type": "file_url", "file_url": { "url": "https://...", "mime_type": "application/pdf" } }
```

`image_url.detail` accepts `auto`, `low`, or `high`. `file_url.mime_type` accepts `audio/mpeg`, `audio/wav`, `audio/mp4`, `video/mp4`, and `application/pdf`. URLs must be publicly fetchable, not local `file://` or browser blob URLs; [storage](storage.md#runtime-contract) defines persistent asset addresses.

Function tools use `tools` declarations and `tool_choice`: `none`, `auto`, `required`, or `{ "type": "function", "function": { "name": "..." } }`.

## Structured responses (JSON schema)

`response_format` accepts the OpenAI-style `json_object` or `json_schema` form. The schema form carries `json_schema.name`, `strict`, and `schema`; the returned JSON is still text in `choices[0].message.content`. Support and parameter combinations depend on the selected model and route; the HTTP surface alone does not guarantee support for every schema.

## Response and errors

[Shared error semantics](service-api.md#calling-the-platform-api-surface) apply. Completion `content` can be absent or empty; token usage or a `choices` field alone does not establish that text was returned. A request containing unsupported combinations can return an error instead of a completion.

## Listing available models

`GET $MANUS_API_URL/v1/models` returns OpenAI-standard model metadata. The catalog need not contain the default route's selected ID. Capability metadata can be sparse: a missing capability field does not establish support or lack of support for that feature.

## Thinking / reasoning

The `thinking` and `reasoning` extension parameters pass through unchanged, without platform defaults. The documented family-specific request shapes are:

| Family | Extension |
| --- | --- |
| OpenAI gpt-5 | `"reasoning": { "effort": "high" }`; effort values: `minimal`, `low`, `medium`, `high` |
| Google Gemini | `"thinking": { "budget_tokens": 1024 }` |

The numeric budgets above illustrate the fields, not a platform-imposed budget. A model's accepted values belong to that model; `/v1/models` does not promise per-model reasoning examples.

## Streaming

`"stream": true` selects server-sent events. The response is a stream rather than a single completion JSON object.

## Reliable structured output

When requesting `response_format`, name a model explicitly rather than relying on the default route. This avoids an observed default-route failure in which a request consumed completion tokens but returned no content. Inspect the current catalog instead of hardcoding an assumed model ID. Family prefixes can guide selection, but do not infer an undocumented capability from a missing field: verify the required request shape with the chosen model.

For supported JSON-schema output, set `strict: true`, list every declared property in `required`, and use `additionalProperties: false`. The returned value is still text and must be parsed. For nested structures whose schema enforcement is not supported by the selected route, spell the intended shape out in the prompt and validate the parsed result; a prompt description is not enforcement. Use `json_object` only with a model/request combination known to support it. This guidance does not assert that every current model is limited to flat schemas.

Consume results in this order:

1. If the body contains `error`, treat it as failed and read `error.message` without indexing `choices`.
2. If completion content is absent or empty, handle it as no output rather than immediately crashing the job. Retry once without `response_format`, then parse the resulting text. Remove an enclosing JSON Markdown fence; if needed, extract the outermost JSON object and validate it before use.
3. Only consume successfully parsed/validated content. If recovery still produces no usable result, report that outcome rather than claiming success.

An unsupported parameter combination will not become valid through repetition. Change the model, omit the incompatible response format, or record a terminal failure. If a retry returns the same `error.message`, stop repeating that request. An observed case combined JSON mode with a model's built-in tool; treat the returned incompatibility as a request-shape problem, not an invitation to retry indefinitely.

## Streaming and presentation

When proxying an SSE response through an application server, tie upstream cancellation to the downstream **response** closing, not merely the incoming request closing. Guard cancellation with a finished flag so normal request completion does not abort the stream after its first event. Use the equivalent lifecycle signals in the chosen server framework.

Render Markdown-bearing LLM output with an appropriate Markdown renderer instead of printing the raw formatting. Keep the renderer compatible with the application's untrusted-content boundary.

## Game loading and recovery

For AI dialogue and other LLM calls in games, show localized loading/thinking immediately, even
before the first stream chunk. Keep play responsive and block duplicate submits. Clear pending
on success, error and timeout. Errors/timeouts must retain input, explain recovery and offer retry
of the same logical turn without duplicate saves or story advancement. Test delays, failure and
retry in-game.
