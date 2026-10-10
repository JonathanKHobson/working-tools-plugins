# End-to-end UI recipes

These are original operator recipes based on the linked feature guides. Sample dimensions and labels are fixtures, not design-system recommendations. Use the user’s actual specification for production work.

## A. First-run sandbox calibration

**Inputs:** explicit permission to create a page named `UI Operator Sandbox` in the current editable file. Existing content is out of scope.

Inspect the runtime and interface. Create the page through the current File/pages controls, verifying no existing page with that exact name is accidentally overwritten. Create a frame named `Calibration / Card`, set width to 320, and add a text layer containing `Ready to review`. Wrap/layout the intended content vertically, set padding to 16, and choose Hug vertically. Add a second line `This is a disposable UI check.` using the available approved font.

Verify both strings, parent-child structure, 320 width, 16 padding, and the selected sizing modes. Rename only your frame to `Calibration / Verified`. Observe the result. No export or prototype is required.

**Pass:** correct file/page, no unrelated edits, exact content and properties, actual screenshot/observation evidence. **Recovery:** field-focus transaction and exact Layers selection; after two grounded attempts, stop. Keep the sandbox for inspection unless cleanup is explicitly authorized.

References: [frames/text](create-and-edit.md), [layout](auto-layout.md), [calibration template](../assets/ui-calibration-template.md).

## B. Responsive card without destroying the original

**Inputs:** an identified card/frame, approved scratch-copy location, exact copy to preserve, and target test widths.

Inspect the source’s component/variable relationships. Create a safe local test copy within scope and verify its type. Establish a vertical container, explicit padding/gap, appropriate text wrapping, and child width behavior. Reuse existing styles/tokens; do not invent replacements.

Resize the test container across the requested widths, checking text, clipping, hierarchy, and bindings each time. Restore original width and sizing mode. Apply the tested change to the approved target only when the task includes doing so; “investigate” alone does not authorize changing production.

**Pass:** requested responsive behavior and structural preservation at each tested width. **Recovery:** inspect parent-child sizing rather than detaching or manually offsetting every child.

## C. Button with two variants and an instance

**Inputs:** authorization for new sandbox components, label `Continue`, State values `Default` and `Disabled`, and approved visual styling.

Create the text and an auto-layout button wrapper; inspect padding and Hug behavior. Create one main component, then use Add variant. Configure the two State values and their authorized styling. Add an instance through Assets, change its State property, and verify each state. Do not presume a disabled visual style disables a prototype action.

**Pass:** a component set with two unique State values and a linked instance that switches correctly. **Recovery:** inspect component identities and property names, not just artwork.

Figma’s written button tutorial uses the text → auto layout → reusable component progression; this recipe adds operator verification and safe-scope checks. [S26](sources.md#s26)

## D. Apply an existing design token

**Inputs:** exact target property and token name, with collection/library when ambiguity is possible.

Locate the object and inspect the current binding. Open that property’s style/variable picker, select the approved token, and verify token identity plus resolved value. Do not edit the token’s underlying value or create a duplicate. If missing, inspect type, scope, and library availability before reporting a blocker.

**Pass:** one intended property is bound to the correct existing variable. **Recovery:** restore the known previous binding if a mistaken change was made, then stop if the target remains ambiguous.

## E. Two-screen interaction test

**Inputs:** named source/destination frames, exact hotspot, trigger, and expected action.

Select the hotspot, inspect existing interactions, add or edit the scoped interaction in Prototype, and set the intended start point when authorized. Open Preview or Present. Activate the actual hotspot and confirm destination content. Return to the editor and reverify file/page.

**Pass:** actual interaction reaches the intended destination without unintended whole-frame activation. **Recovery:** check hotspot and destination before changing animation options.

## F. Precise copy change in a nested instance

**Inputs:** exact instance path, text/property identity, and replacement string.

Prefer an exposed text component property where available. Otherwise inspect whether the intended nested text supports an authorized override. Change only that text, inspect the instance link and nearby labels, and check wrapping. If a permitted override is unavailable, report that instead of detaching.

**Pass:** exact copy in the intended instance, unchanged main component and sibling instances, no broken link. **Recovery:** one known-action undo if the wrong object changed; disambiguate the hierarchy before retrying.

## G. Selected-frame export

**Inputs:** exact frame, format/scale, destination, and permission to export.

Select the frame and verify its boundaries/content. Configure its scoped Export section and review the preview. Export to the approved destination. Verify the real artifact when the runtime permits file access; otherwise describe the observed save confirmation only.

**Pass:** expected content/format at a real verified destination, no extra pages exported or sharing changes. **Recovery:** check scope, format, and access; never bypass an export restriction.
