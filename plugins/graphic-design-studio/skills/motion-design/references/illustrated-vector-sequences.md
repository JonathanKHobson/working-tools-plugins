# Illustrated vector sequences

Read when creating or reviewing a frame sequence from layered illustrated SVG art: a character action, moving object, or drawing whose pose changes across frames. This is a visual construction and review method. It does not impose Napkin Sketch's six-part rig, cycle tables, app form, scripts or assets on another project.

## Read the picture and map the parts

For an unknown SVG, inspect markup for active content and external references with the existing vector asset checks before any execution-capable render; an already supplied inert raster preview can be read first. Then render the admitted SVG at a bounded size and identify the subject, view angle, facing direction, current action, weight/contact point, and which parts cross or occlude others. Then inspect the SVG source to map visible parts to groups and path bounds. Layer names are clues, not proof: editor-generated IDs or misleading names can coexist with a coherent drawing. For each part, record its current bounds, pivot/joint, parent, depth order and what moves with it (hair, clothing, glove, prop). Compare this map with the actual pixels before posing. Preserve source art and exact path data when a frame can be made by transforms; draw new geometry only when the action truly requires it.

The visual source may have no usable rig. A mirrored pair of narrow shapes near a torso may be limbs; containment and overlapping paint order help infer attachments. Verify the inference against the rendered drawing. A part's near/far status can change as limbs cross; depth and paint order are part of a pose, not a fixed property of the source layer tree. No universal box fractions, group names or rotation signs substitute for reading the actual figure.

## Construct a movement that remains one subject

Define the action's key poses and intended loop or end state before filling intermediate frames. Use the current pose as the starting condition; a sample walk cycle is not a command to make an unrelated figure walk in the same direction. Mark contact, passing, apex/impact and settle frames as appropriate. Set pivots near the joints that actually carry each part, and move attached details with their parent. Apply the subject's overall translation/bob consistently so joints do not separate. Re-evaluate overlaps and layer order after each pose.

For a transform-based frame, keep the inherited geometry stable and change the owned group transforms rather than re-emitting all `d` values. This preserves the path and its Bézier handles. If the pose needs a bend, new facial expression or breaking shape that cannot be expressed by the current groups, create a deliberate new drawing/part and record that change; do not contort a rigid transform until anatomy or object structure fails. Match the current orientation before applying angle signs. When a loop is intended, plan the return to the initial pose and test the wrap in playback; one-shot actions should settle at their endpoint.

Spacing between poses conveys speed and weight. Even gaps read as steadier travel, growing gaps as acceleration, and clustered gaps as a hold or slow apex. A rebound needs reduced height and time on successive bounces, but numerical physics examples are guides to shape, not fixed motion standards. Let the brief's meaning change the pose: a tired walk, a hurried walk and a celebratory jump can share a skeleton yet require different leading parts and holds. Keep every beat legible at actual playback speed.

## Grade the result twice: structure and picture

Render the new frame beside its predecessor and its intended next/key pose. Inspect silhouette, attached joints, contact with ground or held objects, occlusion, tangencies, clipping and scale. Compare movement distance with the figure's own dimensions and the chosen style, then inspect the sequence at speed. Structurally, verify the expected groups are present, transforms/pivots are intentional, IDs do not collide, path data changed only where new drawing was required, and the final frame naming/order is unambiguous to the actual player. A structurally valid layer tree can still produce a bad pose; a polished still can still fail between frames. Record defects and the first meaningful correction; do not inherit a source app's fixed pass count or `npm` grader as an acceptance rule.

Use a preview image for pose and a targeted SVG/JSON read for coordinates or names. If source studies or rigs are supplied, distinguish an actual measured rig from a loose drawing: an old study demonstrates motion character, not an authoritative mapping for the new subject. If no reliable example exists, make a few original key poses and test them instead of forcing an unrelated cycle.

For SVG-to-Lottie delivery, apply Graphic's [animated vector interop method](../../graphic-asset-compositing/references/animated-vector-interop.md). Video Production owns the rendered sequence and audio; UX owns product-player behavior.

## Source and rights

Adapted from `isocialpractice/napkin-sketch` at `5a3675e6227dd741c068d86bd218d58d1a416f4b`, especially `ai-helper/vectors/skills/vector-animations/SKILL.md` and its `animation-essentials.md`, `animation-physics.md`, and `bezier-curves.md` references. Full MIT notice is preserved in [motion/vector notices](../../../docs/motion-svg-source-notices.md). The captured selection omitted its app form, companion drawing skill, preview PNGs and `frame-preview` script; none was executed or imported, and this method does not claim to validate its artwork or cycle metrics.
