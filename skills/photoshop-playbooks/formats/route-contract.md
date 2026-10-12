# Photoshop Route Contract

## Route precedence

1. Preserve an explicit client request: Photoshop Web and Photoshop Desktop are different products.
2. Name the retained output state: F1, F2, W1, D1, or A1.
3. Check route availability and required account, plan, runtime, file, app, and version state.
4. Choose the least fragile mechanism that preserves the requested state.
5. State the route and truth label before mutation.
6. Escalate only for a named missing object, failed representative sample, compatibility requirement, or explicit client lesson.

## Truth labels

| State | Completion label | Must not be called |
|---|---|---|
| F1 | New standalone generated or refined image | PSD, layered file, editable Photoshop state |
| F2 | Deterministically transformed image set | Photoshop batch or Action unless Photoshop actually ran |
| W1 | PSD created or edited in Photoshop Web, with named retained objects verified | Desktop Photoshop state or universal PSD fidelity |
| D1 | Photoshop Desktop state, with named retained objects verified | Reusable automation unless an automation asset was created |
| A1 | Named Action, Batch configuration, Variables template, droplet, or approved script, with replay proof | Merely a completed current batch |

## Object-level questions

Ask only questions that can change the route:

- Is a standalone image enough, or must a PSD remain editable?
- Which editable objects must survive: ordinary layers/masks, paths, Smart Objects, text, Variables, Actions, plugins, or something else?
- Did the user choose Photoshop Web, Photoshop Desktop, or only the Photoshop product?
- Is the goal the current result, a reusable Photoshop asset, or a lesson?
- Are exact text, brand geometry, color profile, print proofing, or installed resources acceptance criteria?

Do not ask for a client preference when every compatible route produces the same accepted artifact. Do ask when an app-native retained state or lesson is part of the product.

## Escalation record

Whenever a route changes, record:

- original route and sample;
- observed failure or named unsupported object;
- new route and additional retained state;
- whether the change requires user approval, app setup, or serialized CU;
- revised verification oracle.
