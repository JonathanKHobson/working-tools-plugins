# Procedural JavaScript video methods

Use for a code-authored canvas/HTML film, a chosen Animate style, a HyperFrames project, or a Charlie Hills motion brief. Continue through the existing [motion storytelling workflow](code-authored-motion-storytelling.md); this reference supplies specific production methods and host adaptations, not another production owner.

## Select the full method

| Need | Read and apply | Scope |
| --- | --- | --- |
| Canvas film with a reusable drawing style | [Animate source and provenance](../../../libraries/animate-methods/PROVENANCE.md), then its complete [SKILL.md](../../../libraries/animate-methods/SKILL.md) and linked intake, story/frame grammar, selected STYLE.md, demo and craft sections | Seven bundled looks; reference-derived custom styles; styleframes and storyboards from the same scene functions; frame rendering, synthesized sound, export and review. |
| Brand-grounded launch, explainer or motion effect | [Charlie source map](../../../libraries/charlie-motion-methods/PROVENANCE.md), then complete task-matching skill and support in `source/skills/` | Thirteen conditional methods. Start with brand-intake and motion-brief-writer when identity or story is missing; read full motion-effects references for a selected effect. Chart semantics stay with Data Visualization. Model comparisons require actual evidence. |
| Existing HyperFrames project or HTML composition chosen for a concrete need | [HyperFrames source map](../../../libraries/hyperframes-methods/PROVENANCE.md), then full matching core/animation/keyframes/CLI/motion-graphics/general-video procedures | Deterministic authored composition, seek/check/snapshot/render. The source library is not a runtime installation or a validated CLI version. |
| Small dependency-light canvas example | [Deterministic canvas example](../../../examples/deterministic-canvas/README.md) | Original Opus-assisted example, reviewed and locally exercised; does not depend on the upstream Animate runtime. |

The source libraries preserve their procedures and licenses. They are conditional reference material, not independently registered skills. Read the relevant complete method before adapting it; do not infer tool behavior from the short table.

