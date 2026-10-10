---
name: figma-to-stitch-design-iteration
description: Select Figma frames, export or copy PNG references, and turn them into focused Stitch prompts and source-checked design iterations. Use for adapting existing UI across desktop/mobile or refining a flow from Figma references; draft-only requests stop before submission.
---

# Figma-to-Stitch design iteration

Produce one bounded iteration: a small reference set, a prompt that assigns each
reference a clear role, and, when generation is requested, a visually checked result.
Use current project evidence to preserve accepted design decisions.

## Choose the output and source authority

Infer the screen, state, target platform, and intended change from the request.
Keep the requested output count; do not multiply one state into a full variant
set. Example-specific labels, geometry, and content apply only when current
project evidence supports them.
Distinguish **prepare references/prompt**, **generate/refine in Stitch**, and
**transfer to Figma**. Complete the authorized stage; a prompt request does not
also request generation or import. A simple Figma-only edit or Stitch-to-Figma
transfer belongs to its existing operator skill.

Identify the Figma file/page/frame or selected group and the intended Stitch
project. Recheck live selection and project before acting. Recorded actions and
old project URLs help locate sources; they do not establish current state or
permission to resume an old draft.

Assign authority by purpose, rather than treating every image equally:

- **Appearance:** the current target-platform Figma shell and components.
- **Behavior:** mobile variants or live-app evidence explaining sequence, states,
  ownership, and return destination. Adapt behavior without copying dimensions.
- **Baseline:** current implementation or older frames used for comparison.
- **Proposal:** an accepted change or an exploratory alternative, labeled as such.

Current explicit user corrections govern the affected detail. Resolve conflicts
from current evidence; ask only when competing sources leave a consequential
choice unresolved. Do not silently blend a baseline into a proposed state.

## Select and export useful references

Choose the smallest set that communicates the decision. A shell, a state example,
and an ownership/detail example often suffice; this is not a fixed image count.
Select the actual frame/group containing the needed parent and children. Avoid
exporting unrelated canvas areas, invisible layers, or detached controls that
lose their context. Do not clean up or rewrite source designs merely to export.

Use a supported Figma export or **Copy as PNG**, then paste into the correct
Stitch composer when attachment is in scope. With clipboard PNGs, paste the image
before copying prompt text. Verify its thumbnail/preview before proceeding.
With file exports, use stable project-local names and verify the actual file.
Do not describe clipboard-only references as saved files.

Keep a compact reference manifest, inline for a small task:

| ID | Figma frame/node | Image path or verified attachment | Role | Preserve / adapt |
|---|---|---|---|---|
| R1 | Exact shell | Actual path or thumbnail identity | Appearance | Shell, labels, spacing |
| R2 | State variant | Actual path or thumbnail identity | Behavior | State and return destination |
| R3 | Parent + details | Actual path or thumbnail identity | Relationship | Ownership and grouping |

Inspect the rendered export at readable size: complete bounds, correct state,
legible labels, and sufficient parent context. A successful export or AX layer
name alone does not prove visual fidelity. Map 3–8 meaningful visual anchors
across the selected references: ID, source/viewport, approximate region,
node/selector if available, observed fact, intended action, and check status.

## Decide what to change and what to keep

Before drafting the iteration prompt, use both
`$ux-design-toolkit:design-studio` and
`$ux-design-toolkit:design-reference-lookup` on the selected evidence. This is an
explicit decision step, not permission for a broader redesign.

Use Design Taste Gate to name the surface, audience, existing style source, and
variance/motion/density/trust dials. Assess usability and state clarity first,
then hierarchy, typography, spacing, restraint, and generic generated elements.
Use UI UX Pro Max's local offline search to inform that judgment: start with its
`--design-system` query for the product/task, then use a narrow UX/domain lookup
only for a remaining question. Treat returned palettes, fonts, and patterns as
advisory comparisons; the established Figma system remains the appearance
authority. Do not persist a replacement design system or assume a code stack
for a mockup task.

