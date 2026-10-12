# 02 · Asset design

Optional reference-design and derivation templates. Master-reference, consistency, and reference-role rules are in the entry point. Read the relevant section for a specific template.

People and products require reference images, following this chapter's hero-image and derivation methods. Settings, lighting, and style can usually be defined through consistent written descriptions, with reference images added when useful. For narrative shorts, a location image that establishes space, lighting, and style together is recommended; voice references establish timbre consistency. Shot design determines action and camera movement; do not maintain consistency by reducing movement or fixing poses

Asset design serves **consistency, visual quality, and the user's intent**. The character hero images, product designs, and reference methods below also apply to ads and UGC

## Establish the Look first

Specify time and key-light direction, shadows, color temperature, saturation, at most three key materials, and picture character. Concrete window light, wet glass, and warm/cool relationships are more useful than simply saying “cinematic”

Most lighting and style can be described directly in words. For narrative shorts, prefer incorporating the Look into a location image. When written descriptions or location images are sufficient, no separate style frame is needed; add one only for a visual requirement that cannot be expressed clearly otherwise

### Look description template

```text
# Asset design

## Picture Look
Mood: {extract from preflight; if none, fill from the script’s tone}
Time of day: dawn / day / dusk / night / indoor artificial light
Key-light direction:
Shadow depth:
Color-temperature lean: cool / neutral / warm
Saturation: crushed / normal / high
Material keywords (at most 3): e.g. wet glass, old wood, metal reflection
Picture character: fine film grain / clean digital HD / slight edge vignette
Elements to avoid: neon cyberpunk, anime outlines, poster-style type, overexposed beauty-filter looks, etc.
```

One clear style frame can communicate shared lighting, color, and materials more accurately than a mood board with many images. Judge whether existing location references can do this before deciding to generate a separate style frame

### Common picture moods

| Picture mood | Description reference | Suitable uses |
| --- | --- | --- |
| Cool solitude | Low saturation, a hint of cyan in the shadows, a trace of warmth retained in skin | Mood films, night scenes |
| Dusk nostalgia | Amber highlights, natural shadows without an artificial blue cast | Narrative films, conveying brand warmth |
| Clean daylight | Soft window light, light shadows, clearly visible material texture | Object displays, a brand's central image |
| Strong contrast | A single light source, large dark areas, emphasized rim light | Conceptual films, key moments of choice |

## Minimum reference set

| Image type | When needed | How to make it | Must never contain |
| --- | --- | --- | --- |
| Style frame | When the written Look or location image cannot lock the style | Optional; generate 1 first at a resolution suited to the final crop | Readable text, watermarks, unrelated image collages |
| Character hero still | Required whenever a person appears on screen | Reuse an approved character image; for a new character, lock one hero still first, then preferably add any necessary angles or details to the same reference image | Independent text-to-image generations of different versions of the same character |
| Costume/makeup variant | When the script explicitly calls for changed makeup or clothing | Derive from the locked hero still, changing only costume/makeup | A completely different new face |
| Object / product design | Required for products; prepare other objects according to appearance-consistency needs | Reuse accurate materials or an approved hero still; later derivatives preserve the same product's shape, proportions, materials, and markings | Redesigning or changing the product during derivation |
| Logo / brand mark | When it must appear accurately | Use a transparent image / clear hero image provided by the user, from an official source, or from an approved design | A model redrawing it from text or changing the lettering |
| Web / phone / app interface | When a page, layout, or product interaction must be shown accurately | Use approved screenshots, screen-recording keyframes, or UI designs; prepare each state when several are needed | Prompt-fabricated exact pages, typography, or brand content |
| Packaging / devices / typography | When recognizable appearance must remain consistent | Reuse a hero image or approved design; add views to the same image for specific gaps in appearance information | A brand name alone that leaves the model to invent the design |
| Location reference image | When a specific location or complex space is hard to describe in words; recommended for narrative shorts | First define the space and Look in words; when an image is needed, show useful views, movement paths, light sources, and landmarks of the same space while also conveying style | Incidental passersby, collages of unrelated locations |

People and products require references. Choose written descriptions, images, or both for settings, lighting, and style according to what needs to be communicated. Each image conveys clear information, and multiple views refer to the same subject or space; use approved materials for real products, brands, logos, web pages, phones, app UI, packaging, and devices

### Combine supplemental views and details in one reference sheet

**When the same person or product needs additional angles or local details, prefer keeping the main view and necessary supplemental views together in one reference image.** Edit or extend the canvas of the same approved hero image, preserving identity, proportions, materials, colors, and markings across all views to reduce drift from generating separate images. Existing real views can be arranged together while preserving their original content

Check every view against the approved source; combining images that have already drifted does not repair consistency. Reuse sufficient existing materials directly, without adding images just to fill a multi-view sheet. Keep each view clear and readable; use separate images only when one sheet cannot communicate the information clearly, and derive all supplemental images from the same source

