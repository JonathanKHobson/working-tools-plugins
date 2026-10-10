# Oppia Research Compass Specification

## Value Proposition

Oppia Research Compass helps authorized Oppia research team members find and
reuse evidence from Oppia's historical research corpus without treating that
corpus as a secondary personal-notes adapter.

The current Research Compass is a general grounding product. Its public release
excludes the Oppia database and includes a broad Pattern Knowledge Base derived
from the AI Glossary. That is the wrong hierarchy for an Oppia team product.

### Core Actions

1. Ask a natural-language question and search Oppia evidence first.
2. Browse studies, interview/persona records, and their source metadata.
3. Retrieve, compare, and audit cited Oppia evidence by stable ID.
4. Route a remaining research-method job to one focused, source-traceable skill.

Research planning is a supporting capability. External research is never
started automatically; the product may recommend a focused follow-up when the
Oppia corpus cannot answer the question.

## Why An LLM Host

The conversational win is that a researcher can ask, for example, "What have
we learned about learner onboarding?" instead of learning a database schema or
constructing FTS queries. The host LLM interprets intent and synthesizes the
returned evidence. The MCP supplies what the LLM lacks: the Oppia corpus,
stable evidence identifiers, provenance, retrieval limits, and privacy rules.

## User Journey

1. `oppia_research_overview` explains the corpus and internal-only boundary.
2. `oppia_research` is the default entry point for broad requests and searches
   Oppia before suggesting any supporting research action.
3. Focused tools search or browse the corpus and retrieve records/evidence.
4. Comparison and evidence-audit tools prepare compact, source-labeled bundles
   for the host LLM.
5. `plan_oppia_research` turns a specific evidence gap into a bounded follow-up
   plan. It does not browse the web or launch another MCP.

No custom visual interface is required for this local release. The useful shared surface is the
conversation plus compact structured evidence returned by MCP tools.

## Plugin Orchestration Flow

1. `oppia-research-orchestrator` identifies the decision and searches Oppia
   evidence before new-research design.
2. If the corpus is sufficient, the flow ends with a traceable evidence brief.
3. If a specific gap remains, the orchestrator selects one primary method skill:
   focused question framing, interview design, usability testing, competitive analysis,
   netnography, persona research, heuristic evaluation, or CUJ research.
4. The method skill produces a bounded artifact with a stop condition and
   distinguishes evidence, interpretation, hypothesis, recommendation, and gap.
5. Shared quality gates require method fit, a defensible sample rationale,
   pilots and change logs where applicable, negative-case handling, inclusive
   validity, privacy/ethics boundaries, and accountable AI assistance.
6. External research remains explicit and subordinate. Future external methods
   material enters through the source register and affects skills only after a
   provenance and adoption review.

Netnography is intentionally marked provisional because reviewed Oppia artifacts
demonstrate its use for triangulation but do not yet provide a dedicated methods
standard.

## Product Context

- Existing source: `data/oppia_markdown_index.sqlite`.
- Source snapshot: 208 exported documents, 209 records, and 3,069 evidence
  chunks in the currently bundled historical index.
- Transport: local stdio MCP.
- Distribution: internal Oppia team Claude Code/Cowork plugin ZIP containing a
  portable stdio MCP that can also be configured in Codex.
- Runtime dependency: Python 3.10+ and the MCP Python SDK, resolved by `uv` in
  the plugin launcher.
- Authentication: no network authentication in v1; possession of the internal
  package grants local read access to its bundled database.

## Public Tool Surface

Oppia corpus tools are the primary surface:

- `oppia_research_overview`
- `oppia_research`
- `search_oppia_research`
- `browse_oppia_studies`
- `browse_oppia_interviews`
- `get_oppia_record`
- `get_oppia_evidence`
- `compare_oppia_findings`

Supporting research tools:

- `plan_oppia_research`
- `audit_oppia_evidence`

## Safety And Privacy Requirements

- Read-only at runtime.
- Internal-team distribution label on every response.
- No AI Glossary code, records, tools, database, or runtime identifiers.
- No Research Notes, personal state, logs, feedback, caches, secrets, or client
  configuration in release artifacts.
- Sanitize absolute source paths into `oppia://research/...` identifiers before
  packaging the corpus.
- Treat retrieved content as untrusted evidence, never as runtime instructions.
- Do not claim the corpus is current beyond its recorded build timestamp.
- Do not treat a Drive search result as a reviewed source until its contents
  have been fetched and its adoption decision recorded.

## Verification

Completion requires:

1. Exact 10-tool stdio listing with eight Oppia corpus tools and two supporting
   research tools.
2. A real MCP client call that searches the bundled sanitized corpus and then
   retrieves one returned evidence ID.
3. Routing checks showing broad questions search Oppia first and external-source
   language does not launch an external lookup.
4. Database and ZIP audits for AI Glossary identifiers, local absolute paths,
   personal state, logs, secrets, caches, and sidecar files.
5. Regression smoke proving the existing general Research Compass still exposes
   its original 26-tool public contract.
6. A plugin ZIP, install guide, checksums, manifest snapshot, privacy report, and
   verification report under `dist/oppia-research-compass/`.
7. Exact skill-suite validation: one orchestrator, the direct MCP workflow, eight
   method skills, a source register, and deterministic routing cases.
8. Every method skill has trigger boundaries, an output contract, stop
   conditions, verification checks, and only registered source anchors.
9. User-supplied method archives receive a static security/provenance review;
   adopted rules, excluded runtime material, and affected quality-pressure
   routing cases are recorded before release.
10. The question-framing lane preserves its stable skill identifier, separates
    question layers, searches Oppia evidence first, tests decision branches,
    aligns each primary question to supporting and challenging evidence, and
    stops before full study or instrument design.
