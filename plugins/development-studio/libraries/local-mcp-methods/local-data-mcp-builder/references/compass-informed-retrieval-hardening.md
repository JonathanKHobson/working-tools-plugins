# Compass-Informed Retrieval Hardening

Use this reference when building or hardening an MCP that sits on a large knowledge base, framework library, bias/lens catalog, vector store, or personal data corpus.

Source research packets:


This file is the distilled operational version. Do not paste the full research packet into runtime prompts.

## Core Pattern

Treat the MCP as a staged, testable retrieval system:

```text
user request
  -> classify route and mode
  -> retrieve compact lens cards / records / evidence
  -> optionally expand through explicit graph edges
  -> rerank and budget
  -> validate bundle shape and safety
  -> return compact result with trace
```

Do not rely on the host model remembering a giant prompt scaffold. Put behavior into schemas, budgets, validators, redirects, and evals.

## Required Contracts

For retrieval-heavy MCPs, define lightweight stdlib contracts before adding tools.

- `RetrievalBudget`: named mode plus caps for results, chunks, lens cards, related entries, graph edges, and approximate context characters.
- `RetrievalBundle`: the actual returned working set, including direct records, search results, related entries, graph edges, and optional trace.
- `LensCard`: compact operational card derived from a source record, with stable ID, use cases, do-not-use cases, misuse warning, related lenses, and token budget.
- `KnowledgeEdge`: lightweight relation with stable edge ID, source ID, target ID, relation type, confidence, and metadata.
- `RetrievalTrace`: machine-readable explanation of budget mode, selected counts, truncation, skipped lanes, and degraded behavior.
- `ValidationReport`: `ok`, blocking failures, warnings, repair hints, and metadata.

Prefer stdlib dataclasses or JSON Schema docs first. Do not add Pydantic unless the project already uses it or runtime validation needs justify the dependency.

## Retrieval Budgets

Every retrieval mode should have measurable caps. A strong default set is:

- `quick`: a few high-signal records for first-pass answers.
- `standard`: default working set for ordinary agent use.
- `deep`: broader context for research or synthesis.
- `debug`: larger result set plus trace fields and diagnostics.

Budgets should cap:

- result count
- chunk count
- lens-card count
- related-entry count
- graph-edge count
- approximate context characters

When a response is trimmed, return a trace field that says it was truncated and which budget governed it.

## Lens Cards

Use lens cards when the corpus contains frameworks, biases, methods, prompts, personas, activities, reasoning patterns, or interpretive tools.

Lens cards should be generated from existing source records rather than manually rewriting the corpus.

Minimum useful fields:

```yaml
lens_id: lens.<collection>.<source_slug>.v1
atlas_id: <source-system-id>
name: Human title
lens_type: pattern | term | bias | mitigation | dilemma | persona | activity | other
summary_short: Compact summary
representation_short: 1-3 sentence operational form
representation_standard: Working form for default retrieval
representation_full: Larger form for deep/debug mode
use_when:
  - Concrete trigger
do_not_use_when:
  - Misuse boundary
misuse_warning: Calibration warning
related_lenses:
  - lens.other.id.v1
token_budget:
  short: 80
  standard: 220
  full: 700
metadata:
  source_slug: original-slug
  source_id: original-id
  source_file: original-file-or-db
```

If the host model names a lens without retrieving a stable source ID, mark it as `host_inference` rather than implying corpus grounding.

## Lightweight Graph Edges

Use graph edges for low-risk retrieval expansion. Start with explicit relationships, not speculative inference.

Good first edge types:

- `wikilink`: source note explicitly links to target.
- `source_related`: source data has an explicit relationship.
- `same_source_slug`: two source lanes intentionally share a slug.
- `same_concept_topic`: both records have an explicit curated topic.
- `supports_workflow`: both records share explicit workflow metadata.

Avoid deriving high-confidence conceptual relationships from vector similarity alone. Vector search finds candidates; graph edges should explain why a one-hop expansion is legitimate.

