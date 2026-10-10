# Create and edit native objects

## Frame with explicit dimensions

**Preconditions:** an editable Figma Design file and authorized target page. Do not create a new team, project, or file unless requested.

Use the frame tool (F when canvas focus is confirmed) or the visible Frame action. Create a frame in the authorized area, then select it in Layers and set W and H through the labeled fields. Rename the exact row. Frames support nesting and layout properties; groups and sections are not interchangeable with frames. [S10](sources.md#s10)

**Verify:** correct parent, frame type, name, width, height, and clipping behavior. If a frame is nested unintentionally, inspect the tree and correct only the intended reparenting. Do not flatten a hierarchy to make it look right.

## Text and copy editing

Select the intended text layer by its parent path. Enter text-edit mode and confirm the insertion context; replace only the requested copy. Check punctuation, line breaks, casing, and overflow against the user’s exact text. For new text, choose an appropriate container rather than placing disconnected labels across the canvas.

Typography controls include font, weight, size, and text-box behavior. Auto width, auto height, and fixed size determine different wrapping and overflow outcomes. Select text-box behavior deliberately instead of hiding clipping with an oversized frame. [S11](sources.md#s11)

**Verify:** the actual string, expected wrapping, font/weight, and bounding box. Inspect at a useful zoom and within the surrounding screen. For longer replacement copy, resize the intended layout or report the conflict; do not silently shorten the user’s wording.

Missing font is a blocker for changes that require that font. Report the exact missing family/style and preserve the current design. Do not purchase, download, or substitute fonts without permission. Font fallback visible on screen is not proof the requested typography was preserved.

## Fills, strokes, and properties

Inspect the relevant fill or stroke row before clicking its swatch. Multiple fills and mixed multi-selection values require special care: changing a selection color can affect more than one object. Enter the exact specified color notation and confirm opacity. Choose an existing style/variable when that is the requested design-system relationship. [S12](sources.md#s12)

**Verify:** property row, resolved color, opacity, binding state, and appearance. A matching screenshot color does not establish a token binding. Do not replace a gradient, image fill, or semantic token with a flat color just because it is easier.

For radius, stroke width, shadow, and dimensions, use labeled fields visible in the selected object’s properties. Confirm units and which sides/corners are linked. Make one coherent style change at a time; mixed selections can mask differing originals.

## Duplicate and reorganize safely

When editing a production object experimentally, use an authorized local duplicate or an agreed checkpoint. Keep the copy in the approved file/page and identify it clearly. Recheck object type and relationship after duplication; do not assume a duplicate of a main component is an independent main component.

To reorder or reparent, use the Layers tree and inspect the drop indicator. Confirm every moved child appears under the intended parent, in the correct order. Auto-layout ordering is not the same as manual X/Y placement. Avoid moving hidden siblings along with the visible target.

A scratch object may be removed only when you can identify it as your own disposable work and its deletion is within the task. Never clean up similarly named objects by broad search-and-delete.

## Import approved imagery

Use the observed Place image/import route with the specific user-approved asset. Confirm the destination object or insertion location before placing it. Check crop, fit, mask, and aspect ratio after insertion. Do not download unrelated stock art or upload private images to a new service to fill an empty placeholder.

## Completion gate

Compare the edited object with the starting state: intended change made, unrelated copy intact, correct hierarchy, no clipping, and no unintended detachments. Visual polish is not permission to restyle surrounding screens.
