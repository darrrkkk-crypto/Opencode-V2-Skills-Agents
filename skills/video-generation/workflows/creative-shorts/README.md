# Creative shorts

Use for conceptual, brand, cinematic, or narrative shorts, centered on an image, choice, or event worth watching to the end. A creative short should stand on its own, usually with one theme, one or two people, a few locations, and its own resolution

This method supports AI-assisted creation, with attention to expression, character events, and the final viewing experience. Choose between it and other work workflows as follows:

| Work's focus | Corresponding workflow | Relationship to creative shorts |
| --- | --- | --- |
| Pain points, selling points, and conversion in the first 2 seconds | [Marketing and growth](../marketing-growth.md) | Creative shorts prioritize an image, choice, or story |
| First-person recommendations and a creator's personal connection | [UGC](../ugc-video.md) | Creative shorts can let character actions take the place of sales statements |
| Copy and voice-over determine the information order | [Narration-led](../narration-led.md) | Images in a creative short can also tell the story independently; narrative defaults to dialogue and action, with voice-over as a supplement |
| Visual movement of type, graphics, and data | [Motion graphics](../motion-graphics.md) | Creative shorts focus more on watchable situations and events |
| Product operation and results take the lead | [Product launch](../product-launch.md) | A product in a creative short can be an object that drives the plot |
| Episodes, character development arcs, and continuing suspense | Serialized storytelling | Creative shorts center on one theme, one or two people, and a few locations, with an independent resolution |

## Enter at the current stage

| What needs doing now | File to read |
| --- | --- |
| A new work's aspect ratio, duration, and expressive direction are still undecided | [00-preflight.md](00-preflight.md) |
| Develop an idea into a story, or revise a script | [01-concept-and-script.md](01-concept-and-script.md) |
| Establish references for recurring people, locations, products, and voice timbres | [02-asset-design.md](02-asset-design.md) |
| Design multiple shots for an established script, preferring one generation request | [03-shot-design.md](03-shot-design.md) |
| Turn an established shot design into video-generation prompts | [04-video-prompts.md](04-video-prompts.md) |
| Compare generated clips and decide their joins and editing | [05-editing.md](05-editing.md) |

Choose the document for the current stage. Continue directly from an existing script, references, or shot design; asset preparation and shot design can run in parallel, and local revisions retain existing settings

For a complete new work, refer to the six-step creative sequence in the common entry point and follow the stages below within this workflow. Reuse the outcomes of stages already completed; asset preparation and shot design can run in parallel:

```text
Preflight (00) → Concept and script (01) → Visual assets (02) → Shot design (03) → Video prompts (04) → Edit and assemble (05)
```

## Stage deliverables

| Stage | What this stage specifically establishes | Recommended deliverable |
| --- | --- | --- |
| Preflight | Current generation conditions, aspect ratio, duration, image quality, and minimum asset scope | A preflight document with confirmed conditions and a stopping strategy |
| Concept and script | One-sentence logline, central image, actions, and dialogue | A script document; the logline and script body can be separate |
| Assets | Written Look and setting descriptions; necessary character, product, brand, and timbre references; location images that also establish style are recommended for narrative shorts | A minimum asset document and a stopping-condition check |
| Shot design | Shots and joins for the complete video; add generation units only when multiple requests are necessary | A complete-video shot table; add a unit table only when requests must be split |
| Video prompts | Convert the complete shot design into submit-ready requests | A complete-video prompt document; organize it by unit only when requests must be split |
| Assembly | Clip assembly, rhythm, continuity, and quality | Keep a local manifest of source clips, order, timing, and output files |

Keep these outcomes as sections of one brief, editable creative plan. Read only the method needed for the current task, batching independent references with parallel tool calls. Generate directly using the [entry-point rules](../../SKILL.md#generate-missing-assets) and current tool schemas; consult long templates only for specific examples.

## Expression and outputs

Narrative shorts default to character dialogue, action, and production sound, with voice-over as a light supplement; follow the user's explicit request for a silent film, pure mood piece, or voice-over work. A brand may appear as an object that drives the plot

People and products require reference images, with consistency following the hero-image and derivation methods in [asset design](02-asset-design.md). Settings, lighting, and style can use shared written descriptions; for narrative shorts, a location image that conveys both space and style is recommended. Shot designs default to text. Read relevant creative sections as needed; use the entry-point generation rules and live tool schema when calling a model

One or several separately delivered model clips can be the final output directly. Use local file-based assembly when clips need to become one film, subtitles and sound require precise arrangement, or graphics need layering. Formal plans record only the currently confirmed creative content in files the user can edit
