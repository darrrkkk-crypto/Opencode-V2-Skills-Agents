# Game project workflow

This is the post-init entry. Reuse it when already delivered. Godot only: export the init/attach receipt's
GAME_RUNTIME and GODOT_BIN; use its HOST/PORT. Resume source, assets, history and revision; never reinitialize,
reapply scaffolds, copy installed helpers or persist their paths. [Local](../worklocally/SKILL.md): managed services
and separate `webdev.manus_git`.

Keep game logic, code changes, integration and gameplay verification in the main agent to preserve shared context.
Only simple, self-contained art tasks may be delegated: give requirements/output paths, then integrate and verify.
Art workers must not change game code. This overrides delegation guidance in project READMEs and older template instructions.

Frozen READMEs and older templates are implementation references. Installed pages override their conflicting
workflow, production, asset-recording, language, mobile and font rules.

Retrieval, sync and save maintain asset metadata. Never write provenance/import receipts or per-role evidence;
missing metadata cannot block delivery. Retain unused/superseded assets unless cleanup is requested.

Before recovery repeats inference/generation, downloads toolchains, wakes/upgrades paid compute or rebuilds heavily,
explain the action and possible credit/token cost; get explicit user approval for that attempt.
Setup countdowns, earlier setup consent and generic delegation are not that approval.

