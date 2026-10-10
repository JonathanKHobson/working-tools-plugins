# Auto layout: structure before appearance

## Establish the container

Inspect whether the target is already a frame, component, instance, or multiple loose objects. Select only the intended container or children, then use Add auto layout or Shift-A with canvas focus. Loose selections may be wrapped in a frame. Figma now offers horizontal, vertical, and grid flows. “Suggest auto layout” is a different, more expansive restructuring action; do not substitute it without approval. [S13](sources.md#s13)

**Verify immediately:** the resulting object type, children, reading order, and chosen flow. If unexpected content was wrapped, undo only this known operation and repair the selection. Do not drag everything back into place and leave a broken structure.

## Sizing decisions

Hug contents sizes around content and padding. Fill container is available to children of an auto-layout parent, not arbitrary top-level objects. Fixed retains an explicit size. A parent hugging an axis and a child filling the same axis can force a sizing change; inspect the resulting relationship. Entering a numeric W/H or manually resizing may switch that axis to Fixed. Min/max bounds are separate controls. [S14](sources.md#s14)

Authoring rule: choose the parent’s sizing behavior before the child’s on each axis. State which element owns the available width. Do not solve a circular relationship by entering arbitrary dimensions repeatedly.

Example design contract, not a Figma default: a full-width card in a fixed-width mobile screen can use Fill horizontally and Hug vertically; its text can fill the available width and grow vertically. The screen, card, text, and button each need separate decisions.

## Direction, gap, padding, and alignment

Horizontal/vertical flow controls direction and alignment. Gap is space between children; padding is between children and container edges. A numeric gap and Auto spacing behave differently. Wrapping introduces another row/column spacing relationship. Inspect the actual alignment controls and do not assume Auto spacing centers a lone child. [S15](sources.md#s15)

For exact values, edit the fields. Verify whether padding sides are linked. Reorder the children in Layers when their reading order is wrong; do not compensate with empty spacer layers unless the requested design calls for them.

## Grid flow

Grid auto layout uses rows, columns, track sizing, and gaps. It is not a visual layout guide. The current controls allow specifying rows/columns and adjusting tracks. Deleting a row or column can delete content, so do not use deletion as a casual way to redistribute cards. [S16](sources.md#s16)

For a card-grid task, inspect the requested column count and each child’s assigned cell/span. Confirm track behavior and no missing content after changes. Check the final tree as well as the rendered grid. Avoid promising responsive breakpoint behavior that was not actually configured and tested.

## Bound spacing and tokens

A bound gap/padding value is a design-system relationship, not merely a number. Preserve it when changing unrelated geometry. Figma’s on-canvas spacing handles can detach number-variable bindings; use the appropriate field/picker for token-aware changes. [S20](sources.md#s20)

If the user requests a specific numerical exception, make clear whether it overrides a token at this instance or changes the token itself. These have different scopes.

## Resize test

Use an authorized scratch copy or an explicitly permitted resize of the target. Record the original dimension, then test a narrower and wider size through the width field. Example test widths 320, 390, and 768 are authored probes, not universal device requirements; use the user’s target widths when supplied.

At each width, inspect text wrap, clipping, alignment, button size, content order, and child sizing modes. Restore the original dimension and recheck its sizing mode and variable binding. A screen that looks correct at one width has not passed a responsive-layout test.

## Troubleshooting order

Check selection → parent layout → child sizing → min/max bounds → text sizing → visibility/clip → gap and padding. Check whether a child is deliberately excluded from flow before changing it. Never detach a component instance to reveal a missing control; identify the proper override or ask for a scoped main-component change.
