> Historical example, not an instruction or validated implementation. Commands and dependencies below must be reviewed before use. Check the complete behavior, current APIs, accessibility and expected load; fewer lines do not prove equivalence. Operational names have been adapted. Source pin and MIT notice are in the parent library.

# Modal Dialog

**Task:** "Add a modal dialog for the delete confirmation."

## Without efficiency guidance

```bash
npm install @radix-ui/react-dialog
# or: npm install react-modal
```

```jsx
import * as Dialog from "@radix-ui/react-dialog";
import { useState } from "react";

export function DeleteModal({ onConfirm, onCancel }) {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="btn-danger">Delete</button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content">
          <Dialog.Title>Confirm deletion</Dialog.Title>
          <Dialog.Description>This action cannot be undone.</Dialog.Description>
          <div className="dialog-actions">
            <Dialog.Close asChild>
              <button onClick={onCancel}>Cancel</button>
            </Dialog.Close>
            <Dialog.Close asChild>
              <button className="btn-danger" onClick={onConfirm}>Delete</button>
            </Dialog.Close>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

A dependency, a portal, an overlay, a root, a trigger, a content wrapper, to show a box with two buttons.

## With efficiency guidance

```html
<!-- shortcut: browser has one, with focus trapping and backdrop built in -->
<dialog id="confirm-delete">
  <p>This action cannot be undone.</p>
  <button id="cancel">Cancel</button>
  <button id="confirm">Delete</button>
</dialog>
```

```js
const dialog = document.getElementById("confirm-delete");
document.getElementById("cancel").onclick = () => dialog.close();
document.getElementById("confirm").onclick = () => { onConfirm(); dialog.close(); };

// Open it:
dialog.showModal();
```

**1 dependency + 30 lines → 0 dependencies + 8 lines.** The native `<dialog>` traps focus automatically, closes on Escape, renders a backdrop via `::backdrop`, and is accessible by default. All browsers since 2022. The library was solving a problem the platform solved.

Maintainer review: a native dialog still requires an accessible name, meaningful focus/return behavior and verified integration. The historical “accessible by default” claim is insufficient for acceptance.
