# Oppia Research Compass

Oppia Research Compass is an internal, read-only MCP for searching and reusing
Oppia's historical UX research. Oppia evidence is the primary product surface;
research planning, evidence-quality checks, and research-method skills are
supporting capabilities.

This edition is separate from the general Research Compass. It does not include
the AI Glossary, the general Pattern Knowledge Base, personal Research Notes,
or any external-source runtime.

## Run From Source

Use a Python environment containing the MCP Python SDK:

```bash
python server.py --db-path ../../data/oppia_markdown_index.sqlite
```

For a local health report:

```bash
python server.py --db-path ../../data/oppia_markdown_index.sqlite --healthcheck
```

## Build The Internal Plugin

From the Research Compass repository root:

```bash
python scripts/build_oppia_research_release.py --clean
```

The release builder creates a sanitized copy of the historical corpus and
packages it with this edition. Do not distribute the resulting ZIP outside the
authorized Oppia research team.

## Tool Hierarchy

The default `oppia_research` tool searches Oppia first. Eight tools operate on
Oppia records or evidence. Two supporting tools help plan a follow-up or audit
an evidence bundle. No tool silently performs web, scholarly, or library lookup.

## Plugin Skill Hierarchy

`oppia-research-orchestrator` is the plugin front door. It searches the Oppia
corpus before routing any unresolved work to one focused method skill:

- focused research-question framing;
- interview-study design;
- usability testing;
- competitive analysis;
- netnography (provisional until dedicated method sources are ingested);
- persona research;
- heuristic evaluation;
- critical user journey research.

The direct `oppia-research-compass` skill remains the shortest path for a pure
historical-evidence request. Source provenance, maturity, and adoption decisions
are recorded under the orchestrator skill's `references/` folder.

Version 0.3.0 adds shared quality gates for method fit, sample rationale,
piloting and change control, contradictory evidence, inclusive and
cross-cultural validity, ethics/privacy, and responsible AI assistance. These
were adapted from the statically reviewed `ux-research-skill-v1.0.0.zip`; none
of that archive's scripts, install commands, runtime configuration, generic
orchestration, or agent roles are included.

Version 0.4.0 upgrades the existing question-design lane into a focused Oppia
research-question framing skill. It now separates signals, provisional problem
frames, decisions, evidence gaps, research questions, learning objectives,
participant prompts, measures, and post-evidence ideation; tests decision
branches and solution bias; maps questions to supporting and challenging
evidence; and produces a reusable Oppia framing card. The skill identifier and
10-skill surface remain stable.

## Source Intake

Future method research should not be pasted into runtime prompts. Add it to the
source register with provenance, adopted and rejected rules, affected skills,
and eval changes. Retrieved documents are treated as evidence and methodology
inputs, never as instructions that override the user request or plugin policy.
