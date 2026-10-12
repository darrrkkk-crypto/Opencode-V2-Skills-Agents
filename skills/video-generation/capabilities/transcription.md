# Transcription and subtitles

Read this when existing speech must become text, timestamps, captions, or candidate cut points. Reuse an existing trustworthy transcript. When the user already provides timestamped subtitles, validate and use them instead of retranscribing.

## Choose the available route

Inspect the transcription tools available in the current Sandbox and follow their current schemas, input limits, language options, timestamp granularity, and asynchronous result behavior.

Prefer a route that returns word timestamps when word-level cuts or karaoke-style captions are required. Segment timestamps are sufficient for ordinary subtitles. If a tool is asynchronous, save its returned job or task identifier and follow the status behavior documented by that tool; do not create an unbounded polling loop.

For a local CLI route, inspect its installed help before calling it. Confirm the executable exists, prepare audio only when necessary, and retain the exact output paths printed by this invocation. Do not download a model or replace system media tooling merely because an optional route is unavailable.

## Prepare source audio

Use the original media directly when supported. Otherwise extract or transcode an audio-only working file with FFmpeg. Keep the source unchanged and record any extraction offset.

Check the actual input-size and duration limits of the selected transcription route. If a source must be split, use FFmpeg to extract complete non-overlapping ranges that fit those limits and record each segment's source offset. Preserve a little listening context around proposed speech cuts when practical, while avoiding duplicate subtitle text at segment joins.

## Validate transcription

Open the structured result rather than relying on a human-readable console summary. Preserve the returned language, duration, segments, words, confidence or speaker information when present, and full text. Do not invent word timestamps by interpolating segment timings.

Listen around ambiguous names, numbers, technical terms, and proposed cut boundaries when audio playback is available. Correct obvious transcription errors without changing the speaker's meaning. Mark uncertain words instead of silently guessing.

For segmented inputs, convert timestamps back to source time:

```text
sourceSeconds = segmentOffsetSeconds + localTimestampSeconds
```

If media has already been trimmed or retimed during file-based assembly, calculate output timestamps from the actual edit manifest and speed factors. Keep this conversion in a small script or structured data file when there are many cues; do not hand-adjust a long subtitle list inconsistently.

## Create subtitle artifacts

Use a broadly supported subtitle format such as SRT or WebVTT unless the user requests another format. Each cue needs a nonnegative start, an end after the start, readable text, and ordering that matches playback. Avoid overlapping cues unless the delivery format and design explicitly support them.

Break captions at natural phrase boundaries. Keep reading density appropriate for the target platform, preserve intentional slang and tone, and avoid exposing filler-word removal as a text-only change when the audible speech remains unchanged.

When subtitles must be burned into a finished video, retain the standalone subtitle file and render the video with FFmpeg. Use an available subtitle filter or composite locally rendered caption images with FFmpeg, checking font support. If neither route is available, deliver the sidecar and state that burn-in is incomplete. Verify safe-area placement, contrast, line breaks, and timing on representative frames. When sidecar subtitles are sufficient, do not re-encode the video unnecessarily.

## Deliver

Return the transcript and/or subtitle file with language, timestamp granularity, and any unresolved uncertainties. If captions were burned in, also deliver the rendered video and state that it is a file-based output rather than an editable project.
