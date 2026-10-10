# Prompt patterns

Fill only the fields that change this iteration. Keep the brief beside its
reference mapping; a small task does not need a separate planning packet.

## Pre-prompt judgment

Use Design Taste Gate plus the local UI UX Pro Max guidance to settle a compact
Change/Keep/Defer list. State the source anchor and reason for each choice. The
lookup suggests things to consider; it does not override the product's Figma
components. Feed the decisions directly into the prompt below.

## Reference-led generation or refinement

```text
Refine [existing named screen/component] in [project] for [audience/task].
Output [specific desktop/mobile states], at [target size when known].

Reference roles:
R1 — [frame + attachment identity]: visual authority for the target-platform
shell, typography, controls, spacing, labels, identity assets and navigation.
R2 — [frame + attachment identity]: behavior/state reference for [sequence].
Adapt its behavior to the target platform; R1 governs target-platform appearance.
R3 — [frame + attachment identity]: ownership/grouping reference for [relationship].
[Baseline images explain existing behavior; they are not proposed replacements.]

The user [trigger]. After [action], return to [destination], showing [new state].
Keep [child content] visibly attached to [owning parent] using [supported pattern].
Include [only requested meaningful variants, including absent/present data].
Preserve the distinction between [related but separate content/contexts].
Use these exact labels: [labels].

Change only [bounded region/behavior]. Preserve [accepted constraints].
[If exact shell fidelity is required: generate the insert alone for assembly
inside the existing Figma shell, without redrawing the surrounding screen.]
Name outputs [names that identify scope and state].
These are [static proposals / requested prototype behavior].
```

Keep delivery instructions outside the text intended for Stitch: “draft only”
controls the agent's action, not the design generator's brief. Do not import the
synthetic example's screen names or specific connector treatment into another
project without supporting evidence.

Do not leave bracketed placeholders in a submitted prompt. If a reference is
removed, update the mapping before submission. If only a prompt was requested,
return it without interacting with the user's Stitch composer.

## Targeted correction

```text
Refine [exact selected output].
Anchor [ID], [region]: the current render shows [observed discrepancy].
Reference [ID / region] shows [specific desired source treatment].
Change [precise geometry, label, grouping, or state].
Preserve [already correct shell/components/content].
Return [same state or narrowly specified revision].
```

Example: “Under the second question, the generated comment looks like an issue
follow-up. Keep it as a sibling of the issue card within the question's details
group, using R3's boundary. Preserve the question controls and desktop spacing.”
Use this only if the current source actually establishes that relationship.

## Completion evidence

A concise closeout can state: “Prepared [prompt location/text] with R1–R3 from
[named frames]. [Images saved / clipboard-only / attachments visually verified].
[If generated: output names and changed-anchor checks]. [Remaining discrepancy].”
Do not collapse attachment, generation, Figma import, and editability into “done.”
