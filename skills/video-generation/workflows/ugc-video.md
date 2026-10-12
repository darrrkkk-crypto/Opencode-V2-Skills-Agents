# UGC and Creator Recommendations

Use this for creator unboxings, reviews, first-person experiences, AI on-camera shorts, and vertical feed ads. The aim is a believable, authentic creator speaking to camera, with a consistent creator throughout and believable settings that may change with the content

## Establish Credible Content First

A common sequence is an authentic opening, shared pain point, hands-on use, specific judgment, and a way to act. Short videos can combine beats; highlight one experience per video and choose beats according to the content

Use confirmed materials for products, offers, conclusions about the experience, and user feedback. For existing selfie footage, select takes and product details directly. The templates and examples below demonstrate creative methods; use content confirmed for the current project in the actual copy

When the user supplies a reference to adapt or recreate, preserve each beat’s purpose, especially the later proof and close. Rewrite the operation, camera setup, and required time for the new product’s actual mechanism instead of copying the original product action. For a request to borrow only a specific passage’s camerawork, stay within that scope

## Five Creative Baselines

1. **One face.** Reuse the same character master reference throughout, keeping facial features, hair, and clothing consistent. Prefer GPT Image 2 for the first character master reference, using the model identifier exposed by the current image tool schema. Derive different angles, outfit changes, and creator-product composites from the approved master image
2. **Believable settings.** Use indoor or outdoor locations, and change locations when the content calls for it. Prefer natural daylight outdoors and keep the overall image authentic. Describe the layout, key objects, and light for each scene, keeping light, time of day, and weather coherent within that scene; the whole video need not stay in one room. Add a location reference image when a specific space or complex layout needs accurate reproduction
3. **The real product.** Use approved product images or real footage, accurately preserving proportions, shape, packaging materials, label layout, hardware, and branding
4. **Arrange copy separately.** When compositing is needed, put prices, offers, and CTAs on separate title layers; preserve the text and branding on real packaging according to the product reference
5. **Separate the sound.** Generate dialogue and ambient sound together with voiced creator clips, and prepare the final music separately; align them during local assembly when the work requires it

Use the entry point for reference, image, and video generation rules. Read [asset templates](creative-shorts/02-asset-design.md) or [video prompt examples](../capabilities/model-video-generation.md) only for a concrete example beyond those rules.

## Image Prompt Structure

For character references, setting plates, and product composites, describe the subject, appearance or materials, space, light, photographic composition, style, and fidelity boundaries in the same order:

```text
subject → appearance or material detail → scene and background → light → camera and composition → style and quality → a concise fidelity or style clamp
```

Build realism through concrete photographic conditions; the following indoor examples can be adapted to outdoor natural light:

- Front-facing phone camera: `mixed indoor light, slightly uneven exposure, soft shadow under the chin, light sensor grain, natural skin texture`
- A natural, unretouched appearance: `available natural light appropriate to the location, untouched natural skin with visible pores and minor imperfections, background kept in focus, relaxed spontaneous selfie posture`

Indoors, use available room or window light; outdoors, prefer natural daylight. Keep the lighting believable for the location rather than defaulting to a studio or ring-light look. Retain raw skin texture and small imperfections, keep the background recognizably in focus, and use a casual selfie posture. The person's credibility then comes from light, skin texture, composition, and action, rather than excessive polish

<a id="ugc-image-1-template"></a>
### Template 1: Creator Archetype Reference

Use this to establish the shared character identity for later derivatives. Set the person's age and appearance, clothing, background, light, and phone-camera texture in this one master image

```text
Front-facing head-and-shoulders portrait of a believable <CREATOR_ARCHETYPE>, <AGE_AND_APPEARANCE>, <WARDROBE>; simple <BACKGROUND>; <LIGHT_DIRECTION_AND_QUALITY>; eye-level framing; natural skin texture, believable front-camera selfie detail, slight grain; available natural light appropriate to the location, untouched natural skin with visible pores and minor imperfections, background kept in focus, relaxed spontaneous selfie posture
```

<a id="ugc-image-1-example"></a>
#### Complete Example: At-Home Tech Creator

