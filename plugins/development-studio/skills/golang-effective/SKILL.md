---
name: golang-effective
description: Source-backed Go task router and baseline workflow. Use when Codex is writing, refactoring, debugging, reviewing, or designing Go code and needs Effective Go, Google Go Style, Uber Go Style, testing, naming, API, error, panic, or review guidance without loading unnecessary context.
---

# Golang Effective

Use this as the local router for Go work.

This skill was installed from the MIT-licensed `qtnx/golang-effective-skills`
topic-page harvest. This public edition retains the complete original method and both retrieval scripts. The existing populated index and all810third-party source chunks are excluded. Supply an authorized corpus/index through GOLANG_EFFECTIVE_INDEX; a bundled synthetic fixture tests retrieval without claiming third-party source rights.

## Workflow

1. Identify the Go task type from the prompt and touched files.
2. Use the routing table below to choose the primary lens.
3. Prefer repository conventions unless they harm correctness, readability, or
   testability.
4. Run `gofmt` after Go edits.
5. Run the narrowest useful Go test command when behavior or tests changed.
6. For source-backed grounding, run the local query script before citing style
   rules:

```bash
python3 skills/golang-effective/scripts/query_chunk_index.py \
  --index "$GOLANG_EFFECTIVE_INDEX" \
  "when should Go code wrap errors with %w"
```

Open only the returned source chunk files that are relevant.

## Routing

| Task | Lens |
| --- | --- |
| Style, readability, comments, control flow, idiom | `go-style-core` lens |
| Package names, exported APIs, comments, receivers, getters | `go-naming-api-design` lens |
| Errors, wrapping, sentinels, panic/recover, logging | `go-errors-panics` lens |
| Unit tests, table tests, helpers, examples, benchmarks | `go-testing` lens |
| PR or agent-generated Go review | `go-code-review-checklist` lens |

## Lens Checklists

### Go Style Core

- Prefer clarity over cleverness.
- Keep happy paths easy to scan.
- Let `gofmt` own formatting.
- Comments should document invariants, decisions, and non-obvious tradeoffs.
- Remove abstractions that do not reduce real complexity.

### Go Naming And API Design

- Read names from the call site.
- Keep package names short, lower-case, and domain-specific.
- Avoid `util`, `common`, and `helper` when a domain name exists.
- Avoid stutter between package and exported symbol names.
- Use `Name()`, not `GetName()`, for ordinary getters.
- Keep receiver names short and consistent.

### Go Errors And Panics

- Return errors when callers can handle failure.
- Add context at boundaries where callers need it.
- Use `%w` only when callers should inspect wrapped identity.
- Log an error once at the layer that adds useful context.
- Panic only for programmer errors, impossible states, or init invariants.

### Go Testing

- Test behavior, not implementation details.
- Use table-driven tests when cases share setup and assertions.
- Give rows names that explain the scenario.
- Call `t.Helper()` in helpers.
- Make failure output identify input, got, and want.
- Control time, randomness, filesystem, network, and concurrency.

### Go Review Order

1. Behavior and API correctness.
2. Error and cancellation paths.
3. Tests and failure quality.
4. Package boundaries and abstractions.
5. Readability and idiomatic style.
6. Performance only when the change touches a hot path or claims speed.

## Guardrails

- Do not load full raw source docs during ordinary coding tasks.
- Do not invent style rules when the repository has a clear local pattern.
- Do not optimize without evidence when performance is not the task.
- Distinguish correctness risk from style preference.
- Use `code-intelligence` when symbol navigation or LSP-vs-rg choice matters.

## Provenance

Reviewed source:

- `qtnx/golang-effective-skills`, MIT, commit `88d1f96`

Installed locally:

- compact skill router
- retrieval scripts
- external authorized `sources/index` and `sources/chunks` are recipient requirements, not bundled
- licenses and third-party notices

Not installed:

- raw source cache
- upstream install script
- agent profiles

