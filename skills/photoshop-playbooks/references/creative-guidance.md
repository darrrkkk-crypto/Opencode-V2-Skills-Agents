# Design and Guidance (Cards 7 and 9)

## Card 7 — Text effects, posters, and composites

**Use when:** the user needs a campaign visual, poster, social asset, product composite, or stylized text treatment. Typical cases include retail promotions, events, creator thumbnails, entertainment key art, and localized campaigns.

**Primary channel:**

- F1 for a visual concept or standalone composite where exact editable text is not required.
- F2 for exact flat text and geometry rendered deterministically.
- W1 for ordinary editable Photoshop Web layers, masks, and text that survive a representative round trip.
- D1 for a named desktop-only or web-limited object such as Pen/path text, a required Smart Object operation, installed plugin/resource, or explicit Desktop lesson.

**Escalation trigger:** move to W1/D1 only for the exact editable object graph, explicit client, installed resource, or failed round trip; “PSD” alone is insufficient.

**Hybrid handoff:** F1 creates concepts/source art, F2 renders exact copy/geometry, and W1/D1 assembles only the retained Photoshop object graph.

**Verification:** exact-copy OCR/human review, dimensions, hierarchy, safe zones, asset/font status, and named objects after reopen.

“PSD handoff” alone does not prove Desktop is required. Name the exact object graph. Generated lettering is not exact copy; verify text with OCR and human review or render it deterministically.

**Workflow:** lock copy, dimensions, brand constraints, references, and retained objects; produce a concept/sample; choose client from the object graph; assemble and verify exact copy, hierarchy, safe zones, and editability.

**Failure and recovery:** preserve source assets and copy authority. Report missing/substituted fonts, rasterized objects, and unsupported retained state.

**Record as skill:** record only a client-specific, live-proved construction or lesson with a disposable asset.

**CU display:** conditional; a Desktop-specific editable construction or lesson qualifies, while a standalone poster does not.

## Card 9 — Photoshop lessons

**Use when:** the outcome is learning the requested Photoshop client rather than merely receiving an image.

**Primary channel:** use Photoshop Web through My Browser for a proved web lesson and Photoshop Desktop through CU for a proved desktop lesson. Create or copy a safe practice asset first.

**Escalation trigger:** switch clients only when the requested lesson requires a missing control/object or the user explicitly chooses the other client.

**Hybrid handoff:** native or deterministic tooling creates disposable practice assets; the requested client performs the lesson and produces the repeat checklist.

**Verification:** record exact client/OS/version, observable start/end state, saved disposable artifact, repeat checklist, and recovery path.

Launch lessons independently; do not treat a catalog as one validated workflow. Priority lesson families are:

1. create and refine an editable layer mask;
2. use Select and Mask on a disposable cutout;
3. record an Action and replay it on an unseen sample;
4. bind a Variables/data-set template and regenerate one unseen row;
5. configure a safe Batch/export destination without overwriting sources.

Each lesson needs an exact client/OS/app version, start state, observable end state, one recovery path, a concise repeat checklist, and its own live replay. If that proof is absent, provide conceptual guidance or hold rather than inventing menus.

**Record as skill:** this card exists to create repeatable teaching procedures, but every lesson is recorded separately and parameterizes asset names, destinations, and app state.

**CU display:** yes only for a live-proved Desktop lesson. My Browser lessons are browser capability, not CU.
