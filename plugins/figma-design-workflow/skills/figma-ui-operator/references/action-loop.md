# Observe, act, verify

This guide is an authored operating policy, not a claim that Figma exposes a particular automation API.

## State contract

Maintain only what is needed: authorized window, file/page, target hierarchy, selected object(s), current mode, keyboard focus, overlays, zoom, and the last verified change. Revalidate the affected parts whenever the interface changes. Do not keep scrolling through unrelated documents to gather context.

For each operation, decide the intended postcondition before input. “Click at a point” is an action; “the selected frame’s horizontal padding field reads 16 and its text stays centered” is a postcondition. Define structural and visual checks when both matter.

## One logical mutation

Observe → identify → act → observe → compare. Use small batches only while target, focus, and layout are stable. Selecting a known property field, replacing its value, and committing can be one batch. Opening a modal, choosing an unknown result, and typing several values cannot.

Prefer an exact property field to a drag for numerical changes. Prefer a visible menu choice to an uncertain shortcut. Prefer a unique Layers path to coordinates in overlapping artwork. For canvas-only operations, use the most recent screenshot and a comfortably visible target.

Input success does not imply application success. Wait for the expected state using fresh observations or a runtime-supported wait. Do not use a long blind sleep as evidence. Stop if a spinner, sync warning, modal, or permission prompt changes the task state.

### Virtualized Layers and constrained frames

A locator can match the right layer text while scrolling or rerendering causes the input to land elsewhere. After selecting a layer, verify its actual name/hierarchy and node identity when exposed before renaming or editing. If semantic input targets incorrectly, inspect the current visible row and use a supported coordinate click derived from that fresh observation; do not hard-code row indexes or replay an old point. For rename, check the rename field's current value before replacing it. A property update followed by a fresh observation is safer than selecting another virtualized row in the same blind batch.

Frame-height changes can move bottom-constrained controls, not merely trim blank canvas. Inspect footer/CTA constraints and their rendered positions before and after resizing. If an unrequested collision appears, restore the original dimension and verify the restoration. Do not standardize all frame heights as incidental cleanup.

## Field-entry transaction

1. Identify the target object, property label, existing value, and any variable/style binding.
2. Focus the field. Confirm a caret, highlighted field contents, or the runtime’s equivalent semantic focus evidence.
3. Only now select that field’s contents and type the replacement. Match the tool’s text-entry contract; typing and paste are not universally interchangeable.
4. Commit using the visible control or appropriate field action. Check the committed value after focus leaves the field.
5. Check sibling properties and the canvas for side effects. Stop if a binding disappeared or sizing behavior changed unexpectedly.

Select All is prohibited when focus is uncertain. Never issue it on a canvas as a convenient way to find a field. A failed shortcut could have focused the browser address bar or Actions search; inspect before typing again.

## Coordinates and transformations

Screenshot pixels, device pixels, accessibility coordinates, browser CSS pixels, and Figma design units are different spaces. Use the runtime’s documented coordinate system. Do not assume a Retina multiplier, browser scale, window origin, or screenshot crop offset. If conversion is required, use observed metadata and a documented transform; otherwise do not guess.

After zooming, panning, switching pages, opening sidebars, moving a window, or dismissing a modal, discard old click points. A design-space width of 320 is entered as 320 in Figma’s width field; it does not mean dragging 320 screenshot pixels.

For a drag, identify both endpoints and the expected drop indicator. Hold modifiers only for the intended action, then release them. Read the resulting Layers hierarchy; visual overlap alone does not prove reparenting. If the tool cannot perform the required drag reliably, use a documented menu/field route or report the limitation.

## Flow connectors and pointer placement

Before drawing flow arrows, inspect the file's existing connector asset and interaction convention. Reuse an editable connector designed for routing, attachment and labels when one exists; duplicate it and adjust its handles. Do not substitute a generic arrow/vector merely because its color matches. Verify the selected asset's actual type and editing behavior in the current UI; a screenshot or user description alone does not establish its API capabilities.

For a board that distinguishes route meanings, preserve that convention: dotted arrows communicate screen/state jumps; solid connectors with the existing pointer-hand asset communicate clicks. Place the hand just outside or beside the target control, with only slight overlap if useful. Keep the button label, plus icon, and other clickable content readable. Match source hand size, connector weight, bends and endpoint treatment. Where supported, attach the connector to the hand and use its native label feature rather than rebuilding the route from disconnected primitives.

Check each route at reading zoom and board overview: correct source/target, recognizable route meaning, readable controls, no unintended crossings through screens or annotations, and preserved editable asset structure. Human approval of a current board plus a future-only correction authorizes recording the lesson; it does not authorize revising that approved board.

## Focus and interruption

Esc can exit a text editor, dismiss a picker, or change selection depending on state. Use it once and inspect, not as an unconditional “reset” macro. After user intervention, reacquire the screen and selection instead of replaying the next cached command. Never act on stale coordinates after an unexpected notification or window switch.

## Evidence at a checkpoint

Verify exact values in the properties panel; hierarchy/type in Layers; appearance at useful zoom; and interaction in actual playback when relevant. A screenshot cannot prove hidden data, a link relationship, full accessibility, or server persistence on its own. State what remains unverified.

Keep the audit trail compact: intended change, actual result, evidence identifier if available, and whether recovery occurred. Do not include internal reasoning transcripts or unrelated private content.

For a requested cleanup or recolor, record the affected component's behavior separately from its appearance. Intentional overlays, repetition and timing are not disproved by one screenshot. Reuse inspected source colors/style bindings rather than guessing a familiar warning palette; update accompanying annotations when color-based descriptions become stale. Canvas annotations and native Figma comments are different deliverables: create and read back both only when requested, and never report an annotation as a posted comment.
