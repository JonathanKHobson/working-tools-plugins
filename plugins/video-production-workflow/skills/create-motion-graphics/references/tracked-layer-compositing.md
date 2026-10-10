# Tracked elements, layer order and selective effects

Use for text behind an element, attached labels, tracked graphics, depth relationships or selective foreground/background treatment. An element can be a person, product, diagram node, UI panel, cursor, vehicle, landscape feature or authored graphic. Choose it from the communication task; do not search for a face in every video. A clip with no meaningful foreground may need ordinary 2D layering rather than segmentation.

## Plan one bounded effect

In the existing animation-slot brief, record the source/hash, source and output time ranges, target identity, intended anchor, space (source pixels, output frame or authored scene), offset, transform needs, layer order, matte/alpha source, protected content, and loss/exit behavior. These are authoring decisions, not newly executable manifest keys. Choose position-only following, rotation/scale following, planar placement or authored scene transforms according to the actual surface. A bounding box is not a contour matte, and tracking motion does not by itself separate foreground from background.

For generated diagrams or UI graphics, reuse known layer geometry and animation paths. For a screen recording, account for scrolling, panel motion, crop and cursor movement separately. For filmed objects, use a verified track or manually reviewed keyframes; a deforming foreground also needs a changing matte. Correct source/output time and coordinate transforms after any trim, speed change, crop, resize or reframing. Never reuse a track unchanged after its reference footage or timing has changed.

## Put a graphic behind the right element

Build the composite from back to front: base/background picture, inserted graphic, isolated foreground from the same source frame, then essential captions/UI annotations that must remain readable. For several elements, make their intended depth order explicit; a title may sit behind one and in front of another. Do not simply send the title behind a full opaque source clip: it disappears rather than becoming correctly occluded.

Use native layer alpha for authored assets, or an authored/keyed/segmented matte for footage. Confirm matte polarity, coordinate alignment, timing and straight versus premultiplied alpha. Review fine edges, holes, thin details, motion blur and any edge color spill against the actual composite. Feathering should suit the edge and resolution; indiscriminate softness makes a halo. A partially occluded decorative title is acceptable only if intended meaning remains accessible and the overlap serves the composition.

## Attach a label without losing identity

Track the chosen feature and place the label at a deliberate offset, with a leader line if useful. Keep it clear of captions, platform controls and the annotated feature. Apply only the needed transform components: a label may follow position while staying upright and readable. Inspect drift, jitter, perspective changes and target swaps. Smoothing must not create visible lag.

At an occlusion, cut, exit or ambiguous match, hide/fade the label, hold only a defensible position briefly, or use a manually reviewed continuation. Reacquire the same target before resuming; do not silently attach to a nearby similar object. Start a new track at a shot change unless continuity is actually verified. Keep any uncertainty in the review notes instead of claiming an automatic lock.

## Keep one region sharp

For selective blur, create a background branch and a sharp foreground branch with the reviewed matte, then combine them in the intended order. Use suitable edge extension/clean-background treatment when needed to avoid foreground colors bleeding into the blurred background. Check matte chatter, blur spill, hair/thin details, semi-transparency and changing focus through movement and occlusion. Keep demonstrated controls and information-bearing detail sharp when they are the focus; blurring a useful screen recording can defeat the lesson. A decorative blur is not verified privacy redaction.

## Execution boundary

The current core `video_workflow.render` normalizes sequential segments, assembles transitions, mixes mapped audio and burns captions. It does not execute arbitrary layer stacks, tracks, segmentation, selective blur, video transform keyframes or grading/LUT instructions. Its small zoom/pan path is image-only; video/animation uses fixed cover/contain. Extra manifest data may pass validation yet be ignored, so schema acceptance is not proof of effect support.

Choose a currently available, licensed editor/compositor or authored filter graph and verify it with a short representative pilot. The motion-graphics wrapper recommends a renderer; it does not create a track or matte. FFmpeg can combine supplied layers/mattes and apply filters, but filter availability is not an automatic tracker or segmentation engine. An adapter pointing at Blender does not prove Blender is installed or that a scene is authored. Do not install a renderer or download a model as an incidental effect step.

The core segment route flattens to an opaque picture and strips segment audio. For integration, precompose the **complete picture slot** externally, normalize dimensions/fps/color/timebase, and add it as an existing supported segment. Carry desired audio separately in the audio map. A transparent asset is appropriate only when the selected downstream compositor truly preserves and combines alpha; verify it rather than promising an overlay in the core assembly route.

## Temporal acceptance

Inspect first/payoff/final frames plus the hardest crossing, occlusion, maximum movement and re-entry. Scrub a frame sequence around trouble spots and watch the complete effect at normal speed; a contact sheet alone cannot prove tracking stability. Review each delivery crop. Record source/track/matte/render hashes and untested spans. Existing automated QA cannot certify matte quality, target identity, color accuracy or real caption readability.

Primary technical references (consulted 2026-10-02): [Adobe motion tracking](https://helpx.adobe.com/after-effects/desktop/animate-in-after-effects/track-motion/tracking-stabilizing-motion-cs5.html) distinguishes tracked features, attach offsets and transforms; [Adobe mattes](https://helpx.adobe.com/after-effects/desktop/roto-brush-and-refine-matte/roto-brush/roto-brush-refine-matte.html) explains foreground isolation and edge refinement; [FFmpeg filters](https://ffmpeg.org/ffmpeg-filters.html) documents filtering/compositing primitives. These are conceptual references, not installed-provider claims or copied implementations. Local behavior was checked against render.py, manifest.py and the current schemas.
