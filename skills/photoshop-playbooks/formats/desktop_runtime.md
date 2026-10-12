# Photoshop Runtime Preflight

Run only the sections required by the selected route.

## Native image route

- Confirm the current session exposes the required image tool and permits the request.
- Confirm references are accessible and the output contract fits. Image refinement creates a new flattened PNG; it does not create Photoshop layers, masks, paths, or Actions.
- Use a representative sample. If exact text, identity preservation, transparency, or brand geometry matters, verify it independently and fall back to a deterministic or Photoshop route when the sample fails.

## Deterministic file route

- Confirm all inputs are attached, retrieved, or inside the authorized Desktop shared folder.
- Probe the required codecs and libraries in the active Sandbox; prompt guidance is not proof that a runtime is installed.
- Write to a separate destination and build an expected-output manifest before scaling.
- For large files, account for chunked transfer and local bridge limits rather than assuming one-shot reads.

## Photoshop Web through My Browser

- Confirm My Browser is installed, ready, authenticated to the intended Adobe account, and selected as the browser route.
- Confirm the requested object and operation exist in the current Photoshop Web build and plan. Product feature tables drift.
- Use a copied representative PSD. Save/export, reopen, and inspect the exact required objects before scaling.
- Treat My Browser as browser control, not Computer Use. A browser command success does not prove PSD fidelity.

## Photoshop Desktop through Computer Use

- Confirm Photoshop is installed and resolve the intended version from installed-app state. Do not rely on a remembered filesystem path.
- Confirm the CU helper is ready and no other session owns the desktop-control lease.
- Open a disposable copy and capture fresh coherent state. Never encode absolute coordinates or replay stale element handles.
- Batch only coherent subgoals, then re-observe the target state, destination, and saved artifact.
- Use state-based bounded waits. If the app remains incoherent or a required control cannot be established, stop, preserve the copy, and report the blocked step.
- Finish the CU session exactly once after the final verification.

## Reusable Photoshop automation

- Separate the reusable Photoshop asset from the Manus procedure that creates or teaches it.
- For Actions/Batch/Variables, use a copied template, separate output destination, fresh unseen replay, and persistence check after reopen.
- A Photoshop-hosted script is optional and setup-dependent. Current Manus Desktop does not provide a general Photoshop scripting connector. Use such a script only when the user accepts the artifact and a supported invocation path is proved.
- Do not claim that “the user handles the script or secret” completes an execution design; invocation, permissions, failure handling, and logs must also be bounded.

## Parallelism

Run native-image, deterministic-file, and independent browser tests in parallel only when they do not mutate the same assets. Run all Desktop CU cases serially.
