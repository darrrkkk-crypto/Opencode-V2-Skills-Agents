# 03 · Shot design

Use to design multiple shots from an established script, completing them in one video-generation request by default. Retain the story, characters, and lines when only the filming approach changes

This stage delivers a shot table for the complete video; add a generation-unit table only when separate requests are actually needed

## Plan the complete video as one generation first

Use the [model video capability](../../capabilities/model-video-generation.md#creative-approach) to check the current tool schema, including duration per call, reference capacity, audio, aspect ratio, and resolution. Generate all shots that fit together in one call. Describe location, day/night, wardrobe, and camera-position changes within their shots; these do not require separate requests. When splitting is necessary, record the specific limitation or separate-delivery requirement and the minimum number of requests

Number shots Shot 1, Shot 2. See [Shot density](../../capabilities/model-video-generation.md#shot-density) for pacing and its use cases. Use U01, U02 to distinguish generation units only when multiple requests are needed

For social video, design the first two seconds first: what information the viewer receives, what moves, and what they hear. Open directly on the most compelling event, then let subsequent shots continue it; do not spend several seconds on a static introduction before the content begins

### Generation-unit index example

These are planning values for a specific project; still check the current tool window before running it

```text
U01  Store lights off → person in the rain outside → across the counter
     9:16   26s total   one request, when supported by the current tool
     Shot 1, Shot 2… cover the whole sequence, including interior/exterior cuts.
```

## Write one shot table for the complete video

Record the estimated total duration, aspect ratio, model, location, characters, written setting, references used, and start/end states in the table header. By default, one table corresponds to one complete generation; use separate tables for each unit only when multiple requests are necessary. Mark an image as missing only if it is actually needed and has not yet been prepared

Use Shot 1, Shot 2 and other shot numbers in the table, with pace, shot size or camera position, one main camera move, visible action, character lines, and synced sound. The action column states trajectory, range, and speed; the camera column states path and pace. Explain the expressive purpose of stillness or a hold. Total duration is for production management; model prompts do not give per-shot start and end times

### Complete unit table and continuity example

This example builds suspense with restrained action; locked cameras and a slow push serve this particular story. Usually prioritize purposeful moving shots. See [Multi-shot examples](../../capabilities/model-video-generation.md#multi-shot-examples) for other filming approaches

```text
## U01  Store lights off
Planned duration: 8s
Aspect ratio: 9:16
Model: {selected current model}
Location: convenience store (describe the layout and light; this narrative example recommends a location reference that also establishes the Look, if useful)
Characters: clerk (cite the approved character hero still; any derived references must retain this same identity)
Key object: bento case
State join: start = she is reaching to turn off the lights; end = only the cooler is still lit, she looks toward the glass door and asks who is there

| Shot | Pace | Size / position | Camera move (pick only one) | Action the viewer can see | Synced sound design |
| --- | --- | --- | --- | --- | --- |
| Shot 1 | Brief insert | Hand close-up | Locked perpendicular to the panel, switch and fingertips visible | She presses the light-row switch; cut on the click | Crisp switch click, rain continues |
| Shot 2 | Brief insert | Tight view down the ceiling light row | Locked at an upward angle, preserving the row's depth | Warm lights go out from near to far; cut on the last light | Electrical hum fades |
| Shot 3 | Longer reaction | Close over her left shoulder | Slow forward push along her eyeline, ending on the door beside her cheek | Hand stays on the switch, head turns to the door; cut as her gaze reaches it | Cooler hum becomes clearer, rain outside |
| Shot 4 | Full line | Front three-quarter face close-up | Locked at eye level to read her reaction | Eyes stay toward the door off camera; she says quietly, “Who’s there?”; end after the complete line | Lip-synced line, rain overlapping but not obscuring the last word |

If the story continues outside, add that view as the next shot in the same request; her silhouette stays in the same place. Extend the total duration within the tool's supported range.
```

### Actions should be concrete and visible

- State who acts on whom or on what
- Give the action a complete path, from starting position to ending position
- State speed and range clearly. “Turn her head toward the door” and “Spin around, take two large steps, and push the door open” are different actions and must follow the script; do not quietly substitute a different event during prompt writing
- Leave a visible result, such as a light going out, water falling, or a cup moving
- Give every on-screen person a state, even if they are only standing and watching the other person's hand

“An oppressive atmosphere,” “a broken relationship,” and “deep loneliness” are emotions and themes; shot design realizes them through people, objects, light, and action

### Camera movement and aspect ratio

The camera column states the starting shot size and camera position, camera path and speed, and ending composition or position relative to the subject. See [Describe camera movement and action in every shot](../../capabilities/model-video-generation.md#describe-camera-movement-and-action-in-every-shot). Carry all of this information into the English prompt in the next stage

For vertical video, prioritize face and hand close-ups; vertical motion is usually easier to read than a wide horizontal pan. Two people can be covered in alternating single-person close-ups; keep key information away from bottom interaction areas such as likes and comments. Reserve broad lateral staging and large empty establishing shots mainly for widescreen horizontal frames

## Make the joins work

Record gaze, hand position, clothing, and object state clearly at the end of a unit, then specify how the next unit picks up: continued action, a reverse shot, an object transition, or sound arriving first. Leave enough action handles in sections that need trimming and state the planned edit point

The opening unit directly presents the script's viewer-retaining event. Shot design defaults to text; do not generate an image per shot or force storyboard images to animate as first-frame / first-last-frame inputs. Draw diagrams when the user explicitly wants a visual storyboard or complex action needs explanation; these diagrams do not automatically become video reference assets

Check each seam: where the character looks at the end of the previous section, where their hands stop, and whether their clothes are wet; how the next section's first frame joins through continued action, a reverse shot, an object, or sound first; and whether the sections hard-cut directly or retain overlapping action for trimming. Mark planned head/tail trims and sections that need emotional continuity and action overlap

## Complete template for converting a script into shot design

```text
Using the Concept and Script and the Visual Asset Pack (leave blanks if assets are not finished), break this short into concrete shots.
Model: {the selected model identifier from the current tool schema}
Duration per call: {current limit from the selected model schema} seconds
Aspect ratio: {aspect ratio}

Output the following:
1. One request for the complete video by default. If current tool limits or explicitly requested separate deliverables require multiple requests, list the minimum units, their durations, and the concrete reason for splitting.
2. Beat-table detail: one table per unit, using shot numbers, with pace, shot size, one main camera move and its path and pace, visible action with its trajectory, speed and range, character lines, and synced sound.
3. Join notes: exit and entry states between units, written clearly.

Breakdown rules:
- Absolutely no new characters, locations, plot, or lines.
- Do not force a line of mood description from the script into a shot.
- Names of people and places must match the script exactly.
- Seedance 2.5, Seedance 2.0, and MiniMax share this shot design and prompt structure. Use “Shot 1, Shot 2…” with natural-language pacing, not exact per-shot start and end seconds.
- Choose pacing for the platform and content: usually two to three seconds per shot, quicker for fast-paced social montages, longer for full performances, readable details, or deliberate suspense. Location, lighting, wardrobe, or camera changes belong in the shot descriptions, not separate requests by default.
- Describe each shot's starting view, main camera direction/path/pace, and ending framing or position relative to the subject. For social video, design the first two seconds around a strong event with immediate information and visible motion, adding synchronized sound when audio is wanted. A silent video's hook must work visually.
- Put only the script's approved dialogue into the matching shots, with lip sync when characters speak. Design ambient sound and action SFX for audible footage; respect requests for no dialogue or complete silence. Voice-over cannot replace character conflict.
- At the end of each unit, write the character’s position, ongoing action, and continuing camera movement clearly so the next unit can pick them up.
- Finally, list unresolved assets by name and their approved reference source, following the existing asset-design workflow.
```

## Local shot-revision template

Use when only a unit's filming approach needs adjustment:

```text
Rewrite only the shot language of unit {U0X}.
Keep the existing plot, lines, and characters unchanged.
Adjustment goal: {e.g. clearer action range / faster tracking / a deliberate pause / join during an action}
Requirement: one main camera intention per beat; preserve the story while making the action's path, speed, and range clear.
```

## Responsibilities of shot design and prompts

| Shot design plans | Prompts execute |
| --- | --- |
| How many cuts this unit needs and what each cut shows | Translate these “cuts” into sentence structures the model understands |
| Who moves from which position to which position | Describe action intensity, the body parts involved, and how actions connect |
| Which information this shot describes in text and which needs one or more reference images | Reuse the written setting; when images are attached, describe each `@ImageN`'s subject, view, and role |
| The unit's total duration and shot density | Use shot numbers in every version, without per-shot start and end seconds |

Shot design ends at cut content, action paths, reference selection, and rhythm planning; enter the video-prompt stage when actual generation is needed

## Outputs

Deliver the unit index, each unit's shot table, join notes, and specific asset gaps. A local shot change updates only the relevant unit; after shot design is complete, continue to video prompts only when generation is needed