```text
Front-facing head-and-shoulders portrait of a believable female tech creator, late twenties with loosely tied dark brown hair and a casual beige crew-neck sweater; simple modern home office background with a soft plant leaf; warm morning window light from camera left; eye-level framing; natural skin texture, believable front-camera selfie detail, slight grain; available room and window light only, untouched natural skin with visible pores and minor imperfections, background kept in focus, relaxed spontaneous selfie posture
```

<a id="ugc-image-2-template"></a>
### Template 2: Setting Continuity Plate

Use when a location reference image is needed. Place the approved person in the chosen indoor or outdoor location, showing its layout, key objects, light direction, time of day, and clothing. The camera height and shot size in this image explain the space; shot design determines the video camera positions. Skip this image when written descriptions sufficiently describe the setting

```text
Compose the person from Figure 1 at <LOCATION>. Lock an eye-level <SHOT_SIZE> camera, <LIGHT_DIRECTION>, <ENVIRONMENT_FEATURES>, <KEY_OBJECTS>, <TIME_OF_DAY>, and <WARDROBE>. Natural creator-video realism. This is the continuity reference for later shots. The frame contains the person and setting; promotional text is prepared as a separate title layer
```

<a id="ugc-image-2-example"></a>
#### Complete Example: Morning-Light Bathroom

```text
Compose the person from Figure 1 inside a bright modern bathroom with white subway tile walls and a clean wooden vanity counter. Lock an eye-level waist-up camera, soft diffused daylight from right window, light oak mirror frame, 9 a.m. morning light, and cream-colored linen shirt. Natural creator-video realism. This is the continuity reference for later shots. The frame contains the person and setting; promotional text is prepared as a separate title layer
```

<a id="ugc-image-3-template"></a>
### Template 3: Creator Holding the Product Hero Frame

Use separately approved references for the character identity and product angle. During compositing, preserve the product's label orientation, material, cap, hardware, and colors, keeping the gesture natural and the important product details visible

```text
Figure 1 is the approved creator identity. Figure 2 is the verified <PRODUCT_ANGLE>. Compose the person from Figure 1 naturally holding the product from Figure 2 with the verified angle facing the camera. Match <SETTING_PLATE> camera distance and light direction. Preserve packaging proportions, label layout, material, cap, hardware, and color exactly. Keep the hand natural and the product unobstructed. Preserve only the verified product markings; promotional text is prepared as a separate title layer
```

<a id="ugc-image-3-example"></a>
#### Complete Example: Holding a Serum Bottle

```text
Figure 1 is the approved creator identity. Figure 2 is the verified front-facing 50ml glass serum bottle. Compose the person from Figure 1 naturally holding the product from Figure 2 at chest level with the verified front label facing the camera. Match bathroom setting plate camera distance and morning light direction. Preserve packaging proportions, label layout, amber glass material, white dropper cap, and gold branding exactly. Keep the hand relaxed and the label unobstructed. Preserve only the verified product markings; promotional text is prepared as a separate title layer
```

## Video Generation Routes

By default, generate the complete video's selfie, product-detail, use, and feedback shots together in one request. Check the single-call range in the [model video capability](../capabilities/model-video-generation.md#default-plan-the-complete-multi-shot-video) before deciding whether splitting is necessary

| Route | Input selection | Performance strengths | Confirm when calling |
| --- | --- | --- | --- |
| Continuous performance with multiple references | Reuse approved character and product references; location images are optional, and prepare timbre references according to dialogue needs | Multi-beat performance, switching front and rear cameras, synchronized dialogue, and continuity of props and angles | Use the live schema for the current window, reference capacity, and image/audio combinations |
| Short shot from one composite hero frame | One approved creator-product composite frame | One simple physical action, product macro shots, and high-fidelity detail | The current tool's single-reference route and audio support; configure for ambience/interaction sound when that is all that is needed |

Bind `@ImageN` according to the actual attachment order, stating which character identity, product design, or setting information each image supplies; the current tool determines exact durations and attachment limits

## Phone Camera Positions and Prompt Rules