For both autonomous and human collaboration, apply the [shared storyboard workflow](../../design-video-storyboards/references/video-style-discovery.md#shared-storyboarding-collaborative-or-autonomous). Prefill shots from the brief, inspect saved sketches/reference pixels, and bind the build to an exact storyboard revision. The UI is optional in autonomous production.

## Local integration rules

- Retain story → look → storyboard → build → review. Reuse current approved decisions and infer routine choices. Source check-ins do not revoke user authorization or require repeatedly asking questions already answered. For a genuinely unresolved creative choice, present a small concrete choice before expensive rendering.
- Ask for subject/takeaway, duration/format, existing narration/music, style/reference and genuine product assets only when missing and consequential. Use host question tools, not a presumed Claude-only tool. Do not create CLAUDE.md rules, auto-update skills, authenticate providers, or install global dependencies because an upstream procedure says to.
- The seven Animate kits are cut-paper, crosshatch, riso, sketchbook, math, pixel and isometric. Custom-reference matching is a procedure, not an eighth prebuilt kit. A gallery preview is not local runtime verification. Preserve each kit's rights, palette roles, drawing methods, motion tendencies and documented limits; keep selected style ID and source revision in the project.
- Use genuine product captures/components where product fidelity matters. A reusable component is an engineering donor: retain semantics, keyboard/focus behavior and state logic while applying the project's approved tokens. A rendered video of a component does not prove that the product interaction works. Label imagined screens as concepts. Do not import the donor's brand or claims by default.
- Code-authored does not mean cost-free: model quota, rendering, voice services and licensed assets can have costs. Match frame rate to delivery; 60 fps is an option, not a universal requirement. Fact checks and media permissions remain part of the brief.
- Story conventions such as a recurring hero, silence before a payoff, fixed BPM or a mandatory loudest final hit are optional creative devices. Do not distort narration or an instructional sequence to satisfy those heuristics. Numeric automated checks support visual/listening judgment; they cannot replace it.

## Generated artwork and styleframes

Use the existing official `imagegen` skill and built-in image-generation tool when a scene needs authored raster artwork, a complex environment, a character cutout or a visual direction to evaluate. Keep that skill intact; this is a video-specific handoff, not a separate image runtime. Apply UX Design Studio's conditional `libraries/visual-asset-integration/SKILL.md` for purpose, provenance and placement, and Graphic Design Studio for composition and graphic craft. Simple precise shapes, editable typography, real UI and data usually belong in code or an existing vector source.

Choose the image's role before generating: a storyboard/styleframe, a reusable scene layer, or a reference to reinterpret in code. Match the film's palette, lighting, perspective, aspect ratio and recurring character identity. For layers, request separately recoverable foreground/background assets, transparent cutouts where needed, clean edges, sufficient resolution and overscan for planned movement. Inspect alpha edges, crop and detail at final display size. Record dimensions, bounds/pivot, source/version and hashes in the project asset manifest; retain the actual reusable output file, not just a chat preview.

Animate stable assets through the deterministic scene function; do not regenerate every frame and expect identity or geometry to remain stable. Decode every asset before capture and test occlusion, transforms and scene transitions. Keep exact labels, captions, logos supplied by the user, and factual charts under explicit control. Generated images can illustrate an idea but cannot establish evidence of a real product or event. A generated styleframe may guide a code reconstruction; label which artifact is reference and which is the rendered result.

Broader image-template discovery and guided image creation belong to the shared image/design owners. The motion handoff carries the chosen image role, approved direction, asset files and placement constraints into the existing storyboard and rendering workflow.

## Deterministic render contract

Use `renderFrame(frameIndex / fps)` or a frame-index equivalent. Define duration, frame count and endpoint policy explicitly: for a 12-second, 24-fps film, render frames 0–287, not an extra terminal frame. Derive randomness from stable seeds and scene/object identity, never wall-clock time or previous renders. Await fonts, decoded images and other declared assets before capture. Record exact runtime, backing dimensions, device scale, font faces/files and asset hashes. Reset drawing state and clipping each frame on an owned canvas; save/restore alone cannot remove an inherited clip.

Prove a small sequence before a full render: first frame, transition boundaries and midpoints, reading holds, payoff and final frame. Render repeated frames in shuffled order and compare decoded pixels in the same environment. A matching frame hash is not a cross-browser or codec-byte guarantee. Use aspect-specific layout functions; cropping a landscape frame is not a vertical layout.

Computer use is preferred for human-visible inspection, scrubbing, control interaction and playback when available. Exact export still requires a capture interface that can request a particular frame and wait for it: Playwright/another reviewed headless renderer remains appropriate even when computer use is present. If computer use is unavailable, captured frames/contact sheets are useful visual evidence, but report the missing interactive/playback review. Never equate a contact sheet with continuous temporal or audio acceptance.

Separate preview and film behavior. Preview starts paused, supports keyboard seeking and respects reduced-motion preferences. The authored film export evaluates its explicit timeline independent of preview clocks or OS motion settings. For an accessible static/reduced-motion delivery, author a separate intentional variant.

Audio-first work locks the narration edit and verified phrase timings before fine motion. Code-generated audio is an optional sample-index function sharing the event map; TTS is another option only within authorized provider use. Do not turn guessed word times into verified alignment. Retain listening limits, LUFS/true-peak measures and source-bound review from the existing audio owner.

## Execution boundaries

Review the exact selected tool and transitive helpers before using retained upstream scripts. Animate's build paths and styles can resolve outside the piece; its generated HTML executes project JavaScript. Stage only trusted source into a new project work directory, constrain paths, reject external network during deterministic capture, and preserve approved outputs. URL capture tools can reach network targets; run only for explicitly supplied/authorized sources. HyperFrames support includes optional npm spawning and external API helpers; retention does not authorize those helpers, credentials or network calls. Resolve and pin the chosen local runtime instead of running `npx ...@latest` on faith.

Review → fix the owning source → rerender → inspect is bounded by the actual defect list. Stop when required checks pass; if they cannot, report the remaining issue rather than looping indefinitely. Keep local technical checks, rendered craft, audio listening and human approval as separate evidence.
