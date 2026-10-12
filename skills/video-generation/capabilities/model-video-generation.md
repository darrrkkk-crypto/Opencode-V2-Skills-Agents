# Model Video Generation

Optional video-prompt and camera-pattern library.

Use the currently available Manus video tools. Establish the aspect ratio, target duration, action, references, and sound requirements first. Generate and deliver one clip or several separately requested clips directly; use FFmpeg in the Sandbox when assets need assembly, precise arrangement, subtitles, or overlaid motion graphics

Current execution guidance: the creative method below is shared across video models. The actual generation tool schema determines model availability, duration per call, reference counts and combinations, and audio support. The selected production workflow continues to guide the work's direction; deliver generated clips directly through the route above

**Core requirements: consistency, visually effective video, and alignment with the user's request.** Use reference images to keep characters and products consistent; combine a shared written setting with applicable references for the space, lighting, and style. Shot design, action, camera movement, composition, and sound work together to determine the viewing experience. Content and expression must serve the user's goal. Plan all three requirements together and check each after generation

## Creative approach

- **Video generation**: choose among models actually available in the tool
  - Use MiniMax / H3 when cost matters or when using fast mode
  - Prefer Seedance 2.5 when quality matters; Seedance 2.0 is also an option
  - When people or products appear, use approved reference images through **references-to-video**. Text-to-video is suitable when there are no people or products and text can adequately describe the picture. Do not default to first-frame / first-and-last-frame generation

**Seedance 2.5, Seedance 2.0, and MiniMax share the same shot-design and prompt method.** Use `Shot 1, Shot 2…` for multi-shot videos, with natural-language pacing rather than exact per-shot start and end seconds. Tool parameters control total duration; the methods for designing shots, camera movement, action, and sound are the same

Check model differences against the current tool before submission. Do not infer parameters from model names or apply another model's limits:

| Parameter or capability | Check before submission |
| --- | --- |
| Model identifier | Use an actual enum listed in the current schema; do not construct one from a product version name |
| Multi-shot support and duration per call | Confirm that the complete video can fit in one request; split only when it exceeds the tool's capabilities |
| References | Confirm image, video, and audio counts, combinations, and citation methods; attach only supported assets |
| Sound | Check support for synced audio, timbre references, and audio-only input; use the corresponding audio capability for models without synchronized audio |
| Output | Use an aspect ratio and resolution supported by the current tool and appropriate for the delivery and crop requirements |

## Video prompts

Use this section when writing Seedance / MiniMax video prompts for promos, talking-head videos, UGC, and short films. When a category has additional constraints, also read the matching `workflows/` file

**All instructions sent to the model must be in English**, including reference roles, style, action, camera movement, and sound. Preserve user-specified dialogue and visible text as literal quoted content in the requested language; English instructions do not change the video's language. Fill all template placeholders and remove unused references and conditional instructions before submission

### Default plan the complete multi-shot video

