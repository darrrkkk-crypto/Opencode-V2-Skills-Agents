# Narration-led Video

Use this for explainers, in-depth news, documentary shorts, video essays, and knowledge content. Sound is the skeleton and visuals are the skin: narration determines information order, actual timing, and emotional tone, while visuals follow the real timestamps of that audio track. For changes to an existing segment, retain its established copy and sound

## Obtain the Actual Audio First

Inventory existing recordings and visuals before writing. Write copy that uses their strengths, then decide what must be made. Reuse existing narration directly; use [speech generation](../SKILL.md#generate-missing-assets) when new audio is genuinely needed

1. **Prepare narration by sentence**: when sentence gaps need precise control, generate separate files sentence by sentence and record their order in the assembly manifest. Generating a whole passage at once retains that take's built-in sentence rhythm
2. **Measure before picture lock**: probe each audio file and calculate its actual start and end in the planned assembly
3. **Obtain fine timing**: when alignment or cuts need word-level precision, read the media's existing word timestamps. Use [transcription](../capabilities/transcription.md) only if they are missing
4. **Build a beat map**: use measured audio timing to decide which visual information appears at each moment, so visuals fit the audio's actual length

A gap of about 0.2 seconds between sentences is a useful starting point for natural breathing; preserve emotional pauses according to the content

## Beat-map Example

Record each passage's actual speech window, measured line, visual intent, asset source, and specific treatment. The timings below illustrate an editing beat map. Measure this run's audio first, then substitute its real intervals. Use shot numbers and verbal pacing for video-model shots

| Window | Line (measured) | Visual intent | Source | Treatment |
| --- | --- | --- | --- | --- |
| 0.0–4.2s | “Global computing demand has grown tenfold in five years.” | Macro scale; one number bursts into view | Stock B-roll, web assets, or generation | Wide data-center view; a 10x number emerges from the center |
| 4.2–8.8s | “But physics is pushing Moore's Law to its limit.” | Micro scale; a warning mood | Chip close-up or 3D render | Slow push-in as the light gradually dims |
| 8.8–14.5s | “Until this Stanford team introduced a photonic architecture.” | The team and a new result | Paper screenshot plus location footage | Screenshot settles from soft focus, with a box around the key sentence |

## Asset Sources and Presentation Variety

Real footage, screen recordings, the existing local library, and reliable public B-roll often provide more credibility. Build the visuals from these materials first, using generation to fill actual gaps

Switch between an on-camera presenter, screen recordings, atmospheric B-roll, charts, and a card with one large line of text. One sentence can span several visuals, and several sentences can share one visual section. Organize shots around information changes to keep the rhythm varied

Reveal numbers when they are spoken and introduce people or objects when they are mentioned. Align subtitles and titles with their corresponding words so viewers hear and see information together. Static images typically hold for 3–5 seconds; when a longer hold is needed, use a slow push, local highlight, or change of detail to sustain reading

## Audio Hierarchy

Keep narration in the lead: clean, clearly articulated, and at a stable level. Use calm, narrative instrumental music below the voice, with a smooth 1.5–2 second finish

Use sound effects sparingly when a major idea lands, a number moves, or a section turns, such as a light whoosh or chime. Give the point weight without taking over the narration

## Videos Longer Than Two Minutes

Lock the whole video's central idea first. Prepare all narration and measure its actual timing, divide the beat map into sections, then complete the visuals section by section. Update the assembly manifest after every batch so later sections remain grounded in confirmed audio starts and ends

## Completion Criteria

When sentence gaps require control, narration has been prepared by sentence and pauses sound natural. The beat map uses measured timing, and every narration passage has accurate visual coverage. Titles and subtitles align with information arrival; music stays below the voice and resolves smoothly. Use the file-based assembly and verification guidance in the Skill entrypoint. If the user only wants the sound itself, deliver the audio directly
