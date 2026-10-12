# Motion Graphics works

Use this workflow for complete works led by typography, graphics, data, UI, or brand motion, and for rendered lower thirds, animated keywords, data animations, logo stings, and transition elements. Follow the established direction when adding graphics to an existing video.

Read [Sandbox rendering guidance](../references/motion-graphics.md) before implementation.

## Define the picture's role

**Full-frame works** own the background and communicate through composition, hierarchy, color, and movement. Define what each section communicates and how the picture changes, then design its entrance, stable reading hold, and transition.

**Overlays** serve footage underneath. Use transparency when the available renderer and requested delivery format support it. Leave space for people, subtitles, and key actions, and align each entrance with the word, number, or event being emphasized.

## Common graphic types

| Graphic | Typical use | Content guidance | Motion rhythm |
| --- | --- | --- | --- |
| Lower third | A person's first appearance or chapter cue | At most two short lines | quick entrance, readable hold, complete exit |
| Animated keyword | Emphasize a pain point or quotable phrase | One main phrase | decisive entrance, stable hold, restrained exit |
| Data or chart | Comparisons, progress, or results | One primary relationship at a time | reveal or count, highlighted hold, transition |
| Logo sting | Opening or closing brand moment | Approved logo asset | assembly or reveal, clear brand hold |

These are patterns rather than fixed durations. Size the reading hold to the actual content and target audience.

## Typography, timing, and layers

Keep one main focus at every moment. Let movement land one information point and keep decoration secondary. Translation, scale, masks, stroke reveals, and number interpolation should clarify relationships rather than merely add activity.

Use the supplied brand palette, typography, logos, and UI assets. Keep essential text within safe areas and clear of subtitles or platform controls. When font files are unavailable, choose a deliberate local fallback and disclose the substitution.

Pair sound only with meaningful movement: a restrained whoosh for a reveal, a click or pop for a snap, or a chime for a completed value. Align it to the exact motion event. Keep overlays silent when the destination edit is expected to provide sound.

## Produce and verify

Make the picture in code. Prefer p5.js or plain JavaScript without a framework. Install dependencies if needed. Do not assume Hyperframes. Preserve source when reusable Motion Graphics were requested, and render a playable preview or final video.

Review the complete composition and sample the initial state, every reading hold, important transitions, and final state. Confirm text is legible and unclipped, motion settles fully, brand assets are accurate, and intended transparency or background treatment survives the chosen output format.

Deliver the rendered media and any requested self-contained source. State the dimensions, duration, frame rate, audio state, and whether transparency is preserved.