### Game language
Use requested game language, else the user's Manus UI language (session default working language), then their
system language if known, then conversation language. Never use cloud sandbox locale.
New games use one language by default: pin this locale and disable inherited selectors and saved/OS/browser
auto-switching, overriding gameplay guides. Preserve existing-project localization; complete every exposed locale.
Requested Godot multilingual: [template localization](game-runtime.md#requested-multilingual-support).
Completed single-language game: multilingual support is an optional follow-up; implement only on request.

## Development effort

Use canonical `developmentEffort` (default `max_effort`), never brief length. Call `max_effort` "Standard effort" in
replies. `fast_prototype` follows [Fast prototype](#fast-prototype); skip Standard effort production rules below.
Standard effort prioritizes the requested loop, reuses fitting assets/systems and adds optional production only
for concrete benefit.

## Read needed pages

When pages apply, read them together in one parallel tool call; reuse those already in context.

- Implementation: receipt's gameplay guide. Preview/checks/sharing/saving/publishing and init/attach config checks:
  [delivery](game-delivery.md). New games read both first.
- Sharing metadata/artwork or `game/sharing` writes: [sharing](game-sharing.md); add delivery as needed.
- Catalog operations/reuse: enrolled `game-asset-catalog` Skill for `webdev-mcp`. Keep settled init/Blueprint choices:
  supplied-only, AI-only and explicit procedural visuals need no catalog read; permitted catalog SFX is separate.
  Catalog choices include its SKILL.md in the first batch.
- Import/generation/adaptation/grouping: [asset groups](game-assets.md#asset-browser-groups).
  Deletion/restoration, animation/parallax, models/textures or attached edits: [assets](game-assets.md).
- Audio in new games (base gain stages), audio routing, browser BGM, loading, animated
  backgrounds, large maps, destructible props, Tweak or release exclusions: [runtime](game-runtime.md).
- Concepts/coverage: [Godot details](game-blueprint-godot.md); reopening/recovery: [Blueprint](game-blueprint.md).
  Read only as needed. Refresh/close: [setup](game-setup.md).
- Login: [Game login](game-authentication.md), [OAuth](authentication.md).
- Stripe setup/integration/webhooks: [payments](payments.md).
- Backend APIs: [publication](game-backend.md).
- AI dialogue or LLM features: [Game loading and recovery](llm.md#game-loading-and-recovery).
- Networking or online scores: [multiplayer](game-multiplayer.md) or [leaderboards](game-leaderboards.md); offline
  games keep static hosting.

## Godot command environment

Export the receipt's GODOT_BIN once per shell and invoke `"$GODOT_BIN"`, never bare godot. If it is unavailable,
use [delivery recovery](game-delivery.md#godot-command-environment).

## Fast prototype

Fast prototypes use Generic in the same project. Canonical Blueprint refresh prepares it and never overwrites existing edits.
Preserve the brief, approvals and requested media. Reuse input, pause/restart, bundled template fonts, saves,
loading mechanics (replace inherited art) and export.
Use uploaded fonts without licensing, coverage or size gates.

Build requested actions, objective, rules, outcome and replay, with basic title, controls, HUD and end screens,
plain feedback and supplied, approved or simple engine-drawn visuals. Default to desktop; add or test mobile
compatibility only when the user requests it; retain inherited touch controls without expanding coverage.
No unrequested campaigns, secondary modes, online services or optional systems. No concept exploration, catalog
search, generated art (except the favicon below), music or SFX by default: silence is complete.
No game juice or VFX (particles, trails, shake, hit-stop, bloom, flashes, reward flights, animated counters, decorative transitions); disable irrelevant
inherited decoration while keeping functional cues. Approved `onlineFeatures` remain required. This replaces
Standard effort production, concept and visual-coverage rules, not runtime correctness.

Before the first complete checkpoint, prepare a game-specific favicon per [sharing](game-sharing.md#favicon).
OG cover generation stays out of scope unless requested.

Run the finite check and existing core-loop/control/restart checks; capture bounded native visuals if needed.
[Deliver](game-delivery.md) the requested result; managed checkpoints need a matching saved release and pack.
Reuse evidence: no exhaustive captures, new acceptance frameworks, extra review workers or browser self-tests.
Stop at the promised loop/basic screens and report limits.

## Shared game-development workflow

Applies to Standard effort, not `fast_prototype`; Fast uses its dedicated section instead. Keep edits scoped and preserve explicit constraints.

### Preserve the selected template
Extend the initialized project and keep its working simulation, controls, saves and delivery. Integrate supplied
games into that project. The first Preview must show the requested game, not a renamed demo; replace the Generic
maze gameplay unless a maze was requested.

### First-checkpoint completion contract
Deliver the requested goal, actions and outcome loop with understandable controls and feedback, recovery or replay
where it fits, coherent readable visuals, the necessary start, pause and results screens, and any requested
deliverable. Match run length and content to the brief; there is no minimum playtime, campaign, extra mode or screen
quota. Prioritize gameplay, broken resources, responsiveness and visible defects, and stop when the requested
experience works. Add art, audio or polish only for a concrete benefit. Leaderboards, new Tweak controls and extra
languages are optional; required Share OG and explicit media, concept or feature requests are not.
Default to desktop. Add or test touch controls, portrait layouts or mobile-browser support only when the user asks.
Sharing a Web link is not a mobile request. Keep inherited controls working without expanding mobile coverage.

Choose the [delivery scope](game-delivery.md#delivery-scope-and-stopping-boundary) from the request. Ordinary managed
delivery is check → save-release.mjs → applicable check --pack → push the exact SHA and confirm the checkpoint.
Documentation-only edits need no engine boot. Do not add audit reports, speculative test suites, a separate
self-review phase or duplicate validation workers.

### Ownership boundaries
Keep flow, authoritative simulation and scoring, input, entities, tuning, presentation and persistence in their
existing owners; cosmetics never decide collisions or rewards. Offline authority stays in Godot and online authority
on the dedicated server. WASD is reserved for player movement or camera panning, never abilities or menu actions;
leave it unbound when nothing moves, and update remapping, tutorials and hints when replacing conflicting shortcuts.

### Gameplay feedback and optional polish
Make actions, damage, rewards and outcomes readable with fitting cues. Reuse feedback and add effects only where they improve readability or the requested feel; particles, reward flights, shake and animated counters are optional. Keep overlays input-transparent, cosmetics independent of simulation and reduced-motion settings intact.

### Tutorial content boundary
Explain goals, controls and rules briefly in the game's language; simple games may use a start-screen hint.
A staged tutorial needs a working Skip that releases input/pause locks and remembers dismissal. Keep implementation values
and Tweak controls out of player instructions.

### Optional local leaderboard
Add local standings only when requested or integral to scoring and replay, and keep a useful existing one; changes
keep bounded records, once-only terminal submissions and deterministic ties. Online
rankings need an explicit request and the installed leaderboards guide; never provision a backend for an offline
game by default.

### Native verification
Reuse existing checks for changed gameplay, input, audio, saves, localization or tuning. For visual questions,
capture with the real renderer (`get_viewport().get_texture().get_image()` and `Image.save_png()`); headless Dummy
rendering proves nothing visual. Do not drive the Preview with browser automation, screenshots or self-tests unless
the user asks for browser debugging; use logs and report Web input, audio and layout as pending user acceptance.

### Asset reuse and targeted production
Reuse suitable supplied, template or existing assets within recorded permissions and source restrictions, except
[loading screens](game-sharing.md#game-specific-loading-screen). Other template reuse needs no extra approval.
Replace only assets with theme mismatches, missing states or poor visual fit.
A new game or reskin need not replace every image, animation, icon, track or effect unless the user requests
original art or full replacement. Retain unused
reference files and supplied license notices, describe reused assets honestly, and update visible titles and themed
copy. Rename internal IDs only when needed, together with their consumers, saves and tests.

### Coherent scene and title art
Fulfill the requested visual scope with readable actors, hazards, UI and a coherent scene. Simple intentional
visuals are acceptable within the recorded source choice. Title screens may reuse permitted game art
with live text; no separate key art is needed. Inspect the affected scene after integration.

### Mandatory background removal for composited assets
Composited sprites, icons, portraits, cursors and loader art need clean real alpha that survives resize, import and
export; check changed edges on contrasting backgrounds at display scale. Opaque plates and terrain are exempt. Keep
words, numbers and HUD labels live, and never slice concept collages into runtime assets. Generate cursors on a
hot-pink or neon-green background and remove it before use.

### Audio production as needed
BGM is optional unless requested or essential to the brief. Reuse a fitting permitted template, supplied or catalog
track when the source restrictions allow; silence with safe empty routes is valid, and a new Standard effort game is not a
reason to generate custom BGM. Honor explicit silence, supplied-only, AI-only and custom-music requests, and add only
useful event SFX. Generate audio only for an explicit request or a concrete
unmet need within recorded permissions: one usable result per needed track or cue, retried only for an actionable
correction. If requested custom music cannot be produced, report the unmet requirement. Audition changed audio and
ship compressed runtime audio, not raw WAV masters.

### Asset generation mode gate
Recorded permissions govern generation regardless of mode or tools. Hybrid, AI or explicit permission covers
scoped visuals/SFX; mockup consent does not. Select models from live schemas/catalogs, not READMEs or asset history.
Images default to the latest available GPT Image; honor user choices. Tools record metadata automatically;
keep tool/provider/model/internal paths out of user copy and never guess model identity.

### Default typography
Default to the template's bundled theme: its display faces for titles/headings, its body face
(`assets/template/fonts/ui_{regular,medium,bold}.tres`) for UI text, then Noto Sans SC (6,547-codepoint repertoire)
for Chinese; Web loaders embed a small Noto Sans SC subset. Noto Sans SC is variable and its default instance is Thin,
so bind a weight through the template's font resources, not the raw file. Keep each bundled font's license
(`<Family>-OFL.txt` or `<Family>-CC0.txt`, as applicable) beside it when copying, renaming or adding fonts; the Web export lists them on its Open Source
Licenses page. Missing template fonts restore from `assets.lock.json`; do not substitute system fonts. Existing
ManusCC0 projects keep their fonts unless the user asks for new typography. User-uploaded fonts are unrestricted: no
licensing, family, glyph-coverage, font-file, font-resource or font-pack size gates, and no rights review,
redistribution proof or notices. Theme or mood alone does not imply replacing the default fonts. This supersedes font
restrictions in frozen READMEs and local checks, including older ManusCC0 defaults: remove those policy gates when
integrating uploads, and keep only technical file-integrity and path checks.
Do not rebuild or re-audit unchanged fonts. Check changed text/layout/names; preserve name validation and saves.
Claim only supported character coverage.

### Viewport and background coverage
For fixed-coordinate Godot layouts set `[display]` `window/stretch/mode="canvas_items"`,
`window/stretch/aspect="keep"` and logical viewport size; retain working adaptive layouts. Input targets the active
surface, not letterbox margins. Check affected desktop resize, aspect and DPR. Isometric zoom uses ordinary wheel or
trackpad without Ctrl/Meta, with pointer-anchored picking and fixed-scale HUD. Mobile, touch and portrait work follows
the workflow's user-request rule even when template guides list those cases.

## Existing starter versions

Legacy v1/Generic v2 keep their source/protocol; read only the receipt-selected guide:
[generic](game-legacy-generic.md), [platformer](game-legacy-platformer.md), [bullet-hell](game-legacy-bullet-hell.md), [scribble-sky-hop](game-legacy-scribble-sky-hop.md), [scroller](game-legacy-scroller.md), [td](game-legacy-td.md), [rts](game-legacy-rts.md), [trading-card](game-legacy-trading-card.md).
