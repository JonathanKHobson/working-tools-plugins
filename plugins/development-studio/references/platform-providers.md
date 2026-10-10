# Platform methods and execution providers

Discover the named installed plugin first and resolve `skills/<directory>/SKILL.md` below from that provider root. Read the complete selected procedure and its required support. Direct namespace invocations use the actual frontmatter name, which can differ from the directory. The file routes here avoid that ambiguity. Do not hardcode versioned cache paths, create copied provider metadata or reconfigure connections just to make a route appear installed.

The reviewed manifest versions are recorded in [provider inventory](../docs/provider-inventory.json). That is source evidence from the inspected version, not a promise about current service status. No provider files were copied or modified.

| Official provider | Full method directories and selection | Execution prerequisite |
| --- | --- | --- |
| Build Web Apps | `frontend-app-builder` for new UI/redesign; `frontend-testing-debugging` for rendered defects and QA; `react-best-practices` for React/Next; `shadcn-best-practices` for shadcn components; `supabase-best-practices` for Postgres; `stripe-best-practices` for payments | Existing app runtime and dependencies; current host browser for rendered QA; provider accounts only when the chosen integration needs them |
| Build iOS Apps | `swiftui-ui-patterns`, `swiftui-view-refactor`, `swiftui-liquid-glass`; `ios-app-intents` for system actions; `ios-debugger-agent` for Simulator; `ios-simulator-browser` for mirroring; `swiftui-performance-audit`, `ios-ettrace-performance`, `ios-memgraph-leaks` for evidence | macOS/Xcode, selected simulator/device and supported deployment target; retained XcodeBuildMCP where used; trace tools only for the matched method |
| Build macOS Apps | `build-run-debug`, `swiftpm-macos`, `swiftui-patterns`, `view-refactor`, `window-management`, `appkit-interop`, `telemetry`, `test-triage`, `liquid-glass`, `signing-entitlements`, `packaging-notarization` | macOS/Xcode or Swift toolchain appropriate to project; signing/notarization credentials only for distribution |
| Test Android Apps | `android-emulator-qa` for UI reproduction; `android-performance` for CPU/frame/memory evidence | Android SDK, adb, booted authorized device/emulator and matching app variant; profiling permissions where required |
| Plugin Eval | `plugin-eval` for routing; `evaluate-plugin`, `evaluate-skill`; `improve-skill` for reviewed changes; `metric-pack-designer` for a custom rubric | Its separately available runtime/CLI and compatible Node environment; model benchmark harness only when real trials are requested and supported |
| Game Studio | All nine source methods are inventoried for the separate Game Creation Studio: `game-studio`, `web-game-foundations`, `phaser-2d-game`, `three-webgl-game`, `react-three-fiber-game`, `sprite-pipeline`, `web-3d-asset-pipeline`, `game-ui-frontend`, `game-playtest` | Retain official package. Games route out of this studio; browser/engine/assets remain external execution prerequisites |

The Build iOS Apps manifest owns an XcodeBuildMCP declaration using an unpinned `npx` runner in the inspected version. This package does not copy it, change it or start another server. Inspect the current runtime/version before a task needs it and use the existing native provider connection.

## When a dependency is missing

State the missing method/tool/device/account precisely. Finish useful source work and local tests that do not need it. Do not claim compatibility, deployment or benchmark success from an installation record. A provider installation, authentication, selected project authorization and successful operation are separate states.

Personal neighboring owners are optional: Work Management for project structure and product definition, UX Design Studio for design review, Master Security Toolkit for source admission, and Data Visualization Toolkit for chart correctness. If unavailable, apply the task’s explicit quality requirements and report the absent specialized review; do not fabricate a tool call.
