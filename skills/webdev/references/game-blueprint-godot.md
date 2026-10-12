# Godot Blueprint details

Read only for Godot concept submission, session-owned coverage, legacy setup or native production questions.
Use the latest canonical revision and preserve pending/cancelled approvals.

## Submit concepts

Godot only; Three.js has no concept stage.

### Concept work by request
Concepts are conditional, not a routine production step. Follow the Blueprint's recorded mockup choice and do not
offer a second concept workflow when the direction is already clear. For an explicit request, produce distinct,
coherent interpretations of the brief and keep the selected identity through revisions. The Game Concept Design flow
needs exactly three separate mockups generated under the recorded image consent, presented through the existing card
and explicitly approved; never label mockups as screenshots. Outside that flow, honor the requested count and
approval method. Mockup consent is not consent for production assets.

For Godot authorized concepts, POST `game/blueprint/concepts` with `{expectedRevision, concepts}`: exactly three distinct entries,
each with id, name, description and exactly one absolute local PNG `imagePath` or saved `assetRef`. The runtime uploads
images. For requested shorter captions, rewrite once and resubmit all three at the same revision with existing images.
Present only through Game Concept Design unless asked for chat copies; wait for explicit approval. On generation
failure, POST `{expectedRevision, error:"generation_failed"}` to the same path. After a lost reply, read canonical state before retrying;
accepted images are not regenerated or reuploaded. Revision consent covers only that revision.

## Session-owned coverage

For Godot only, canonical `author_coverage` with saved `visualCoveragePlanning: "session_owned"` delegates coverage to this agent.
From the full brief and choices, POST `game/blueprint/refresh` at the handoff revision with
`{expectedRevision, question: {question, options:[{id,label,description}], recommendedOptionIds}}`: 1–12 roles,
≤8192 UTF-8 bytes; recommended IDs must come from options. An empty list permits no optional enrichment. No planner
retry, sourcing or implementation until the next action allows it. On stale revision, reassess returned state.

Otherwise the init planner owns visual roles; coverage is agent-only scope with no coverage page/questions.
Preserve explicit empty optional lists, inclusions/exclusions, source permissions and deliberate procedural design,
and check the integrated game against that scope.

## Legacy setup

Only for supported legacy preparation, follow the live schema/receipt and reuse clientRequestId and arguments on retries.
`visualCoverageMode: "delegate"` delegates authoring; supplied choices.visualCoverage holds
`{roles:[{id,label,description}],customRequest?}`. When the receipt requests session-authored coverage, prepare
`visualCoverageQuestion:{question,options,recommendedOptionIds}` or use advertised submit_visual_coverage with
blueprintId, expectedRevision and question: group relevant roles (usually 4–8, at most 12) under stable lowercase IDs.
Existing pre-init Blueprints initialize with `gameEngine: "godot"` and approved ID/revision; never omit them to bypass pending/cancelled state.
Older init tools retain their supported flow, with non_interactive only where supported and never with mockups:true.
Do not discover retired operations from old messages.

## Production choices for cards and native questions

The wording below applies to Godot. Three.js model choices follow [Three.js Blueprint](game-blueprint.md#threejs-blueprint).

### Asset-production choice wording
Fast prototype follows its bounded workflow. New managed games call `webdev.init_project` once direction is clear,
with the complete brief; the canonical card settles unresolved choices, not parallel chat questions or a separate
Blueprint. Session-agent catalog search, access, downloads and delegation wait for successful initialization plus a
settled Blueprint, required plan and requested concept approval; in-flight or failed init is not success. Only
initialization's bounded metadata assessment may precede the card, never production downloads, generation or
integration. Standalone search or retrieval needs no project but does not justify speculative new-build sourcing.
Use the conversation language and call the catalog 游戏素材库 in Chinese. Recommend Hybrid mode for 2D, 3D and
unknown games. Card options for 2D/unknown: Manus game assets catalog, Hybrid mode, AI generation; Hybrid means
catalog plus AI art/audio, not scratch visuals. Known 3D: Game asset library and procedural generation, Hybrid mode,
AI generation. Only initialization's evidence-backed insufficient core-visual fit changes the first 3D label to
Procedural generation (Faster, lightweight, minimal token consumption); Unknown/sufficient fit or missing decoration
does not. Preserve historical accepted permissions; never infer them from option names or recommendations.
Only missing card support or a structured `planning_unavailable` receipt moves unresolved setup to one native
single-choice question; canonical state wins. For 2D/unknown: Manus game assets catalog, Hybrid (Recommended), AI
generated. Known 3D: Curated asset catalog and procedural (lowest token cost; catalog first, permitted gaps),
Hybrid (Recommended), AI generated (highest token cost). Keep these labels and this order, and record the answers.
No-questions sessions use
the recommended option within existing permission, which is not new consent. Additions to an existing game ask only
an unresolved production choice; delegation inherits constraints.
Accepted `choices.visualAssetSource: procedural` needs no repeated visual search/gap proof; audio follows its own
source restrictions and optional-production workflow. Catalog and Hybrid sourcing, including required-gap handling,
follows the game-asset-catalog Skill. Procedural permission never implies music composition.
