# Talking Heads and Interviews

Use this for creator monologues, tightly edited interviews, recorded speeches, and personal-brand shorts. Start with accurate audio cut points, bring the strongest moments forward, then deliberately handle portrait framing, punch-ins, and B-roll. If the user only specifies removing one line, changing subtitles, or exporting, work directly on that scope

## Let Speech Determine Cut Points

Reuse existing transcripts first. For speech edits, see [Speech cut points](../capabilities/transcription.md#speech-cut-points). Sentence boundaries guide the rough cut; for ambiguous boundaries or joins, inspect word-level timing and audition them, preserving the complete first and last syllables

A gap of about 0.2 seconds between sentences is a starting point for natural pauses, roughly 5–6 frames at 30 fps. Fast promotional speech can tighten to 0.10–0.15 seconds; reflective or important emotional beats can hold for 0.30–0.50 seconds. Adjust pauses to the content and retain small natural inhalations so speech can breathe

A few minutes of talking-head footage can produce dozens of clips. Build a keep/delete list around the arguments. After each batch of splits, inspect the produced files and continue with their actual paths and source-time ranges. Update the next batch's plan from the file-based edit manifest

## Select Takes and Organize the Delivery

When an idea is repeated, compare completeness, natural delivery, and rhythm, and choose the best take. A later take is often smoother, but decide from the actual sound and completeness of information. Remove preparation before the first line, repeated attempts, meaningless thinking gaps, and the sound of stopping the recording after the final line

By default, retain the original order for faithful delivery. For a stronger opening, bring the original line with the most insight, surprise, or emotional force into the first 3 seconds, add a bold title, then return to the natural order of development. Preserve qualifications and necessary context so reordering retains the speaker's intended argument

## Punch-ins and B-roll

At an emphasized line or a turn in the argument, use a punch-in of about 1.10–1.15, returning to 1.0 on the next sentence. A slight framing change relieves the monotony of a fixed camera and can hide a jump cut. A typical acceptable range is about 1.08–1.15; inspect source quality first. Above 1.3, clarity and framing room are more likely to suffer

B-roll should correspond to a specific object, procedural step, event, or idea being mentioned, appearing when the keyword arrives. Arriving too early reveals the point prematurely; arriving too late separates the picture from its explanation

For example, on “Apple launched the new M4 chip,” cut to the relevant footage at the first visual moment of “Apple,” hold while that point is explained, and return to the person when the explanation ends at a sentence pause

## Reframe for Portrait by Shot

Filling a 9:16 portrait canvas with 16:9 landscape footage crops the sides. Actual scale and crop depend on the source and canvas dimensions. Establish the fill geometry first, then adjust horizontal position from the image so faces, gestures, and the objects being discussed remain within the usable area

Use stable framing for each shot and change position at cuts. When the subject is stable within a shot, keep a fixed horizontal position. Adjust when the person moves noticeably; following every small sway frame by frame can create mechanical jitter

1. Set a portrait canvas and place the source using a fill strategy
2. Sample representative frames from each split shot to determine whether the person is left, center, or right, and identify any board, slide, or object that needs to remain visible
3. Use FFmpeg crop and scale filters to give each clip a stable horizontal position. Default to centered framing. If a person and board occupy opposite sides, compensate in the direction that preserves the important content in the actual image
4. Check the beginning and end. Sample additional moments in shots with substantial action, check whether faces or gestures approach the edges, and adjust that shot's framing

For two-person conversations, choose reverse angles, a stacked layout, or the full landscape frame so both people's faces and actions remain visible

## Complete Editing Workflow

1. **Confirm delivery**: audience, aspect ratio, target duration, existing assets, and the main line of expression
2. **Obtain speech timing**: reuse transcripts first and add sentence- or word-level timestamps as required
3. **Rough-cut the content**: remove noise, meaningless gaps, and repeated attempts, retaining the best take
4. **Build the opening**: choose the strongest original line as a 0–3 second hook, reordering when useful while preserving the complete argument that follows
5. **Refine audio joins**: start with sentence gaps of about 0.2 seconds and clean tail noise. Treat 1–2 frames of margin as a starting point; choose by the actual audio
6. **Reframe as needed**: for portrait, sample each shot, set stable horizontal positions, and check beginnings, endings, and action peaks
7. **Arrange visual changes**: use punch-ins to emphasize points, align B-roll to the words it explains, and return to the person after the explanation
8. **Finish audio and subtitles**: clean room and join noise. Keep music below the voice, just loud enough to mask room tone at cut points, and synchronize subtitles to the actual speech

## Completion Criteria

- Speech timing supports the cut points; first and last syllables, plosives, and natural breaths remain intact
- Pauses suit the delivery, repeated attempts and NG takes are removed, and the best take is retained
- The first 3 seconds contain insight or an effective hook; meaning and context remain intact after reordering
- The subject stays stable and clear in portrait, with enough image quality and framing room after punch-ins
- B-roll aligns with keywords, subtitles remain readable and clear of faces and platform controls, and music stays below the voice

For batch splitting, position changes, or visual reframing, use deterministic local media operations and retain the source-time mapping needed to reproduce the result
