---
project: graphic-design-studio
type: compositing-reference
status: active
tags: [occlusion, masks, contact, effects]
---

# Spatial contact

Use this guide when a composited image must depict a specific physical relation. These are original implementation heuristics; [research](../../graphic-design/references/research.md) distinguishes the source-backed nondestructive workflow from design judgments.

Translate the request into visible evidence. “Gripping armor” might require some fingers behind a shoulder, others in front, and a contact shadow restricted to the surface being touched. “Emerging through paper” needs a visible opening, an edge with thickness or deformation, and a coherent relation between that edge and the emerging object. If the supplied viewpoint cannot show these cues, use a suitable image-editing workflow or explain the limited achievable result before claiming it depicts the relation.

Make a simple layer-order sketch in working notes. For a grip: background → rear fingers → subject → contact shadow on subject → front fingers. Actual order depends on the source geometry. One object can require multiple masks; one global z-index is insufficient for interleaving.

Keep masks attached to the transform of the asset they describe. Rotation or scale changes can invalidate a previously correct mask and shadow. Inspect the new render at the contact point rather than assuming the previous review still applies.

Contact shadows tend to be tight at contact and change as surfaces separate; use the scene's light direction. A broad black outline makes an object look pasted on. Shadows should fall on plausible receiving surfaces, not arbitrarily darken the page behind them.

Do not repeatedly regenerate an entire composition to fix a local relation. Preserve approved type, facts, logos, cast, and background when the request is local. After a reasonable revision, compare the actual result with the requested evidence. If the geometry still fails, change the method or narrow the claim; repeating the same failed masking assumption is not progress.

Review three scales: close-up for mask edges and occlusion; full graphic for whether the action reads; intended output size for whether the detail survives. A compelling close-up can disappear at poster distance. A convincing full-page effect can still have distracting edges in a print file.

## Generated object consistency

Use these checks when generated imagery depicts physical objects. Define the focal relation before generation and inspect it in the actual final image; photoreal texture or handmade styling can conceal incorrect geometry.

- A magnifier should enlarge/distort the same underlying content at a plausible position. Paper lines, marks and edges should continue consistently across its boundary; unrelated contents inside the lens fail the relation. Refraction may alter their apparent position, but should form one coherent scene.
- Reflections and transparent objects should relate to the scene's viewpoint, light and nearby objects. Highlights alone do not establish believable glass.
- Hands, tools and objects should meet through plausible grip, contact and occlusion. Check the handle connection, front/back order, receiving shadows and separation from surfaces.
- Paper, screens and layered materials need consistent edges, thickness, perspective and folds. A diagram's marks should carry a readable idea rather than imitate technical notation without meaning.

Deliberate surrealism or collage can depart from physical realism when that departure communicates the intended idea and its visual rules are coherent. If a difficult prop adds no useful meaning, simplify the concept or use an authentic source artifact. Do not invent a product screen to make the scene seem credible. Preserve approved type and assets when correcting a local defect, use the current image-editing tool for actual image edits, and inspect the changed relation plus the full composition again.

For repeated distress, vary form and placement according to the material or gesture. Reusing an identical splatter in every corner may expose the stamp. However, purposeful repetition can be a brand system; judge the effect against the intended style. Preserve quiet regions around text and codes.

When a user rejects a complex effect and asks for a simpler one, the new direction replaces the old target. Verify the simplified result and describe only what is visible. Do not keep claiming a paper tear, grip, or other effect that the current design no longer attempts.
