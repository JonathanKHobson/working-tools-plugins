# Artifact Captions

Artifact captions bridge visuals and proof. They should make the artifact useful even when the reviewer skims.

## Caption Formula

```text
[Artifact] shows [what it shows] and matters because [why it mattered]. Decision influenced: [decision].
```

## Required Fields

For each artifact, capture:

- artifact name
- artifact type
- what it shows
- why it mattered
- decision influenced
- alt text
- use context
- confidentiality status
- missing context

## Caption Examples

Generic supported caption:

```text
[Research synthesis board] shows how open-ended responses were clustered into decision themes and matters because it helped the team prioritize the next discovery questions. Decision influenced: [MISSING INFO: exact decision].
```

Generic design caption:

```text
[Prototype screen] shows the revised entry flow and matters because it made the key action, error state, and next step easier to evaluate. Decision influenced: [MISSING INFO: review or launch decision].
```

Generic workflow caption:

```text
[Workflow map] shows where handoffs, dependencies, and review steps occurred and matters because it made the operational bottleneck visible. Decision influenced: [MISSING INFO: process change].
```

## Alt Text

Alt text should describe what is visible, not sell the candidate.

Use:

```text
Diagram showing [main visual elements] connected by [relationship or flow].
```

Avoid:

```text
Beautiful portfolio artifact proving strategic excellence.
```

## Missing Context

If any required field is absent, return:

```text
[MISSING INFO: artifact context needed before captioning]
```

Do not invent a decision, user outcome, or metric to make the caption feel complete.

## Traceable Source Record

In the private evidence map, record the original file or stable source URL plus
the exact locator: Figma file/page/node or frame; Loom/video recording and timestamp
or time range; PDF page; deck slide. For a screenshot derivative, retain native
dimensions and crop coordinates, any redaction, derivative filename, and the claim
it supports. Record source/version date when available. A crop must preserve the
relevant state and not imply a different sequence or outcome.

Public captions need a concise artifact description and truthful work stage, such
as "proposed navigation, 2024" or "original lesson frame." Keep private URLs,
participant information, filesystem paths, and extraction notes out of exports.
Label a retrospective synthesis or reconstruction when its origin matters to
interpretation; never caption it as an original research artifact or shipped UI.

## Caption Audit

Flag captions that:

- describe the artifact but not why it mattered
- imply a result without support
- expose sensitive internal detail
- lack alt text
- sound like a generic project label
