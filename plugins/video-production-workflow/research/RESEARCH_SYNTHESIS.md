# Programmatic Video Production for Codex — Research Synthesis

## Executive finding

The strongest architecture is not a single giant “edit video” prompt and not a renderer-specific plugin. It is a **declarative editorial system**: a project manifest stores assets, timeline intent, text, audio, style, delivery targets, and provenance; analyzers produce evidence; editorial agents revise the manifest; one of several render adapters executes it; automated and human QA approve the result.

FFmpeg and ffprobe are the lowest-common-denominator production spine. Python is well suited to orchestration, analysis, file generation, and deterministic helpers. OpenTimelineIO or CMX3600 provides interchange. Remotion, HyperFrames, Motion Canvas, Manim, Blender, MoviePy, PyAV, and MLT are specialized options rather than mandatory foundations.

## What existing AI video skills do well

### Conversation-led editing

`browser-use/video-use` demonstrates a strong editorial loop: inspect material, converse about intent, confirm the strategy, execute, preview, self-evaluate, iterate, and persist. Its most transferable technical lessons are output-timeline subtitle offsets, precise cut boundaries, fades at audio cuts, PTS-aware overlays, source transcript caching, and staged compositing.

### Video understanding

`bradautomates/claude-video` treats a video as transcript plus a bounded set of scene-aware frames. Its useful contribution is not merely “extract frames”; it explicitly varies fidelity by duration and question, deduplicates near-identical images, and zooms into named moments.

### Longform-to-shortform

`AgriciDaniel/claude-shorts` connects transcript scoring, interactive selection, word/sentence/silence boundary snapping, content-aware reframing, animated captions, platform export, and validation. Its limitation is specialization around shorts and Remotion.

### Renderer-specific production systems

`DojoCodingLabs/remotion-superpowers` shows the value of splitting production knowledge into rules for audio, captions, stock, effects, 3D, data visualization, and CI. Official/internal Remotion skills show focused project scaffolding and video layout rules. These are useful patterns, but a renderer-specific system cannot be the universal editorial model.

## Gaps this plugin is designed to fill

1. **Shared editorial intermediate representation.** Existing tools often jump directly from prompt to FFmpeg command or React composition. A stable manifest gives Codex an inspectable contract and makes revisions cheap.
2. **Music structure beyond “show a waveform.”** Beat timestamps, downbeats, onset strength, energy envelopes, silence, section boundaries, phrase length, and editorial density must be translated into cut windows—not treated as automatic taste.
3. **Design system for video.** Typography, hierarchy, safe zones, contrast, line length, negative space, rhythm, subject preservation, and motion semantics need first-class rules.
4. **Renderer selection.** The right engine depends on the shot: FFmpeg for assembly, PIL for cards, HyperFrames for browser-native motion, Motion Canvas for explanatory animation, Manim for mathematical diagrams, Blender for 3D/VFX, and Remotion when its ecosystem and license fit.
5. **Interchange and escape hatches.** OTIO/EDL export allows finishing in a nonlinear editor instead of trapping the user in generated code.
6. **Evidence-based QA.** A render should produce probe data, frame/contact-sheet review, cut-boundary views, audio measurements, caption checks, black/freeze/silence detection, and a pass/fail report.
7. **Provenance and licensing.** Every external asset, font, model, stock clip, tool, and source has rights/status metadata.
8. **Caching and resumability.** File hashes prevent re-transcription, re-analysis, or re-rendering unchanged stages.
9. **Accessible delivery.** Captions, contrast, readable typography, meaningful audio description/alternatives when needed, and reduced-motion variants should be planned rather than patched in at the end.

## Recommended workflow

1. **Intake and rights:** define purpose, audience, runtime, aspect ratios, distribution, brand, accessibility, and permission status.
2. **Inventory:** hash, probe, normalize, proxy, and index assets; preserve untouched originals.
3. **Analyze:** transcript/diarization, shot boundaries, faces/subjects, blur/exposure, music beats/energy/sections, and reference style.
4. **Editorial brief:** narrative arc, must-keep/avoid moments, pacing model, design tokens, and acceptance criteria.
5. **Storyboard and timeline:** compose a beat sheet and declarative manifest with explicit reasoning for non-obvious decisions.
6. **Specialist asset production:** captions, title cards, diagrams, motion overlays, reframed clips, and audio stems.
7. **Draft render:** low-cost proxy at target aspect ratio, not merely a desktop preview.
8. **Automated QA:** structural, codec, color, loudness, caption, freeze/black/silence, and timeline assertions.
9. **Human/agent visual review:** watch at normal speed and inspect cut boundaries, first/last frames, high-information text, and representative platform crops.
10. **Final conform:** high-quality encode, metadata, captions/sidecars, variants, checksums, manifest, and provenance bundle.

## Music-aware editing model

Waveforms reveal amplitude, not musical meaning. Use a layered model:

- **Signal layer:** duration, sample rate, channels, clipping, silence, RMS/peak, loudness.
- **Pulse layer:** tempo estimate, beat timestamps, downbeat confidence, onset strength.
- **Phrase layer:** repeated beat groups, bars, cadence, fills, drops, breakdowns, and section changes.
- **Energy layer:** smoothed loudness/brightness/density curves.
- **Editorial layer:** map major visual changes to high-confidence phrase or section boundaries; use ordinary beats for local motion accents; leave breathing room in low-energy passages; avoid cutting every beat unless the format explicitly calls for it.

A good automatic planner exposes confidence and alternatives. It must support “strict beat sync,” “phrase-led,” “narrative-led,” and “ambient” modes rather than one universal cut rule.

## Visual design model

Video design is temporal graphic design. Every frame must work as a still, but hierarchy also changes over time.

- Establish one primary focal point per moment.
- Use a modular safe-area system, then recheck against the actual platform UI at delivery time.
- Measure text rather than guessing: cap line length, avoid edge collisions, and give reading time based on language and complexity.
- Separate information motion from decorative motion. A reveal should have a semantic reason.
- Use easing, anticipation, follow-through, and holds. Linear motion is appropriate only when it communicates constant physical or data rate.
- Preserve faces, hands, products, and gaze direction during reframing.
- Treat contrast as local and dynamic: text can pass against one frame and fail against the next, so use scrims, boxes, outlines, shadows, or tracked backgrounds.
- Create reduced-motion and caption-safe variants when the audience or channel needs them.

## Audio model

Dialogue intelligibility takes priority over music. Use stems when possible. Measure loudness and true peak with BS.1770-compatible tools; choose a target from the delivery context rather than claiming one number is universal. Apply fades/crossfades at edits, room tone or ambience under dialogue cuts, sidechain ducking or automation under speech, and a two-pass final loudness process when accuracy matters.

## Quality and governance

Automated checks cannot certify taste. They can catch missing streams, wrong dimensions, bad duration, clipping, illegal pixel format, black/frozen sections, caption overlap, unsafe text, and obvious sync errors. The plugin therefore requires both machine evidence and a human/agent watch-through before marking a final master approved.

Platform presets are data with a review date, never timeless truths. External downloads require rights. Fonts are not redistributable merely because fontTools can inspect them. Copyleft and source-available tools may be invoked while remaining separate from the MIT plugin.
