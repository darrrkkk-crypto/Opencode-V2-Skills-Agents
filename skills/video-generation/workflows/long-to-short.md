# Long Video to Short Clips

Use this for podcast excerpts, livestream edits, recuts of long interviews, and condensed speeches. Find the moments with the strongest emotion, the biggest surprise, or the most standalone value, bring the most powerful original line to the opening, and reframe for portrait. When only trimming an already specified clip, work directly on the range the user selected

## Find Segments Worth Watching on Their Own

| Signal | Language or visual markers to look for | Why viewers stay | Typical finished length |
| --- | --- | --- | --- |
| Counterintuitive claim | “Almost everyone gets this wrong,” “Stop doing X” | Overturns an assumption and invites the explanation | 30–60 seconds |
| Emotional peak | Genuine laughter, heated disagreement, choking up, a shocking moment | Empathy and emotional force | 20–45 seconds |
| Dense practical value | “Three steps,” “This lesson cost me a lot” | Concrete benefits and lessons worth saving | 45–90 seconds |
| A story with a turn | “There were only five thousand left in the account, and then...” | A reversal creates narrative pull | 60–120 seconds |

First scan existing transcripts for quotable lines and emotional peaks to locate candidates quickly, then confirm them with audio and visuals. For speech edits, see [Speech cut points](../capabilities/transcription.md#speech-cut-points). The lengths in the table guide editing rhythm; the argument must still be complete

## Make Each Clip Stand on Its Own

**One clip, one point**: for example, focus a 60-second clip on one idea or one story. Keep the context, qualifications, and resolution needed to understand it, and remove surrounding material that does not serve that point

**Lead with the hook**: bring the most compelling original line into 0–3 seconds and add a bold title. Once attention is secured, return to the natural order of explanation. Open immediately with a claim or suspense; provide background after viewers have a reason to keep listening

**Reframe for portrait**: when a 16:9 long video becomes a 9:16 social clip, rebuild the framing so the speaker's face remains clear and stable at the visual center while preserving important actions

## Portrait Layouts

| Layout | Treatment | When it helps |
| --- | --- | --- |
| Crop and center | Scale the landscape image to fill portrait, then set its horizontal position | Most immersive for a single speaker; check face and gesture boundaries |
| Letterbox with a soft background | Center the original landscape frame and fill above and below with a blurred copy of the same image | Preserves the full original frame and its surroundings |
| Two speakers stacked vertically | Put the questioner above and the respondent below | Keeps the interview exchange clearly visible |

Check faces, gestures, and the objects being discussed shot by shot, keeping the framing stable within each shot. Keep titles and subtitles away from edges occupied by platform controls and leave clear space for the person. Use B-roll when it explains the current sentence

## Complete Excerpt Workflow

1. **Find peaks in text**: scan for quotable lines, emotional highs, and dense value, then confirm with audio and visuals
2. **Select a complete passage**: choose in and out points that preserve the full argument, typically targeting 30–90 seconds. Extend stories and other types according to the table and content needs
3. **Lift the hook**: place the strongest original line at 0–3 seconds with a bold title, then return to the natural development
4. **Reframe**: choose a centered crop, soft background, or stacked layout so people remain clear and readable
5. **Tighten the rhythm**: remove hesitation, connective filler, and repeated attempts while preserving complete syllables, natural breaths, and emotional pauses
6. **Add subtitles**: synchronize them throughout, emphasize key phrases, and check platform-safe placement

Use FFmpeg to trim the selected ranges, reorder and concatenate highlights, reframe, and export each clip. Remap subtitle cues from source time to the resulting output time after cuts or reordering. Perform large numbers of splits in deterministic batches; after each batch, check outputs with ffprobe, update the keep/delete list and source-time ranges, then continue from that manifest

## Completion Criteria

Each clip centers on one self-contained point and preserves the speaker's position and meaning. The first 3 seconds contain a real hook or a bold line that creates suspense. The subject stays clear and stable, pacing is tight while speech remains intact, and subtitles are accurate and readable throughout. Deliver the requested excerpt files and the reproducible assembly manifest when requested; follow the entry point for rendering and verification