Produce a short decision table tied to the source anchors:

| Anchor / feature | Decision | Evidence and reason | Prompt instruction |
|---|---|---|---|
| Existing shell/controls | Keep | Source and task fit | Preserve exact treatment |
| Observed task obstacle | Change | Concrete problem and intended benefit | Bounded correction |
| Unresolved alternative | Defer | Missing evidence or outside current scope | Exclude this pass |

Keep working elements explicit; do not manufacture flaws to fill the table.
Prioritize a few changes that affect this iteration. Translate the **Change**
rows into requested edits, **Keep** rows into constraints, and **Defer** rows
into boundaries. When rendered evidence is unavailable, mark visual judgments
as provisional and keep a draft-only brief useful without inventing observations.

## Draft and attach the prompt

Read [prompt patterns](references/prompt-patterns.md) for a ready-to-adapt brief
and a targeted correction format. Translate dictation into precise requirements;
preserve meaning and exact approved labels. State:

- the bounded output and exact existing screens to refine;
- what each attached reference controls and which source wins for each purpose;
- the user's trigger, resulting state, and return destination;
- parent/child relationships and meaningful variants;
- what may change, what must survive, and the output names needed for review.

For cross-platform work, separate visual authority from behavioral guidance in
the prompt itself. Ask for localized components/inserts when the surrounding
screen already exists and must remain exact. Do not request a whole new shell
as an incidental way to show a new state.

If using Stitch, follow the installed **stitch-design-studio:stitch-workbench**
for current browser access and draft preservation, and **stitch-design-partner**
for bounded generation. Discover their current installed paths; do not depend on
an old cache version, selector, iframe index, or assumed Stitch MCP. If unavailable,
use the current browser tool contract or deliver the prepared prompt/references.

Inspect existing text, attachments, and selected-screen context chips first.
Preserve unrelated drafts and attachments. After adding or removing task-owned
references, reconcile the prompt's R1/R2/R3 mapping against the actual remaining
images. Removing a context chip is different from deleting a canvas design.
Never submit an unrelated existing draft to clear the composer.

## Iterate against the sources

When generation is requested, start with the smallest representative state or
bounded set that tests the requested decision. Inspect the actual result at
reading zoom using the source anchors. Check exact labels, type/spacing/density,
identity assets, ownership grouping, comment/media treatment, and requested state
coverage. Correct words alone do not establish a faithful design.

Use **stitch-design-studio:stitch-design-review** for a generated-result review.
Reapply Design Taste Gate and the relevant UI UX Pro Max guidance against the
Change/Keep/Defer decisions: verify both intended improvements and preservation
of working elements. Reuse relevant lookup results unless new evidence changes
the question; another database search is not itself verification.
Give each revision a specific anchor, observed discrepancy, desired change, and
preserved features. Recheck changed anchors after generation. If repeated shell
redraws still drift, preserve the source shell and request only the missing insert;
mark rejected variants as superseded in review notes without assuming authority
to delete or rename them. Do not restart accepted work for more stylistic variety.

Static frames demonstrate intended states. Only executed interaction evidence
can demonstrate navigation, persistence, scrolling, or save behavior. Report
untested behavior explicitly rather than inferring it from a before/after pair.

## Close at the requested stage

For preparation, deliver the prompt plus reference mapping and actual export/
attachment status. For generation, add the exact project/screen location,
checked anchors, and remaining discrepancies. Keep **drafted → attached →
submitted → generated → visually checked → exported → imported → editable**
as distinct claims; report only observed stages.

If editable transfer is requested, use the installed
**figma-design-workflow:stitch-figma-handoff** and verify destination nodes and
native layers. Otherwise stop with the requested prompt or reviewed design.
Preserve source frames and user drafts; hand back browser control through the
Workbench's task-owned-session cleanup.

Read [the synthetic iteration example](references/smarttagit-example.md) only when its source-fidelity decisions would clarify the workflow. The filename preserves the source route; no original client evidence is included.
