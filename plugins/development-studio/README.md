# Development Studio

Current edition **0.2.2** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

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
| Native macOS architecture and implementation | [Native macOS App Builder](skills/native-macos-app-builder/SKILL.md) |
| Code navigation and refactors | [Code Intelligence](skills/code-intelligence/SKILL.md) |
| Go source-backed review and query engine | [Golang Effective](skills/golang-effective/SKILL.md) |
| GitHub CI and review comments | [Fix CI](skills/gh-fix-ci/SKILL.md), [Address Comments](skills/gh-address-comments/SKILL.md) |
| Local Docker/PocketBase/Quick Tunnel workflow | [Local App Pipeline](skills/local-app-pipeline/SKILL.md) |
| ChatGPT Apps SDK | [ChatGPT Apps](skills/chatgpt-apps/SKILL.md) |
| Web-game implementation loop | [Develop Web Game](skills/develop-web-game/SKILL.md) |
| Installation review and local diagnosis | [Safe Install Review](skills/safe-install-review/SKILL.md), [Systematic Debugging](skills/systematic-debugging/SKILL.md) |
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

This public edition retains all 21 discoverable heads, 15 Superpowers methods, two Alpic methods and two first-party local-MCP methods with their full support. The [rights record](LICENSE.md) gives original MIT/Apache grants and unchanged upstream notices. No source methods are omitted; execution providers and unmigrated legacy sources remain external.

## Maintenance

The full Superpowers 6.4.2 snapshot and Alpic 1.0.1 method closure are preserved, not replaced with summaries. Focused skills require the applicable full methods. Read [method adaptation](references/method-adaptation.md) for host precedence, tool substitutions and optional helper boundaries. Existing Build MCP Apps procedures/support are carried forward with recorded portability changes.

Use the [project map](docs/project-map.md), [provenance](docs/provenance.md), [source dispositions](docs/legacy-disposition.md), [admission review](docs/admission.md) and [handoff](docs/install-handoff.md). Run `python3 scripts/validate_package.py` from the package root. Static integrity checks do not prove actual-host usability or functional parity.

## Public edition, prerequisites and missing providers

Version 0.2.0 retains all 21 top-level skill heads and their complete eligible procedure/support closure; private state and the uncleared Go corpus are excluded as documented below. Original first-party text has an explicit grant; unchanged third-party snapshots retain their own grants and notices. No restricted source methods are omitted. See [source attribution](SOURCE-ATTRIBUTIONS.md), [third-party notices](THIRD_PARTY_NOTICES.md) and [exact provenance](PROVENANCE.json).

Reading and applying the methods needs supplied task/context and permission for the selected project. Helpers need the language/runtime declared in their source; Python helpers require Python 3.10+ and Node helpers require a compatible Node environment. Generated projects install their own pinned SDK/dependencies after review. Alpic deployment requires the separately available current Alpic tooling, an authorized account/project and deployment target. Widget acceptance requires a current supported MCP App host and its actual browser/bridge behavior. Native/mobile workflows require separately installed providers and their SDK/device tools. Source inclusion supplies no credentials or host connection.

Example task: “Repair my picker so selection reaches the conversation.” If the host bridge/provider is missing, inspect supplied source, preserve selection state and design/test its local event contract with synthetic inputs. Then report: “The local state/event checks passed; the current host bridge is unavailable, so conversation delivery is unverified.” Identify the missing supported provider and actual-host check. Do not deploy, reconfigure every MCP or claim live delivery from a synthetic test. This is an authored expected response, not a recorded provider run.

## Version 0.2.0 standalone integration

Complete local native-macOS, Code Intelligence, ChatGPT Apps, web-game, GitHub comment/CI, systematic-debugging, safe-install, Go and local-app-pipeline methods and their support are retained. No thin replacement heads were used. Exact copied/transformed inputs are in `docs/standalone-imports.json`. Go's existing 810document chunks/populated index are excluded; supply an authorized index through `GOLANG_EFFECTIVE_INDEX`. The complete query engine opens it read-only. Docker/PocketBase/cloudflared, Go/Swift/Node/Python/toolchain dependencies, GitHub auth and provider accounts remain recipient requirements. Pipeline templates bind PocketBase to 127.0.0.1 and must be copied to an authorized external workspace; installation starts no containers or tunnels.

## Starter app first-run behavior

The Apps SDK fallback scaffold now has bounded host requests, capability-aware controls, actionable error and empty states, and a copy-ready request for standalone or unsupported hosts. Message acknowledgement is reported separately from verified chat delivery or a model response. The local server binds to 127.0.0.1 by default; set `HOST` deliberately when configuring an authorized deployment.

Validate the generated project with `npm install` and `npm run check`. The bridge regression check is `node tests/test_starter_bridge.mjs` from this package. It uses a simulated host. Real local HTTP protocol and browser checks support the public sample; they do not establish native ChatGPT acceptance.
