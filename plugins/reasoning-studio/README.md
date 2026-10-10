# Reasoning Toolkit

Pressure-test a claim, clarify an assumption in dialogue, or compare credible explanations so the next decision rests on stronger reasoning.

## What you can do

- Check a claim against its strongest credible alternative.
- Work through a consequential assumption one question at a time.
- Audit supplied reasoning with Critical Compass and preserve evidence, uncertainty and dissent.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “Stress-test this claim and tell me what evidence would change it.” | The claim, its context and available evidence. | A calibrated conclusion, strongest objection and discriminating next check. |
| “Help me think through this assumption, one question at a time.” | The assumption and decision it affects. | Focused dialogue, not a simulated participant study. |

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [alternative-perspectives](skills/alternative-perspectives/SKILL.md) | Compare credible explanations or viewpoints for a claim or decision and preserve consequential disagreement without false balance or simulated evidence. |
| [critical-reasoning](skills/critical-reasoning/SKILL.md) | Stress-test a claim, argument, plan or method in any domain; use Critical Compass for bounded content and paper audits and scoped Atlas reasoning lenses. |
| [socratic-questioning](skills/socratic-questioning/SKILL.md) | Help a user examine an assumption or clarify a decision through focused Socratic dialogue, one consequential question at a time. |

## Tools, setup and access

`critical-compass` provides claim/text audit tools; `atlas-reasoning` retrieves reasoning lenses. Read the [Compass contract](docs/critical-compass-integration.md) before tool use. `claim_stress_test` handles a bounded claim, `quick_scan` supplied text, and `audit_text` a guided audit; honor pauses and consent. For selected lenses read [Atlas guidance](references/atlas-library.md). Bindings live in `an operator-selected Compass JSON binding` and `atlas-library.json`. A missing binding or mount calls for setup repair, not backend installation.

Reasoning frameworks and model agreement do not supply independent evidence. Advanced panels are an explicit mode, and human-loop questions require real user answers.

Installation makes a package available; it does not establish a working server or permission for every action. These private bindings are host-specific; another host needs its own supported configuration. On the receiving host, inspect the selected provider configuration and required runtime/data files. This public package installs no automatic MCP registration. Verify tool discovery and one harmless scoped read/overview. Keep credentials in the provider’s supported setup, never in a chat or this README. Report missing configuration, unreachable service, insufficient permission and an empty search as different conditions. Preserve the original task through setup; verify uncertain writes before retrying. Any historical verification notes are dated evidence, not current readiness.

For requested visual reasoning, [the shared drawing route](references/draw-think.md) uses Creative Studio’s Draw and Think connection and saved board IDs. It is a conditional neighboring capability, not a second server bundled here. Verify that owner and tools are available; drawing alone does not start a formal audit.

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintainer and existing integration notes

Pressure-test claims, examine assumptions in dialogue and compare credible alternatives. Three focused skills reuse the existing Critical Compass runtime and scoped Knowledge Atlas, preserving consent, evidence provenance and dissent. See [project map](docs/project-map.md).

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public edition and prerequisites

Version 0.1.3 retains all 3 top-level method heads. Four nonoperative icon/automatic-registration files excluded; no operative methods omitted. See [source attributions](SOURCE-ATTRIBUTIONS.md), [license](LICENSE), [notices](THIRD_PARTY_NOTICES.md) and [provenance](PROVENANCE.json). No account, provider, data corpus or live connection is installed by this package.

Methods work from a supplied claim/evidence and the current user's actual answers. Formal tools require separately available Critical Compass; lenses require an authorized Atlas source; drawing/review require their separate providers. Optional helper actions need Python 3.10+, the MCP SDK for the full client, a reviewed existing provider environment, and an explicit `--binding` JSON. Binding shapes are `{"critical-compass":{"interpreter":"/path/to/python","server":"/path/to/server.py","args":[],"env":{}}}` for Compass, `{"interpreter":"/path/to/python","server":"/path/to/server.py","database":"/path/to/database"}` for fixed reasoning Atlas, and `{"interpreter":"/path/to/python","server":"/path/to/server.py","data_dir":"/path/to/data"}` for Critical Review. Real binding files remain recipient-controlled outside this package; credentials use provider setup.

Example: “Stress-test the claim that shorter onboarding will improve retention.” If Compass is absent, inspect the supplied evidence and perform a labeled internal reasoning check, identify alternative explanations and the discriminating next observation. Report the absent Compass audit; do not invent scores, human answers or independent reviewers. For an advanced audit, preserve its actual approval/pause/report gates. This is an authored expected behavior scenario, not a recorded live provider run.
