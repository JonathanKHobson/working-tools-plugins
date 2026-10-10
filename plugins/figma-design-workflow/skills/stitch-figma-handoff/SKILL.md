---
name: stitch-figma-handoff
description: Transfer selected Stitch designs into editable Figma frames and verify the receiving structure. Use for export, Convert/Copy recovery or resumed transfers, not code export or general design generation.
---

# Stitch to Figma

Read the [transfer workflow](../figma-ui-operator/references/stitch-to-figma.md) and [runtime contract](../figma-ui-operator/references/runtime.md). Use the user's existing project and destination. No new plugin, account change, publishing, or code implementation is an incidental prerequisite.

Identify selected source screens and the destination Figma file/page/area. Maintain a compact batch manifest and preserve the user's unsent Stitch draft and attachments. The recorded workflow uses batches of at most 16 screens; inspect the current UI limit.

Follow the observed Export → Figma → Convert → wait → Copy route, then paste once into the verified Figma canvas. The demonstrated desktop fallback is the context-menu Paste here command. Check for existing pasted nodes before repeating anything. Do not overwrite a rich clipboard with text helpers.

Reconcile every expected screen root and inspect native child layers and text properties. A bitmap showing a screen does not satisfy editable UI import. Compare source and destination with visual anchors; do not assume fonts, auto layout, components, tokens, or interactions survived conversion.

When Copy stalls, use two distinct evidence-based recoveries at most, then ask for only the blocked human copy/paste step. Resume from actual destination state. For arrangement, read [import and presentation](../figma-ui-operator/references/import-and-presentation.md); inspect parent heights and clipping before repositioning children.

Close with actual converted/copied/pasted/editable/verified/synced states, source and destination evidence, unresolved gaps, restored temporary selection, and browser handoff. Historical demonstration is not proof of the current transfer.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UI Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
