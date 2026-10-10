# Oppia Research Compass

Oppia Research Compass is a public read-only runtime for searching and reusing
an independently authorized Oppia historical UX research corpus. The bundled
starter contains no research records or participant data. Oppia evidence is the primary product surface;
research planning, evidence-quality checks, and research-method skills are
supporting capabilities.

This edition is separate from the general Research Compass. It does not include
the AI Glossary, the general Pattern Knowledge Base, personal Research Notes,
or any external-source runtime.

## Run From This Public Source Edition

Use a reviewed Python 3.10 or newer interpreter; Python 3.12 and MCP SDK 1.26.0
were used for the actual release-archive stdio check. From this runtime folder,
create a recipient-local environment using your selected interpreter:

```bash
python3.12 -m venv .runtime/venv
.runtime/venv/bin/python -m pip install 'mcp>=1.12,<2'
.runtime/venv/bin/python server.py --healthcheck
.runtime/venv/bin/python server.py
```

Use another supported interpreter for the first command if `python3.12` is not
available. The server defaults to the packaged `data/oppia_research.sqlite`, an
empty database created from the original schema. An overview or research query
therefore returns zero evidence. It does not show that research never occurred.
For “what have we learned about learner onboarding?”, call `oppia_research`
first, report the evidence gap, and use `plan_oppia_research` for one bounded
follow-up. No web or Drive lookup runs automatically.

For your own authorized schema-compatible database, keep it outside this
installed package and select its absolute path explicitly:

```bash
OPPIA_RESEARCH_DB_PATH="<absolute path to your authorized compatible corpus.sqlite>" \
  .runtime/venv/bin/python server.py
```

The CLI also accepts `--db-path` and `--healthcheck`; inspect `server.py --help`.
A missing selected database exits with `Oppia research database not found`,
rather than silently creating a file or substituting empty evidence. Check the
selected path and schema, or remove the override to use the empty starter.
The runtime opens SQLite read-only and does not import, rebuild or edit a corpus.

For a recipient-owned MCP client, use the selected environment's Python as the
command, this folder's absolute `server.py` path as an argument, and optionally
`OPPIA_RESEARCH_DB_PATH` as environment configuration. The preserved MCPB
`mcpb_launcher.py` is an alternative entry; it uses the same empty default and
honors the same override. Installing the plugin methods alone does not launch
this server. The runtime provides ten tools and no resource items/templates.

## Public Distribution And Private Corpus Boundary

See [the package README](../../README.md) for methods, licensing, installation
and updates. This released package supplies the complete runtime and the
schema-compatible empty starter. It does not bundle a sanitized team corpus,
private export or source-repository release builder. No absent internal builder
or personal database path is needed to run it.

Synthetic fixtures can verify search, evidence retrieval and audit behavior;
they establish no real Oppia findings. Recipient-supplied research remains
subject to its original consent, access and redistribution restrictions. Do
not publish a real corpus merely to repair setup. Retain external recipient
data when updating or removing this source package.

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
