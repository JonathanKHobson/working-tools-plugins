# Art-directed motion: typography, photography and spatial storytelling

Apply by default when producing an original motion piece or materially redesigning its visual language. Reuse an approved direction for continuation. A routine trim, caption correction, faithful deck animation or export does not require a new direction or proof passage. Static type, flat design and restrained movement can be deliberate successful choices.

## Define an identity before implementation

Write a brief visual thesis: what the viewer should feel/understand, and the visual mechanism that makes that happen. “Premium”, “cinematic”, “like Opus” or a renderer name is not an actionable style. Use supplied assets and the incumbent brand; infer reversible choices when direction is delegated. Do not insert a new approval hold.

Make the following choices concrete in the existing brief/storyboard rather than a new set of mandatory documents:

- **Typography:** display/reading/caption roles; character of type, weight/width/spacing, scale relationships and alignment; how significant words reveal, occupy space, connect or transform. Use licensed available fonts and measure actual glyphs. A typeface change alone is not a different typographic direction.
- **Photography/imagery:** why each picture belongs; subject scale, framing, light/color, texture, crop and how type relates to it. Real photographs may be the visual subject, an environment or a texture; do not reduce every photo to a background under the same label. Preserve originals, authenticity and rights.
- **Composition:** focal point, negative space, hierarchy and how those relationships evolve from opening through transformation, readable payoff and ending. Specify a persistent element or motivated cut when it connects beats.
- **Space:** choose flat 2D, layered 2.5D or actual 3D from the communication job. Record foreground/background relationships, overlap, perspective and camera intent when relevant. A flat piece need not acquire shadows or camera moves to pass.
- **Motion:** describe character and semantic roles—tactile, fluid, mechanical, restrained or another bounded choice—with trigger, trajectory, acceleration/settle, hold and interruption/transition. Derive movement from the subject rather than reuse one fade/slide/spring everywhere.

Keep one coherent grammar within a piece. For requested alternative styles, differentiate multiple relevant dimensions (type behavior, composition, image treatment, spatial organization, motion logic); changing only accent color or font is usually insufficient. Brand invariants can span a series, and deliberate reuse is allowed. Do not maximize novelty at the expense of recognition.

## Reference evidence and uncertainty

Inspect an accessible reference passage and record 3–8 anchors: source/time or frame, region/object, observed relationship, intended Keep / Change / Defer. Compare mechanisms as well as surface styling. A transcript supports described ideas, not exact fonts, lighting, trajectories, easing or camera timing. Stills show composition; playback is needed for temporal claims. If the reference is absent, label the proposed treatment as an original hypothesis and test it; do not claim reference fidelity. Reuse ideas without copying protected assets or assuming source rights.

## Design what changes, not just what is labeled

For each key beat specify opening state → meaningful transformation → fully visible/readable payoff → ending, together with the focal point and type/image relationship. Text can act as geometry, a masked reveal, an object-attached element, a scale change or a semantic transition. Use these only when they serve the words. Stable readable text and ordinary lower thirds remain valid for speech captions, names, data labels and restrained briefs. Accessible captions are a separate complete reading channel; kinetic display text is not a replacement transcript.

A useful conceptual test: remove the decorative overlay. Does the remaining motion still communicate the intended relationship? If not, strengthen the visual idea before adding more effects. An animation is not distinctive merely because all objects are moving.

With photographs, choose motion that fits the actual image: meaningful reframing, a match of shape/light/subject between shots, an authored mask reveal, or restrained depth separation. A push-in on every still is not automatically expressive photography. Do not animate facial anatomy or invent unseen photo detail to create depth. Matte/cutout edges, occlusion and newly exposed areas require playback review; parallax is not proof of a true 3D reconstruction or real camera event. Route filmed tracking/mattes to [tracked layer compositing](tracked-layer-compositing.md).

Use actual 3D when geometry, rotation, changing viewpoint, dimensional explanation or material/light behavior contributes. Define geometry, material, light, camera and framing together. Layered depth may achieve the brief with less cost; heavy particles or 3D are not a quality guarantee. Choose the available licensed renderer after the treatment. This procedure installs no Three.js, Blender or other runtime and makes no model-superiority claim.

## Prove the direction at low cost

Before extending an unresolved original direction into the whole piece, render a representative passage at the final aspect ratio and realistic display size. About 6–10 seconds is often sufficient; use the shortest passage that tests the key mechanism, readable hold and transition. An already approved treatment or a tiny bounded asset may need only its relevant interval. Preserve source and render revisions. When production is delegated, proceed to review/fix without an obligatory human checkpoint; honor an explicit review hold.

Inspect opening, transformation midpoint, readable payoff and ending, then playback. Ask:

