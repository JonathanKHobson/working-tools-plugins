# Development Studio

Development Studio turns a software request into a scoped, implemented and verified change. It includes complete development methods and MCP app procedures, and selects the official platform provider when specialist tools are needed. Game design and production belong to the separate Game Creation Studio.

Try “Implement and verify this feature,” “Find the cause of this regression,” or “Build a local data MCP with a usable widget.” Bring the repository or source, expected behavior and any target platform. The result is a reviewable change with evidence and explicit remaining runtime gates.

## Choose a workflow

| Need | Entry |
| --- | --- |
| Scope a software change or get help | [Development Studio](skills/development-studio/SKILL.md) |
| Implement a feature or accepted plan | [Implement software](skills/implement-software/SKILL.md) |
| Diagnose a failure | [Debug software](skills/debug-software/SKILL.md) |
| Regression tests and evidence | [Test software](skills/test-software/SKILL.md) |
| Review feedback and delivery | [Review and release](skills/review-and-release/SKILL.md) |
| Web app implementation and rendered QA | [Build web software](skills/build-web-software/SKILL.md) |
| Apple apps and Android QA | [Build native software](skills/build-native-software/SKILL.md) |
| MCP app/widget implementation | [Build MCP apps](skills/build-mcp-apps/SKILL.md) |
| Local data MCP and attachment diagnosis | [Local MCP systems](skills/local-mcp-systems/SKILL.md) |
| Alpic project operations | [Use Alpic](skills/use-alpic/SKILL.md) |
| Evaluate methods or a scoped session | [Evaluate development workflows](skills/evaluate-dev-workflows/SKILL.md) |

## Setup and execution dependencies

This is a method package. It declares no MCP server, hooks, background job, external account or bundled SDK. Source preparation does not mean it is installed. Install/update through the native plugin manager, then verify fresh skill discovery and source/cache parity.

- Keep official Build Web Apps, Build iOS Apps, Build macOS Apps, Test Android Apps and Plugin Eval as separate providers. Their complete methods and supporting assets remain at their installed roots. The [provider map](references/platform-providers.md) explains exact selection and prerequisites.
- Xcode, simulator runtimes, Android SDK/emulator/adb, browser tooling, package dependencies, signing credentials and deployment services must be available for the task that needs them. Verify discovery, authentication and a harmless read separately. Do not install a duplicate XcodeBuildMCP connection.
- Alpic operations require the actual Alpic/Skybridge project and separately installed/authenticated CLI or service. A non-Alpic MCP app stays on its existing framework.
- Resolve skill/provider roots from the current host’s discovery/catalog. Private machine paths, credentials, workspace lists and theme preferences stay in host configuration or the owning project, not this distribution. [Private profile example](docs/host-profile.example.json) documents optional values without loading them automatically.

This public edition retains all 11 discoverable heads, 15 Superpowers methods, two Alpic methods and two first-party local-MCP methods with their full support. The [rights record](LICENSE.md) gives original MIT/Apache grants and unchanged upstream notices. No source methods are omitted; execution providers and unmigrated legacy sources remain external.

## Maintenance

The full Superpowers 6.4.2 snapshot and Alpic 1.0.1 method closure are preserved, not replaced with summaries. Focused skills require the applicable full methods. Read [method adaptation](references/method-adaptation.md) for host precedence, tool substitutions and optional helper boundaries. Existing Build MCP Apps procedures/support are carried forward with recorded portability changes.

Use the [project map](docs/project-map.md), [provenance](docs/provenance.md), [source dispositions](docs/legacy-disposition.md), [admission review](docs/admission.md) and [handoff](docs/install-handoff.md). Run `python3 scripts/validate_package.py` from the package root. Static integrity checks do not prove actual-host usability or functional parity.

## Public edition, prerequisites and missing providers

Version 0.1.1 retains all 11 top-level skill heads and every source file. Original first-party text has an explicit grant; unchanged third-party snapshots retain their own grants and notices. No restricted source methods are omitted. See [source attribution](SOURCE-ATTRIBUTIONS.md), [third-party notices](THIRD_PARTY_NOTICES.md) and [exact provenance](PROVENANCE.json).

Reading and applying the methods needs supplied task/context and permission for the selected project. Helpers need the language/runtime declared in their source; Python helpers require Python 3.10+ and Node helpers require a compatible Node environment. Generated projects install their own pinned SDK/dependencies after review. Alpic deployment requires the separately available current Alpic tooling, an authorized account/project and deployment target. Widget acceptance requires a current supported MCP App host and its actual browser/bridge behavior. Native/mobile workflows require separately installed providers and their SDK/device tools. Source inclusion supplies no credentials or host connection.

Example task: “Repair my picker so selection reaches the conversation.” If the host bridge/provider is missing, inspect supplied source, preserve selection state and design/test its local event contract with synthetic inputs. Then report: “The local state/event checks passed; the current host bridge is unavailable, so conversation delivery is unverified.” Identify the missing supported provider and actual-host check. Do not deploy, reconfigure every MCP or claim live delivery from a synthetic test. This is an authored expected response, not a recorded provider run.
