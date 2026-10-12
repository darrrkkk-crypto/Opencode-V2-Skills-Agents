# Generated video production

Use this workflow to plan a complete generated video, or to preserve continuity across clips when more than one request is necessary.

## Plan generation units

Separate the creative plan from tool calls. First identify the intended audience, format, total duration, aspect ratio, narrative or message, visual direction, dialogue, and sound. Ask only for missing choices that would substantially change the work; otherwise make a visible, reversible assumption.

Plan all shots of the complete video in one request by default, following the [single-request rules](../capabilities/model-video-generation.md#default-plan-the-complete-multi-shot-video). Location, time, clothing, camera, and action changes belong in the shot descriptions. Split only when duration, reference capacity, output settings, or multi-shot support actually require it, or when the user explicitly requests separate clips. Record the concrete reason and the fewest necessary requests.

For every unit record:

- its purpose and approximate duration;
- location, people, objects, and reference assets;
- the opening state and the visible ending state needed by the next unit;
- concrete actions, camera intent, dialogue, ambient sound, and synchronized effects.

Use `Shot 1`, `Shot 2` for shots within a request. Use stable unit identifiers such as `U01` and `U02` only when multiple requests are needed.

## Prepare references

Use the reference rules already in the entry point; [asset templates](../workflows/creative-shorts/02-asset-design.md) are optional for a concrete derivation example. Reuse approved person and product references; consistent text can describe settings, light, and style. Follow its rules for necessary supplemental views and shared reference sheets. Bind every cited reference to the actual attached file and state what it supplies.

## Write executable prompts

Describe only things the viewer can see or hear. Replace abstract mood or intent with lighting, color, lens character, material, expression, body movement, object state, dialogue, ambience, and sound effects.

Use the [shared shot-number template](../capabilities/model-video-generation.md#shared-shot-number-template). Write model instructions in English, quoting specified dialogue and visible text in the requested language. Each shot needs a starting view, camera direction/path/pace, ending framing, visible action and result, sound, and cut point. Describe a planned locked camera explicitly. Use natural-language pacing, with total duration in tool parameters and no per-shot start/end timestamps. Preserve the established plot, characters, actions, and lines.

Specify the end state of hands, gaze, wardrobe, weather, lighting, and important objects when the next unit must continue the action. Describe continuing subject and camera movement and a clear action point for the join.

When the model supports synchronized audio and the user has not requested silent footage, include the actual dialogue, speaking character and delivery, room or environmental ambience, and action-synchronized effects. Treat non-diegetic music as a separate assembly choice unless the user wants it generated in-scene.

## Generate and assemble

Submit the complete planned sequence in one request whenever possible, using current tool parameters. When requests must be split, preserve dependencies between their continuity states. Keep a small manifest of unit IDs, prompt or prompt file, references, returned clip paths, duration, aspect ratio, and audio status so retries do not lose provenance.

Retry only when a result materially misses the request or is unusable. Change the smallest relevant variable: prompt language, reference choice, unit boundaries, or model setting. Do not repeatedly spend generation calls chasing imperceptible differences.

A complete multi-shot video generated in one request can be delivered directly. When separately generated clips must become one film, assemble them in the planned order with FFmpeg. Normalize dimensions, frame rate, and audio only as needed; preserve generated dialogue and synchronized production sound. Add music, narration, titles, or captions only when requested or clearly part of the brief.

Verify container integrity and reported duration with ffprobe. If visual inspection is available, check the joins and identity continuity. If only clips were requested, deliver those clips without inventing an edit.
