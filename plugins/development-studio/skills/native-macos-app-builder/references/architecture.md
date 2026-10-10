# Architecture

## Folder structure

Use a clear, shallow layout:

- `App`: entry point, scenes, commands, app delegates
- `Views`: SwiftUI views and small view-specific helpers
- `State` or `ViewModels`: presentation state and interaction logic
- `Models`: domain types and shared data structures
- `Services`: file I/O, networking, sync, parsing, export, system integrations
- `Persistence`: `UserDefaults`, file stores, SwiftData, Core Data, SQLite adapters
- `Utilities`: cross-cutting helpers
- `Resources`: bundled assets, templates, plist-backed data

Keep app startup minimal. Do not hide service wiring in views.

## State patterns

Default to the simplest pattern that keeps the app testable:

- Use lightweight observable state for small utilities and single-window tools.
- Use MVVM when screens have meaningful presentation logic, async orchestration, or reusable state transitions.
- Use coordinator-style objects only when multiple windows, navigation flows, or platform integrations need centralized control.

Do not create extra abstraction layers unless the app shape requires them.

## Persistence choices

Choose storage based on data complexity, not framework fashion:

- `UserDefaults`: preferences, toggles, recent values, lightweight UI state
- file-based JSON or plist: local-first documents, small structured datasets, import/export-friendly storage
- `SwiftData`: modern native persistence for structured app data when the app benefits from model-driven queries
- `Core Data`: existing codebases, mature relational persistence, or heavier query history
- `SQLite`: explicit schema control, sync engines, larger datasets, or cross-process compatibility

If the user does not specify persistence, choose the lightest option that supports the feature set.

## App-shape patterns

### Single-window utility

- Keep one main scene.
- Prefer lightweight state and simple persistence.
- Use toolbar and menu commands for frequent actions.

### Multi-window productivity app

- Separate shared services from per-window state.
- Use dedicated models for window identity and restoration.
- Keep global settings distinct from document or window state.

### Document-based app

- Treat open, save, autosave, import, export, and conflict behavior as first-class.
- Decide early whether to use built-in document APIs or a custom file workflow.
- Keep document data separate from app preferences.

### Menu bar app

- Minimize launch overhead.
- Decide whether the app also needs a settings window or a companion main window.
- Avoid heavy, hidden background behavior unless the user explicitly needs it.

### Local-first app

- Keep storage and import/export flows explicit.
- Design for offline usability and data durability.
- Add cloud sync only when the product requirement is clear.

### Cloud-backed client

- Separate transport, auth, cache, and UI state.
- Keep offline behavior explicit even if it is degraded.
- Avoid tying every view directly to network calls.

## Architecture defaults

- Put business logic in services or state objects, not views.
- Make file access, permissions, and distribution constraints visible in the design.
- Favor narrow interfaces and simple data flow over large protocol hierarchies.
- Add tests for state transitions, persistence, and data conversion logic when they are non-trivial.
