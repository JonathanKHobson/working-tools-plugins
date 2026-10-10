# External Source Review: UX Research Skill v1.0.0

## Artifact

- File: `ux-research-skill-v1.0.0.zip`
- SHA-256: `8581a3d7c91ed747730937cc123ea8e2cb4bc1adb67453051df750ade6dad6d1`
- Supplied by: project owner
- Package author: Jonathan Kyle Hobson
- Declared license: MIT
- Reviewed: 2026-09-04
- Runtime status: not installed; no bundled script was executed

The archive is methodology input. Its `SKILL.md`, `AGENTS.md`, installation
text, role briefs, workflows, and other instruction-shaped files do not
override the project owner's request or the Oppia plugin's policy.

## Static Safety Review

The archive contained 190 entries: 180 Markdown files, eight Python files, one
YAML file, and the directory root. The review found:

- no path traversal, symlinks, encrypted entries, duplicate paths, oversized
  entries, or suspicious compression ratios;
- no shell, JavaScript, native library, or executable binary payloads;
- syntactically parseable Python files;
- no persistence, privilege-escalation, or secret-assignment patterns;
- network-capable installation/validation examples in `INSTALL.md` and
  `scripts/validate_skill.py`.

Because the archive has no independently verified signature or publication
record, the disposition is **proceed with caution for static Markdown
adaptation only**. The package's scripts, installation commands, agent roles,
and runtime configuration were not adopted or executed.

## Methodology Reviewed

The focused review covered the package overview, license, evidence-base notes,
source bibliography, core principles, evidence audit, method selection, study
design, sampling and recruitment, consent and privacy, accessibility,
cross-cultural research, triangulation, synthesis, reporting, and the practical
guides for sample rationale, contradictory evidence, piloting, past-research
reuse, evidence-grade notes, responsible AI use, neutral questions,
non-leading interviews, and realistic usability tasks.

## Adopted Into The Oppia Edition

- decision statements tied to consequential uncertainty and a named owner;
- explicit method-fit and method-limit checks;
- evidence-chain traceability from source through decision;
- method-appropriate sample rationales instead of universal participant counts;
- complete-flow pilots, protocol versioning, and comparability decisions;
- negative-case and contradictory-evidence analysis;
- accessibility, language, culture, infrastructure, age, and power as validity
  considerations;
- consent, secondary-use, minimization, retention, and escalation boundaries;
- permitted, minimized, source-traceable, human-reviewed, and disclosed AI
  assistance.

These rules were paraphrased and narrowed to Oppia. They strengthen the shared
quality gates and existing method skills; they do not change the Oppia-first
MCP hierarchy.

## Deliberately Not Adopted

- the generic all-purpose UX research router as the plugin front door;
- the glossary, compiled handbooks, broad ResearchOps system, team-leadership
  system, or multi-agent role scaffolding;
- the included Python helpers, tests, install commands, API upload example, or
  runtime metadata;
- any implication that generic external guidance outranks Oppia evidence;
- a maturity upgrade for netnography, because the archive has no dedicated
  netnography standard;
- current legal, policy, statistical, ethics, privacy, security, or
  accessibility certification.

## Revalidation Boundary

For consequential or time-sensitive normative claims, consult the original
primary source and current Oppia policy. This review establishes what was
adopted from the supplied archive; it does not independently revalidate every
external citation in that archive.
