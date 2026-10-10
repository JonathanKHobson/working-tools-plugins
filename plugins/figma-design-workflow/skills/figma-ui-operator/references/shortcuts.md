# Small, context-checked shortcut reference

Every shortcut assumes the correct Figma editor has focus and no text field or modal consumes the input. Verify the displayed shortcut on non-US layouts and when behavior differs. Figma’s keyboard guidance provides a current reference; keyboard operation does not cover every function. [S07](sources.md#s07)

| Intent | macOS | Windows | Condition/source |
|---|---|---|---|
| Actions search | Command-K | Control-K | Read result before confirming. [S06](sources.md#s06) |
| Frame tool | F | F | Canvas focus. [S10](sources.md#s10) |
| Text tool | T | T | Not already editing text. [S05](sources.md#s05) |
| Rectangle tool | R | R | Not in a prototype viewer. [S03](sources.md#s03) |
| Hand tool / temporary pan | H / hold Space and drag | H / hold Space and drag | Release after action. [S03](sources.md#s03) |
| Fit canvas / selected object | Shift-1 / Shift-2 | Shift-1 / Shift-2 | Second requires known selection. [S08](sources.md#s08) |
| Add auto layout | Shift-A | Shift-A | Inspect selected subtree first. [S13](sources.md#s13) |
| Create component | Command-Option-K | Control-Alt-K | Not bulk creation. [S18](sources.md#s18) |
| Deep select | Command-click | Control-click | Prefer Layers path for ambiguity. [S09](sources.md#s09) |
| Select child / parent | Enter / Shift-Enter | Enter / Shift-Enter | Canvas selection, not text field. [S09](sources.md#s09) |
| Inline prototype preview | Shift-Space | Shift-Space | Confirm viewer focus afterward. [S23](sources.md#s23) |

For rename, duplicate, undo, visibility, lock, and other operations, prefer the verified context/main-menu label when the exact mapping is not established. Do not build a long speculative shortcut macro.

## Known traps

**File sidebar shortcut:** current navigation documentation and older selection documentation disagree about the Windows modifier. This package intentionally does not prescribe either as universal. Use the visible File navigation entry, or inspect the shortcut shown in the running version. [S04](sources.md#s04) [S09](sources.md#s09)

**Mouse-wheel zoom direction:** documents and user settings can differ. Use explicit zoom menu values or the verified fit shortcuts rather than assuming a wheel direction. [S08](sources.md#s08)

**Export shortcut:** Command/Control-Shift-E may open a bulk-export route. Select the intended object and use its scoped Export controls for ordinary export tasks. [S24](sources.md#s24)

**Escape and Select All:** Escape is state-dependent. Select All is allowed only after positive field-focus identification. These are safety rules for the operator, not modified Figma shortcuts.
