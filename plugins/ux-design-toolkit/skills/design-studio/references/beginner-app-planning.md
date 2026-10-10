# Beginner app planning and experience checkup

Use this when someone has a fuzzy app idea, needs a usable concept to hand to a
builder, or wants to untangle an existing app experience. Scale the language to
their familiarity; explain a term when it first matters. Infer routine details
from supplied evidence and ask only for missing facts that change the result.
Do not force every phase, question, or diagram onto a small request. The
preserved [Vibe Check method library](../../../libraries/vibe-check/README.md)
provides optional depth, including its [full source procedure](../../../libraries/vibe-check/UPSTREAM-SKILL.src.md)
for a substantial beginner planning or checkup request. Its older universal
workflow rules do not govern this skill.

## Find the need and evidence

Capture three plain lines: the person's **goal**, what they **do now**, and
why that **workaround frustrates** them. Ask about a concrete struggling
moment if it is not already in the brief. Name the one outcome that would show
the product worked. If a feature is described as a need, ask what problem it
solves. Mark what is observed, a hunch, or a guess. Research Studio owns a
deeper evidence search; do not invent interviews, demand, or customer quotes.

When evidence exists, sort it through five lenses: what incumbents already do
well, exact pain language, recurring objections, reasons people switch or
abandon a workaround, and the words different buyers use. Keep source and
bias with each note. For a rough prioritization, rate **Pain** and **Served**
from 1–10 and calculate `Opportunity = Pain + max(0, Pain - Served)`.
This is a transparent discussion heuristic, not a validated survey score or
proof of market demand. Do not turn weak evidence into precise rankings.
The strongest underserved need suggests a differentiator; well-served basics
that users still expect are table stakes. Work Management owns the actual V1
scope. Use [discovery depth](../../../libraries/vibe-check/references/DISCOVERY-DEEP-DIVE.md)
only when a source-backed comparison is needed.

For a marketplace or other multi-sided product, name each side, its struggling
moment, expected basics, and what one side needs the other to do. Run the
opportunity and journey pass separately; the other side's basics may be table
stakes for your side. Identify the smallest useful experience before network
effects work. Use [multi-sided](../../../libraries/vibe-check/references/MULTI-SIDED.md)
and [cold-start](../../../libraries/vibe-check/references/COLD-START.md) depth
when supply/demand dependency changes the design. Work Management owns launch
sequencing and Marketing owns acquisition.

## Make the experience visible

Sketch several meaningfully different ways to deliver the core value when the
direction is unsettled. Compare the actual user moment, not cosmetic variants,
then combine the strongest parts into one simpler approach. Check it for
desirability, usability, feasibility, viability, and ethics: does it address
real need, work for the intended audience, fit likely constraints, have a
plausible cost shape, and avoid manipulation or harm? Take one second look for
a generic default or avoidable complexity, then move on.

Find the **aha moment**, the first point at which a user feels the promised
value. Design the entry and onboarding backward from it. Do not assume an
arbitrary number of seconds or require signup before value when the product
does not need it. Map the **happy flow**, a **rough-day flow** under stress or
interruption, and relevant **edge cases** such as empty data, returns after a
long absence, large collections, failures, and account deletion. For each
journey step, ask what must be true for the person to continue; those needs
become candidate capabilities for the backlog. Use the
[experience blueprint](../../../libraries/vibe-check/references/EXPERIENCE-BLUEPRINT.md)
or [diagram system](../../../libraries/vibe-check/references/DIAGRAM-SYSTEM.md)
only when a visual map improves the decision. Static templates do not prove a
rendered or tested experience.

## Connections and decisions

Record where the user's data starts, who owns it, where it goes, what can be
exported or deleted, and what permissions an integration would request. Note
messages, AI suggestions, money movement, offline use, and multiple devices
only when relevant. Translate build decisions into product consequences:
who can access it, what survives a device change, what a failure looks like,
and what users can take with them. For each important stack choice, give a
recommendation, reason, alternative, and cost/risk to verify; route actual
technology selection to the platform builder. Confirm current provider terms,
privacy obligations, and price before making payment or legal claims.

A compact blueprint can show the goal, audience, evidence and confidence,
journey/aha, three flows, capabilities, data connections, decisions,
accessibility and failure states, and open assumptions. It should distinguish
existing behavior from proposed behavior. If an HTML version helps, the
[blueprint reference](../../../libraries/vibe-check/references/HTML-BLUEPRINT.md)
is an optional source template with external CDN requirements, not a required
export path. Render and inspect any visual artifact before claiming quality.

## Reality check and handoff

Name the riskiest assumption and the cheapest ethical way to test it. Check
whether the concept solves the original goal or simply implements a favored
solution. Estimate cost and complexity as ranges with explicit assumptions;
do not invent a budget, schedule, or provider approval. Separate the smallest
useful first release from later improvements, including the table stakes needed
for a real user to switch. Flag accessibility, privacy, security, error
recovery, backup/export, and support needs for the appropriate owner.

If sharing, inviting, or a visible output is part of the natural experience,
design that moment into the flow and hand distribution strategy to Marketing.
Do not add a viral mechanic merely to claim a growth loop. The conditional
[growth-loop reference](../../../libraries/vibe-check/references/GROWTH-LOOPS.md)
has deeper patterns. Give Work Management the proposed scope, test, open
decisions, and staged handoff; give platform builders technical and deployment
choices. For a live product, verify its actual path before calling it shipped.

For an existing experience checkup, compare current screens and flows against
the three goal/workaround/frustration lines. Identify the one contradiction or
failure that most blocks value, show evidence, and fix or propose that bounded
change. Use [Code Checkup](../../../libraries/vibe-check/references/CODE-CHECKUP.md)
only if the concern is code health, with the platform owner; similarly route
[code navigability](../../../libraries/vibe-check/references/KEEPING-CODE-NAVIGABLE.md),
[Git/deployment](../../../libraries/vibe-check/references/GITHUB-AND-DEPLOYMENT.md),
and [AI-build discipline](../../../libraries/vibe-check/references/MANAGING-YOUR-AI.md)
to their owning workflows. If the proposed product is an AI agent or skill,
consult [what a skill is](../../../libraries/vibe-check/references/WHAT-A-SKILL-ACTUALLY-IS.md)
before promising background autonomy.