First establish all shots in the complete video, what each communicates, and how action and sound connect; then use [Shot density](#shot-density) below to plan the rhythm

**By default, generate all shots of the same video together in one video-generation request.** Put `Shot 1, Shot 2…` in one prompt and set total duration through tool parameters. A request for multiple shots is not a request for multiple generation calls. Changes in camera position, location, day or night, or wardrobe can all appear as shot changes in the same generation; they do not require separate calls. This is more direct and reduces later assembly

Split into the minimum necessary requests only when total duration, reference capacity, shared output parameters, or multi-shot support exceed the current tool's capabilities, or when the user explicitly requests independent clips for separate delivery. Record the specific reason for splitting; when one call can generate the complete video, generate and deliver it directly

### Shot density

Usually **cut every 2–3 seconds**, with each cut bringing new action, perspective, or information; adjust for the platform and content:

- **Faster is possible**: energetic unboxings, sports montages, product-feature showcases, or beat-synced videos in Douyin, TikTok, and similar feeds can advance through **shots of about 1–2 seconds**. An opening impact detail can be shorter if its point reads at a glance. A long line can continue across cuts without holding on the same face throughout
- **Slower is possible**: mood pieces, suspense build-up, complete performances, and shots that need time to read information or understand an operation should have the time they need

Follow the user's request for a continuous take or a specified pace. Faster cutting does not make action more forceful: design subject action and camera movement within each shot separately, and do not use dense cuts to hide a lack of movement

### Reference-image design and consistency

Reference and generation rules are in the entry point. Consult [asset templates](../workflows/creative-shorts/02-asset-design.md) only for a specific derivation example.

Characters and products require reference images. Locations, lighting, and style may be described in text; for short films, a location image is recommended to establish the space and style together

Reuse approved assets directly and state each reference's role. Execute the planned action and camera movement; do not weaken movement on your own to preserve consistency

### Describe the visual style clearly

Every prompt must say **what the picture looks like**. Do not leave the style entirely to the reference images

Where possible, be specific about:

- **Which kind of image from which film**: describe what kind of night scene, rainy night, or interior lighting from *XX* you mean; do not just name the film
- **Which visual habits of a director**: whose framing, lighting, or camera-movement rhythm you are referencing. Describe visible habits, not “the feel of so-and-so”
- **Which camera and lens**: film or digital cinema camera, focal length, shallow or deep depth of field, whether it is anamorphic widescreen, handheld or tripod
- **The light and materials themselves**: color temperature (cool / warm), saturation (high / low), key-light direction, shadow depth, and what is visible in the air (rain streaks, dust, steam)

Do not write “cinematic,” “premium,” or “atmospheric.” Reuse the same style sentences throughout a film. What changes is who does what, not a new grade or a different director in every prompt

### Write only what is visible

Write only **what can be seen or heard**

Write who does what and what changes into what. She presses the switch, and a row of warm lights goes out. The corners of her mouth drop, and her gaze turns toward the glass door. The bag slips from her hand onto the floor

Do not write psychological states, intentions, themes, or symbolism. The model cannot see “she is lonely,” “inner struggle,” or “an oppressive atmosphere.” Translate these into changes in faces, hands, bodies, object states, and light

Plan dialogue, ambience/action SFX, and background music separately. “No voice-over” does not mean complete silence, and adding BGM later does not mean disabling video audio.

For audible footage on a model that supports synchronized audio, include the needed dialogue, ambience, and action SFX in the prompt and enable audio; specify lip sync when there are spoken lines. Non-diegetic BGM can be generated separately and added during post-production assembly; in that case, exclude only BGM from the video prompt, retaining ambience and action SFX. With Seedance, ambience and action SFX must be generated with the picture in the same video request, not through a separate SFX generation step. Describe each sound source and its corresponding action in the shot prompt. Do not deliver only BGM when planned SFX are still missing. Honor requests for complete silence by generating or adding no sound.

Let approved character action and dialogue advance a narrative short, with narration as a light supplement. Music with an identifiable source visible in the frame can be generated with the picture

### Describe camera movement and action in every shot

Describe each shot's **starting shot size and camera position → camera direction, path, and pace → ending composition or position relative to the subject**, so movement reveals information, follows action, or changes the perspective. For example: “Track sideways at waist height, matching the runner's speed and keeping her centered as nearby pillars sweep quickly past.” Use a locked camera for deliberate comparison, reading, or performance, explicitly stating the composition it holds; do not make it the default for every shot

`selfie view`, `close-up`, and `handheld` describe a viewpoint, shot size, and shooting method respectively; they do not say where the camera moves. `camera follows` must also specify whom it follows, in which direction, and how it maintains the framing. `Hard cut` is an edit and cannot replace camera movement

Describe the subject action's trajectory, range, speed, and visible result as well, such as “She pushes off into acceleration, takes long strides past three pillars, and her shirt hem flutters backward.” One main camera move can accompany subject movement and environmental response; the person need not stay fixed in place. Usually keep natural speed, using slow motion only to emphasize selected moments. Design cutting frequency and movement within the shot separately

Enter while action is underway and cut at an appropriate action point. State what the subject is doing at the end, how the camera continues, and how the next shot connects. See [Multi-shot examples](#multi-shot-examples) below for specific wording

### Design the first two seconds for social video

Design information, movement, and sound together in the first **two seconds** so viewers immediately have a reason to keep watching:

- **Information**: start with the most compelling result, contrast, question, or ongoing event. Make one point readable at a glance and leave background explanation for later
- **Movement**: enter on clear subject action or camera movement, such as a product rushing into close-up, tracking a person starting to run, or a quick pullback revealing a contrast. Show a visible change immediately; do not wait through a slow empty establishing shot for the content to begin
- **Sound**: in videos with audio, start event-synchronized sound on the first frame. Use a short, forceful line, action sound, or musical downbeat to attract attention, without meaningless silence or a fade-in. When the user requests silence, let the picture carry the hook

All three should work toward the same point. Information density comes from clear events and changes, not a screen full of text or unrelated sound effects. Make the opening work before developing the following shots

### Before submitting

1. **Ready to submit**: are all instructions in English and all placeholders filled? Do the model, total duration, aspect ratio, resolution, attachments, and audio comply with the parameter table above? Are all shots that can fit in one call in the same request?
2. **Consistency**: do characters, products, and any brand or UI that needs accurate depiction use the correct sources? Does each reference map to an actual attachment with a clear role? Are the setting and visual style specific and consistent?
3. **Understandable movement**: can someone reading only the prompt describe each shot's subject action, camera path and speed, composition changes, and cut point? Do not rely on explanations elsewhere that were not carried into the prompt, or reduce action on your own for fidelity
4. **Rhythm and sound**: do cuts serve information and complete action, is audio enabled for audible Seedance footage, with needed ambience and action SFX written into the prompt, do sound effects sync with events, and does dialogue have enough time? Does a social video's first two seconds establish a clear hook?

### Shared shot-number template

**Asset references (required for characters and products) → setting and visual style → one-sentence overview → action beat by beat → close**

Repeat the Shot line for the actual shot count and complete every shot; do not substitute ellipses. Omit `[Assets]` when there are no references; otherwise number references in actual attachment order. Select the reference lines below as needed and add audio references only when there is dialogue and the tool supports timbre references

```text
[Assets]
@Image1 is for {character} appearance, hair, and costume. Do not take the background or pose.
@Image2 is for {location} spatial structure, materials, and light. Do not take the people in the frame.
@Image3 is for {object} shape and material. Do not take the scene around it.
@Audio1 is for {character} timbre and speaking manner. Do not take the words in the sample.
@Image4 is for the whole unit's light, grade, and materials. Do not take the people's action.

[Setting and style]
{location layout, key objects, spatial depth, and the areas used by the action and camera movement}.
Light and grade like {a type of scene from a film}, with a little of {a director}'s usual framing / camera-move habits. Shot on {camera + lens}: {film grain / clean digital}, {focal length or depth of field}. {color temperature}, saturation {high/low}. Key light from {direction}, shadows {deep/shallow}. Visible materials: {wet glass, old wood, metal reflections…}.

[Overview]
{who} is in {where}; {the visible sequence of events across the whole video}. Generate all shots below together in one request.

[Pacing]
{overall rhythm and which beats are quicker or longer, matched to the action and dialogue}.

[Shots — repeat this complete structure for each shot]
Shot {number}: Start at {shot size, camera height, and angle}. The camera {one main movement, direction, path, and pace}, ending with {final framing or maintained position relative to the subject}. {Who acts from where to where, with what speed and range; the visible physical result}. {Exact dialogue and speaker, when present; synchronized action sound and ambience}. Cut on {a visible action point that joins the next shot, or completes the video}.

[Close]
Keep character, wardrobe, setting, and visual style consistent with the written design and any supplied references. Accurately reproduce specific products, logos, webpages, phones, and UI from their supplied references when required. Keep the planned synced dialogue, ambient sound, and action SFX; no watermark, caption bar, or end card.
```

### Common shot patterns

The following shot fragments can be inserted into a complete prompt; supply references, style, and sound consistently for the whole video. Keep one main camera move per beat; subject action and environmental response may occur together

**Spatial atmosphere**

```text
{subject is doing one concrete thing} in {a concrete space}.
Start at {shot size, camera height, and angle}. The camera {one movement with direction, path, and pace} from {starting view} to {ending composition}, revealing {new spatial information}. Use {focal length or depth of field}.
{key-light direction, shadow depth}.
{what you can see in the air: rain streaks, dust, steam}.
Generate synchronized ambient sound and on-set SFX that match the action. No background music; BGM will be added separately.
End or cut as {a specific visible action reaches its planned state}.
```

**Walking follow shot**

```text
Start at {shot size and camera height}, {behind / beside / ahead of} {character}. Track {direction and path} at {speed relative to the character}, keeping {framing and distance} as the character walks from {start} to {destination} across {ground material + light patches}.
The gait is {pace, stride length, and visible body motion}.
Light comes from {direction}.
Cut as {a specific step or gesture occurs}, with {the visible walking state and camera movement at the cut}.
```

**Object reveal**

```text
A {object} with {material and wear} sits on {a surface}.
Start at {camera height, angle, and shot size}. The camera {one selected move, with direction and path} at {explicit pace}, moving from {starting view} to {ending view}.
Key light from {direction}, with {reflection or transmitted light} at the edge.
End on {a concrete visible result or newly revealed detail}. {Specify any planned hand interaction, or state that no person or hand appears}.
```

### Multi-shot examples

Each example below is a complete English prompt, with all its Shots submitted together as one request. Submit total duration, reference slots, and audio settings according to the current tool schema. Adapt the examples to the user's story and product while preserving the approved actions and dialogue

These examples provide images only for people or products that need accurate reproduction; ordinary settings, lighting, and style are described directly in text

**Athlete: push off → side tracking → run into depth**

```text
[Assets]
@Image1 defines the runner's face, hair, and sportswear. Do not copy the reference pose or background.

[Setting and style]
An outdoor red rubber running track, a row of pillars along its outer edge, distant spectator stands. Warm morning side light, cool shadows, a 24mm wide-angle look with readable track texture. Natural-speed athletic action, brisk cuts, roughly two to three seconds per shot. Generate all three shots as one video.

Shot 1: Ground-level shoe close-up from behind and just outside the lane. The camera pushes forward briskly along the track toward the planted rear shoe, tightening on the sole as it drives off the ground. She is already leaning into acceleration; the foot sweeps forward out of the close-up. A sharp shoe scrape starts on the opening frame, followed by forceful footfalls. Hard cut on the next landing.
Shot 2: Waist-height side medium shot. Track parallel to the runner at her speed, keeping her torso centered and the camera-to-runner distance constant. She takes long strides past three pillars, pumping her arms, her shirt hem fluttering backward. Near pillars sweep across the foreground faster than the distant stands. Footfalls quicken with her acceleration. Hard cut as her leading foot lands.
Shot 3: Rear medium-wide view down the lane. The camera tracks forward behind her along the lane, slower than her running speed, so she recedes toward the bend while the track markings pass beneath the camera. Keep her full body in frame as she continues running. Preserve synchronized footfalls and breathing; finish during an ongoing stride and forward camera travel.
```

**Drink product: open the pull tab → pour onto ice → slide the glass into frame**

```text
[Assets]
@Image1 defines the drink can's shape, color, and exact label artwork. Preserve these details as the can moves and rotates.

[Setting and style]
A clear straight-sided glass filled with ice stands on a pale stone bar. Bright side-backlight reveals the silver can, condensation beads, glass edges, and translucent ice. Only the operator's hands enter the frame. Crisp natural-speed actions and brisk cuts; give the pour enough time to read. Generate all three shots as one video.

Shot 1: Start in a tight three-quarter view of the can in one hand. The camera is already pushing briskly toward the top when, on the opening frame, the other hand snaps the pull tab open with a synchronized metallic click and gas hiss. Continue the push to a close-up of the now-open rim and raised tab; condensation beads catch the backlight. Hard cut as the opened can starts to tilt.
Shot 2: Close side view of the glass rim, locked off to make the rising liquid level easy to compare. The tilted can enters from above and pours a continuous stream onto the ice. Ice cubes collide and turn, the liquid rises, and bubbles race up the glass. Keep the rim and impact point in frame with synchronized pouring and ice clinks. Cut as the stream ends.
Shot 3: Bar-height medium close-up; the can is now upright on the right. A hand slides the filled glass from left to right beside it. Track right with the glass at its sliding speed, then continue past its final position far enough to reveal both glass and label together. The glass base scrapes to a stop while the liquid sloshes and settles. Finish during the camera's rightward travel with ripples still visible.
```

**Everyday UGC: lift the lid → pick up and try → turn toward the camera**

```text
[Assets]
@Image1 defines the creator's face, hair, and clothing, not her reference pose.
@Image2 defines the headphones and packaging, including their real structure, colors, and markings.

[Setting and style]
The creator sits behind a pale wooden desk with a plain wall and bookcase behind her. Soft daylight enters from the left. Casual phone footage, natural skin texture, decisive hand movements, natural speed. Brisk cuts between three connected actions, allowing the headphone fitting to finish. Generate all three shots as one video.

Shot 1: Overhead close-up of the box. Lower the camera straight toward the open box in a short, brisk push, ending on the exposed headphones. She is already lifting the lid while her other hand steadies the base. Cardboard friction starts on the opening frame, followed by the lid tapping the desk. Cut as her hands reach for the headphones.
Shot 2: Side medium shot, initially framed from her chest to the box. Raise the camera vertically at the same pace as she lifts the headphones to her head, ending at eye level with her face and both earcups in frame. She puts them on and adjusts both earcups, leaning forward then straightening. Keep handling sounds and clothing rustle synchronized. Cut as her fingers release the earcups.
Shot 3: Front medium shot at eye level. Move the camera backward at a steady walking pace from a chest-up view to a waist-up view that includes the desk. She turns to face the lens, points to the headphones with one hand, and slides the empty box aside with the other. Keep her face and headphones centered while the tabletop enters the wider frame. Preserve the box scrape and room ambience, with no spoken dialogue. Finish as her pointing gesture completes during the pullback.
```

### Local adjustments

Change only one category at a time: visual style / light / camera movement / action intensity / sound. If you change too much, you cannot tell which sentence made the difference

### Patterns that cause problems

| Wrong | Right |
| --- | --- |
| “No blur,” “no broken faces” | “Clear skin texture,” “stable, accurate facial features” |
| Writing people's names by hand on reference images | Bind them through `@ImageN` slots |
