---
name: build-native-software
description: "Build or debug iOS/macOS software, or reproduce and profile Android emulator behavior through the official platform methods."
---

# Build native software

For native macOS architecture and implementation, read the full [Native macOS App Builder](../native-macos-app-builder/SKILL.md) and the relevant included architecture, UI, packaging or troubleshooting reference. Official providers remain necessary for actual execution.

Use [platform providers](../../references/platform-providers.md) to select and read the complete matching official method. This package does not supply Xcode, signing identities, Android SDKs, simulators or XcodeBuildMCP.

1. Resolve the repository, target OS/version, build system, scheme/variant, device and current failure or desired behavior. Inspect the existing architecture before adding a new app shell.
2. For iOS choose SwiftUI UI/refactor, App Intents, Liquid Glass, simulator debugging, browser mirror, ETTrace, performance audit or memgraph analysis by the actual task. Discover the retained XcodeBuildMCP provider before using its tools.
3. For macOS choose build-run-debug or SwiftPM, desktop SwiftUI, view refactor, window management, AppKit interop, telemetry, test triage, signing or packaging/notarization. Keep AppKit bridges narrow and preserve existing entitlements.
4. For Android choose android-emulator-qa for reproduction and android-performance for measured profiling. Record the exact target and app variant before installing or collecting logs. Test Android Apps is not an Android code generator or a provisioned emulator.
5. Implement the requested change and collect appropriate evidence: compile/test output, runtime reproduction, rendered states, traces or signing checks. Compare equivalent scenarios when claiming performance improvement.
6. Report built, launched, simulator-verified, device-verified, signed and distributed separately. Clean up only task-owned helpers. Missing devices, credentials or provider discovery are explicit gates; a mocked result cannot close them.

For changed screens map and recheck 3–8 rendered anchors and affected accessibility states. Reuse existing authorization for requested actions; do not repeat approvals merely because a historical method uses a confirmation sentence.
