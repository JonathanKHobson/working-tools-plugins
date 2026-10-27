# Image-generated assets in code-authored motion

Use when an illustrated or tactile direction needs richer assets than convenient procedural primitives provide. Image generation is a design/material supplier. Code still owns the event sequence, composition, camera, exact typography and sound unless the brief intentionally uses generated lettering.

## Specify an asset contract before generating

Start with the hardest interaction and final composition. Define each asset's role, canvas dimensions, alpha requirement, crop-safe margins, registration point, viewing angle, lighting, scale relationships, palette and material. A sprite atlas needs explicit cell layout and padding; a pose set needs identity and anchor consistency. A background plate must leave room for animated actors and type. Avoid baking the subject, shadow and text together when they need to move independently.

Use one style reference across assets. Request transparent cutouts where needed and preserve generated alpha. Inspect the actual output; do not assume the generator obeyed cell boundaries, empty backgrounds or exact geometry. If an asset must be revised creatively, use the image-generation/editing workflow. Renderer-side cropping, UV sampling, masks and transforms should be explicit reproducible scene operations.

Keep exact labels and small typography in a measured code/font layer when that serves readability. Generated lettering can work for a material-specific sign or expressive title, but record it as generated/custom artwork rather than inventing a font name. Do not redraw every visual element procedurally while claiming an image-generated asset experiment.

## Make the artwork survive motion

A beautiful plate can hide unusable joints, cropped edges, inconsistent pose proportions or baked lighting. Test a registered pose transition, occlusion/contact, growing reveal and typography interaction at playback speed before generating a large batch. Use scene-space attachment points instead of eyeballed offsets. Save measured alpha/content bounds, padded crop rectangles, joints, scene anchors and any background-to-world mapping against the exact artwork hash. Atlas cells may overflow their requested rows. Normalize pose identity, display scale and attachment points independently of cell centers so pose changes do not jump. A changed image invalidates those measurements; remeasure before reusing them. If only one rigid illustration exists, describe the result as a moving cutout, not newly generated character acting.

Code controls deterministic state at the project’s declared evaluation rate (for example, frame/60 for a 60 Hz brief). A reference with deliberate pose holds should preserve and label them. Quantized pose animation may be intentional, but preserve continuous scene motion where the brief calls for it. Cache expensive static texture preparation separately from frame-dependent transforms, masks and explicit pose holds. Test direct seeking and the rendered transition after caching. Do not use interpolation, metadata changes or whole-frame repetition as evidence of native continuous motion; intentional holds are not a defect by themselves.

## Evaluate the experiment honestly

Keep a baseline and change one meaningful production factor. Compare matched shot intervals and final composition for clarity, material identity, coherent style, edge quality, contrast, temporal consistency and story readability. Generated imagery is not automatically higher quality, nor is additional detail automatically useful at phone scale. Record whether the variant is an improvement, a tradeoff, or a rejected approach. Preserve remaining issues and user feedback.

Every accepted asset must have a stable project path, role, dimensions, SHA-256, exact prompt, input reference and actual model/tool provenance available to the agent. Record candidate/accepted-persisted/rejected-disposable status. Retain code for masks, cropping and registration alongside the images. Save selected images out of the conversation transport cache. Follow the user's session image/storage limits and clean only task-owned disposable intermediates after the lane closes.

A deliverable includes full encoded film, source, image assets, animation/registration map, font identity, audio source, prompts, contact sheet, making-of images, corrections and known limitations. Promote cross-style discoveries through evolve-video-workflow; keep visual identity in the selected template.

For character acting from generated pose strips, use [coherent sprite animation](generated-sprite-animation.md). It adds the timed director/asset-maker contract, connected-pose extraction, shared scale, prop contact, transitions and semantic motion acceptance.
