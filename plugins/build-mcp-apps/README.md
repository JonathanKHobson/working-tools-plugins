# Build MCP Apps

Current edition **1.0.5** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Build or improve interactive MCP apps and their servers, from a clear user task through protocol and host verification.

## What you can do

- Create a widget that lets someone select, compare or edit real information.
- Repair state, retries, host messaging and tool contracts in an existing MCP app.
- Use Alpic deployment workflows when the project actually uses Alpic.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “Improve this MCP picker so the selection reaches the conversation.” | Existing app source and target host. | A bounded implementation with separate local and real-host verification. |
| “Help me get started with Build MCP Apps.” | The task people need to perform and any existing project. | A suitable implementation route and the smallest first working interaction. |

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [build-mcp-apps](skills/build-mcp-apps/SKILL.md) | Create an MCP widget or build/update MCP servers and MCP Apps with an end-to-end, capability-aware workflow. |
| [use-alpic](skills/use-alpic/SKILL.md) | Use Alpic Cloud and Skybridge deployment workflows for projects that actually use the Alpic provider. |

## Tools, setup and access

No MCP server is declared by this plugin. The servers you build are separate project outputs. For Alpic account/deployment work, select [Use Alpic](skills/use-alpic/SKILL.md) and verify the actual provider and environment.

This is a development method package. It does not install a server, create an Alpic account, supply credentials or prove that a host supports every widget feature.

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintenance

Edit the public source in this package. See [project map](docs/project-map.md). Validate changed skills, references and retained snapshot hashes before releasing a separately versioned update. Installed caches are generated copies.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public edition, prerequisites and missing providers

The public edition retains all 2 top-level skill heads and every source file. Original first-party text has an explicit grant; unchanged third-party snapshots retain their own grants and notices. No restricted source methods are omitted. See [source attribution](SOURCE-ATTRIBUTIONS.md), [third-party notices](THIRD_PARTY_NOTICES.md) and [exact provenance](PROVENANCE.json).

Reading and applying the methods needs supplied task/context and permission for the selected project. Helpers need the language/runtime declared in their source; Python helpers require Python 3.10+ and Node helpers require a compatible Node environment. Generated projects install their own pinned SDK/dependencies after review. Alpic deployment requires the separately available current Alpic tooling, an authorized account/project and deployment target. Widget acceptance requires a current supported MCP App host and its actual browser/bridge behavior. Native/mobile workflows require separately installed providers and their SDK/device tools. Source inclusion supplies no credentials or host connection.

Example task: “Repair my picker so selection reaches the conversation.” If the host bridge/provider is missing, inspect supplied source, preserve selection state and design/test its local event contract with synthetic inputs. Then report: “The local state/event checks passed; the current host bridge is unavailable, so conversation delivery is unverified.” Identify the missing supported provider and actual-host check. Do not deploy, reconfigure every MCP or claim live delivery from a synthetic test. This is an authored expected response, not a recorded provider run.
