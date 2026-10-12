# Speech-to-text (transcription)

This Whisper-compatible surface uses [shared platform authentication](service-api.md#calling-the-platform-api-surface).

## Endpoint

`POST $MANUS_API_URL/v1/audio/transcriptions`, multipart form data.

| Field | Contract |
| --- | --- |
| `file` | Audio bytes; supported formats are webm, mp3, wav, ogg, m4a |
| `model` | Model field; documented identifier `whisper-1` |
| `response_format` | The endpoint selects `verbose_json`, including when this field is omitted |
| `prompt` | Optional context hint, including domain vocabulary or language context |

## Response (`verbose_json`)

The response fields are `task`, `language`, `duration`, `text`, and `segments`. `text` is the full transcription; `language` is detected language. Each segment can include `id`, `start`, `end`, `text`, and confidence metadata `avg_logprob`, `no_speech_prob`, `compression_ratio`. Omitting `response_format` does not select a text-only response.

## Capture, persistence and errors

When the speaker's language is known, say it explicitly in `prompt`; add relevant domain vocabulary as a context hint. For example: “Transcribe the user's voice to text; the working language is <language>.”

Capture audio in the browser, validate upload size, and send it to a trusted application server or durable storage. The server sends the audio bytes to the transcription endpoint as multipart data and returns the result. When later application behavior needs the transcript or timestamps, persist `text` and `segments` in the database.

Show upload-size and unsupported-format errors to the user. Retry only transient service failures; a permanently invalid recording should not trigger a retry loop.