## SQLite, FTS, And Chroma

Use SQLite/FTS as the reliable baseline:

- Build JSONL and SQLite first.
- Store records, chunks, aliases/tags/topics, sources, relationships, quality flags, lens cards, graph edges, and build metadata.
- Open the server DB read-only or query-only.
- Make Chroma optional and lazy.

For Chroma:

- Commit SQLite first.
- Build Chroma second.
- Cache semantic health in build metadata.
- Make live Chroma checks explicit maintenance/debug actions.
- If external-drive Chroma writes are unreliable, build the vector store in local temp storage and copy the complete store back.
- Verify Chroma count equals SQLite chunk count when live semantic health is requested.

## Validators

Validators should run after build and on important runtime bundles.

Build validators:

- SQLite `PRAGMA integrity_check`.
- Expected record counts by collection or source lane.
- JSONL count equals SQLite count.
- FTS row count equals source table count.
- Lens cards exist for every active record.
- Lens cards have stable IDs, source IDs, representations, misuse warnings, and token budgets.
- Knowledge edges have valid source/target IDs and allowed relation types.
- Source-path and provenance fields are preserved.
- Chroma count matches chunk count when live Chroma is enabled.
- No `.DS_Store`, `._*`, `__pycache__`, or `.pyc` files in generated artifacts.

Runtime validators:

- Budget limits are obeyed.
- Public result envelope has the expected shape.
- Wrong-lane calls return redirects instead of doing wrong lookups.
- Private data and source-scope labels are preserved.
- Placeholder/debug strings do not leak into user-facing output.
- Degraded paths return partial useful results with warnings.

## Retrieval Evals

Add small JSONL eval fixtures before trying to tune retrieval by feel.

Minimum fixture shape:

```json
{
  "query": "help me improve my resume",
  "budget_mode": "quick",
  "expected_ids": ["lens.task-templates.resume-tailor-rewrite-feedback.v1"],
  "must_not_include": ["lens.paradoxes-puzzles.birthday-paradox.v1"]
}
```

Track:

- Recall@5
- Precision@5
- MRR
- must-not-include violations
- latency
- budget compliance

Default gate: zero must-not-include violations. Treat recall as a baseline until the fixture set is mature.

## Source Truth And Presentation Metadata

Separate source truth from presentation layers.

Source truth fields preserve original identifiers:

- source slug
- source ID
- source file/path
- source category/lane
- source tags/categories

Presentation fields support retrieval and browsing:

- curated topics
- graph-facing tags
- personal/practical surface fields
- workflow roles
- display titles and paths

Do not overwrite source IDs or slugs to make the presentation cleaner. Add new fields instead.

## Memory And Write Boundaries

For memory, living docs, personal corpora, feedback stores, and private archives:

- Explicit user write actions may write when the intent and target are clear.
- Inferred writes become a patch proposal or confirmation request.
- Patch proposals should include target, source quote/reference, proposed change, confidence, sensitivity, rationale, and whether approval is required.
- Read-only MCPs should not ship hidden write tools.

## Knowledge Atlas Worked Pattern

The Knowledge Atlas AI layer is the current local example:

- Sidecar code: `<external-ssd>/Documents/Knowledge Atlas/ai-layer`
- Sidecar data: `<external-ssd>/Documents/Knowledge Atlas/data`
- Human vault: `<external-ssd>/Documents/Obsidian Vaults/Knowledge Atlas`

Pattern to reuse:

- active corpus stays in the human-facing vault
- AI sidecar builds JSONL, SQLite/FTS, and optional Chroma
- SQLite commits before Chroma
- Chroma is optional and health-checked separately
- lens cards are derived from existing records
- graph edges are lightweight and explicit
- eval fixtures include expected IDs and must-not-include IDs
- validators check counts, edge targets, budget compliance, and sidecar cleanup

This pattern is especially useful for Compass-style systems where the right answer depends on selecting the right small set of lenses rather than loading every framework into context.
