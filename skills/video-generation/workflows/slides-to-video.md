# Slides to video

Use for online courses, training, internal briefings, and academic explanations. Organize by teaching section, with each section's established narration take and matching slides accomplishing one learning objective, making structure and synchronization clear. Handle local revisions directly on the specified page

## Structure by section

Usually divide the work into 3–8 sections. The five-section template below gives each section's teaching task and common duration; add or remove sections according to the course materials:

```text
Section 1  Context and challenge     (10–20s)  pose the problem, set the stakes
Section 2  Core concept              (30–60s)  the underlying logic, formula, or architecture
Section 3  Process and steps         (30–60s)  walk the procedure step by step
Section 4  Worked example            (30–60s)  a concrete case or a code walkthrough
Section 5  Recap                     (15–30s)  three takeaways and what to do next
```

Reuse existing explanation recordings directly; use [speech generation](../SKILL.md#generate-missing-assets) for new voices and [transcription](../capabilities/transcription.md) when speech timing needs to be added. Lock the narration take for each section, measure its actual start and end, then determine when pages, formulas, and key points appear

## Choose images by learning objective

| Teaching content | Visual treatment | Why this treatment works |
| --- | --- | --- |
| Processes, causality, data flows | A flowchart or animated diagram that unfolds with the explanation | Steps appear as they are explained so viewers can follow the logic |
| Numerical comparisons, formula derivations | Changing numbers, animated bars, step-by-step derivation | Makes changes and differences visible, helping viewers remember the result |
| Historical background, metaphor, stories | High-quality photos, illustrations, or substantiated examples | Concrete images establish atmosphere and improve viewing quality |
| Software demonstrations, original teaching slides | Real screenshots or screen recordings with a slow push in | Preserves information credibility while keeping images readable and alive |

Reuse existing images, slides, and SVG graphics directly; read the [Motion Graphics rendering guidance](../references/motion-graphics.md) when complex animation is needed

## Section cards

Start each section with a 2–3-second card stating the section number and topic, placed at the upper left or center, with a light page-turn sound or whoosh. This rhythm reset lets viewers see the course structure rather than only hearing a change of section in the explanation

Fill in a card for each section using the following:

| Item | Content and treatment |
| --- | --- |
| Section number | Matches the section order of the whole film |
| Topic | A brief title stating this section's learning objective |
| Position | Upper left or centered, continuing the film's typography, colors, and whitespace |
| Duration | 2–3 seconds, enough to read the number and topic |
| Sound | A light page turn or whoosh synced to the entrance, followed by the section's narration |

## Maintain readability and synchronization

Put frameworks, diagrams, and keywords on slides, and let the spoken explanation carry details; keep each page's substantive content to at most four lines and bold key terms. Check typography, contrast, and whitespace on a phone or in a small window so viewers can read clearly while watching

Make formula or diagram elements appear when narration mentions them. When a section exceeds 20 seconds, use visual changes to support the current explanation: highlight the part being discussed, apply a slow push to about 105–110%, or insert 2–3 seconds of relevant UI / examples before returning to the main teaching image. Leave reading time after important animations finish

Choose quiet, low-presence instrumental music that keeps the teacher's voice clear. Fully subtitle spoken explanations for muted viewing; slide text carries the framework, while subtitles carry what is actually said

## Completion checks

- Each section has a section title card and a clear learning objective
- Matching images and narration share the section's start and end, with key points appearing in sync with the words
- Diagrams and animations hold long enough to read, with large type and clear contrast
- Music is gentle, voices are clear, and subtitles cover the spoken explanation while avoiding bottom controls
- Multi-page assembly, subtitles, rendering, and verification follow the file-based guidance in the Skill entrypoint
