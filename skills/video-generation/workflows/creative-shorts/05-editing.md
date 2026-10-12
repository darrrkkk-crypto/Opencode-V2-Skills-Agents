# Assembly and review

Use this stage to join approved generation units into a finished short and evaluate rhythm, continuity, picture, and sound. If the user requested independent clips only, verify and deliver them without inventing an assembly.

## Check each source clip

Keep the original generated files. For every unit, record its path, actual duration, dimensions, frame rate, audio streams, planned head/tail trims, and continuity state. Use ffprobe for stream inspection and FFmpeg for frame extraction. Mark properties that cannot be checked as unverified.

Reject or regenerate a clip only for a material miss: unusable corruption, wrong identity or required object, missing key action or line, broken continuity, or a visible artifact that harms the requested result. Do not spend repeated generation calls chasing negligible differences.

## Build a file-based edit manifest

Create a structured manifest or deterministic assembly command that records:

- ordered source paths;
- in/out trims and speed changes;
- output canvas, frame rate, and audio layout;
- transitions, titles, captions, narration, music, and mix decisions;
- the intended final output path.

Use the exits and entries from shot design to choose direct cuts, action overlaps, object matches, sound-first joins, or restrained transitions. Preserve synchronized dialogue and production sound. Keep non-diegetic music, titles, and captions in assembly rather than generation prompts.

Assemble with FFmpeg, normalizing codecs, dimensions, frame rate, time bases, and audio layout as needed for concatenation. Use stream copying only when compatibility and cut accuracy permit it; re-encode for exact trims or filters. When exact timing matters, measure the rendered result rather than trusting planned durations.

## Review the assembled result

Inspect the output with ffprobe and confirm it is playable. Use FFmpeg to extract representative frames covering openings, endings, joins, action peaks, titles, and Motion Graphics holds, optionally arranging them in a timestamped contact sheet. Sample densely around fast action or transitions.

Check:

- plot and information remain understandable;
- character, location, lighting, wardrobe, and object state stay continuous where required;
- dialogue remains intelligible and synchronized;
- music does not mask speech;
- captions and titles are readable and inside safe areas;
- no accidental black frames, frozen tails, clipped transitions, or missing audio streams appear.

If visual or audio inspection is unavailable, report that limitation and retain the timestamps that still need review.

## Deliver

Deliver the final video file, plus separate subtitle, audio, source-clip, or assembly-manifest files when the user requested them. Clearly identify whether the result is a finished assembled video or a set of generation units. This Skill does not produce an editable project timeline.