1. Can the visual identity be described concretely from the actual output?
2. Does type express hierarchy and meaning, and remain readable after motion settles?
3. Are photos/illustrations integrated deliberately; are crop, subject integrity and matte edges sound?
4. Does composition evolve coherently, with depth/camera revealing something when used?
5. Do timing, holds and transitions fit the idea rather than a reused template?
6. Is the selected direction meaningfully distinguished from an unwanted generic baseline or alternatives, while preserving approved anchors?

Record evidence and the highest-value defect. Fix its owning brief/type/geometry/image/timing source, rerender the bounded passage and compare the changed anchors. Expand only when the proposed treatment is usable or its remaining limits are explicit. A contact sheet, smooth frame rate, “3D” tag or technical QA pass cannot certify taste. Sound may reinforce the chosen semantic events; more whooshes do not repair weak visual direction.

## Compare alternatives fairly when selection is the task

Use the same approved content, narration/source edit, factual assets and target aspect ratio for candidate treatments. Keep duration and reading opportunity comparable; do not make a busy candidate seem better by removing its caveat or captions. If the source is synthetic, label it clearly and never fabricate real citations. Use a compact animatic when sequence/pacing is unresolved, styleframes for appearance and playable exports for temporal comparison. Do not require three options or a fixed 12-second test on every project; use the scope the decision needs.

Compare concrete differences in typography, composition, image construction, surfaces/light and movement. Grayscale can diagnose palette-only variation, but color can legitimately carry identity. Inspect important settled frames; intermediate smears/blurs are not required to be finished posters. A muted pass can expose how attention works, without requiring all storytelling to be independent of narration or sound. Preserve quiet-testing requests and record listening limits.

Notebook inquiry, editorial poster and miniature demonstration studio are possible hypotheses, not a permanent aesthetic. Their useful distinction is how the same relationship develops: investigation across a page, a graphic argument, or inspectable spatial objects. A fixed comparison passage tests craft; a second subject tests whether the selected grammar transfers without repeating the same scene template. Choose strengths from actual renders, with the existing user's decision state visible.

## Reuse a selected direction through project evidence

After actual selection, keep a concise style record in the existing owning project's brief/design files. Link accepted frames and a playable excerpt, their source/output hashes and reasons they work. Record use/unsuitable use, real font families and roles, composition/image treatment, materials/light when relevant, motion verbs/camera/holds, sound character, renderer/build entry point and provenance. Add an actual rejected tendency with the reason/correction when such evidence exists; never invent prior approval or a rejected render.

Label the direction provisional or selected and state what remains unresolved. Read this record at the next original production start and pass it to bounded workers. Preserve its recognizably useful grammar while redesigning actions for the new subject. Recheck changed fonts, assets, aspect ratios or runtime before assuming transfer. Do not promote one selected project's style into plugin-wide aesthetics or create a new gallery/database to retain it.

## Conditional Remotion spatial implementation

Only when the chosen scene uses Remotion with actual 3D, verify the installed versions and read the official [Three integration](https://www.remotion.dev/docs/three) and [ThreeCanvas](https://www.remotion.dev/docs/three-canvas) contracts. They document React Three Fiber integration, animation derived from Remotion's `useCurrentFrame()` rather than an independent `useFrame()` loop, canvas dimensions and GL/export configuration. Derive camera/object state from the requested frame and test direct seeking plus the actual exported passage. Async textures need their documented capture handling. Frame-state reconstruction does not guarantee identical pixels across hardware or make the direction expressive. A working browser preview is not export acceptance. These are conditional execution requirements, not a claim the integration is installed here or an instruction to add dependencies without a scene need. Reviewed October 7, 2026; recheck version-sensitive behavior at use time.

## Ownership and evidence

`plan-video-production` owns the brief; `design-video-storyboards` owns timed visual relationships; `create-video-typography` owns text; `create-motion-graphics` owns production; `validate-video-quality` owns delivered playback review. Video carries this minimum contract even when companion plugins are unavailable. Graphic Design's `motion-design` supplies deeper visual direction when present; UX owns actual interactive state, focus and reduced motion. Do not substitute a website's simulated controls for working behavior.

This original method responds to creator feedback and supplied tutorial transcripts. The transcripts describe reference-first animation, composed photography, Figma-informed designs, Three.js environments and iterative render/sound work. Their speed, model-quality and capability claims were not independently verified and are not workflow requirements. No tutorial code, artwork, fonts or assets were imported. The method's behavior is reviewed through the plugin scenarios; future output quality requires actual project renders and user/reference comparison.

For illustrated or tactile work, choose procedural geometry, authored/licensed assets, generated artwork or a hybrid from the visual premise. Prove the hardest subject interaction and its payoff in the representative passage, not camera motion alone. [Generated assets for motion](generated-assets-for-motion.md) owns measured joints, masks and registration; [production learning transfer](../../evolve-video-workflow/references/production-learning-transfer.md#capture-the-executable-template) owns the portable recipe. Routine approved edits retain their existing scope.
