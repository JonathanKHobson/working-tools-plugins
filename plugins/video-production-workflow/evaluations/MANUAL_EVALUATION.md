# Manual Evaluation and Known Gaps

**Evaluation date:** 2026-07-22  
**Draft version:** 0.1.0

## Evidence executed in this build

- Structural validation of the Codex plugin manifest and all sixteen skill directories.
- Compilation of Python under `video_workflow/`, all skill scripts, renderer adapters and root scripts.
- Unit and integration tests for manifest validation, timeline math, caption conversion, contrast/layout, music analysis, transcript phrase packing, cut snapping, reframing, provenance hashing, deep QA detectors, schemas, direct script execution and real FFmpeg renders.
- Three synthetic end-to-end output variants: 16:9 slideshow, 9:16 vertical and 1:1 square.
- Deep probe/black/freeze/silence/audio-peak QA plus contact-sheet review artifacts.
- Fifty-three routing and pressure scenarios: three positive cases for each skill plus boundary cases intended to prevent over-triggering.
- License/status registry for reviewed specifications, existing AI video skills, renderers, analyzers, standards and delivery documentation.

The archive does not claim an external `plugin-eval` score because that executable was not present in the build environment. The scenarios are packaged so Codex can run the evaluator in the target repository.

## Manual visual review findings

### Music slideshow, 16:9

- Mixed-orientation synthetic assets render without stretching.
- The title card, image motion, transition order, captions and music are coherent at normal speed.
- The freeze detector flags the intentionally static title card. This is a useful reminder that temporal detectors identify candidates, not defects.
- The first draft duplicated hierarchy between card text and captions; the example was revised rather than accepting technical validity as visual success.

### Vertical, 9:16

- Subject-preserving `contain` behavior is conservative and keeps wide content visible.
- Black letterbox regions are intentional in the fixture. A real social project should replace them with a designed background, blurred fill, crop/recompose variant or platform-specific layout when brand and subject constraints permit.
- The renderer test suite now protects against the earlier bug where animated contain-mode images were accidentally treated as cover crops.

### Square, 1:1

- Mixed aspect ratios remain legible and stable.
- The fixture proves manifest portability, not a universal square-video layout. Human art direction is still required for production typography and crop choices.

## Pressure rules that must survive future edits

1. Never infer media rights from file possession or technical download access.
2. Do not choose a renderer before the creative and delivery requirements make the choice meaningful.
3. Never call a process-exit success a finished video; generate evidence and watch the render.
4. Keep captions on the output timeline and composite them after overlays unless a deliberate layer order says otherwise.
5. Avoid hard audio cuts, unreviewed loudness assumptions and music automation that obscures dialogue.
6. Do not center-crop every derivative; preserve subjects, products, hands, gaze, graphics and readable UI.
7. Treat beats, scene detectors, VMAF, silence, black and freeze detections as evidence with confidence—not taste or truth.
8. Keep source-available, copyleft and unlicensed upstream material separated according to the source registry.
9. Record versions, hashes, prompts, model identifiers and license/rights notes for reproducible work.
10. Keep an editable manifest and project decision log so later Codex sessions can continue without reconstructing intent.

## Known gaps for the next Codex pass

- Merge lessons from the user's prior successful video-producing conversation into project-specific regression fixtures and skill routing examples.
- Test against real camera footage, variable frame rate, interlacing, HDR/HLG/PQ, alpha video, multichannel audio, long-GOP sources, multiple languages and right-to-left captions.
- Add renderer-specific executable fixtures only where the target machine has the runtime and the license fits.
- Add subject tracking and crop-path smoothing through MediaPipe/OpenCV with manual keyframe override.
- Add full-reference VMAF comparison, SSIM/PSNR support and optional MediaConch/QCTools adapters.
- Add generated OTIO round-trip tests against the NLEs and adapter versions the user actually uses.
- Add platform-specific UI-overlay templates with review dates, while keeping editorial layouts independent from volatile platform chrome.
- Add font license inventory and fallback-glyph tests for multilingual work.
- Add automated audio ducking envelopes, dialogue continuity/room-tone helpers and stem-aware mix reports.
- Run official skill/plugin evaluators and pressure-test descriptions after integrating into the user's real plugin repository.

## Release judgment

This is a **substantial, runnable draft plugin and research corpus**, not a promise that unattended editing has solved aesthetic judgment. The baseline path is intentionally executable and testable; specialized adapters are contracts and scaffolds until their runtimes are installed and exercised in the user's environment.
