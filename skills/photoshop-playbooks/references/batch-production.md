# Batch Production (Cards 1, 4, 5, and 8)

## Card 1 — Product and specification-safe ID batches

**Use when:** the user needs consistent crop, margins, background, size, naming, or delivery across a batch. Typical cases include ecommerce catalog images, marketplace listings, staff-badge photos, school portraits, and licensed campaign assets.

**Why it matters:** paid service markets, community requests involving hundreds or thousands of files, creator tutorials, and first-party batch documentation converge on this family. Product imagery is the primary demand case; ID photos share some mechanics but carry stricter integrity limits.

**Inputs:** source folder, geometric specification or reference, background/alpha requirement, naming rule, output sets, retained-state requirement, and approved identity-safe edits.

**Primary channel:**

- F2 for measurable crop, resize, naming, conversion, compression, and validation.
- F1 for standalone subject-aware background or object changes when the native route is exposed and the sample passes.
- W1 for an ordinary editable mask that survives a proved Photoshop Web round trip.
- D1 for a named desktop-only object such as a clipping path or a specific unsupported web control.
- A1 when the user needs a retained Action for future batches.

**Escalation trigger:** move beyond F1/F2 only for a named retained object, explicit client lesson, failed representative sample, or measured fidelity gap.

**Hybrid handoff:** F2 inventories and normalizes the batch; F1 handles approved standalone semantic changes; W1/D1 handles only retained-state outliers; A1 packages a reusable deterministic tail.

**Verification:** reconcile count, dimensions, names, alpha/background, edge rubric, source hashes, and review list; reopen or replay any promised retained Photoshop state.

**Workflow:**

1. Freeze the specification and retained product.
2. Inventory sources and classify fixed transforms versus semantic transforms.
3. Build a representative sample across easy and difficult edges.
4. Approve the sample; separate outliers by observed failure, not file name.
5. Run each subset through its chosen route into a separate destination.
6. Reconcile count, dimensions, names, alpha/background, source preservation, and review list.

**Failure and recovery:** resume from the manifest; never rerun completed names blindly. Difficult hair, translucent objects, reflections, edge contamination, or identity-sensitive regions go to review or a proven retained-state route.

**Record as skill:** record only a closed Photoshop-specific Action/Batch or lesson branch. F1/F2 branches should remain parameterized procedures rather than coordinate recordings.

**CU display:** conditional. Show only when the user explicitly needs Desktop Photoshop state or a reusable Action; a routine flattened catalog batch is not a CU showcase.

## Card 4 — Data-driven variants

**Use when:** structured rows must produce exact names, numbers, images, or offers. Typical cases include sports jerseys, event credentials, certificates, product colorways, localized ads, and personalized sales graphics.

**Inputs:** copied template, field contract, CSV/TSV or spreadsheet, asset paths, font requirements, output naming, and desired retained asset.

**Primary channel:**

- F2 for exact standalone outputs rendered from a deterministic template.
- A1 for a reusable Photoshop Variables/data-set system in Desktop Photoshop.
- Do not use generative image tools for exact names, numbers, regulated copy, or mandatory brand text.

**Escalation trigger:** use A1 only when a reusable Photoshop Variables/data-set asset must remain; otherwise keep exact rendering in F2.

**Hybrid handoff:** deterministic tooling validates and normalizes rows/assets before a proved Desktop Variables branch consumes the copied template.

**Verification:** valid rows equal outputs; exact copy/assets/names reconcile; A1 additionally requires reopen and fresh-row regeneration.

**Workflow:**

1. Normalize field names and validate blank values, quoting, non-ASCII text, duplicates, text overflow, missing assets, and missing fonts.
2. Use a copy of the template and a separate destination.
3. Generate a small row set and reconcile every field.
4. For A1, create or bind the Variables system only through a live-proved procedure.
5. Generate the full set and compare output count to valid rows.
6. Prove one unseen row can be regenerated after reopen.

**Failure and recovery:** quarantine failed rows with reason codes; never overwrite the template with an applied data set.

**Record as skill:** strong candidate after Variables has app/OS-specific live evidence. The recording should parameterize data path, field mapping, destination, and naming rather than hard-code sample values.

**CU display:** yes only for the retained Variables workflow. Flat exact-output rendering is a file workflow.

## Card 5 — Action, Batch, and reusable automation

**Use when:** the user wants repeatable Photoshop steps available for future files, not merely the current output.

**Inputs:** demonstrated process, deterministic-versus-judgment split, copied sample set, Action name, destination, naming policy, error policy, and supported Photoshop client/version.

**Primary channel:** A1 in Photoshop Desktop. A Photoshop Action is app state; the Manus skill is the routing and teaching procedure around it.

**Escalation trigger:** if the user needs only the current output or the sequence contains unsafe image-dependent decisions, keep those parts in F1/F2 or reviewed manual passes rather than recording them.

**Hybrid handoff:** deterministic tooling prepares fixtures and validates outputs; CU creates and tests only the retained Photoshop automation asset.

**Verification:** prove Action persistence after reopen, fresh unseen replay, isolated destination, exact output manifest, and unchanged sources.

**Workflow:**

1. Decompose the demonstration into deterministic steps and per-image judgment.
2. Exclude changing selections, brush strokes, and taste decisions unless the app operation itself generalizes safely.
3. Record the Action only after the exact current procedure is live-proved.
4. Configure source, separate destination, naming, and error behavior. Do not use a source-overwrite mode by default.
5. Replay on an unseen sample, inspect the result, reopen Photoshop, and prove the Action remains discoverable and editable.
6. Deliver the Action usage contract, excluded steps, and failure recovery.

**Failure and recovery:** stop on the first unexpected source mutation or destination collision. Reconcile output names before retrying.

**Record as skill:** flagship CU candidate after O1 closure because both the app asset and repeatable Manus procedure remain useful.

**CU display:** yes. Reason: the user keeps a Photoshop-native automation asset that cannot be created by flattened image generation or deterministic file conversion.

## Card 8 — Delivery and export pipeline

**Use when:** one source set must become web, marketplace, print, review, or archive variants.

**Inputs:** one measurable specification row per output set: format, dimensions, quality/size, alpha, naming, metadata/profile requirements, and retained Action requirement.

**Primary channel:**

- F2 for ordinary format, dimension, quality, size, and naming transformations.
- W1 only when Photoshop Web supports and preserves the exact required source state.
- D1 for a named desktop-only proofing, plugin, or export behavior that has current evidence.
- A1 for a reusable export Action.

**Escalation trigger:** use W1/D1/A1 only for a named retained source object, proof/profile/plugin behavior, or reusable Action that F2 cannot preserve.

**Hybrid handoff:** Photoshop produces only the app-specific master or retained automation; F2 creates and validates mechanically equivalent derivatives.

**Verification:** inspect signatures, dimensions, duration-independent image properties, byte ceilings, names, alpha, requested metadata/profile, and Action replay when promised.

**Workflow:** build the specification table, preflight routes, export to separate destinations, then validate signatures and every measurable requirement independently of app success messages.

**Failure and recovery:** retain the manifest and rerun only missing or invalid outputs. Do not use “color-managed” as a blanket Desktop trigger; name and test the exact profile or proof requirement.

**Record as skill:** only the closed reusable Action or exact app lesson branch.

**CU display:** conditional; routine export variants belong to deterministic processing.