This sheet is a unified reference for one subject. Video generation uses its appearance information, while the prompt still determines shots and actions; do not turn the reference layout into a split-screen video

Choose still and video resolutions separately from the current tool schemas and final crop needs. Prioritize clear, consistent reference information rather than merely adding pixels

## Character hero still and derivation process

For the same costume, lock the character's face through text alone once; confirm the hero still before adding the views that are needed. If it needs adjustment, redo and re-lock this one image before continuing derivation. A costume change alters only the required clothing, makeup, or hairstyle while retaining bone structure and body shape

Prefer GPT Image 2 for the first character hero still, using the model identifier exposed by the current image tool schema. The hero still should make the face, hair, clothing, and body recognizable. Derive face and full-body references from the same hero still so two independent text-to-image generations do not produce different faces

### Hero-still confirmation steps

```text
1. Write the character’s visible design details explicitly.
2. Use only one text-to-image call for the character hero still, on a neutral solid background and at a resolution suited to the final crop. Prefer a hero that fully shows face, hair, clothes, and body.
3. Confirm the hero still by hand. If it is not right, redo and re-lock this one still only. Do not keep producing other angles at the same time.
4. After the hero still is locked, derive any needed face detail, full-body supplement, turnaround, or costume/makeup variant from it via image-to-image / variation. Prefer one reference sheet that retains the approved main view and adds the necessary views on the same canvas. Check that every view preserves the same identity; do not generate independent faces and combine them afterward.
```

Use a neutral background and natural expression for newly made character references. Keep object hero stills separate from people; describe the action of a person holding the object in the video prompt. When a location image is needed, it can show a few consistent views of the same space on one canvas

A neutral background keeps the character asset independent; written setting descriptions or necessary location images describe room furniture. State the purpose of hero stills, existing photographs, and derivatives; multiple angles of the same character must clearly refer to the same person

### Purpose of costume/makeup variants

A costume/makeup variant shows clothing, makeup, or hair needed in another scene; preferably add character angles and close-up details to that character's unified reference sheet. A variant must retain the same bone structure and overall body shape, changing only what needs to change. Reuse the existing hero still when no costume change is needed

### Character description form

```text
Character name: {must match the script exactly}
Apparent age:
Face: contour, brow and eye traits, any obvious mole or scar (write “none” if none)
Hair: color, length, current state
Clothes and makeup: layers, color, and material of this costume
Body: height and build, way of walking
Signature details (at most two, and they must read on both the full-body still and the close-up):
Hero still status: awaiting generation / locked (main view and any necessary detail views on one reference sheet)
Costume/makeup variants: none / list each required set
Voice timbre: no dialogue / sample awaiting generation / locked (duration accepted by the selected tool)
```

