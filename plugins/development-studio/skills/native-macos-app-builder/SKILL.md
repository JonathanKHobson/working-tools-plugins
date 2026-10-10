---
name: native-macos-app-builder
description: Build, modify, debug, and ship native macOS applications in Xcode using Swift, SwiftUI, and AppKit. Use when Codex needs to create or update a real native Mac app project; scaffold Xcode projects; implement app architecture, views, menus, settings, window management, file handling, persistence, or app lifecycle behavior; bridge SwiftUI with AppKit; fix Xcode build errors; configure targets, schemes, entitlements, sandboxing, signing, notarization, and distribution; or convert rough product ideas into implementation-ready native macOS app plans and code. Prefer native macOS implementation over cross-platform wrappers. Do not default to Catalyst, Electron, React Native, Flutter, or web tech unless the user explicitly asks for them.
---

# Native macOS App Builder

Build production-minded native macOS apps using Xcode, Swift, SwiftUI, and AppKit. Assume the goal is a true macOS-native experience unless the user explicitly asks for a cross-platform path.

## Operating Stance

- Prefer Swift as the default language.
- Prefer SwiftUI for new UI work unless AppKit is clearly better for the requested behavior.
- Use AppKit directly or through a narrow bridge when deeper macOS control is required.
- Preserve macOS conventions: menu commands, keyboard shortcuts, settings windows, file dialogs, multi-window behavior, drag and drop, and native terminology.
- Separate UI, state, services, persistence, and platform integrations.
- Treat entitlements, sandboxing, signing, and distribution as architecture concerns, not cleanup work.
- When requirements are incomplete, make reasonable native-macOS-first assumptions and state them briefly.

## Receiving-host requirements

This is the full original local macOS builder method and its support. Xcode, Swift SDKs, signing identities, Figma/other MCPs and optional companion skills are receiving-host capabilities, not bundled providers. Verify the capability before use; if absent, preserve the task and report the unverified compile/runtime/signing gate. Historical companion skill names below are optional and may resolve through the current receiving-host catalog.

## Coordination and MCP Awareness

- Start with this skill for native macOS app planning, implementation, debugging, and packaging.
- Use `$pattern-picker` when the user is blocked on framing or choosing the right thinking model before app planning.
- Use `$work-management:product-definition` when the native app concept needs a feature plan, requirement pack, phased roadmap, or engineering terminology before implementation.
- Use `$mac-ops-toolkit:mac-environment-conventions` when storage placement, runtime location, or external-drive rules affect the app architecture.
- Use `$mac-ops-toolkit:mac-troubleshooter` when the issue is a running app/process/window symptom rather than code architecture.
- Use the `figma` MCP when implementation depends on a concrete Figma node or design-system context.
- Use `knowledge_atlas` when frameworks, glossary concepts, or related patterns would sharpen app planning.

## Workflow

### 1. Classify the app shape

Start by identifying the likely app type:

- single-window utility
- multi-window productivity app
- document-based app
- menu bar app
- settings-heavy desktop tool
- cloud-backed client
- local-first app
- App Store-targeted app
- direct-download notarized app

Use the app shape to drive architecture, scene setup, persistence, window behavior, and distribution choices.

### 2. Choose the UI stack

Use this decision rule:

- Use `SwiftUI-first` for most new apps.
- Use `AppKit` when the work needs advanced macOS behavior such as custom `NSWindow` control, detailed responder-chain handling, advanced table or outline behavior, custom toolbar management, or APIs not exposed well through SwiftUI.
- Use `SwiftUI + AppKit bridge` when most UI can stay declarative but a few controls need AppKit.
- Use `Mac Catalyst` only when the user explicitly wants iPad code reuse or already has an iOS or iPadOS codebase to bring to macOS.

### 3. Structure the project

