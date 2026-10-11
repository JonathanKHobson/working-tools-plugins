---
name: humanizer-deep-audit
description: Audit substantial prose against a source corpus, citation record, or authentic author sample, or help respond to a disputed AI-writing allegation using process evidence. Use for citation integrity, style-drift review, or a comprehensive pattern and false-positive analysis. For an ordinary rewrite or natural-voice edit, use natural-prose-editor instead. Never infer authorship from style or promise detector evasion.
---

# Humanizer deep audit

Use this specialist when the task calls for evidence beyond a close editorial read: checking identifiers and claims against sources, comparing a draft with genuine writing by the same author, or tracing a style diagnosis through the archived taxonomy and research. Ordinary prose editing belongs to `natural-prose-editor`. The source corpus is optional and should stay unloaded until the audit actually needs it.

## Choose the audit

- **Citation and claim integrity:** Read [citation integrity](references/citation-integrity.md), [research evidence](references/research-evidence.md), and [source bibliography](references/source-bibliography.md) as needed. Run `scripts/citation_audit.py` on the draft. Check every flagged identifier, link, quotation, page number, attribution, and claim against its actual source. A script flag is a lead, never verification.
- **Scientific argument or manuscript review:** Route to `research-methodology-local:academic-writing`; [academic handoff](references/academic-review.md) records the boundary. Research Methodology owns manuscript structure and evidence matching; Academic Writing Toolkit remains the existing tool provider.
- **Author-sample style drift:** Read [voice preservation](references/voice-preservation.md) and [human signals and false positives](references/human-signals-and-false-positives.md). Only compare against authentic text from the same author, with genre and audience differences noted. Run `scripts/style_baseline.py` and `scripts/style_drift.py` as descriptive aids. A short or mismatched sample cannot establish a reliable baseline.
- **Disputed AI-writing allegation:** Read [detector dispute](references/detector-dispute.md) only when the user asks about a flag or response process. Check the current institution/employer policy and actual report; use authentic draft/process evidence without inventing a defense or promising an outcome.
- **Corpus-backed pattern review:** Read the relevant pattern guides—[content](references/content-patterns.md), [language](references/language-patterns.md), [structure and formatting](references/structure-and-formatting-patterns.md), or [communication and markup](references/communication-and-markup-patterns.md)—and [false positives](references/human-signals-and-false-positives.md). Use the [coverage map](references/source-coverage-map.md), [source archive](references/source-archive/INDEX.md), and [research source records](references/source-library/INDEX.md) only when the question requires source tracing or complete coverage. Run `scripts/humanizer_lint.py` to locate review cues, then inspect each cue in context.
- **Explicit full release gate:** Apply the everyday editor’s [final outgoing pass](../natural-prose-editor/SKILL.md#final-outgoing-pass) and [editorial gate](../natural-prose-editor/references/editorial-gate.md), then combine the relevant routes above. Inspect the whole piece, not only machine flags. Use the genre-specific [revision examples](references/revisions-by-genre.md) only if they illuminate a proposed change.

The optional [editor lenses](agents/) can divide a large review by evidence, structure, line, voice, formatting, citation, genre, or scene. They are reference prompts, not automatic subagent instructions. Load only the lens the task requires.

For a requested writing-quality rating or scored version comparison, read and apply the full [quality review method](references/quality-scope-and-ethics.md). Use declared criteria, exact evidence, a transparent optional scale and unassessed fields; do not infer authorship or equate a pleasant style with factual reliability.

## Sequence and evidence

1. Identify the reader, purpose, genre, source set, and requested audit scope. Keep the author's strongest specific detail and intentional voice in view.
2. Mark claims that need source support before evaluating style. Do not invent evidence, quotations, lived experience, citations, or replacement facts.
3. Run the relevant deterministic checks from this skill directory. For example:

   ```bash
   python3 scripts/citation_audit.py draft.md --format markdown
   python3 scripts/humanizer_lint.py draft.md --format markdown
   python3 scripts/style_drift.py authentic-sample.txt draft.md --format markdown
   ```

4. Verify each reported concern manually. Distinguish a confirmed error, a plausible concern, a deliberate style choice, and an unresolved source question. Pattern clusters may justify revision; individual words or punctuation marks do not establish authorship.
5. After revisions, rerun affected checks on the final text and inspect adjacent-sentence progression, repeated hooks/metaphors, unsupported contrasts and compound stacking under the [post-edit check](../natural-prose-editor/references/editorial-gate.md#post-edit-check). A clean lint result is not a release verdict.
6. Report exact location, reader or evidence cost, and a concrete fix. Preserve authorial choices that serve the text. Where the user requested a rewrite, provide the rewrite; where they requested an audit, give a concise `Keep / Change / Verify / Status` review.

The scripts flag review cues and never prove who wrote the text. Do not optimize for AI-detector evasion. Preserve intentional dialect, formality, fragments, repetition, and punctuation. The archived third-party corpus is private local evidence; inspect its indexes and license notes before reusing or distributing any source text. The prior broad Humanizer instructions are preserved as [migration provenance](references/migration-originals/SKILL.original.txt), not a parallel routing entrypoint.

## Full source procedures

For a request matching a named procedure, consult the [native procedure map](../../library/source-procedures/INDEX.md), then read the selected complete bundled body and its applicable support. Use the current facts, scope and requested artifact; every ordinary editorial task operates without a separate writing-method plugin.
The full local Humanizer corpus, scripts, and original instruction are already in this skill; use the precise relevant files rather than a summary when performing a deep audit.

## Distinct writing routes

Use `voice-and-style` for personal/brand voice; `plain-language-editing` for reader accessibility and multilingual clarity; `technical-instructions` for documentation; `long-document-editing` for version and document passes; and `spoken-and-scripted-writing` for narration. Each routes directly to complete bundled methods. Occasional UX follow-up remains in communication.

When auditing a deliberately selected template or blend, consult [writing template selection](../voice-and-style/references/writing-templates.md). Evaluate fact fidelity, voice continuity and reader fit; do not flag purposeful changes in cadence or structure as authorship evidence, or normalize them away. This library adds no detector or new audit runtime.

For obscured agency, repetitive architecture across multiple pieces, or contextual overrides to a blunt anti-slop rule, read [research-informed pattern review](../natural-prose-editor/references/research-pattern-review.md). Use its grammar and collection checks only within the requested audit; no new authorship classifier or mandatory corpus retrieval is implied.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
