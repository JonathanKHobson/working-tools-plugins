---
name: code-intelligence
description: Choose the right code navigation method for semantic, exact-text, fuzzy, and refactor tasks. Use when navigating, reviewing, or refactoring code where language-server, rg, symbol, reference, rename, or search-tool choice affects correctness.
---

# Code Intelligence

Modified public distribution: complete original local adaptation retained; Apache-derived upstream technique is attributed to Anton Babenko. This export adds receiving-host requirements and the full pinned upstream method/reference closure. No language server, semantic-search backend or upstream plugin registration is installed.

Read the complete [upstream method](../../libraries/code-intelligence-ebb3257/skills/code-intelligence/SKILL.md) and its relevant references when the specific LSP/search/degradation procedure is needed. The local rules below adapt its tool choices to the current recipient; unavailable tools must be reported explicitly. See [license and source attribution](../../libraries/code-intelligence-ebb3257/LICENSE).

Pick the search tool by job, not habit. This skill adapts the useful
Apache-licensed guidance from `antonbabenko/agent-plugins` code-intelligence
for the local Codex workflow.

For shipped app/native binary/package or version questions that source cannot answer, or a concrete discrepancy between source and shipped behavior, use [Reverse engineer software](../reverse-engineer-software/SKILL.md) for the missing artifact evidence. Choose this from the task without requiring “REA”; ordinary source navigation and refactoring remain here.

## Tool Choice

| Goal | Prefer | Why |
| --- | --- | --- |
| Definitions, references, call sites, rename safety | Language server when available | Uses language semantics |
| Known names, config values, filenames, exact counts | `rg` and direct file reads | Exhaustive text evidence |
| Vague concepts, "where might this live" | Semantic/fuzzy search if available | Discovery, not proof |
| Public docs or current API behavior | Official docs or primary sources | Avoid stale memory |

## Rules

- For exact local text search, use `rg` first.
- For semantic tasks, anchor on a real file position before trusting LSP output.
- A bare symbol search returning nothing is not proof that the symbol has no
  references.
- If an LSP call is cold or empty, retry once after checking that the server can
  return document symbols in an in-scope file.
- If LSP is unavailable, say what was intended, what was used instead, and the
  impact on completeness.
- Never claim a tool is missing or shimmed without checking it directly.
- Do not use fuzzy or semantic search for counts, completeness claims, or final
  proof.
- Read returned locations before making claims; tool results are pointers, not
  evidence by themselves.

## Disclosure Line

When substituting tools, put this on the first line of the response:

```text
Intended: <tool>. Actual: <tool>. Reason: <why>. Impact: <confidence/completeness>.
```

Skip the line when no substitution happened.

## Refactor Guidance

- Prefer native rename/reference support when the language server supports it.
- If not, enumerate references with text search and inspect each match before
  editing.
- Config, docs, generated code, tests, and examples can contain meaningful
  references that LSP misses.
- Keep tool limitations visible in review findings.

## Verification

Before final claims:

- exact names searched with `rg`
- semantic references checked with LSP or disclosed fallback
- relevant files read directly
- tests or type checks run when code changed

## Provenance

Reviewed source:

- `antonbabenko/agent-plugins/plugins/code-intelligence`, Apache-2.0, commit
  `ebb3257`

Adoption decision:

- Installed as a lightweight local skill because the local skill set had many
  task skills but no explicit LSP-vs-rg tool-choice discipline.
- Upstream plugin metadata and marketplace packaging were not installed.
