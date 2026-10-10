# Asset lifecycle and delivery

Use when generating, adapting, exporting or delivering visual assets for a kit. Plan the role and inventory before generation. Reuse current accepted work where it fits; avoid generating every control state as an image.

## Inventory before production

For each asset record ID, role, target component/page, description, source/rights, dimensions/aspect ratios, composition variants, protected regions, transparency, target formats, delivery sizes, status, dependencies and intended acceptance check. Distinguish icons, identity, illustration, texture, frame, background, empty/error-state art and social preview. Required text and control behavior remain live.

Generate only after the relevant rules, layout and asset brief are settled. A prompt should describe subject, style anchors, composition, reserved UI zones, dimensions, transparency and exclusions. Preserve prompt and source references as production evidence without treating the output as accepted automatically. Use the available image-generation workflow for creative generation/edits; deterministic export is a separate production step under the task's authorization and tool policy.

## Masters and derivatives

Persist reusable masters in project-owned storage, with ID, path, role, dimensions, SHA-256, provenance and candidate/accepted/rejected status. Acceptance records must state what was approved: asset, composition, page or viewport. Do not relabel all siblings as accepted. Keep rejected experiments out of public delivery; retain required provenance and rejection reasons under the project's retention policy.

Keep originals and website copies. A smaller delivery image does not replace the master. Record parent hash, transformation tool/version, crop/resampling, color/alpha handling, dimensions, output hash and bytes. Art-directed variants need their own master identity; multiple resolutions of one source share that source lineage.

“Lossless encoding” and “pixel-identical” are different claims. Only a decoded comparison at matching dimensions/color representation can establish a particular pixel equality claim. Resizing or cropping necessarily changes the raster. A losslessly encoded resized derivative is not pixel-identical to its original. Check transparent edges, color and texture at actual use size.

## Browser delivery

Use `picture` for intentional source/composition selection and correctly declared `srcset`/`sizes` for resolution selection. Cap candidates at actual native detail; a filename cannot create resolution. Include intrinsic dimensions or a stable ratio to control layout shift. Keep likely critical opening images appropriately eager/prioritized; defer secondary content intentionally. Tiny decorative accents and identity assets belong in the budget too. See [responsive image mechanics](https://web.dev/learn/images/responsive-images).

Verify the browser's actual selected URL, source dimensions, rendered dimensions, viewport and DPR. Measure at representative densities; a DPR 1 improvement may leave DPR 2 expensive. Distinguish encoded file bytes, transferred bytes, decoded memory, initial viewport and fully scrolled unique resources. Record cache state, compression assumptions and network scope. Local image-byte reductions do not establish LCP, Core Web Vitals or physical-device speed.

Inspect the optimized output beside the source where meaningful. Tolerate explained codec/antialiasing differences only within the stated review; do not call perceptual similarity pixel identity. A style change must not be smuggled into an optimization pass. Recheck composition anchors after source selection changes.

## Public and private packaging

Publish only selected runtime assets and necessary notices. Keep private brand strategy, voice source, discarded art, internal prompts and test fixtures outside a public build. Provide consumers with working relative paths and fallback behavior. At an authorized deployment, check content type and actual served bytes or hashes for important assets; HTTP 200 may serve stale content or an HTML error page.
