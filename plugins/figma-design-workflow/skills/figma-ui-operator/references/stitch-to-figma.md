# Export selected Stitch screens into editable Figma

## Evidence and scope

Google documents a paste-to-Figma handoff in its [Stitch introduction](https://developers.googleblog.com/en/stitch-a-new-way-to-design-uis/). The route below also incorporates a user demonstration reviewed on 2026-09-09: Export → Figma → Convert → wait → Copy → Figma desktop context menu → Paste here. A 16-screen batch limit was explicitly reported in that session. Treat 16 as the observed ceiling for this workflow; honor a smaller current limit and recheck if the UI changes. Do not assume the same controls or permissions exist in every mode/account.

The historical demonstration was human-operated after an automated Copy stalled. It establishes a usable route, not measured autonomous reliability. This skill's current live import test status is recorded separately from package tests.

A request to write this guide does not authorize a test import into a real file. A request to transfer selected screens does authorize its routine source selection, conversion, copy, and destination paste. Inspect the destination before starting; do not demand approval again for each step. If only local export is requested, do not transfer to another service.

## 1. Identify one batch

Inspect the exact Stitch project and selected screen names/previews. Record a compact manifest: batch ID, source screen names and count, intended Figma file/page/area, and current import state. Distinguish accepted screens from similar old variants and supporting flow maps. Preserve existing prompt text and attachments; selecting screens can add composer context chips.

Use batches of no more than 16 screens in this observed workflow, starting with a small representative batch when runtime behavior is unproven. For 20 requested screens, plan two batches, not 20 simultaneous conversions. Do not use canvas Select All to discover the selection. Verify the count in the source UI. A disabled Export or “No screens selected” indicates selection must be corrected first.

## 2. Export and convert

Open the observed Export control and select **Figma**. Avoid confusing Figma with Code to Clipboard, Copy prompt, a PNG/ZIP export, or a hosted partner destination. If shown, choose **Convert** once. Observe the progress state until conversion finishes and **Copy** is available. An enabled Convert button alone is not completion evidence.

Wait using fresh supported observations, with progress updates during long work. Do not repeatedly trigger conversion while the same batch is processing. If the UI shows an error, address that exact error before retrying.

## 3. Copy the converted design

Activate the export's **Copy** button after conversion. Keep the source batch stable. A copied indicator is useful but provisional evidence. Do not rewrite the clipboard with `pbcopy`, type the copied text into Figma, or inspect only `pbpaste` and conclude a structured design payload is absent. Clipboard helpers that stringify content can discard rich design data.

## 4. Paste into the destination

Switch to the already identified Figma Design file and page. Reobserve the current app, destination area, selection, and focus. Exit text editing or a property field through an observed safe action. Paste once into an empty authorized canvas location.

The demonstrated fallback is a right-click in the intended blank area followed by the current **Paste here** menu item. Use it when ordinary paste focus or placement is uncertain. Do not guess a fixed coordinate or paste into a similarly named file. For a browser destination, follow the available paste controls and permissions; do not promise desktop behavior.

Wait for nodes to appear, then inspect before another paste. If the user says they already pasted, inventory the destination first. Do not replay the entire batch and create duplicates.

## 5. Verify arrival, editability, and fidelity

Update the manifest only as each state is evidenced:

- **Converted:** source conversion finished for the identified batch.
- **Copied:** source confirms Copy; destination receipt still unverified.
- **Pasted:** expected new top-level screens actually appear in the intended page.
- **Editable:** expand imported frame hierarchies; inspect text/shape layers and their properties. One PNG or image fill is not editable UI. Count screen roots separately from child layers or an import wrapper.
- **Verified:** reconcile every expected screen, check names/order/dimensions, and visually compare source and destination using anchors for typography, key actions, icons/images, spacing, and clipping. Check all screen overviews; inspect representative interiors and every mismatch in detail.

Do not promise component links, variable bindings, auto layout, fonts, or prototype interactions survived conversion. Inspect the relationships actually present. Do not flatten screens to conceal import defects. Record fonts/assets or behaviors still missing.

## 6. Recover and arrange

If nothing appears, first inspect destination Layers and nearby/offscreen content to avoid duplicate paste. Then check destination focus and the source Copy state. Make at most two distinct grounded recovery attempts: for example, one fresh post-conversion copy followed by the observed Paste here route, then one smaller identified batch if evidence points to batch failure. Never repeat a failing Copy loop indefinitely.

When the clipboard bridge remains blocked, ask the user to perform only that copy/paste step and resume from verified destination state. Preserve the designs; report converted/copied/imported separately. API reconstruction, a bitmap export, or a new third-party plugin is a different output/route and cannot silently replace editable import.

After one batch is verified, arrange only its intended roots and proceed to the next. Use [import and presentation checks](import-and-presentation.md) for container sizes and callouts. Restore temporary Stitch context chips without deleting source designs or draft text, verify sync if observable, and complete browser handoff.
