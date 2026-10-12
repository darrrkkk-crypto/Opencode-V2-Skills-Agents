# Motion graphics production

Use this workflow for complete videos led by typography, shapes, logos, UI, diagrams, or data rather than generated live-action footage.

## Establish the composition

Decide whether the result is a full-frame work or a transparent overlay. Full-frame work owns the background and the whole composition. An overlay must reserve space for the underlying subject and subtitles and must use a rendering path that preserves alpha when the requested output format supports it.

Turn the message into a small sequence of information states. At any moment, keep one primary focus. Use motion to explain hierarchy or relationships; decoration should not compete with the content.

Set dimensions, frame rate, duration, palette, type system, safe areas, and audio intent before authoring. Follow supplied brand assets and typography. Never redraw a logo or alter branded text unless the user asks.

## Design readable timing

Each information state usually has an entrance, a stable reading hold, and an exit or transition. Size the hold to the amount of text rather than applying one fixed duration. Keep lower thirds concise, data labels legible, and essential text away from platform UI and subtitle regions.

Favor decisive movement with clear endpoints. Translation, scale, masks, stroke reveals, number interpolation, and opacity are useful when they support the message. Avoid simultaneous unrelated motion that makes the eye search for the subject.

Pair sound only with meaningful motion: a light whoosh for a reveal, a click or pop for a snap, or a restrained chime for a completed value. Do not add sound when the requested asset is silent or intended as an overlay.

## Author and render in the Sandbox

Make the picture in code. Prefer p5.js or plain JavaScript without a framework. Install dependencies if needed. Do not assume Hyperframes.

For p5.js videos intended for social media, default to 1080p, 30 fps rendering and streaming-friendly encoding unless the user requests other settings.

Keep the project self-contained: store source, fonts, images, and data locally; avoid remote runtime dependencies and CDN assets. Make animation time-driven and reproducible so individual frames can be rendered consistently. Use generated raster or video assets only when they add value and their visual variability is acceptable.

## Verify

Check at least one frame from the initial state, every stable reading hold, important transitions, and the final state. Confirm that text is not clipped, brand assets are correct, intended transparency is preserved, and the animation fully enters and exits. Probe the final file for dimensions, duration, frame rate, codecs, and audio streams before delivery.
