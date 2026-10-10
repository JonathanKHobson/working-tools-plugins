# UI Patterns

## Choose SwiftUI vs AppKit

Use `SwiftUI` by default for new native macOS UI.

Use `AppKit` when the task needs:

- custom `NSWindow` behavior
- advanced table, outline, or tree handling
- deep responder-chain control
- detailed first-responder or focus behavior
- custom menu or toolbar integration beyond SwiftUI defaults
- rich text or legacy macOS APIs that SwiftUI does not expose well

Use a narrow SwiftUI-AppKit bridge when only one area needs AppKit.

Do not default to Catalyst unless the user explicitly wants iPad reuse.

## macOS conventions

- Prefer menu commands for core actions.
- Add keyboard shortcuts for common and repeated work.
- Use desktop terms such as window, settings, toolbar, sidebar, and document.
- Respect selection models, focus, hover affordances, and secondary-click behavior.
- Favor stable window layouts over mobile-style stacked navigation.

## Menus and commands

- Put app-wide actions in commands rather than burying them in isolated screens.
- Keep menu labels action-oriented and concise.
- Match shortcuts to macOS expectations when a standard shortcut exists.
- Avoid duplicate actions in too many places unless discoverability justifies it.

## Toolbars

- Use toolbars for global actions that affect the current window.
- Keep the primary toolbar compact and scannable.
- Prefer clear labels for uncommon actions; icons alone are often ambiguous on desktop.
- Do not overload the toolbar with settings that belong in the settings window.

## Settings windows

- Use a dedicated settings scene or settings window for durable preferences.
- Keep settings separate from per-document or per-window state.
- Group settings by user goal, not internal subsystem names.

## Drag and drop

- Add drag and drop when it materially reduces friction for file-based or rearrangement workflows.
- Make valid drop targets obvious.
- Provide a non-drag path for the same action.
- Confirm import, move, or destructive consequences when the result is not obvious.

## Multi-window behavior

- Decide explicitly whether the app supports one window, many windows, or document windows.
- Keep per-window state isolated.
- Keep shared data and preferences in services or shared stores.
- Support restore or reopen behavior only when the product benefits from it.

## Interaction language

- Use macOS-native naming over web or mobile metaphors.
- Prefer settings over preferences only if the surrounding app already uses that language consistently.
- Use sheet, panel, inspector, and sidebar precisely when those patterns actually match the UI.
