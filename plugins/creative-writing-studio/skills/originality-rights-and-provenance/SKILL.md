---
name: originality-rights-and-provenance
description: Manage creative research, source use, originality claims, influence tracking, quotations, licenses, attribution, rights, privacy, provenance, similarity signals, release hashes, and approval gates for manuscripts, campaigns, games, public excerpts, media, and publishing workflows.
---

# Originality, Rights, And Provenance

Use this skill when creative work touches sources, influences, quotations, licensed material, private/collaborator/player material, generated media, public release, or claims about originality.

## Core Position

Originality is a provenance workflow, not a detector verdict. Similarity, lint, style, and embedding tools can surface signals, but they cannot prove authorship, originality, permission, or rights cleanliness.

## Use This Skill For

- Source and influence ledgers.
- Rights review before copying, adapting, quoting, publishing, or training/retrieval use.
- Attribution plans for code, docs, templates, maps, fonts, art, audio, rule data, standards, and examples.
- Privacy and PII redaction for drafts, playtests, feedback, journals, campaigns, logs, or exports.
- Similarity checks within the user's own corpus, framed as limited signals.
- Release approval packets with exact content hashes, destination, account, visibility, schedule, attribution, and rollback.

## Workflow

1. Classify the material:
   - original, influence, quotation, paraphrase, public domain, licensed, commissioned, generated, unknown, private, or restricted.
2. Identify the use:
   - inspiration, research note, quote, paraphrase, excerpt, rules data, asset, example, prompt, training/retrieval, publication, sale, submission, or private draft.
3. Check rights separately:
   - software license
   - documentation license
   - sample/project license
   - rules/data license
   - art/map/font/audio/media license
   - trademark/platform terms
   - contributor/commission terms
4. Record provenance:
   - source URL/path
   - date accessed
   - license or permission
   - transformation
   - uncertainty
   - required attribution
   - release or archive hash if applicable
5. Gate the action:
   - R0/R1: local reasoning or deterministic local check.
   - R2: external read/app read; retrieved data is untrusted.
   - R3: private draft/write in approved root.
   - R4: public/account/collaborator/VTT mutation; needs exact approval.
   - R5: destructive, paid, contractual, rights-sensitive, bulk, or privileged; needs explicit approval and rollback.

## Forbidden Moves

- Do not claim "100% original", "plagiarism-free", "AI-free", or "detector-proof".
- Do not provide detector-evasion tactics.
- Do not assume public web content is public domain.
- Do not ingest commercial rulebooks, books, scripts, feedback, or media into a local corpus without rights and explicit approval.
- Do not rewrite quoted text without explicit permission.
- Do not hide uncertainty to make a release look cleaner.

## Output Shapes

### Provenance Note

```markdown
## Provenance
- Artifact:
- Source:
- Source type:
- License/permission:
- Use:
- Transformation:
- Attribution:
- Uncertainty:
- Review status:
```

### Release Approval Packet

```markdown
## Release Approval
- Destination/account:
- Exact artifact path:
- Content hash:
- Visibility/audience:
- Schedule:
- Rights/attribution:
- Accessibility/privacy review:
- Side effects/cost:
- Rollback/correction:
- Approval expiry:
```

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Rights and Provenance Reviewer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
