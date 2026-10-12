# 00 · Preflight

Use when the direction of a new short is still unclear. If there is already a clear script or only a local revision is requested, retain the existing settings

Understand the current AI-generation boundaries first, then outline the work clearly. Address what the available information supports, and leave undecided details in the plan for gradual confirmation. Seedance 2.5, Seedance 2.0, and MiniMax share the same creative methods. Choose the video model from the current tool schema according to the work's quality, continuity, reference, audio, duration, latency, and cost needs

## Lock the conditions that would cause rework first

Confirm the aspect ratio and the duration of the finished film or clip; align on these two items first if they are not yet clear. Form a brief plan from audience, location, dialogue, central-image, and other information that can be inferred from the materials

Aspect ratio determines character framing, location composition, and reference-image design; changing it midway usually requires recomposition and additional assets. Duration affects generation-unit breakdown and the rhythm of assembly. Align on these two items first, while the remaining script, asset, and shot-design details can be documented and confirmed gradually

Establish whether the user wants independent clips or a complete short that needs assembly. Deliver one or several independent model clips directly; create a local assembly plan when a finished short is needed

## Prefer generating the complete video in one request

Confirm the single-request duration, reference capacity, and multi-shot support from the current tool schema. By default, generate all shots of the complete video in one request; describe camera-position, scene, or costume changes within the shots. Split into the fewest units only when actual capability limits or independent-delivery requirements demand it; record the reason and prepare joins across units. Assemble them with FFmpeg when needed; units delivered separately remain independent files

The generation window defines the total duration of one request, which can contain several short shots. Keep the number of people and locations restrained, while choosing shot density according to distribution rhythm and story needs; judge these separately

## Choose the expressive direction

The plan should state the audience, playback channel, length, aspect ratio, central image, number of people and locations, dialogue, intended model version, and visual elements to avoid; for longer works, also estimate generation calls. Organize what is known and leave missing items to be clarified

| Form | Main objective | Common finished duration |
| --- | --- | --- |
| Conceptual short | Convey an idea or a particular constraint that matters more than specific plot events, with the plot built around it | 30 seconds–2 minutes |
| Brand short | Let the brand philosophy enter naturally and change the story's direction | 30 seconds–2 minutes |
| Mood / atmosphere film | Establish an atmosphere and let the viewer remain in a feeling | 20–90 seconds |
| Narrative short | A character makes a choice or witnesses an event | 45 seconds–3 minutes |
| Cinematic social short | Establish visual quality and retain viewers through an opening event | 15–60 seconds |

These are reference ranges for forms of work; the user's needs determine the actual delivery

Fewer characters and locations make joins between clips easier. Develop a conceptual short from its central image; for vertical video, consider faces, hands, vertical movement, and the bottom safe area from the concept stage. Look for suitable recent references when the user wants a contemporary feel or social distribution, borrowing structure and visual ingenuity to develop an original story

## When to reference contemporary work

When the user wants the work to be memorable, suited to social posting, or to make a brand feel more current, or when the idea is still an abstraction such as “a lonely rainy night,” refer to relevant good works from the past year. Analyze what makes the premise work, which frame is most compelling and worth taking a screenshot of, which treatments would weaken this film, and how the structure and ingenuity can serve the user's own story

Possible sources of inspiration include near-future technology entering everyday life; one extreme constraint sustaining the whole film; a warm object changing the plot in a cool-toned space; a familiar everyday product; or a contemporary choice in a traditional setting. Use this direction only when the user needs it, and keep the work watchable in one sitting with its own resolution

The more focused the theme, people, and locations, the easier continuity is to maintain across units. Enter through an event already happening, placing background information where viewers actually need it to understand the current choice. Locking the Look, characters, objects, and voices early reduces drift across generations; when enough information is available, the script can still be written first and assets filled in gradually

## Clarify the event and rhythm first

Plot defaults to dialogue, reactions, and actions, with voice-over lightly supplementing background; follow explicit requests for no dialogue, pure atmosphere, or a voice-over video. When synced audio is supported, design and generate lines, lip sync, ambient sound, and action SFX together as the same on-screen event, such as alarms, footsteps, keyboards, doors, buttons, breathing, and room tone. Voice-over only adds facts spanning scenes or background that characters cannot naturally say; character actions carry relationships, choices, and suspense. Arrange non-diegetic music together during assembly; handle actual sources such as an on-screen radio with the shot

First plan how the shots connect. Choose [shot density](../../capabilities/model-video-generation.md#shot-density) according to the platform and content, and describe subject action and camera movement in every shot. For social publication, design the information, movement, and sound in the first two seconds as one hook from the concept stage; see the [model video capability](../../capabilities/model-video-generation.md#design-the-first-two-seconds-for-social-video) for specific guidance

Use Shot 1, Shot 2 numbering in shot designs and prompts, with natural language expressing pace; estimate each unit's total duration in project-management documents, keeping exact per-shot start and end seconds out of model prompts. The density above is creative guidance; confirm the generation window from the live schema

## Asset scope at the start

Consistent recurring character appearance, recurring locations, recognizable objects, and the same character's timbre are default production requirements

On-screen people and products require reference images, following the hero-image and derivation methods in [asset design](02-asset-design.md). Keep settings, lighting, and style consistent through shared written descriptions or suitable reference images; prepare character timbres according to dialogue needs

- Start by describing a setting's layout, movement paths, key light, and landmarks in words. For narrative shorts, a location reference that combines space, lighting, and style is recommended; ordinary settings do not require an image
- Style can usually be described in words. When written descriptions or location images already convey color, light, and materials, no separate style frame is needed
- Shot designs default to text tables converted directly into video prompts. Do not generate a still per shot or force storyboard stills to animate through first-frame / first-last-frame generation. Make a visual storyboard only when the user explicitly needs it or complex action needs a diagram; diagrams do not automatically become video reference assets
- Reuse accurate existing photos of the same person directly. For a new character, establish the hero image first, then derive face, full-body, turnaround, and costume-change images from that same hero image through image-to-image / variation
- For exact brands, pages, device appearance, and typography, use user-provided, official, or already-approved references; prompts specify only which parts of the image to use

Once written descriptions and the necessary character, product, brand, and timbre references are ready, move to shot design and video prompts. Handle ordinary expressions, actions, and camera positions with text; correct references when a specific consistency issue appears. See [asset design](02-asset-design.md) for detailed design and templates

## Resolution and model selection

Choose video and still-image resolution separately from each tool's current schema and the delivery need. More pixels do not compensate for weak references or unstable generation; improve reference quality and prompt clarity before increasing resolution

| Selection dimension | How to judge |
| --- | --- |
| Several plot beats or precise voice alignment | Choose an available model that covers the complete shot design, required duration, and synchronized audio in one request |
| Quality and budget | Compare quality and cost across currently available models; do not write a separate shot design just to change models |
| Reference capacity and audio inputs | Confirm image, video, and audio counts and whether audio can be input independently from the schema; for character shorts, prefer binding timbre to a character image |
| Continuity within one film | Check the conditions for each generation against the version actually selected, keeping output specifications and reference strategy consistent |
| Prompts | Seedance and MiniMax share templates, using shot numbering and written rhythm; generation parameters control total duration |

Choose according to the work's beats, synchronization, reference capacity, quality, and cost. See [model capabilities and generation-unit selection](../../capabilities/model-video-generation.md) for current limits and capability differences

## Record the decisions

Record the confirmed aspect ratio, duration, direction, minimum asset strategy, and undecided information. Use this editable preflight document to move forward, then enter the stage currently being worked on directly
