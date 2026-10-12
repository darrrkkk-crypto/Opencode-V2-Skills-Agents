# Game Template — Godot Browser Card Battler

Legacy-only gameplay contract: keep the installed project and protocol; new initialization selects newer revisions. Read the selected starter's matching guide; paths below are relative to its project root. [Game workflow](game-workflow.md) owns initialization, Preview, release preparation and deployment. Source-specific test/export commands are diagnostics only, not lifecycle replacements; serialize them with active Game builds. [Shared game rules](game-workflow.md) take precedence for gameplay/art/audio policy. First-checkpoint completion means the first completed-game deliverable, excluding bootstrap and intermediate version saves.

This repository is a production-tested **Godot 4.7.2 browser card-game template**. Its example game, **Emberpan**, is a single-player culinary roguelike deck-builder with three battles, two intermissions, a Hearthstone-style spatial grammar, procedural game juice, bilingual UI, local persistence, runtime tuning, and an optional global leaderboard.
> **Important:** this is a strong scaffold, not a genre-neutral engine. `scripts/card_game.gd` owns most runtime state, rules, input, presentation dispatch, persistence, and screen UI. `scripts/card_database.gd` owns content data and static-art registration, but changing that file alone does **not** complete a pivot. (`scripts/card_game.gd` in the matching project)  (`scripts/card_database.gd` in the matching project)
Use this README as the operating contract for an AI agent adapting the template. Preserve the invariants below unless the product brief explicitly replaces them, then replace the corresponding tests as deliberately as the implementation.
## Browser multiplayer PvP
The title screen includes **MULTIPLAYER** with one-click Host Room, Join Room and guest reconnect. Hosting creates a private room and shareable invite automatically; opening an invite joins directly. Players never configure service URLs. This separate, browser-only mode supports 2–4-player unranked PvP through player-hosted WebRTC and TURN fallback; host leave ends the match. Solo saves and leaderboards remain separate.
See the multiplayer contract (`multiplayer/README.md` in the matching project) for rules, authority/privacy boundaries, reconnect, build compatibility, configuration and tests. The shared lobby/TURN service is operator-managed infrastructure; project initialization does not deploy it. Set `GAME_MULTIPLAYER_SIGNALING_URL` on the game runtime/checkpoint environment; preview and publication deliver `multiplayer/bootstrap.json` automatically. A bundled `multiplayer/config.json` endpoint is a fallback for external publishers. Keep the template static and never export TURN secrets.
## Template font wiring
Follow the [current typography contract](game-workflow.md#default-typography): default to bundled ManusCC0 with ManusCC0 Sans CJK SC fallback, and allow unrestricted user-uploaded fonts. For font changes, update theme overrides, hydration pins, loader sources and project-local checks together; preserve gameplay and protocol. Check chosen-font rendering, Chinese player names and actual Web font resolution; diagnostics do not block uploaded-font choices. Update the existing resource wrapper and localization font overrides together.
## Card-game tutorial requirements
Every tutorial **MUST explicitly teach** these combat fundamentals in every supported language:
- **Minions (units) can attack enemy minions and can also attack the opponent player directly** by targeting the enemy hero portrait. Explain readiness and Guard restrictions so players understand when each target is legal.
- **The objective is to defeat the enemy player by reducing their Health to 0.** Defeating enemy minions helps achieve that objective; clearing the enemy board alone does not win the battle.
## 1. Declare the Change Class First
Before editing, classify the task. This determines which systems and gates are mandatory.
| Change class | Typical scope | Minimum required gate |
| --- | --- | --- |
| Visual-only reskin | Static art, palette, audio, particles, copy with unchanged mechanics | Asset import, layout/alpha tests, localization, captures, full source test |
| Content/economy | Cards, decks, recipes, encounters, rewards, numbers | Gameplay, localization, tutorial, reliability, full source test |
| Mechanics | New effect, resource, combat rule, AI, progression | Deterministic mechanic tests, smoke test, reliability, full source test |
| Layout/input | HUD geometry, cards, targeting, drag/drop, controls | Battle layout, cursor, tutorial, captures at every profile, full source test |
| Persistence/leaderboard | Saves, score fields, API, schema, migrations | Atomic-save, leaderboard, WebDev server tests, offline/retry tests |
| Export/deployment | PCK, loader, hosted assets, API ownership | Fresh export, manifest/PCK verification, packaged-runtime and browser tests |
For the lowest-risk reskin, **retain semantic IDs and filenames and replace file contents**. Renaming requires coordinated changes to `CardDatabase.ART`, card and encounter records, direct `DB.art(...)` consumers, cursor and audio registries, localization, tests, save compatibility, and export checks.
## 2. Repository Ownership Map
| Path | Authority |
| --- | --- |
| `scenes/card_game.tscn` | Minimal full-screen root scene. The scene is intentionally thin. |
| `scripts/card_game.gd` | Main run/battle state machine, combat, enemy AI, cooking, rewards, title/battle/intermission/result UI, input, saves, scoring, tutorial integration, and semantic presentation events. |
| `scripts/card_database.gd` | Static art registry, card definitions, starter deck, recipes, legendary rewards, encounters, and enemy decks. |
| `scripts/battle_layout.gd` | Sole authority for battle HUD zones, 1280×720 reference geometry, safe-canvas projection, and compact profile. |
| `scripts/localization.gd` | Locale detection/preference, paired-catalog loading, fallback behavior, placeholder validation, and shared EN/CN font application. |
| `scripts/pause_input_router.gd` | Always-processing Escape input while the scene tree is paused. |
| `scripts/juice_director.gd` | Procedural particles, overlays, shakes, flashes, card ghosts, ingredient flights, BGM, voiceover, and SFX playback. |
| `scripts/hearthstone_juice_profiles.gd` | Effect tiers, mechanic kits, motion scaling, and concurrency budgets. |
| `scripts/juice_target_line.gd` | Curved source-to-pointer targeting line and arrowhead above elevated cards. |
| `scripts/sleep_particle_emitter.gd` | Animated or static localized Sleep-state feedback. |
| `scripts/cursor_director.gd` | Semantic custom cursors, trails, halos, blocked/valid feedback, and touch hiding. |
| `scripts/tutorial_callout.gd` | Tutorial dimmer, live spotlight, guide, pointer, callout placement, and input containment. |
| `scripts/runtime_tweak_controls.gd` | Metadata-driven 61-control tuning UI, validation, persistence, and rank-affecting classification. |
| `scripts/atomic_json_file.gd` | Validated temporary write, backup rotation, and corrupt/missing-primary recovery. |
| `scripts/leaderboard_client.gd` | Local/global score contract, same-origin HTTP, retries, fallbacks, diagnostics, and sorting. |
| `localization/en.json`, `localization/zh-CN.json` | Paired English and Simplified Chinese catalogs. |
| `test/` and `scripts/smoke_test.gd` | Executable specification. Preserve behavioral intent when renaming theme-bound tests. |
| `web/` | **Generated output. Never treat it as source.** |
`ScreenLayer` is the authored HUD canvas. `JuiceLayer`, tutorial, cursor, and tweak controls are separate presentation spaces. Cross-layer effects must use live `CanvasItem` transforms; raw local positions drift under HUD scale, shake, responsive projection, and entrance animation. (`scripts/card_game.gd` in the matching project)  (`scripts/battle_layout.gd` in the matching project)
## 3. Current Game Loop and Stage Model
A normal run contains **three battles**:
| Stage | Encounter | Purpose |
| --- | --- | --- |
| 1 | Picklemancer | Teaches Mana, targeting, Guard, and exact-lethal harvesting. |
| 2A or 2B | Mold Monarch or Ember Butcher | Branching defensive or aggressive pressure. |
| 3 | Banquet Tyrant | Final mixed encounter with a half-Health escalation. |
The flow is: title → first battle → Kitchen Break and legendary choice → route selection → second battle → Kitchen Break and remaining legendary choice → final battle → victory/defeat ledger. Chef Health persists between battles; armor, board, hand, Mana, deck/discard, fatigue, and hero-power state reset for each encounter. (`scripts/card_game.gd` in the matching project)  (`scripts/card_database.gd` in the matching project)
A pivot may ship one stage, two stages, or the complete three-stage scaffold. If stages are removed, update route logic, score validation, victory invariants, tutorial assumptions, leaderboard version, and tests together.
### Lifecycle and asynchronous transitions
`screen_name` is the presentation state. `run_active` is the terminal ownership flag and remains true through Battle, Kitchen Break, and route selection. `_finish_run` is idempotent, so repeated end checks cannot record the same run twice.
Treat `battle_generation` and `opening_deal_generation` as **cancellation tokens**, not stage counters. Every awaited enemy-turn or staged-opening continuation must verify its captured token and current screen before it mutates state. Returning to title, starting a replacement run, starting an encounter, and finishing a run invalidate outstanding work. Existing tests cover stale delayed enemy turns, but staged-opening interruption still lacks equivalent coverage.
Resign is available from paused Battle, Kitchen Break, and route screens and is terminal. `battle_finished(true)` also fires for a nonterminal encounter victory before Kitchen Break; consumers that require run completion must additionally require `screen_name == "end"` or `run_active == false`.
## 4. Core Card-Game Mechanics
### Cards, deck, hand, and discard
The starter deck has 15 cards. Runtime copies have stable UIDs. The default hand cap is 8 and can be tuned from 4–10. **Drawing into a full hand burns the top card only when the deck is nonempty.** Reshuffle and player fatigue are evaluated only on a draw attempt with hand room: an empty deck reshuffles discard, and when both are empty fatigue starts at 1 and rises on subsequent empty draws. With a full hand and empty deck, current behavior is no burn, reshuffle, or fatigue. Enemy draws have the analogous full-hand early return and otherwise reshuffle without fatigue.
Every card definition must preserve or deliberately migrate these fields: stable card ID, `name_key`, `text_key`, `type`, `cost`, `art`, `rarity`, optional `attack`, `health`, `guard`, `ingredient`, `servings`, `effect`, `value`, and `aura`. Static definitions are copied before runtime mutation; never mutate the database record directly. (`scripts/card_database.gd` in the matching project)
### Mana, actions, and cancellation
Player maximum Mana rises by one per player turn. Enemy maximum Mana rises by the `enemy.mana_per_turn` tuning value, one by default and valid from 0–4. Both refill to their new maximum and remain capped by `gameplay.max_mana`. Mana is charged only when an action resolves.
A player action is legal only during the battle screen, on the player turn, while input is unlocked, after staged draws finish, and while Service History and blocking modals are closed. Escape clears a pending target without spending Mana or losing the card and preserves the player turn. End Turn also abandons a pending target, but commits the turn to the enemy. During a card drag, Escape clears the drag as part of immediately opening Pause; it is not a drag-only cancellation.
A targeted-card transaction is bound to the selected runtime card UID. While it is pending, other hand cards and Chef Power are unavailable; End Turn or Escape may still abandon it. Resolution validates target legality and affordability again before payment. Failed payment clears the stale transaction without spending Mana, removing the card, emitting card-play presentation, or mutating the target. The shared payment helper also refuses every invalid index or unaffordable charge, so player Mana cannot cross below zero.
### Mandatory visual arrow targeting
**When selecting a card that can target another card, you MUST use the visual arrow targeting system provided by this template.** This includes targeted damage, friendly buffs, and minion attacks; preserve the same system when the enemy player is a legal target. Use `scripts/juice_target_line.gd` through the pending-action flow and `_refresh_target_line()` in `scripts/card_game.gd`.
Show the curved arrow from the selected card or minion toward the pointer while choosing a target, including during the tutorial. Preserve its live source transform, visibility above cards, and cleanup on resolution or cancellation. Target highlights and instructional text may supplement the arrow, but must never replace it.
### Units and combat
Summoned units enter asleep, become ready on their controller’s next turn, and attack once before becoming unready. Unit combat is simultaneous. Armor absorbs hero damage before Health. **Guard currently constrains unit attacks only; targeted enemy Techniques can bypass Guard, including when targeting the enemy hero.** If the pivot intends universal Guard protection, add the same legality check to targeted-spell resolution. The default board cap is 4 and may be tuned from 2–6.
Chef Power costs 2 Mana by default, grants 2 Armor, and gives the next friendly summon +1 Attack. It may be used once per player turn.
### Exact harvest, Pantry, recipes, and servings
Ingredient-bearing enemies reward arithmetic rather than random drops. A player-caused lethal hit harvests an ingredient only when **final resolved player damage**, after outgoing/incoming multipliers and rounding, is no greater than current Health plus the configured tolerance. Excess lethal damage records **Overkill** and ruins the ingredient. Nonlethal damage yields nothing. Sovereign Cleaver is an explicit forced-harvest exception.
Fungus, Herb, Meat, and Ember are run-level Pantry resources spent during Kitchen Breaks. Each positive ingredient requirement is scaled at cook time as `max(1, ceil(base × recipe_cost_multiplier))`. A wildcard recipe automatically spends Fungus → Herb → Meat → Ember. Recipes are repeatable while affordable and add another UID-bearing runtime dish copy.
Dish Cards have servings: a played dish returns to discard while servings remain, decrements its matching run-deck copy, and is removed after its final serving.
### Rewards, encounter passives, and AI
Kitchen Break cannot advance until the player chooses or explicitly skips a legendary reward. **Selected legendary IDs are run-unique.** Skipping does not retire an offer: after selecting at the first default break, two unclaimed IDs remain; after skipping, all three remain eligible at the second break.
The example passives are first-summon Health, conditional Fungus healing, first-summon Attack, and a once-only half-Health board enrage. Banquet Tyrant checks the enrage threshold only through `_damage_enemy_hero`; Cursed Onion self-damage can cross the threshold without triggering enrage until a later qualifying hero-damage call.
The enemy AI is deterministic priority logic rather than a general planner: refill/draw, play up to its card limit using highest-cost affordable units, attack Guard first, otherwise kill the lowest-Health reachable ally, otherwise attack the hero. If you add tactical effects, ingredient strategy, lethal search, or a new card type, extend the AI and its deterministic tests rather than assuming it understands the new rule.
Each encounter also pre-plates its mapped opening enemy unit `enemy.starting_units` times, one by default and tunable from 0–3. These setup units are outside the shuffled encounter deck, skip on-play effects, and do not consume the first actual enemy-turn summon passive. Equal-cost AI plays and equal-priority targets retain their first current-array order.
### Scoring and ranked eligibility
Score version 2 is:
```text
max(0,
  victory × 3000
  + battles_cleared × 1000
  + precise_cuts × 150
  + dishes_cooked × 100
  + health_remaining × 25
  - ingredients_ruined × 50
)
```
Changing a Gameplay, Player, or Enemies tweak makes a run local-only. UI, audio, and environment tweaks remain eligible. The server recomputes the score; it never trusts a client total.
`completed_battles` is the authoritative progression counter. It resets with a new run and records the current battle number exactly once when encounter victory resolves, before entering an intermission or finalizing the run. Defeat and resignation submissions read that counter directly, so first Kitchen, route selection, and second Kitchen correctly report 1, 1, and 2 cleared battles.
### Current example content contract
`card_database.gd` remains authoritative. This compact inventory lets an adapting agent identify every current content seam without rediscovering the example game from event branches.
| Card ID | Type, cost, stats/servings | Implemented effect |
| --- | --- | --- |
| `coal_squire` | Unit, 1, 1/2 | On play: gain 1 Armor. |
| `pan_paladin` | Unit, 2, 2/4 | Guard. |
| `pepper_mage` | Unit, 3, 3/2 | On play: deal 2 to the enemy hero. |
| `broth_elemental` | Unit, 3, 2/4 | On play: draw 1; if the draw succeeds, heal 1. |
| `truffle_knight` | Unit, 5, 5/6 | Guard; defined but absent from the starter/reward pools. |
| `precise_chop` | Technique, 1 | Deal 2 to an enemy unit or hero. |
| `searing_arc` | Technique, 3 | Deal 2 to every enemy unit. |
| `mise_en_place` | Technique, 2 | Draw 2. |
| `kitchen_guard` | Technique, 2 | Gain 5 Armor. |
| `seasoned_strike` | Technique, 2 | Give a friendly unit +2/+2. |
| `mise_the_thousand_handed` | Legendary unit, 6, 4/7 | After a player card costing 2 or less: restore 1 Mana up to cap and draw 1. |
| `the_sovereign_cleaver` | Legendary technique, 7 | Deal 5 to the enemy hero and every enemy unit; lethal unit hits force harvest. |
| `bell_of_the_last_service` | Legendary technique, 8 | Heal 8; give every current ally +3/+3 and Ready. |
| `mooncap_broth` | Dish, 1, 2 servings | Heal 2 and draw up to 2. |
| `braised_bulwark` | Dish, 2, 2 servings | Gain 5 Armor; summon an asleep 2/3 Guard if board space exists. |
| `dragonpepper_roast` | Dish, 3, 1 serving | Deal 6 to the enemy hero. Its Ember recipe is currently unreachable in normal play. |
| `leftover_stew` | Dish, 1, 2 servings | Heal 4 and draw 1. |
| `pickle_imp` | Enemy unit, 1, 2/2 | Herb ingredient. |
| `moldling` | Enemy unit, 2, 2/4 | Guard; Fungus ingredient. |
| `cursed_onion` | Enemy unit, 2, 2/3 | On play: deal 1 to its controller’s hero; Herb ingredient. |
| `dough_golem` | Enemy unit, 3, 3/5 | Guard; Herb ingredient. |
| `meat_mimic` | Enemy unit, 4, 5/4 | Meat ingredient. |
| `cellar_rat` | Enemy unit, 2, 3/2 | Herb ingredient. |
| `gravy_specter` | Enemy unit, 3, 3/3 | On play: heal the enemy hero 2; Fungus ingredient. |
The starter deck contains four Coal Squires, two Pan Paladins, and one Pepper Mage, Broth Elemental, Searing Arc, Mise en Place, Kitchen Guard, and Seasoned Strike, plus three Precise Chops. The legendary pool contains the three legendary cards above. Default reward count is three: the first break offers all three; the second offers two after a selection or all three again after a skip.
| Recipe | Cost | Added card |
| --- | --- | --- |
| Mooncap Broth | 1 Fungus + 1 Herb | `mooncap_broth` |
| Braised Bulwark | 1 Meat + 1 Herb | `braised_bulwark` |
| Dragonpepper Roast | 1 Meat + 1 Ember | `dragonpepper_roast` |
| Leftover Stew | Any 2 ingredients | `leftover_stew` |
| Encounter | Health | Passive |
| --- | ---: | --- |
| Picklemancer | 20 | First actual summon each enemy turn gains +1 Health. |
| Mold Monarch | 25 | At enemy-turn start, heal 1 if a surviving Fungus unit exists. |
| Ember Butcher | 24 | First actual summon each enemy turn gains +1 Attack. |
| Banquet Tyrant | 34 | On the first `_damage_enemy_hero` call resolving at or below half Health, every current enemy unit gains +1/+1. |
## 5. Required UI and Alignment Contract
### Screen inventory
A complete pivot should retain or deliberately replace the following:
| Screen/system | Required behavior |
| --- | --- |
| Start screen | Title, primary start action, EN/中文 toggle, leaderboard, settings, and global Enter/Space start while unobscured. There is no explicit initial-focus contract. |
| Battle HUD | Both heroes, concealed opponent hand, opposed permanent rows, player hand, decks, Mana, Chef Power, encounter passive, history, Pantry, turn state, and one End Turn control. |
| Pause menu | Always-processing Escape path and blocked underlying input. The visible overlay has **Settings** and **Resign** only; Escape is the current Resume control and returns from nested settings first. |
| Kitchen Break | Health recovery, deck inspection, recipes, reward choose/skip gate, route continuation. |
| Result screen | Victory/defeat, score summary, local/global standings, immediate replay. |
| Runtime tweaks | Searchable categories, validated values, reset scopes, persistence, hover/focus clarity, F10 access. |
| Tutorial | Live-control spotlight, pointer/callout, step-gated keyboard path, spatially constrained pointer/touch path, and skip. |
### Hearthstone-style board grammar
Use the **spatial grammar**, not Blizzard trade dress:
**1.** Opponent hand and hero are top-centered. **2.** Opponent permanents occupy one upper row. **3.** The center remains an open combat corridor. **4.** Player permanents occupy one lower row. **5.** Player hero and physical hand sit at bottom-center. **6.** Service History and Pantry occupy the left rail. **7.** Opponent/player decks, Mana, and the single End Turn action occupy the right rail.
Do not add a second End Turn control. Do not place permanent UI in the combat corridor. Do not copy Hearthstone card backs, crystals, tavern ornament, medallions, logos, characters, target arrows, or other protected trade dress.
### Geometry rules
`scripts/battle_layout.gd` is the only placement truth. It projects a **1280×720, 16:9** design into the largest centered safe canvas. It selects `compact` when safe-canvas width is below 1120 pixels. Ultrawide surplus is intentional scenery or letterboxing; do not stretch gameplay distances into it. (`scripts/battle_layout.gd` in the matching project)
All HUD elements consume named zones. The visual drop overlay, card-release legality, cursor validity, tutorial corridor, and insertion preview share one `play_region`. Never introduce an independent drop or targeting rectangle.
Permanent rows use count-sensitive one-to-six circular slots. The player hand uses one count-sensitive one-to-ten fan with exposed cost corners and a bottom-center hero pocket. The reference places inspection previews in the fixed left-side `preview` zone within the safe canvas; adaptations may reserve a right-side zone through the same layout owner.
**Compact card inspection:** hover/focus previews must stay in a reserved zone on the **left or right side of the game board**, keeping the combat corridor, permanent rows, player hand, legal targets, and essential controls such as End Turn visible and usable. Never use a full-screen panel, centered modal, dimming backdrop, or input-blocking overlay for hover inspection. Wrap the popover closely around its art, cost, title, description, stats, and optional footer with modest padding. Preserve art aspect ratio and wrap description text within the bounded card width, retaining the two-line limit below. Prevent full-rect anchors, expand/fill sizing, inherited minimum sizes, or oversized spacers from stretching the panel across the viewport; a small card in a mostly empty screen-sized panel is a failure.
Keep the preview inside the safe canvas after resize and at supported preview scales. If space is tight, use a compact side layout or reserve the opposite side through `scripts/battle_layout.gd`; never fall back to covering the board. Previews must not intercept pointer input or disrupt dragging and targeting, and must dismiss when inspection ends. When changing previews, verify native rendered views in regular/compact layouts and both locales, including long descriptions and optional footer states: the content must fit tightly without clipping or large empty gutters, and the board must remain visible and usable.
The safe-canvas transform applies to all authored screens, but **only Battle rebuilds after resize and switches between Hearthstone and compact zone maps**. Title, Kitchen Break, route, result, leaderboard, and their fixed-reference overlays currently scale their existing 1280×720 composition without screen-specific compact reflow.
`ui.hud_scale` and safe-canvas projection are not currently composed. Applying the tweak assigns `ScreenLayer.scale`; a later resize replaces it with safe-canvas scale. Do not promise persistent custom HUD scaling or safe-bound preservation at a nondefault HUD scale until the two transforms are combined and regression-tested.
### Text, focus, and accessibility
Gameplay text is native and localized, never baked into generated art. Critical HUD labels are bounded, single-line fitted, outlined for contrast, and allowed an ellipsis fallback. Cards and the opaque high-z inspection preview both keep clipped two-line descriptions with ellipsis; the preview is not a general full-rules renderer.
Preserve tooltips, touch parity, captions, audio controls, flash/shake controls, and Full/Reduced/Minimal motion. Minimal motion removes flavor particles and trails but must keep essential state/result feedback. Visible focus is **not universal** today: chromeless hero, unit, passive, End Turn, and Service History controls use an empty focus style. Author and test visible focus plus modal/title initial focus before advertising complete keyboard accessibility.
Keyboard controls are contextual. Enter/Space starts from an unobscured title. In battle, Enter ends the turn, Q uses Chef Power, and 1–8 selects the matching hand slot. F10 toggles Runtime Tweaks. Escape follows modal-first precedence, cancels a pending target before ordinary battle pause, and is constrained by tutorial state.
Service History’s left rail shows the newest four events. Its modal blocks battle actions without pausing and exposes every retained encounter event. Kitchen Break’s View Deck is opaque and input-blocking; runtime cards are inspection-only, its card strip scrolls horizontally, and its rules/servings summary scrolls vertically. Both close through their native control or Escape.
Current hard ceilings are 180 tracked particles, 8 tracked overlays, and **12 concurrent transient SFX players**. Persistent BGM and the dedicated voiceover player are additional. Float text, contact rings, card ghosts, and ingredient flights self-clean but do not currently participate in equivalent admission counters. (`scripts/hearthstone_juice_profiles.gd` in the matching project)
## 6. Tutorial and Localization Contract
A normal new run intentionally renders an empty hand, then deals five guaranteed opening cards sequentially while input is locked. The repeating four-step tutorial uses the normal combat path: select Precise Chop, target the opening Pickle Imp, observe exact harvest, then End Turn. It yields during the enemy turn and may be skipped with Escape. It currently repeats for every new run and stores no completion flag.
Tutorial keyboard input is semantically step-gated. Pointer/touch input is spatially constrained by the dimmer and its clear spotlight or corridor, but is **not independently validated against the expected tutorial target**. Do not claim fully semantic pointer/touch gating until ordinary card/unit handlers enforce tutorial authorization and wrong-target tests exist.
Update `localization/en.json` and `localization/zh-CN.json` together. Key sets and placeholders must match exactly. Every card, recipe, encounter, history event, tutorial message, status, and control must resolve through a localization key. Run localization and fit tests after changing copy, art metrics, or fonts. Use the current CC0 primary/fallback chain and verify all shipped Simplified Chinese glyphs.
Locale resolution order is `PROTO_CARD_LOCALE` → graphical-session `user://localization.cfg` → normalized operating-system locale → English. Missing active-locale text falls back to English; a missing English key surfaces as its key. Preserve this precedence and test it when adding locales or changing preference storage. (`scripts/localization.gd` in the matching project)
## 7. Complete Reskin Asset Matrix
The safest complete reskin replaces content at the existing paths. Static images must be original, text-free, readable at runtime scale, and free of baked rules, numbers, labels, state badges, particles, environmental shadows, or logos. Godot owns those layers.
| Domain | Current contract | Generation notes |
| --- | --- | --- |
| Backgrounds | `title_kitchen.webp`, `battle_board.webp`, `kitchen_break.webp`; 1280×720 | Generate three text-free 16:9 environments with protected negative space for each screen’s UI. |
| Characters | `chef_sama.webp` and four encounter portraits; 512×512 | Transparent, centered, complete silhouettes; consistent camera, light, and scale. |
| Card illustrations | One image for every `CARDS[*].art`; 24 current faces at 384×576 | Generate illustration only. Godot supplies frame, name, cost, rules, stats, rarity, badges, and targeting states. |
| Card backs | Legacy `assets/template/cardgame/card_back.webp` plus live `assets/template/cardgame/juice/card_back.png` | Replacing only the legacy WebP does not reskin visible deck/draw/opponent-hand backs. |
| Combat icons | `icon_sword.webp`, `icon_shield.webp`; 96×96 | Simple high-contrast silhouettes at small scale. |
| Ingredients | `ingredient_{fungus,herb,meat,ember}.png`; 256×256 | Transparent resource emblems with distinct shapes, not color alone. |
| Foreground props | Card back, Mana burner, armor pan, Pantry jar, encounter seal, selection knife, cooking cauldron | Preserve semantic role and transparent silhouette. `juice_armor_pan` remains test-required even though normal runtime use is limited. |
| Leaderboard/tutorial | `leaderboard_crest.png`, `tutorial/mise_guide.png`, `tutorial/spoon_pointer.png` | No baked instructional text; callouts remain native. |
| HUD frames | Nine PNGs under `assets/template/cardgame/layout/` | Preserve exact dimensions and transparent apertures; always run the HUD processor. |
| Cursors | Twelve 96×96 RGBA PNGs under `assets/template/cardgame/cursors/` | `default`, `interact`, `inspect`, `grab`, `grabbing`, `serve`, `attack`, `support`, `cook`, `route`, `blocked`, `wait`. |
| Font | `assets/template/fonts/Figtree.ttf`, `resources/figtree_font.tres`, and `assets/template/fonts/EmberpanSansSC.otf` | Historical paths to migrate under the current typography contract; verify EN/CN glyph coverage, card fit, and HUD fit. |
| SFX | 28 non-looping WAV cues under `assets/template/cardgame/sfx/` | Keep semantic keys unless registry/tests change; new-game replacements use mono 48 kHz OGG under the shared export rules. |
| BGM | `assets/template/cardgame/music/emberpan_midnight_service.wav` | Current contract is stereo, 48 kHz, 16-bit, 82.5-second forward loop. |
| Voiceover | `assets/template/cardgame/voiceovers/legendary_summon.wav` | Current contract is mono, 48 kHz, non-looping; friendly legendary summon ducks BGM. |
| Code-native look | Palette, StyleBoxes, filters, targeting line, cracks, particles, flashes, vignettes, shake, card ghosts, sleep marks | A pixel swap does not change these. Reskin the owning scripts and effect kits deliberately. |
Supplemental live visual dimensions:
| Runtime file | Native dimensions |
| --- | ---: |
| `card_back.webp` | 384×576 |
| `juice/card_back.png` | 341×512 |
| `juice/mana_burner.png` | 237×256 |
| `juice/armor_pan.png` | 256×236 |
| `juice/pantry_jar.png` | 256×244 |
| `juice/encounter_seal.png` | 243×256 |
| `juice/selection_knife.png` | 256×170 |
| `juice/cooking_cauldron.png` | 512×512 |
| `leaderboard_crest.png` | 384×384 |
| `tutorial/mise_guide.png` | 512×512 |
| `tutorial/spoon_pointer.png` | 512×260 |
HUD runtime dimensions are contractual:
| HUD frame | Runtime dimensions |
| --- | ---: |
| Hero station | 512×252 |
| Unit plate | 264×264 |
| Passive medallion | 128×128 |
| Turn marker | 440×76 |
| End Turn | 256×176 |
| History ticket | 144×116 |
| Pantry tray | 384×280 |
| Mana rack | 300×144 |
| Deck cradle | 256×288 |
## 8. Preferred Manus Max Mode Static-Art Workflow
In Manus Max Mode, use the preferred built-in static-image generation tool. Outside Manus Max Mode, ignore this preferred-tool instruction, follow the shared asset generation mode gate, and use only the method selected by the user. For the preferred workflow, batch up to five related images per call. Use the default quality setting unless fine text is unavoidable; gameplay assets should contain no text. For transparent PNGs, provide a transparent-background setting using a color absent from the subject.
A useful prompt formula is:
```text
[asset role and subject], [camera/composition], [original art direction], [lighting and palette], fully contained silhouette, readable at [target size], no text, no numerals, no logo, no UI, no particle effects, no drop shadow, no copyrighted franchise characters or trade dress, transparent background.
```
Example tool payload:
```json
{
  "quality": "default",
  "images": [
    {
      "path": "/absolute/source-workspace/new_hero.png",
      "prompt": "Original full-body fantasy card-game hero portrait ...",
      "aspect_ratio": "1:1",
      "transparent_background": "#00FF66"
    }
  ]
}
```
Keep raw generations outside runtime directories. Record prompt, generation metadata, date, rights, and source hash. Inspect every output for copied IP, baked text, malformed hands/props, clipped silhouettes, checkerboard pixels, and inconsistent light. Normalize the approved images with a project-owned, portable process and reimport with Godot. The
historical `scripts/process_card_assets.py` and `scripts/process_hud_layout_assets.py` are not included
in this reference, and raw generation sources are not provided. Do not claim the original art pipeline
is reproducible or invoke these missing scripts. Preserve the documented HUD aperture, transparency
and hidden-RGB cleanup requirements in any replacement processing workflow.
## 9. Generate Music and Sound
### Preferred Manus Max Mode BGM workflow
Follow [audio production as needed](game-workflow.md#audio-production-as-needed). Reuse fitting permitted audio or safe silence for optional BGM. Only when new music is needed, use the authorized live generation workflow. For the preferred workflow, describe genre, mood, tempo, instrumentation, structure, loop behavior, and gameplay intensity. Never name an artist, song, or album. End instrumental prompts with `Instrumental only, no vocals`.
```json
{
  "path": "/absolute/source-workspace/gameplay_loop.wav",
  "prompt": "Original instrumental card-battle score, 96 BPM ... clear loop-safe ending, restrained midrange for UI readability. Instrumental only, no vocals"
}
```
Generate to a source workspace, audition in context, then master/convert the final runtime file to stereo 48 kHz OGG under the shared export rules. Migrate the reference WAV path and forward-loop import to the looping OGG, updating registries and tests together; preserve the Music bus, persistent playback, mute behavior, and legendary-voice ducking. If duration changes from 82.5 seconds, update the importer, `juice_director.gd`, runtime-audio tests, and export checks deliberately.
### Small SFX
Use [audio production as needed](game-workflow.md#audio-production-as-needed): retain fitting cues, produce only missing effects that aid gameplay, and verify changed mappings. No full HUD/UI sound inventory is required.
When using procedural SFX, implement concise original one-shots with Godot `AudioStreamGenerator` and `AudioStreamGeneratorPlayback`: envelope-shaped sine/triangle tones for UI, short pitch sweeps for actions, filtered noise for impacts/fire/steam, and layered taps for material cues.[8] Push frames into a short buffer, stop and release the player after the envelope, route it to the existing bus, honor mute/settings, and add deterministic registry and playback tests; if retaining the static-stream registry, author source WAVs with Godot `AudioStreamWAV` data outside the runtime tree, then convert them to OGG and update registry paths/imports/tests before upload. When using built-in generative SFX, follow the baseline's internal routing. Audition changed cues in context; original procedural SFX are valid final assets. This choice is for **SFX**. BGM remains optional under the shared policy; preserve specifically requested voice acting.
Current audio buses are `Master`, `UI`, `Cards`, `Combat`, `Ambience`, `Music`, and `Voice`, with shipped gains of −3/−2/−1/0/−8/−5/−4 dB. The 28-key `SFX_KINDS`/`SFX_STREAMS` registry is one-to-one: UI cues route to UI, draw/play to Cards, caption voice to Voice, and other effects to Combat. The Ambience bus currently has no authored stream; ambient motes are visual only. (`scripts/juice_director.gd` in the matching project)
Mute pauses BGM, stops voiceover, and blocks new SFX; already-playing one-shots are allowed to finish. Friendly legendary voiceover ducks the BGM by 9 dB and restores it when the voice stops or finishes.
## 10. Reskin Code-Native Game Juice
Static art does not replace the template’s visual identity by itself. Review and update:
| Owner | Theme-bound behavior |
| --- | --- |
| `card_game.gd` | Semantic colors, panels, native card chrome, labels, filters, screen shades, state badges, event dispatch. |
| `juice_director.gd` | Particles, rings, flashes, vignettes, shake, card ghosts, ingredient flights, drop overlay, audio routing. |
| `hearthstone_juice_profiles.gd` | Blade/fire/broth/armor/meat/fungus/boss kits, colors, particle families, tiers, budgets. |
| `cursor_director.gd` | Cursor registry, halos, trails, ripple, wait rotation, semantic modes. |
| `tutorial_callout.gd` | Dimmers, spotlight, corridor, pointer, callout treatment. |
| `card_crack_overlay.gd` | Seeded damage-crack geometry. |
Preserve semantic event meaning, bounded effect counts, captions, motion tiers, coordinate transforms, and cleanup. Essential information must survive Minimal motion and muted audio.
Sleep feedback is motion-aware: Full mode spawns animated localized Z labels, while Reduced and Minimal show a static trail. Targeting uses a live transformed card/unit source, a pointer-following curved line, Ember for ordinary/enemy targets, Teal for friendly buffs, and a fixed high layer. Cancel, leaving Battle, or opening Runtime Tweaks dismisses it; an in-Battle rerender retains the pending action and refreshes the line from the live source transform.
Ambient motes are visual-only. Battle/title use Ember-like motes and Kitchen/route use pale steam; reduced motion, the ambient-particle toggle, and signature sequences suppress them.
> **Current presentation divergence:** cooking animates ingredient flights, but normal precise harvest does not. The precise-cut event emits a fallback sword flight only when ingredient art lookup fails. Either make normal precise-harvest flights intentional and test them or avoid claiming that behavior in a reskin. The published budgets also remain partial until float text, rings, ghosts, and flights receive explicit admission/eviction policy and saturation coverage.
## 11. Extend Content or Mechanics Safely
For a pure reskin, keep IDs and effects stable and replace art/copy. For a new mechanic:
**1.** Add or revise the data contract in `card_database.gd`. **2.** Implement resolution in the owning path: `_resolve_nontarget_card`, `_resolve_targeted_spell`, `_resolve_on_play`, `_trigger_mise_engine`, combat, harvest, turn, or progression logic as appropriate. **3.** Add localized EN/CN name, rules, history, tutorial, and error text. **4.** Give the effect a semantic Juice event, accessibility caption, and audio/visual behavior. **5.** Teach enemy AI and tutorial gates if the rule affects either. **6.** Add deterministic positive, cancellation, edge, defeat, stale-turn, and exported-runtime coverage.
Encounter passives are currently hard-coded branches. Refactor them to data-driven passive IDs before adding many encounters; otherwise every new encounter increases hidden coupling in `card_game.gd`.
## 12. Runtime Tweaks, Persistence, and Sandbox Sync
The tweak panel exposes 61 validated controls across UI, Gameplay, Audio, Player, Enemies, and Environment. It pauses safely, persists nondefault deltas after a debounce, supports per-parameter/category/global reset, and applies audio values immediately. (`scripts/runtime_tweak_controls.gd` in the matching project)
Catalog `mode` values such as `LIVE` and `NEXT BATTLE` are **UI metadata**, not a globally enforced scheduler. Trace each consumer before relying on its label. For example, maximum board slots and the enrage threshold can affect an active encounter despite their timing labels. Keep label, consumer timing, rank eligibility, and tests aligned.
`AtomicJsonFile` writes a validated `.tmp`, rotates a valid primary to `.bak`, promotes the replacement, and recovers from corrupt or missing primary data. (`scripts/atomic_json_file.gd` in the matching project) Current saves cover preferences, lifetime stats, local scores, pending global submissions, and tweak deltas. **They do not save or resume an active run.**
Headless and `GAME_CAPTURE_DIR` sessions deliberately neither read nor write stats, tweak deltas, or locale preference. Source-test and capture success is therefore **not persistence or restart evidence**; save changes need a graphical filesystem/restart test.
`emberpan_card_stats.json` uses schema 1. Loading accepts schema ≤1, retains score/pending records only for the current score version, and upgrades the legacy singleton `pending_global_submission` into the FIFO `pending_global_submissions` array on a subsequent save. Local history keeps the top 20 completed runs after deterministic sorting, including custom-rule runs marked unranked. Only ranked-eligible results enter the global retry queue.
Browser `user://` data is local to that browser/device. It does not automatically sync to a Manus account, the parent iframe, or the sandbox. If a project requires **sync back to sandbox**, implement it explicitly as a development-only feature:
| Requirement | Recommended contract |
| --- | --- |
| Export | Add an explicit **Export Config** action that serializes schema version plus validated nondefault tweak values. |
| Bridge | Use a narrow `postMessage` bridge or `/api/dev/tweaks` endpoint; validate origin, schema, IDs, ranges, and body size. |
| Authorization | Enable only in development, require loopback or a short-lived secret, and never expose arbitrary file paths. |
| Destination | Write to a dedicated ignored sandbox artifact such as `captures/runtime-tweaks.json`; do not mutate source or `project.godot` silently. |
| Import/conflict | Require an explicit import action and define local-wins/server-wins/version-mismatch behavior. |
| Production | Disable the bridge unless account sync is an intentional authenticated product feature. |
Do not tell users configuration is synced until this bridge exists and has security, persistence, and conflict tests.
## 13. Local Leaderboard Default and Optional Global Implementation Reference
New games ship the local leaderboard and its UI by default. Do not carry forward the global tab, HTTP client, retry queue, development server, hosted integration, or global deployment work unless the user explicitly requests a global leaderboard. The details below document optional reference code in this template; an opted-in game must use a Manus WebDev database and complete the database, API, UI, and integration workflow defined above.
The Godot client uses `GET /api/leaderboard?limit=5` and `POST /api/leaderboard` with `score_version: 2`. It tries browser same-origin first **only for loopback and approved HTTPS `.manus.space` or `.manus.computer` origins**; another Web host must update the origin policy or provide an explicit API URL. It then tries configured canonical fallbacks, with request IDs, a 20-second timeout, transient retries, route-missing failover, local FIFO retry storage, and player-visible diagnostic codes. (`scripts/leaderboard_client.gd` in the matching project)
Keep game and API same-origin when possible. Every client request adds `X-Request-Id`. The bundled server has CORS disabled by default; a cross-origin deployment must explicitly allow the requesting origin and that header, then pass a real browser preflight test.
The standalone `scripts/leaderboard-server.mjs` is the **only leaderboard server implemented in this repository**. Its standalone entry serves generated `web/` and stores the best 1,000 records in `data/leaderboard.json` by default. Read limits clamp to 1–20, request bodies are capped at 16 KiB, and its health route reports process/API status rather than managed-database readiness. (`scripts/leaderboard-server.mjs` in the matching project)
Ranked submissions persist FIFO and post one at a time. A queue head is retried on result completion, title entry, or leaderboard refresh. One operation makes `max(3, configured endpoint count)` immediate attempts without delayed background retry or backoff. The pending queue is currently uncapped, and version-mismatched saved entries are discarded on load.
The current Manus deployment depends on a **separate, pinned WebDev project**, `junnyboi/scissorhands` branch `proto-card-web`, at commit `54ad156b107c0889559a7613b5267c378196023b`.[9] At that pinned revision, the external project provides the minimal iframe shell, Express routes, Drizzle repository, MySQL/TiDB schema/migration, database-aware health, CORS failover, request diagnostics, and API tests. Future agents must verify or update that pin before relying on those claims; the external service may evolve independently.
That external production server validates all fields, enforces possible victory/defeat combinations, recalculates score, deduplicates immutable submission IDs, ranks by score descending then creation time and submission ID ascending, and exposes database-aware health. Its owning paths are `server/leaderboard/`, `drizzle/`, `client/public/game.html`, and `client/src/pages/Home.tsx` in the pinned repository.
Any score-contract change must update, in one change set: game counters, Godot client, local save migration, score version, development server, hosted domain validation, database schema/migration, documentation, API tests, offline retry tests, and UI copy.
When using that external host, keep its shell as a minimal responsive iframe loading same-origin `/game.html`; the game then calls same-origin `/api`. Upload/rebase loader JS, PCK, WASM, splash, and icons as one identity-consistent set. That external repository is separate reference infrastructure; Manus Game projects use the packaged prepare-release and publish flow. Do not replace the Addon host with this standalone service.
## 14. Phase-Gated Delivery Workflow
Stop after each phase, test, and inspect before continuing.
| Phase | Work | Required evidence |
| --- | --- | --- |
| 0 — Baseline | Pull, inspect clean status, classify change, run source suite | Clean baseline and captured current behavior |
| 1 — Data/copy | IDs, content, effects, EN/CN | Gameplay, localization, tutorial, reliability tests |
| 2 — Assets/audio | Generate, provenance, normalize, import | No missing resources; dimensions, alpha, apertures, audio contracts pass |
| 3 — Layout/presentation | HUD, cards, effects, cursors, filters | Layout/cursor/Juice tests plus visual review at standard, compact, dense, both locales, larger text, and every motion tier |
| 4 — Persistence/services | Saves, tweaks, leaderboard, config bridge | Atomic recovery, offline queue, idempotency, server/database/API tests |
| 5 — Source gate | Complete implementation | `pnpm test` passes with no parser/resource/leak diagnostics |
| 6 — Package gate | Fresh Web export | Manifest digest, PCK validation, exported-runtime tests pass |
| 7 — Browser release | Hosted bundle and API | Cache-busted desktop/mobile boot, correct assets, no console errors, API health, leaderboard retry/submission |
A green headless suite does not approve artistic crops, contrast, character scale, transparent edges, card readability, or animation timing. Human visual inspection remains mandatory. The computer is excellent at counting pixels and remains admirably indifferent to taste.
`pnpm capture` is a **1280×720 diagnostic PNG dump**, not a pixel-regression or responsive-approval test. Verify the expected files exist and inspect them, then separately capture or manually validate compact safe-canvas states. `pnpm test:exported-runtime` mounts the PCK in headless Godot; it is not a browser, iframe, CORS, isolation-header, or hosted-API test.
The shared Godot launcher currently has no process watchdog. Add launcher-enforced per-gate timeouts that kill a hung child and print captured output; test-local semantic waits are not a suite watchdog. Record `pnpm release:check` output and Godot-native visual checks before checkpoint delivery, then hand off desktop/mobile browser acceptance to the user under the shared verification workflow. Record pending user acceptance separately and use [Game workflow](game-workflow.md) for verification scope. (`scripts/run-godot-test.mjs` in the matching project)
## 15. Commands
Godot 4.7.2, Node.js 22+, pnpm, Python 3, and Pillow are expected.
```bash
pnpm install
# Focused source gates
pnpm test:game
pnpm test:localization
pnpm test:layout-assets
pnpm test:battle-layout
pnpm test:cursor
pnpm test:tutorial
pnpm test:tweaks
pnpm test:hearthstone-juice
pnpm test:juice
pnpm test:atomic-json
pnpm test:leaderboard
pnpm test:reliability
# Complete source and visual gates
pnpm test
pnpm capture
# Fresh package and release gates
pnpm export
pnpm verify-export
pnpm test:exported-runtime
pnpm release:check
# Manus preview uses the packaged resident Game server (see Game workflow).

```
When working in the pinned external WebDev repository, run its TypeScript, API, and build gates separately, apply Drizzle migrations through the managed database workflow, then verify:
```bash
curl -i https://<published-host>/api/health
curl -i 'https://<published-host>/api/leaderboard?limit=5'
```
Never hand-edit `web/`. `pnpm export` deletes and recreates it. `pnpm verify-export` rejects a stale or mismatched **manifest/source pair** and verifies that the supplied PCK boots with required contents, but it does not cryptographically prove that the manifest, loader JavaScript, WebAssembly module, and PCK came from one export.
Preserve the export’s cross-origin-isolation headers. Because the generated bundle uses stable `index.*` filenames and the reference server caches non-HTML assets for one hour, publish loader, PCK, WASM, splash, and icons atomically and invalidate or version cached assets before release verification.
## 16. Known Gaps and Stop-the-Line Warnings
| Gap | Required response |
| --- | --- |
| **Dragonpepper Roast is unreachable in normal play.** It requires Meat + Ember, but current enemy ingredient records award only Herb, Fungus, and Meat. | Add an ordinary Ember source and reachability/text-contract test, or remove/reprice the recipe and update art/UI/localization/tests consistently. |
| Guard constrains attacks but not targeted Techniques | Decide the intended rule, align targeting legality and rules text, and test unit/hero targets with a Guard present. |
| Banquet Tyrant enrage checks only through `_damage_enemy_hero` | Centralize threshold evaluation if all hero Health loss should enrage; cover Cursed Onion self-damage crossing the threshold. |
| No staged-opening cancellation regression | Interrupt the sequential opening deal with title/replacement/terminal transitions and prove no stale mutation. |
| `ui.hud_scale` is overwritten by resize projection | Compose user HUD scale with safe-canvas scale and test standard/compact/safe-inset resize retention. |
| Tweak timing labels are not uniformly enforced | Audit every `mode`, defer non-live consumers correctly, and add metadata-to-consumer timing tests. |
| Pointer/touch tutorial gating is spatial, not semantic | Reject wrong cards/targets in tutorial handlers and add real touch-event tests before claiming full gating. |
| Visible keyboard focus and initial focus are incomplete | Author focus for chromeless controls plus title/modal initial focus and add tab-order/focus-visibility tests. |
| Headless/capture tests bypass persistence | Add graphical filesystem/restart coverage for stats, locale, tweak deltas, queue migration, and FIFO replay. |
| Custom-domain and cross-origin leaderboard paths are unverified | Make origin policy configurable, allow `X-Request-Id`, and add browser CORS/preflight/custom-host tests. |
| Export manifest does not bind every bundle artifact | Record loader/PCK/WASM hashes and verify identity before deployment. |
| Godot test launcher has no global timeout | Add per-gate watchdogs and kill/report behavior for deadlocked tests. |
| Presentation limits do not cover every transient node | Add counters/eviction and saturation/cleanup tests for text, rings, ghosts, and ingredient flights. |
| Precise-harvest ingredient flight is not dispatched normally | Either dispatch/test the intended ingredient flight or remove the generalized presentation claim. |
| No active-run save/resume | Do not advertise run recovery. Add versioned run-state serialization and stale-action recovery tests before claiming it. |
| Enemy deck loops without fatigue; AI is shallow priority logic | Decide whether this is pressure or a defect. Add enemy fatigue/turn cap and strategic tests if the pivot needs deeper play. |
| No comprehensive content reachability/effect-text contract | Add a data-driven test that every card/recipe is reachable and localized text matches behavior. |
| Rules renderer is not reachable from the current title UI | Wire a visible rules action with EN/CN, focus, Escape, and responsive modal tests. |
| No gamepad implementation | Add actions, navigation, confirm/cancel, glyph strategy, and real-device tests before advertising gamepad support. |
| Safe-inset injection exists, but no demonstrated live mobile notch query | Only for requested mobile support, add the needed safe-area handling and validation. Landscape-only remains the current contract. |
| Historical asset metadata is incomplete | Preserve existing records; do not add a provenance repair task. Fix only actual missing runtime resources. |
| No current config/account/sandbox sync | Implement the explicit narrow bridge described above; `user://` is device-local. |
| Public leaderboard is not anti-cheat | Strong trust requires authentication, signed attestations, server-authoritative runs, or managed abuse controls. |
| Optional external host needs its own deployment contract | Keep it separate from the Addon Game release flow and verify its source/bundle/API identities if explicitly adopted. |
## References
[8]: https://docs.godotengine.org/en/stable/classes/class_audiostreamgenerator.html "Godot AudioStreamGenerator documentation"
[9]: https://github.com/junnyboi/scissorhands/tree/54ad156b107c0889559a7613b5267c378196023b "Pinned external Proto Card WebDev host"
Additional project-specific detail is maintained in `STRUCTURE.md` (`STRUCTURE.md` in the matching project), `ASSETS.md` (`ASSETS.md` in the matching project), `PLAN.md` (`PLAN.md` in the matching project), `MIGRATION_PLAN.md` (`MIGRATION_PLAN.md` in the matching project), and `THIRD_PARTY_NOTICES.md` (`THIRD_PARTY_NOTICES.md` in the matching project).
