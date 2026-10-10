# Code-authored motion storytelling

Use for a complete motion-designed film, animated explanation, channel introduction or a sequence built around authentic recorded narration. `create-motion-graphics` is the canonical production owner. This is a specific workflow within that skill, not a required aesthetic or new renderer. Existing slot production still fits isolated overlays.

## Start with the communication job

Inspect the approved source, existing media and intended viewing context. State what should become understandable through motion and the final audience takeaway. Choose code when reproducible timing, shape relationships or type benefit from it; native animation/editing tools may better fit another brief. Code does not guarantee design quality.

Make a compact animation brief and event map in the owning project. Each beat records: source claim or narration interval; visible state before and after; persistent object; transition trigger; visible start / full-visibility start / stable readable hold / exit start and end; optional audio cue onset and its intended event; caption interval; safe-area constraint. Measure readable hold from full opacity and settled position to exit, excluding competing reading/motion; a caption interval is not proof of that hold. One understandable relationship per beat is a useful starting point, not a fixed scene count. Mark missing assets explicitly. Preserve current approvals and original recordings.

## Build a motion grammar

Pick a small vocabulary of objects, changes and timing roles. Track visual identity by shape, position, color role or movement. A persistent object should change because the story changes: e.g. a step becomes the document it produces. Avoid unrelated decoration masquerading as explanation.

Choose the transition deliberately:
- **Corresponding geometry:** normalize compatible paths to the same point count and ordering, then interpolate positions with eased time. Inspect intermediate frames for twists, wrong correspondence, intersections and speed jumps. Equal point counts alone do not make a good morph.
- **Changing topology:** retract, transform the shared object, then redraw branches or connections. Do not force an ambiguous fork into a loop just to avoid a cut.
- **Attention:** move or reveal only the element needed next, then hold it. Keep reading time separate from entrance/exit time. Moving dots and highlights are optional semantic pointers, not compulsory branding.

Use a single time origin and frame-index evaluation (`t = frame / fps`) for predictable seeking and rerenders. Keep semantic events named in data where practical; derive visual and sound timings from them to avoid drifting duplicate schedules. Test real-time playback as well as keyframes. Smooth position does not establish readable pacing.

## Typography and composition through time

Partner with `graphic-design-studio:motion-design` for styleframes, hierarchy, kinetic type, continuity and cover design. Measure rendered glyph bounds with the actual fonts and weights, including motion excursions and tracking. Fit copy by editing, wrapping and hierarchy before shrinking it below readable size. Check phone-scale output and dense intermediate states, not just design-space rectangles. Platform overlays and crops require actual target evidence; an authored safe box is an assumption until checked.

Separate display, body, label and caption roles when useful. Choose palette and type for the brief. A successful example's Apple system fonts, color scheme and layout are not portable defaults. Verify font availability, variable axes and usage rights; map replacements by role, then remeasure/review every affected composition. Never silently substitute a default font.

## Sound follows events

Plan cue onsets against the event map: start, arrival, confirmation or resolution are different targets. A gradual color change has an interval, not a single magical sync frame. Musical chord changes can support scene mood; sparse accents can mark comprehension events. Shared source timestamps prove scheduling, not perceived synchronization.

Use licensed/owned audio or original authored sound. Keep stems and provenance. Synthesis can be a suitable option; it is not required. Apply short attacks/releases and intentional fades to avoid clicks; reserve headroom and check the encoded mix. Measure sample peak, true peak and loudness with clearly named units where supported. RMS dBFS is not LUFS, and low peak does not prove pleasantness or intelligibility. Listen to the final mix and inspect the visual event at normal speed. If listening is unavailable, disclose it and leave that criterion unverified.

### Authentic narration branch — validate separately

Begin with the user's actual recording, exact source hash and authorized intended use. Reuse existing authorization; resolve only a missing use permission. Select and verify meaningful phrase intervals, preserve the person's voice and intended wording, and keep an edit map from source to output. Do not replace it with TTS or voice cloning unless separately requested. Timing follows the speech: emphasize the referent as it is named, reveal the consequence when explained, and leave room for breaths and understanding. Do not stretch speech to fit an inherited 32-second design.

Lock the narration edit before fine animation and score timing. Reduce competing on-screen prose; captions transcribe the speech while graphics explain it. Align verified word/phrase timings to the final edit, correct names and technical terms, and check every join and caption boundary. Duck music/effects under speech with controlled attack/release, then listen on realistic speakers at ordinary volume for masked consonants, pumping, abrupt joins and distraction. Recheck encoded peaks/loudness and caption readability with native overlays. A silent motion-film approval is not narration-intelligibility evidence. This branch needs its own rendered and listening acceptance before it can be called proven.

## Author, preview, export

Keep the smallest maintainable project structure: brief/event map, editable source, owned assets/stems, preview/final, sidecars and QA receipt. A bounded one-off renderer may be one file; ongoing projects should separate scene data, drawing, audio and export when they change independently. Record dependency/runtime versions and resolved font/encoder paths. Do not install a new provider by default.

For a simple vector/type film, Pillow/NumPy frames piped to FFmpeg can be sufficient. Supersampling can improve edge quality; confirm the actual downsampling filter and cost. Browser, Motion Canvas, Manim, Blender or native tools remain valid choices by need. Preserve the core editorial renderer boundary for embedded slots.

Render a lower-cost preview at the final aspect ratio; inspect first / transition midpoint / payoff / final frames and continuous playback. Revise the highest owning source (brief, event timing, geometry, typography or audio), not the encoded MP4. Export the requested dimensions, cadence, codec, pixel format, color metadata and audio layout; probe and fully decode the output. Derive a separately composed cover from a clear semantic state rather than an arbitrary blurred frame; validate the target crop.

## Acceptance and reproducibility

Use `validate-video-quality` for the rendered delivery. Bind review to exact output/source hashes. Check duration/frame count, stream format, full decode, text bounds across time, transition artifacts, reading holds, flash risks, signal/mix, captions and delivery crop. Simple luma/frame-difference heuristics can flag gross discontinuities; they cannot certify photosensitive safety. A technically valid export still needs visual judgment.

Record 3–8 named anchors with frame/time, region/object, observed fact and Keep / Change / Defer action. Reinspect changed anchors and the complete sequence. If claiming reproducibility, say whether source functions, decoded frames, or final encoded bytes were compared; codec/font/library changes may change the binary. Run rebuilds into a new output directory. Never execute an example's `sidecars`, `final` or verification command in place when it overwrites approved artifacts.

Deliver the final/cover, editable sources, transcript/captions when relevant, audio provenance, build instructions, versions, hashes and bounded QA limits. `social-content-studio:social-publishing` owns platform copy, queue policy, native scheduling/publication and receipts. A changed output hash invalidates approval binding until the relevant review is refreshed. UX Design Toolkit's `motion-and-performance` owns interactive transitions, focus, cancellation, interruption and reduced-motion behavior; a film is not proof of a usable interaction.

## Worked evidence and research intake


Add future supplied research here only after source review: source/date and rights, claimed mechanism, relevant time-based example, what changes in the method, and a bounded test with observed result. Keep raw research in its owning project. Distinguish author claims, lead inference and tested results; avoid a second gallery/catalog. Graphic keeps composition-specific findings and UX keeps interaction-specific findings in their existing motion owners.

For original work, carry the [default art-directed motion contract](art-directed-motion.md) through the brief, event map and representative preview. This supplies the concrete typography/photography/composition/depth treatment before extending the sequence.