Use the [model image capability](../../SKILL.md#generate-missing-assets) for necessary new stills and [speech generation](../../SKILL.md#generate-missing-assets) for a new character voice. Reuse existing images or recordings directly

## Lock the timbre

Establish the timbre of characters with dialogue or noticeable vocalization during the asset stage. Fix one timbre reference per character and reuse it in every relevant later unit

### Timbre confirmation steps

```text
1. Use the platform voice tool or an existing recording to generate a clean single-person dry-speech sample within the selected tool's current duration limits.
2. The line can be a line from the script, or a tone-neutral read. No background music, and no other voices.
3. After you listen and confirm timbre and duration, lock it in the design pack. Later generation only cites (@) this one audio.
4. If it is not right, regenerate this audio. Never swap voices frequently across different video clips.
```

Use the shortest sample that reliably captures timbre and speaking habits under the current tool contract, reducing the chance that the model also copies specific words and breathing pauses from a long recording. Use a script line or a tone-neutral test read; when listening, confirm the voice, cleanliness, and duration together

### Timbre-reference sentence for video

```text
@Audio1 is the timbre and speaking-style reference for {character name}. Do not take the specific lines, ambient sound, or any background music from this recording.
```

Whether the chosen model accepts audio-only input or requires an accompanying image or video follows the live schema. When audio-only references can guide rhythm or tone, character shorts still prefer binding timbre to a character image to keep the voice matched to visible identity

## Object and product design pack

Products require accurate references; prepare ordinary objects such as letters, desk lamps, and paper boats according to appearance-consistency needs. First confirm the product hero image or existing design materials. Derivatives preserve the same product's shape, materials, colors, and markings; follow the existing object hero-image and derivation process below

| View | What it shows | When to add it to the unified reference sheet |
| --- | --- | --- |
| Hero still · front | The side that best shows the object's features and makes it recognizable at a glance | Products require accurate references; prefer reusing existing approved materials |
| 3/4 or true profile | Shows thickness, openings, buttons, or edge details | Add it when existing materials do not cover appearance that must be shown accurately; derive from the same source |
| Back or top | Shows ports, wear, or label placement | Reuse existing views first; add one only when appearance information needed by a shot is missing |
| Material close-up | Shows scratches, printed detail, glass reflections, or fabric weave | Add it when existing images do not clearly show the texture details that need to appear |

Before adding an image, state the specific information missing from the existing materials. Picking up, wearing, turning, orbiting, or shooting a macro close-up is not by itself a reason to add a reference; reuse approved images directly when they support these actions and framings. For unseen connectors, structures, or text on a real product, obtain user-provided, official, or approved design materials; image-to-image derivatives are not evidence of these unknown details

An object hero still shows the object alone; the video prompt describes a person finally picking it up, using it, or turning it. This keeps the object asset independent and lets the same object be reused in different locations

## Logo, web, phone, and interface assets

Logos, product pages, phone appearance, app UI, packaging, device panels, and brand typography are consistency assets that need accurate recognition. Use user-provided, official, or approved design images, and first determine every state that must be shown

- Use `@ImageN` only to specify the logo, page layout, phone appearance, or interface state; other backgrounds follow the current shot design
- For different interaction states of the same page or app, prepare the screenshots or keyframes that need to appear accurately; ordinary camera-position changes reuse these state references
- Retain real brands and web pages when they need to appear; constrain their text, layout, and appearance with reference images so the model does not rewrite brand content
- Readable text, logos, and layouts are information to preserve; random garbage characters, misspellings, and brand variants without references are quality-check items

## Static-reference generation templates

Call the image tools exposed by the current session and select a supported resolution appropriate for the final crop. The templates below are for static references; video generation uses the action, camera-movement, and sound prompts of the next stage

### Style-frame template

```text
Generate one cinematic still — not a movie poster.
Space: {specific interior or exterior; describe visible furniture or street elements}
Time and light: {key-light direction, hard or soft light, whether there is clear volume light}
Color temperature and contrast: {extract from the Look}
A back figure or an empty chair may appear, but there must be no frontal face close-up and no readable type.
Aspect ratio {aspect ratio}. It should feel like a frozen 24fps film frame, with fine film grain.
Avoid: illustration, anime, subtitle bars, unreferenced logos or brand content, multi-image collage.
```

### Full-body character hero-still template

Use for the only text-only face lock for the same costume; confirm the hero still before making the derivatives below

```text
This is the character-design hero still. It needs to be a full-body still. This is not a fashion campaign, and not a shot-design sketch.
Character: {visible appearance, including signature details}
The person is frontal or slightly turned toward camera. Head-to-toe including shoes must be fully visible, standing on a neutral solid background.
Light should be even, so face and clothing detail are both clearly readable.
Expression stays neutral, mouth naturally closed, hands hanging naturally.
Use a supported resolution appropriate for the final crop. Establish one primary full-body view, without type, watermark, or unrelated people or images.
```

### Derived face close-up template

When face details are genuinely needed, attach the locked character hero still and use image-to-image / variation to add a close-up to the same reference image, retaining the main view to constrain identity together

```text
@HeroImage is this character's approved identity source. Edit or extend it into one reference sheet: retain the approved main view and add a readable shoulders-up face detail on the same canvas.
Both views depict the same person. Bone structure, skin traits, hair, clothes, and makeup must match @HeroImage exactly. Change the framing of the detail view, not the identity.
Use a neutral solid background, with both views clearly separated and readable. Output one image at a supported resolution appropriate for the final crop, not separate images or unrelated faces. Do not change face shape or makeup.
```

### Costume/makeup variant template

```text
This is another costume/makeup for the same character, absolutely not a new character.
Facial bone structure and body must match the reference still @HeroImage exactly. Change only the following: {specific makeup / hair / clothes for this scene}.
Retain the approved main view and add the requested full-body costume/makeup view on the same reference sheet. Include a face detail only if needed for readability. Keep the intended costume change distinct while preserving one identity across all views. Use a neutral solid background and output one image at a supported resolution appropriate for the final crop, not separate independently generated portraits.
Do not invent a prettier face. Character traits must stay consistent.
```

Make variants after confirming the hero still; when a variant drifts, return to the hero still for adjustment and use the same identity as the basis for regeneration

### Empty-location template

```text
Generate one location reference still with no people, in a single pass. The same canvas may clearly show 2–3 mutually consistent useful views of the same space, to explain circulation, spatial relationships, and key-light position. They must belong to the same location, not a collage of unrelated pictures.
Location: {must match the place name in the script exactly}
The picture needs to show clearly: spatial depth, ground material, key-light position, and one or two signature objects.
Light atmosphere and color temperature inherit the locked Look. If an optional style frame exists, also stay consistent with it.
The frame must have no people and no post-added subtitles, and must not look like a bright, hard real-estate listing.
```

### Object hero-still template

```text
This is the still-life design hero still.
Object: {material, wear, color, sense of size, signature details}
Use one primary front view that makes the object recognizable at a glance. If additional views are requested, place only those necessary views of this same object on the same canvas, with matching geometry, material, color, and markings.
Keep the background clean. Light: {use side light or similar so material quality reads}.
No hands or specific use scene. Keep every included view clearly readable; do not include unrelated objects or conflicting designs.
```

### Object turnaround or close-up template

```text
Edit or extend @HeroImage into one reference sheet for the same object. Retain its approved main view and add {the specific necessary angle or detail} on the same canvas.
Silhouette, proportions, material, wear, color, and markings must remain consistent across every view. Use the supplied verified source for any real product detail; do not invent unseen connectors, structures, or lettering.
Keep a clean background and consistent lighting, with the main view and detail clearly readable. Output one image containing these related views, not separate newly designed versions. Preserve the original label text exactly.
```

## Complete template for extracting assets from the script

```text
Read the provided Concept and Script. Prepare image references for people and products, and define the written descriptions and optional images for settings, lighting, and style.

Keep the output structured. Do not write it as a long essay:

1. Picture Look: describe light, color, materials, and framing in words. A separate style image is usually unnecessary. For narrative shorts, prefer a location reference that also establishes the Look when useful.
2. Fixed character list: list the single approved identity source first. Derive needed face, full-body, and costume/makeup views from it, preferably together on one reference sheet with the approved main view. Do not text-to-image independent versions of the same person.
3. Product and object list: reuse approved product references. If a specific visual detail is missing, prefer adding its verified view to the same reference sheet, preserving one design across all views. Ordinary background objects can be described in words unless their exact appearance needs a reference.
4. Brand and UI list: list products, logos, web pages, phones, app UI, packaging, and devices that must appear accurately, and assign a user-provided, official, or already-approved reference still to each necessary state.
5. Locations: describe layout, movement areas, light, and landmarks in words. Images are optional for simple settings; recommend a location image that also establishes style for narrative shorts, or use one when a specific or complex space needs visual grounding. Explain which gap each selected image addresses.
6. Voice-timbre needs: which speaking characters need a locked timbre, and how to generate a concise clean sample accepted by the selected tool.

Extraction rules:
- Passing crowds or one-off background plates do not go on the asset list.
- Every name must match the script exactly.
- Make the process explicit: a character is allowed only one text-to-image face lock; the hero still must be reviewed and approved before other stills are derived.
- Spec: stills use a consistent supported resolution appropriate for the intended video crop.
- Do not generate story-state stills for ordinary shots, expressions, poses, or camera positions.
```

## Inherit only the information needed when attaching references

Reuse approved character and product references. Character references provide appearance and clothing; object references provide shape; the current shot design determines background and pose. Settings and lighting can be described in words; explain a location image's purpose when using one. Timbre references provide only voice characteristics and speaking style; design dialogue, ambient sound, and music for the current shot

Show brands, packaging text, and UI according to approved reference designs. Use slot names supported by the model tool and bind them in attachment order

When one image contains multiple angles or details, explain in one reference binding that the views depict the same subject and what each contributes; explicitly exclude the multi-view layout. For example: `@Image1 shows the same product in a main view and detail views. Use them together for consistent appearance and structure; render one product in the scene, not the reference-sheet layout.`

Character and product derivatives inherit the approved hero image; use an approved variant for a costume change. Reuse written descriptions of settings, lighting, and style across shots; use approved current-state images for brands and UI

Character images provide only appearance and clothing, location images only space and light, and timbre only vocal identity and speaking style; state explicitly that the original character background and pose, people in the location image, and sample dialogue are not to be used. Bind each reference to the actual `@Image1`, `@ImageN`, or `@Audio` slot and explain its purpose so the tool knows who or what each resource represents

## Stopping conditions and outputs

Finish asset preparation once written descriptions and character, product, and voice references are confirmed. Put ordinary expressions, actions, and camera positions in video prompts; when generation reveals a specific consistency issue, correct it using this chapter's hero-image and derivation methods

References for on-screen people and products must be complete. Do not count settings, lighting, or style as missing required images when written descriptions can express them. Location and style references are recommended for narrative shorts, with actual use determined by visual needs; prepare dialogue timbres according to voice needs

Organize the asset document as Look, optional-style-frame judgment, character hero stills and derivatives and costume changes, timbres, minimum key objects, brand states, main locations, file paths, and stopping checks. Record locked references and actual paths, unfinished items, and the stopping-condition check. Mark unlocked references as pending; shot design can begin before assets are complete, while video generation that depends on those references begins after they are filled in