- Use specific camera positions such as `iPhone front-camera selfie view`, `iPhone rear-camera close-up`, or `Overhead desk view`, giving the phone-video look a concrete camera position
- For every shot, state where the camera starts, its direction, path, and speed, and the ending composition. `selfie`, `handheld`, and `close-up` do not replace camera movement; see [describe camera movement and action in every shot](../capabilities/model-video-generation.md#describe-camera-movement-and-action-in-every-shot)
- Use one readable action per shot; let product close-ups show the process and result, with natural gestures that leave the label or key parts visible
- Give reactions a visible trigger: she first checks the operation or result, then looks up, nods, or briefly smiles. Choose one or two actions suited to the content rather than a constant smile or an invented trigger
- When action and dialogue can overlap, allow time for the longer one; when operating, checking the result, and speaking must happen in sequence, allow time for each stage. Judge the load by reading the lines and considering the actual action, without cutting sentences or speeding everything up to fit
- Match cuts to the platform and content using [shot density](../capabilities/model-video-generation.md#shot-density), and use `Hard cut` or similar wording to describe the transition between shots. For a single-shot clip, describe the ending action directly without inventing a cut
- Follow the [first-two-seconds hook guidance](../capabilities/model-video-generation.md#design-the-first-two-seconds-for-social-video): show the strongest use result, contrast, or event, synchronizing brief dialogue or interaction sounds with the action
- Spell out the pronunciation of difficult brand names in generated dialogue, such as `A I`, `manus dot im`, or `I V`; retain the correct brand spelling in subtitles
- For voiced clips, specify synchronized dialogue, product interaction sounds, and the location's ambient sound; prepare final BGM as a separate audio track
- Use shot numbers and natural-language pacing for multiple shots, putting the total duration in the parameters supported by the tool; the durations below describe creative rhythm only. Write all model instructions in English, retain specified dialogue and on-screen text verbatim, and replace every placeholder before submitting

<a id="ugc-video-a-template"></a>
### Template A: Single-Action Selfie

A creative rhythm of approximately 3–8 seconds suits one natural action and one conversational line; follow the current schema for the actual generation range. Attach the necessary character and product references, and describe the setting and light directly in words; reuse a suitable existing creator-in-setting image when available

```text
@Image1 is the approved creator identity and wardrobe. @Image2 is the verified <PRODUCT_ANGLE>. Preserve her face, wardrobe, and product details.
Setting: <SETTING_LAYOUT_AND_KEY_OBJECTS>. Lighting: <LIGHT_DIRECTION_AND_QUALITY>.

One continuous shot, iPhone front-camera selfie view at eye level, starting at <STARTING_FRAMING>. She <ONE_ACTION_WITH_DIRECTION_AND_RANGE>. The camera <DIRECTION_PATH_AND_PACE>, ending at <ENDING_FRAMING> with her face and product readable. She says: "<DIALOGUE_LINE>" with sincere, conversational delivery. End as <ACTION_COMPLETES>, after the full line.

Style: casual phone footage, natural skin texture, <LIGHT_DIRECTION_AND_QUALITY>. Source audio: synchronized dialogue, <ACTION_SOUND>, and quiet <LOCATION> ambient sound; no added background music.
```

<a id="ugc-video-a-example"></a>
#### Complete Example: Showing a Serum Bottle

```text
@Image1 defines the approved creator's face, cream sweater, and bright bathroom setting, not a fixed pose. @Image2 defines the serum bottle's shape, amber glass, cap, and label layout.

One continuous shot, iPhone front-camera selfie view at eye level. Start chest-up as she lifts the bottle from chest level to beside her cheek, label facing the lens. With her other hand she brings the phone closer at a steady arm movement, tightening from chest-up to a face-and-bottle close-up. Keep the bottle beside her face so both remain readable. From the opening frame she says: "This is the one skincare step I actually refuse to skip." Use sincere, conversational delivery and a natural smile. End after the complete line, with the bottle beside her cheek.

Style: casual phone footage, natural skin texture, soft daylight from the right-side bathroom window. Source audio: synchronized dialogue, clothing rustle, and quiet bathroom room tone; no added background music.
```

<a id="ugc-video-b-template"></a>
### Template B: Continuous Multi-Beat Performance

An illustrative creative rhythm of approximately 8–15 seconds: a selfie opening, product use, then a return to the person for a judgment. These are three content beats; the total duration and pacing determine the shot count. When needed, expand product use into multiple shots that each add new information. Repeat the middle-shot structure below, fill in the actual actions and camera movements, and number the shots consecutively. Bind character and product references to slots according to the actual inputs; the setting can be described in words

```text
@Image1 defines the creator's face, hair, and wardrobe. @Image2 defines the product's verified shape, materials, hardware, and markings. Do not copy the reference poses or backgrounds.
Setting: <SETTING_LAYOUT_AND_KEY_OBJECTS>. Style: vertical phone footage, <LIGHT_DESCRIPTION>, natural skin texture. Pacing: <RHYTHM_SUITED_TO_ACTION_AND_DIALOGUE>. Generate all planned shots together.

Shot 1: iPhone front-camera selfie view at <HEIGHT_AND_STARTING_FRAMING>. She <ACTION_1_WITH_PATH_AND_SPEED>. The camera <DIRECTION_PATH_AND_PACE>, ending with <ENDING_FRAMING>. From the opening frame she says: "<HOOK_LINE>". Hard cut on <ACTION_POINT>.
Shot <NEXT_NUMBER>: iPhone rear-camera product close-up from <STARTING_ANGLE>. She <PRODUCT_OPERATION_AND_VISIBLE_RESULT>. The camera <DIRECTION_PATH_AND_PACE>, keeping <KEY_PRODUCT_DETAIL> visible and ending at <ENDING_FRAMING>. Synchronize <PRODUCT_SOUND> with the operation. Hard cut on <ACTION_POINT>.
Shot <FINAL_NUMBER>: iPhone front-camera selfie view at <HEIGHT_AND_STARTING_FRAMING>. She <FINAL_ACTION_WITH_PATH_AND_SPEED>. The camera <DIRECTION_PATH_AND_PACE>, ending with <ENDING_FRAMING>. She says: "<CTA_LINE>". End as <FINAL_ACTION_COMPLETES>, after the full line.

Keep the same creator and product across shots, with coherent setting, light, time of day, and weather within each scene. Use each new scene’s specified setting when the location changes. Source audio: synchronized dialogue, specified product interaction sounds, and <LOCATION> ambient sound; no added background music.
```

<a id="ugc-video-b-example"></a>
#### Complete Example: Desktop Device Experience

This example uses approximately 15 seconds and six shots for a front-camera introduction, rear-camera detail demonstration, and front-camera feedback. Submit all shots together, with the actual total duration following the current schema. Dialogue can continue across cuts; a longer spoken line does not require staying on the same face throughout

The experience claims below demonstrate the structure; replace them with confirmed product facts in actual production

```text
@Image1 defines the creator's face, hair, and wardrobe. @Image2 defines the device's matte-black casing, verified ports, proportions, and markings. Do not copy the reference poses or backgrounds.
Setting: a home office with a light wood desk and laptop, lit by daylight from the left window. Vertical phone footage, natural skin texture. Brisk cuts, mostly two to three seconds per shot, with the spoken sentence continuing across Shots 4 and 5. Generate all six shots together.

Shot 1: Eye-level iPhone front-camera selfie, chest-up. She lifts the device toward the lens while drawing the phone closer with her other hand, tightening to a face-and-device close-up. From the opening frame she says: "Three dongles. One device." Keep her face above the device and the casing readable in the foreground. Hard cut as the lift finishes.
Shot 2: iPhone rear-camera close-up of the device lying on the desk beside the laptop. Track left to right parallel to its long edge at the speed of her fingers moving along the casing, maintaining the same close distance. Her nail taps the metal with a crisp synchronized click. Hard cut on the tap.
Shot 3: iPhone rear-camera desk close-up at a 45-degree downward angle, showing the device's top and front edge. Push diagonally down and forward at a brisk, steady pace as she rotates the device a quarter-turn on the desk, bringing its port edge around to face the lens. End tightly framed on that side edge, with the verified port openings and layout visible below the top surface. Synchronize the casing's scrape against the wood. Hard cut when the port edge faces the lens.
Shot 4: Eye-level iPhone front-camera medium shot with the desk in the foreground. She lifts the device from beside the laptop to shoulder level. Tilt the camera upward at the pace of the lift, ending chest-up with her face and the device together. She starts: "It replaced three different dongles…" Hard cut as the device reaches shoulder level, continuing the same sentence into the next shot.
Shot 5: iPhone rear-camera close-up of the device still held at shoulder level. Push forward from the whole device to a tight view of its verified ports as she finishes off-camera: "…on day one." Keep the same speaker and continuous delivery. Hard cut as she starts lowering the device.
Shot 6: Eye-level iPhone front-camera selfie, chest-up. She extends her phone-holding arm at a steady pace, pulling the camera back to include the desk as she sets the device beside the laptop with her free hand. She then points down toward the bottom edge of frame and says: "Link is below." End after the line and pointing gesture, during the pullback.

Keep the same identity, wardrobe, product, room, and light. Source audio: synchronized dialogue, the specified tap and scrape, product handling sounds, and home office room tone; no added background music.
```

<a id="ugc-video-c-template"></a>
### Template C: Product Detail

A creative rhythm of approximately 3–10 seconds suits one clear physical action. Lock the camera position, action, materials, hardware, label, and ending state together, with sound built around actual product interaction

```text
@Image1 defines the approved creator's appearance and the verified product's proportions, materials, hardware, and label layout, not a fixed pose or camera position.
Setting and light: <LOCATION_SURFACE_AND_LIGHT_DIRECTION>. One continuous phone-camera shot starting at <HEIGHT_ANGLE_AND_FRAMING>. She <ONE_PHYSICAL_ACTION_WITH_PATH_SPEED_AND_RESULT>. The camera <DIRECTION_PATH_AND_PACE>, ending with <FINAL_FRAMING_THAT_REVEALS_THE_RESULT>. End when <ACTION_COMPLETES>. Preserve the referenced appearance and product details throughout the movement. Source audio: <SYNCHRONIZED_PRODUCT_SOUND> and <LOCATION> ambient sound; no added background music.
```

<a id="ugc-video-c-example"></a>
#### Complete Example: Dropper and Serum Texture

```text
@Image1 defines the approved creator's hands and the serum bottle's amber glass, white dropper cap, and exact label layout, not a fixed pose or camera position.
One continuous rear-phone-camera close-up at a 45-degree downward angle over a wooden bathroom vanity, lit by soft window light from the right. Start with the bottle, both hands, and dropper in view. She unscrews and lifts the dropper at a natural pace, moves its tip over the back of her other hand, and squeezes out one clear drop. The camera pushes diagonally forward and right from the bottle-and-hands view toward the receiving hand, keeping the dropper tip visible and ending on the drop spreading across the skin. Keep the referenced bottle design unchanged. End as the drop spreads, with a synchronized cap click, quiet handling sounds, and bathroom room tone; no dialogue or added background music.
```

<a id="ugc-five-beat-table"></a>
## Five-Beat Director's Table

The following editing-window example for a 15–30-second finished video helps allocate information and sound; model prompts still use shot numbers. Short videos can combine beats according to the content

| Beat | Window | Camera and action | Example line | Direction |
| --- | --- | --- | --- | --- |
| **Authentic opening** | 0–2s | The product quickly enters close-up, or immediately show a before-and-after contrast | “Three dongles. One device.” | Synchronize action, camera movement, and sound from the first frame so the core information is immediately clear |
| **Shared pain point** | 2–8s | Frustration, a mess | “This used to take me two hours every time.” | Cut to pain-point footage, increase the pace |
| **Hands-on use** | 8–20s | Overhead or macro view of use | “Watch, one scoop and it just melts in.” | Product close-up, actual result |
| **Honest judgment** | 20–25s | Return to the creator, satisfied | “Two weeks in and everyone is asking me for the link.” | Build trust through a specific experience |
| **Call to action** | 25–30s | Offer card and bold text | “There's a deal today, tap the corner.” | Prominent CTA title, musical resolution |

## Completion Criteria and Delivery

- The character and product match their necessary references; each scene’s setting, lighting, and style match its written description or location images in use
- The portrait retains natural light, skin texture, a clear background, and a relaxed posture, with a believable person and gestures
- The chosen route, duration, and reference combination fit the live schema
- Every video prompt has an explicit phone camera position, with the required dialogue, lip sync, interaction sounds, and ambient sound matched
- Every shot clearly describes camera movement; for social publication, check whether information, movement, and sound together engage the viewer in the first two seconds
- Actions and information join cleanly across numbered shots; product use and results are clear, and judgments about the experience have a basis
- When a finished composite is needed, keep subtitles and CTAs inside the vertical safe area and music below the voice

Deliver one or more independently generated clips directly. Use local file-based assembly when the user requests a finished video, placing the final music, offer cards, and CTA text there
