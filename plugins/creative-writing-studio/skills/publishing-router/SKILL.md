---
name: publishing-router
description: Route manuscript assembly, metadata, EPUB/PDF/print/web export, accessibility, citations, excerpts, serialization, public sharing, release approvals, hashes, rollback, and publishing QA for creative projects.
---

# Publishing Router

Use this skill when a creative project leaves draft mode and becomes a build, excerpt, website, serialized post, submission packet, EPUB, PDF, print proof, or public release.

## Route By Output

- Broad creative project, source-of-truth, or pre-release routing:
  use `creative-project-router`.
- DOCX/PDF reading or editing: use `doc` or `pdf`.
- Browser-native presentation or shareable explainer: use `html-presentation-builder` and the Shareables MCP only when the task explicitly needs that public-output lane.
- Story, manuscript, canon, or content revision before export: use `story-book-router`.
- Show/tell, read-aloud, excerpt, blurb, or line-level craft revision before
  export: use `show-vs-tell-craft`; diagnose before rewriting.
- Rights, attribution, privacy, source claims, release hashes: use `originality-rights-and-provenance`.
- Image/media purpose, source status, visual anchors, alt text, crop, and proof
  handling: use `visual-asset-integration`.
- For a new cover or illustration needing a selected method and editable prompt, use the installed `graphic-design-studio:graphic-design` guided image workflow reference; keep rights, export and release gates here.
- Web layout, interaction states, accessibility, and frontend QA:
  use `frontend-ux`.
- Public-facing narrative, audience trust, launch framing, or proof density:
  use `communication-story-crafter`.
- Visual QA for public HTML/web artifacts: use `playwright` or browser tooling only as required, then perform browser handoff.

## Release Gates

Publishing work is not just conversion. Check:

- canonical source and commit/hash
- title, subtitle, contributors, identifiers, language, rights statement
- table of contents/navigation
- headings and semantics
- image alt text and captions
- font/image/media licenses
- citations and source links
- privacy and PII redaction
- links and destination URLs
- EPUBCheck where EPUB is produced
- Ace by DAISY or equivalent automated accessibility signal where EPUB is produced
- human accessibility review
- two reading systems or preview contexts where practical
- print proof review for print/PDF
- release ledger and rollback/correction plan

## Approval Boundary

Do not publish, submit, email, post, serialize, schedule, change visibility, update stores/listings, accept terms, or mutate public accounts without an approval packet from `originality-rights-and-provenance`.

Content changes invalidate prior public approval. New approval must bind to exact artifact path and hash.

## Output Contract

```markdown
## Publishing Route
- Artifact:
- Source:
- Format:
- Destination:
- Risk:

## Build / QA Plan

## Rights And Accessibility Gates

## Approval Needed

## Rollback
```

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Producer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
