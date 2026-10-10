# Build and verify prototype interactions

## Define the transition

Before wiring, identify source frame, exact hotspot layer, trigger, action, destination, and any requested transition. Example contract: the Continue button in Step 1 navigates to Step 2 on the available click/tap trigger. This does not authorize making the whole screen clickable.

Select the source hotspot in Layers and confirm its identity. Open Prototype. Add an interaction through the panel or the visible connection handle; set the trigger, action, and target in the interaction controls. The panel route is preferable when dragging a connector across a large canvas is unreliable. [S22](sources.md#s22)

Verify the interaction’s recorded destination name against the correct page/frame, especially when several screens share names. Inspect existing interactions before adding a new one: do not accidentally stack another action on an existing trigger.

## Preview versus Present

Figma’s inline Preview runs within the editor; Present opens a separate presentation tab. Designs need frames, and a flow starting point determines where a journey begins. The current guide documents Preview in the toolbar and Shift-Space, with Present as a separate toolbar action. [S23](sources.md#s23)

Choose the appropriate mode deliberately. After playback opens, confirm which window receives input. Reacquire screenshot coordinates because the viewer has a different viewport and scaling from the editor.

## Functional test

Begin at the intended starting frame. Activate the actual hotspot using the requested trigger, not a viewer’s “next screen” arrow. Confirm the destination by its distinctive content or screen name and inspect the relevant state change. Test back/close paths when they are part of the request. Do not treat a visible connector line as proof the prototype works.

For overlays, inspect the chosen overlay action, destination, position, backdrop, and close behavior shown in the UI. For scrolling, test the intended scroll container rather than the entire presentation window. For animation, evaluate the actual playback; matching transition settings alone is not enough to claim the motion looks correct.

If an option is unfamiliar or absent, inspect the current menu and consult the official task-specific guidance. Do not infer behavior from a tutorial for another Figma product or silently replace an interactive requirement with a static frame.

## Return to editing

Close or leave the viewer using its visible controls, return to the authorized editor, and verify file/page/selection again. Playback shortcuts can conflict with editor shortcuts. Do not keep typing under the assumption the editor regained focus.

## Report

State which transition(s) were exercised, from which start, with what observed outcome. Distinguish configured, visually inspected, and actually played. Mark untested hover, keyboard, touch, scroll, responsive, or alternative-state behavior explicitly when relevant.
