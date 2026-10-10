# Workshop Facilitation Toolkit

Current edition **0.1.3** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Help a group reach a concrete result through an agenda, activity choice, live facilitation, evidence capture, decision, debrief or rehearsal.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Design a 60-minute discovery workshop for eight colleagues.” | Group, time and intended output | Timed facilitator run sheet and contingencies |
| “Help me respond to this conflict in the room.” | Immediate situation and available time | Speakable next move and fallback |
| “Synthesize these board photos without inventing consensus.” | Authorized photos/notes | Traceable themes, dissent and gaps |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/workshop-design/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Use a specialist directly for activity choice, live help, dialogue, decisions, synthesis, debrief or rehearsal. Workshop-design owns full agendas.

| Task / skill | What it produces |
| --- | --- |
| [facilitator-rehearsal](skills/facilitator-rehearsal/SKILL.md) | Rehearse a workshop opening, explanation, transition, or difficult facilitation moment with bounded simulated participants and observable feedback. |
| [inclusive-group-dialogue](skills/inclusive-group-dialogue/SKILL.md) | Design or repair a group conversation with balanced participation, clear norms, access options, and honest handling of power and disagreement. |
| [live-workshop-facilitation](skills/live-workshop-facilitation/SKILL.md) | Give immediate, speakable help during a live workshop for time, participation, confusion, conflict, energy, and transitions. |
| [workshop-activity-selection](skills/workshop-activity-selection/SKILL.md) | Choose and adapt a small set of purposeful workshop activities using File-O-Fun, group constraints, access needs, and the output required by the next step. |
| [workshop-debrief-transfer](skills/workshop-debrief-transfer/SKILL.md) | Create a workshop debrief, reflection, action capture and follow-through plan; route applicable post-session operational closeout while preserving evidence and authorization. |
| [workshop-decision-making](skills/workshop-decision-making/SKILL.md) | Guide a group from options to an explicit, reviewable decision using agreed criteria, evidence, authority, and documented dissent. |
| [workshop-design](skills/workshop-design/SKILL.md) | Create a complete workshop agenda and facilitator run sheet for a defined group outcome, including timing, participation, materials, and contingencies. |
| [workshop-evidence-synthesis](skills/workshop-evidence-synthesis/SKILL.md) | Transcribe and synthesize workshop notes, photos, boards, or recordings with traceable source IDs, faithful wording, recurrence, and separate interpretation. |

## Availability and recovery

Text workflows use supplied context. This package includes an optional fixed-domain [Atlas launcher](scripts/atlas_library_mcp.py), but does not register an Atlas MCP server or bundle a corpus, server, database or host binding. A recipient can supply a compatible private binding and explicitly register the launcher; the existing local binding remains untouched. Alternatively, use a separately installed, user-configured Activities Templates/Atlas source. See [selection rules and limits](references/atlas-library.md) and verify the actual current tool before a read. If unavailable, the complete bundled methods remain usable and the source-lookup limit is explicit.

See the [project map](docs/project-map.md) and [verification record](docs/verification.md) for methods, provenance and checks. A schedule checker validates timing, not group participation or a live decision.

## Evidence and examples

- [Facilitation evidence](skills/workshop-design/references/facilitation-evidence.md)
- [Personal facilitation evidence](skills/workshop-design/references/personal-grounding.md)
- [File-O-Fun method library](skills/workshop-activity-selection/references/method-library.md)
- [60-minute agenda example](skills/workshop-design/assets/agenda-example.json)
- [Project map](docs/project-map.md)
- [Verification](docs/verification.md)

This public method edition excludes private source locators, transcripts, emails, learner data and full course media. Original workflow and proposed adaptation text remain complete; underlying unknown-rights source summaries and assets are excluded. Attribution does not imply certification, endorsement or a new license for external original content.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public installation and prerequisites

Install this separately versioned package through the [Working Tools repository](https://github.com/JonathanKHobson/working-tools-plugins). Configure the `working-tools` marketplace with the current host's supported flow; in Codex use `codex plugin add workshop-facilitator@working-tools`, then start a fresh task to verify discovery. Use the host's supported removal command to uninstall. Your project, learner and workshop files are separate from the package.

Bring the audience/group, intended observable result, time and approved source material. Text workflows need no account, private Atlas corpus or network service. Original read-only JSON helpers use Python 3.10 or later and the standard library. Visual production needs a separately available document/slide/web or design provider and actual rendered QA. Optional live boards/LMS/media export need your own accounts, permissions and demonstrated provider route. No participant data, credentials, running MCP service, background job, tracking or native Atlas registration is included.

Example when a provider is missing: "I can prepare the complete lesson/workshop plan from the supplied material. This host currently has no authorized board/LMS editing route, so publishing, participant-role tests and rendered interaction remain unverified. I will provide the run sheet, materials and acceptance checks for the receiving environment." This is an authored expected boundary, not a recorded live execution.

Original scripts in this edition are AGPL-3.0-only. Prose, roles and original teaching/adaptation material are CC BY-SA 4.0 with retained source attribution. Read LICENSE and SOURCE-ATTRIBUTIONS.md. Historical package checks and source observations do not prove learning, a live workshop, public LMS launch, native installation or provider availability. Current static/helper checks are summarized in docs/release-validation.md.