- Organize code into folders such as `App`, `Views`, `State` or `ViewModels`, `Models`, `Services`, `Persistence`, `Utilities`, and `Resources`.
- Keep startup code thin.
- Keep business logic out of views.
- Prefer Swift Package Manager for dependencies when practical.
- Add tests when behavior is non-trivial or regression-prone.

### 4. Implement macOS-native behavior

- Use menu commands instead of burying every action inside buttons.
- Add keyboard shortcuts for common actions.
- Use Settings scenes or native settings windows.
- Use file importer or exporter panels for document workflows.
- Support drag and drop when it materially improves desktop usability.
- Use toolbar items for actions that are global to a window.
- Respect native selection, empty-state, focus, and multi-window patterns.
- Keep menu bar apps lightweight and predictable.

### 5. Bridge SwiftUI and AppKit carefully

- Use `NSViewRepresentable` or `NSViewControllerRepresentable` for AppKit-backed controls inside SwiftUI.
- Use coordinators or delegates only where advanced control is required.
- Keep the bridge narrow instead of mixing frameworks broadly.
- If SwiftUI is the problem, isolate the specific limitation and move only that piece into AppKit.

### 6. Handle files and sandboxing deliberately

- Treat file access as a first-class design constraint.
- Prefer user-initiated file selection flows when possible.
- Persist security-scoped access only when the app needs it.
- Do not assume unrestricted filesystem access.
- Favor sandbox-compatible approaches for Mac App Store targets.
- Call out the tradeoffs if direct distribution requires broader access patterns.

### 7. Debug from the failing layer

When fixing an existing app:

1. Identify the failing layer: compile, link, signing, runtime, preview, sandbox, or notarization.
2. Isolate the smallest likely root cause.
3. Fix the root cause before polishing adjacent code.
4. Preserve the user’s intended architecture unless it is the source of the problem.
5. Check common macOS project fault lines:
   - target membership
   - bundle identifiers
   - `Info.plist`
   - entitlements
   - signing settings
   - deployment targets
   - package resolution
   - scene and window configuration
   - concurrency on UI code
   - AppKit lifecycle mismatches

### 8. Plan packaging and distribution early

Ask which delivery target applies:

- local development only
- internal use
- direct download
- Mac App Store

Configure the implementation and release path accordingly:

- app sandbox
- entitlements
- hardened runtime
- Developer ID signing
- notarization
- archive and export flow

## Output Expectations

Depending on the request, produce one or more of:

- Xcode project structure
- Swift, SwiftUI, or AppKit source files
- implementation plan broken into phases
- architecture blueprint
- repair patch for an existing app
- checklist for signing, packaging, or notarization
- feature spec translated from plain language into implementation-ready tasks
- migration plan from a rough concept or non-native approach to a native macOS app

## Reference Files

Load only what the task needs:

- `references/architecture.md`
  - app structure patterns, persistence choices, and app-shape guidance
- `references/ui-patterns.md`
  - SwiftUI vs AppKit selection, native interaction patterns, menus, toolbars, settings, drag and drop, and multi-window behavior
- `references/packaging-signing.md`
  - bundle IDs, targets, entitlements, sandboxing, signing, hardened runtime, notarization, and release workflows
- `references/troubleshooting.md`
  - failure triage for Xcode, SwiftUI, AppKit, signing, previews, runtime issues, and bridge problems

## Defaults

- Default language: `Swift`
- Default UI approach: `SwiftUI-first`
- Default bridge policy: use AppKit only where macOS-native control requires it
- Default distribution assumption: local development until the user states App Store or direct-download requirements
- Default output style: concrete, macOS-native, concise, and implementation-oriented

## Project organization guardrail

Before creating or expanding macOS app project files, consult the `work-management:project-structure` skill. Do not build expandable Swift, SwiftUI, AppKit, or SwiftPM projects as monolithic single-file implementations unless the user explicitly requests a one-off proof of concept.

Keep app entry points thin and separate scenes/views, models, services, commands, resources, configuration, tests, and docs according to Apple platform and repository conventions.
