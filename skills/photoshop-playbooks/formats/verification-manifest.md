# Photoshop Verification Manifest

Use the section matching the promised output.

## Common manifest

- source count and source location class;
- source hashes when practical;
- selected sample IDs;
- destination and collision rule;
- selected route and retained-state code;
- completed, skipped, failed, and review-list counts;
- explicit user approvals for destructive or sensitive steps.

## F1 standalone image

- file signature, dimensions, alpha/background, and intended visible change;
- exact-copy/OCR check when text appears;
- protected-region or identity-preservation comparison when applicable;
- low-confidence list and approved sample.

## F2 deterministic file set

- expected versus actual count;
- format signatures, dimensions, byte-size limits, naming, and collision checks;
- profile or metadata only when explicitly requested and independently inspected;
- source/output hash comparison proving sources were not overwritten.

## W1 Photoshop Web PSD

- authenticated client and copied source;
- exact object list expected to survive;
- save/export destination;
- reopen and editability proof for each named object;
- unsupported, substituted, rasterized, or lost objects.

## D1 Photoshop Desktop state

- app and OS version;
- copied source and saved output;
- named layers, masks, paths, Smart Objects, text, or other required state;
- reopen/editability proof and flattened preview;
- recovery point if the app or batch was interrupted.

## A1 reusable automation

- exact asset type and name;
- source, destination, naming, and error policy;
- fresh unseen replay or fresh-row regeneration;
- persistence and discoverability after reopen;
- variable steps intentionally excluded from automation;
- recovery and duplicate-output reconciliation.

Never infer editable or reusable state from a flattened preview alone.
