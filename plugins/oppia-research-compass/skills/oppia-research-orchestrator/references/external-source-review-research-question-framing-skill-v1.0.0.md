# External Source Review: Research Question Framing Skill v1.0.0

## Artifact

- File: `research-question-framing-skill-v1.0.0.zip`
- SHA-256: `5fafbaf03fa75fbebd0b48b33d1fb63df2a01e217bcb6bf450395aedb0d4a323`
- Supplied by: project owner
- Package author: Jonathan Kyle Hobson and contributors
- Declared license: MIT
- Reviewed: 2026-09-04
- Runtime status: not installed; no bundled script or test was executed

The archive is methodology input. Its instruction-shaped files—including
`SKILL.md`, `AGENTS.md`, workflows, install text, agent roles, and scripts—do
not override the project owner's request or the Oppia plugin's policies.

## Static Safety Review

The ZIP contains 119 files totaling 904,632 uncompressed bytes: 108 Markdown
files, nine Python files, one YAML file, and one extensionless license file.
The review found:

- no path traversal, absolute paths, symlinks, encrypted entries, duplicate
  paths, oversized payloads, or suspicious compression ratios;
- no shell, JavaScript, native library, executable binary, persistence,
  privilege-escalation, credential-access, obfuscation, or dynamic-execution
  payloads;
- syntactically parseable Python files;
- local file-writing behavior in packaging/manifest utilities and subprocess
  use limited to bundled tests;
- web links in documentation and URL parsing in the validator, but no network
  client imported by the runtime utilities.

The download metadata points to a ChatGPT attachment obtained through Chrome.
There is no independently verified signature, attestation, or source-to-build
record. The disposition is therefore **proceed with caution for static
methodology adaptation only**. Nothing from the archive was installed, wired
into the plugin runtime, imported, or executed.

## Methodology Reviewed

The focused review covered the root skill, evidence-base and source notes,
decision-first framing, problem framing, question anatomy and types, question
layer terminology, evidence/method alignment, neutrality and assumption
control, feasibility and ethics, inclusive and cross-cultural framing,
prioritization, practical repair guides, question architecture and quality
templates, and the education-terminology and low-bandwidth examples.

## Adopted Into The Oppia Edition

- the traceable chain from signal through problem frame, decision, evidence
  gap, research question, research learning objective, evidence test, and later
  study instrument;
- explicit separation of research questions from hypotheses, participant
  prompts, measures, and post-evidence “How might we” ideation;
- the decision-branch test requiring plausible answers to change action;
- provisional problem framing that separates signals, possible causes,
  consequences, evidence, assumptions, and boundaries;
- solution-removal, vague-construct operationalization, neutrality, and
  double-barrel repair rules;
- question-to-evidence alignment with supporting evidence, challenging
  evidence, strongest justified claim, prohibited claim, and validity threats;
- focused primary/supporting/deferred question architecture;
- accessibility, language, connectivity, educational context, culture, power,
  non-user, and missing-voice checks when they affect the decision;
- human review rules for AI-generated research questions;
- a compact Oppia-specific framing card and behavioral routing cases.

The adopted material was paraphrased, condensed, and made subordinate to Oppia
corpus retrieval. The existing skill identifier remains stable to avoid an
overlapping eleventh skill or a breaking route rename.

## Deliberately Not Adopted

- the standalone generic research-question router or its non-Oppia scope;
- the instructional learning-objective workflow, because this plugin supports
  research learning objectives rather than course design;
- the glossary, compiled handbooks, large example library, workshop system,
  or specialist multi-agent roles;
- the Python question builder, heuristic linter, validators, tests, installer,
  packaging scripts, or runtime metadata;
- universal question counts, numeric rubric thresholds, or a claim that lint
  scores can approve a research question;
- any current legal, ethical, accessibility, statistical, safeguarding, or
  policy certification;
- any MCP tool, database, network, permission, or runtime change.

## Revalidation Boundary

The source archive's external bibliography was treated as leads, not as
independently reverified authority. Consequential current standards, law,
policy, and method claims still require the applicable primary source and
Oppia owner review.
