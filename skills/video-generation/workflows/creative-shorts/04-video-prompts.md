# 04 · Video prompts

Use to turn an established shot design into submit-ready video-model requests. Retain the confirmed shot count, plot, actions, and dialogue. See the [model video capability](../../capabilities/model-video-generation.md#shared-shot-number-template) for actual calling rules and the shared video-model template, and [editing and assembly](05-editing.md) when assembly is needed after generation. A task only to write or revise prompts can deliver text

## Prepare for submission

Use the entry-point rules directly; consult [video prompt examples](../../capabilities/model-video-generation.md#video-prompts) only if a full template is needed. Carry approved shots, rhythm, action, and camera paths into the prompt without rewriting the story or weakening movement.

Submit all Shots of the complete video together by default. If splitting is necessary, preserve the reason and minimum generation units recorded during shot design. Record total duration, aspect ratio, resolution, audio setting, and attachment list in the request parameters; do not write per-shot start and end seconds in the prompt body

Use the entry point's master-reference and derivation rules, attaching real files with explicit roles. Consult [asset templates](02-asset-design.md) only for a specific example.

## Narrative shorts should generate synced original sound

Unless the user explicitly requests silent footage, enable audio generation on models that support synced audio. Design the following according to the approved script and sound requirements:

1. **Lip-synced dialogue**: when approved lines exist, specify the words, speaker, tone, and volume; do not add lines to a no-dialogue script; reuse the same locked reference for the same character when the tool supports timbre references
2. **Ambient sound**: rain, low machine-room frequencies, street sound, room reverberation, and other sounds occurring in the space
3. **Action SFX**: keyboards, doors, footsteps, clothing, buttons, cups, breathing, alarms, and other sounds synced with visible action
4. **Diegetic music**: include music in generation prompts only when it comes from a real source in the frame, such as a radio, phone, or store PA

Non-diegetic background music is usually controlled during assembly, but this does not justify removing synced dialogue, ambient sound, or action SFX. Prioritize retaining generated dialogue, lip sync, and production sound; post-production music must not cover the lines. Follow the user's explicit silent or pure-mood request

## Translate shot design into a prompt

```text
Input: the approved shot design, written setting and Look, and actual reference files. Use the video-generation capability's shot-number template.
Output: a complete English video prompt for the planned generation unit, with request parameters and attachment mapping listed separately.

Preserve the approved characters, events, actions, dialogue, pacing, and shot count. Keep user-specified dialogue and visible text in their requested language as literal quoted content.
For every Shot, carry over the starting view, main camera direction/path/pace, ending framing, subject action and physical result, exact spoken line if present, synchronized sounds, and cut point. State a locked camera explicitly when planned. Do not replace camera instructions with a shot-size label or an editing command.
Bind only attached references and state each one's purpose. Fill every field; remove unused template instructions before submission.
Read the resulting prompt on its own: it must describe the intended sequence without requiring the model to read the storyboard or other documents.
```

## Example: an 8-second restrained suspense unit

This example builds suspense through small actions, fixed compositions, and gradual approach; it does not define the default movement intensity for every video. Submit all four shots in one request, after checking that the tool supports eight seconds and the required audio reference. If timbre references are unsupported, remove that attachment and its reference. See the model video capability linked above for sports and product-ad examples

```text
[Assets]
@Image1 defines the clerk's approved face, short hair, and dark-green apron. Do not take the solid background or original pose.
@Image2 is for the convenience-store aisle, bento cases, glass-door position, and cooler light. Do not take people from the still.
@Audio1 is for the clerk’s timbre and speaking style. Do not take the sample’s specific lines or ambient sound.

[Style]
Low-saturation quiet interior night, Super 16 grain, 50mm prime. Key light is the cooler’s cool white. After the warm lights go out one by one, wet glass and rain shadows outside remain. Generate the four shots together: two brief inserts followed by longer reaction and dialogue shots, leaving time for the full spoken line.

[Shots]
Shot 1: Hand close-up, camera locked perpendicular to the switch panel, keeping her fingertips and switch in frame. The clerk presses the light-row switch; a crisp click sounds in sync, rain continues outside. Hard cut as the switch clicks into position.
Shot 2: Tight view down the row of ceiling lights, camera locked at an upward angle so the lights' depth stays readable. Warm lights go out one by one from near to far; the electrical hum fades with them. Hard cut when the last warm light goes out.
Shot 3: Close over her left shoulder toward the glass door. Push slowly forward along her eyeline, narrowing from her shoulder and door to the door framed beside her cheek. Her hand stays on the switch and her head turns toward the door; the cooler hum becomes clearer. Cut as her gaze reaches the door.
Shot 4: Front three-quarter face close-up at eye level, camera locked to preserve the readable reaction. Her eyes remain directed toward the door just off camera. She lowers her voice: “Who’s there?” Lips sync to the same timbre as @Audio1; rain briefly overlaps the last word without obscuring it. End after the complete line and her final mouth movement.

[Close]
Character and location stay consistent with the reference stills throughout. Keep the synced line, rain, switch click, and cooler hum. Do not add non-diegetic background music, end-title cards, or an unreferenced logo.
```

## Record and deliver

Save prompts by generation unit, recording actual reference assets, shot count, synced dialogue, and production SFX at the top. Check that every action comes from the shot design, references match files, and video and sound requirements agree

If delivering model clips only, check the local files after generation and finish; enter editing when clip assembly or precise arrangement is needed
