# Recognize the current interface

## Five regions, not fixed coordinates

The current design-file guide identifies a navigation bar, left sidebar, canvas, right sidebar, and toolbar. The navigation bar’s File and Assets entries lead to contextual sidebar content. Design/Prototype properties depend on selection and access; view-only UI differs. These are semantic regions, not screen positions to hardcode. [S03](sources.md#s03)

The newer navigation guide places File, Assets, Tools, and Variables in the far-left navigation bar. Variables can open a dedicated view instead of an older properties-panel modal. Notifications and missing-font information may appear near the navigation bar’s lower area. Feature rollout, window width, and saved layout may change what is visible. [S04](sources.md#s04)

## Orientation procedure

First identify the filename and page. Then locate the File entry and layers tree, determine whether the right sidebar is Design, Prototype, Properties, or a history view, and locate the current selection. Read the visible labels rather than matching color alone. A purple outline, for example, does not establish which component relationship is selected.

A full editing toolbar is useful evidence of edit access, but confirm the actual file state before making changes. An Ask to edit control is not an invitation to bypass restrictions. Do not request a new seat or change access automatically.

Inspect the toolbar’s tooltips or visible menu labels. Move, Hand, Scale, frame/section tools, shapes, and text are different operations. Scale changes proportions; it is not a general substitute for editing frame dimensions. Imported images may be represented as fills rather than a distinct image-layer type. [S05](sources.md#s05)

## Find a target reliably

Start with the named page, then expand the target’s parent chain in Layers. Distinguish similarly named objects using their hierarchy and preview. For an overlapping or nested object, a Layers row or the context menu’s Select layer route is more deterministic than repeated canvas clicking. Deep selection uses Command-click on macOS or Control-click on Windows; Enter can descend and Shift-Enter can select the parent when canvas selection has focus. [S09](sources.md#s09)

Do not assume a selected text layer is in text-edit mode. Outline plus right-sidebar typography is different from an insertion caret. Do not type content until the intended text insertion context is visible.

Use the zoom menu or Shift-1 to fit and Shift-2 for a known selection. Changing canvas zoom is different from scaling the application’s interface. Reacquire target positions after either changes. [S08](sources.md#s08)

## Actions as a fallback route

Open Actions with Command-K on macOS or Control-K on Windows when supported in the focused editor. Search the intended operation, read the result label, and select the deterministic command. Do not press Enter on an unchecked first result: actions may include generative operations, plugins, and destructive commands. [S06](sources.md#s06)

Search is a locator, not authorization. A “replace all” result still needs the scope and review appropriate to a bulk edit.

## Capture an interface profile

Use the [calibration template](../assets/ui-calibration-template.md) to record labels and routes observed in this session. Store semantic routes, not permanent coordinates. Record the date and runtime. Do not save private filenames or screenshots outside the approved workspace, and do not persist user preferences without permission.

Conflicting tutorial: stop using its placement instructions. Reinspect the live menu, then consult the relevant official guide. See the source ledger for the known File-shortcut and Variables-location conflicts.
