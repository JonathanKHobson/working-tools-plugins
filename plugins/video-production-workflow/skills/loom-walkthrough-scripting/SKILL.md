---
name: loom-walkthrough-scripting
description: Turn approved Figma design changes and stakeholder notes into concise Loom walkthrough scripts with spoken bullets, precise navigation cues, and checks for missing demonstration states. Use when preparing or revising a design walkthrough, recording talking points, or Loom speaker notes.
---

# Loom walkthrough scripting

Produce one script the user can glance at, read aloud, and naturally paraphrase while navigating Figma. Default to short spoken bullets, not an essay or a dense design review. The deliverable is the script; recording, design edits, uploads, and messages require their own task authorization.

## Ground the walkthrough

Use the supplied notes, approved changes, existing script, and current Figma frames or exports. Confirm the audience, purpose, approval state, and desired length from available context. Ask only for missing information that materially changes the script; otherwise state a reasonable assumption and draft.

- Separate approved changes, unresolved decisions, reference alternatives, and missing demonstration states.
- After stakeholder approval, frame the opening as a progress or implementation handoff. Do not recycle an outdated closing that asks for approval already given.
- Preserve current product terminology and exact control labels. Resolve conflicts against current user instructions and source evidence, not an old script.
- Inspect available project artifacts directly. Computer History can explain the workflow but is not required on every invocation and does not prove the current design state.
- If sources cannot be accessed, draft from supplied facts and label the navigation or claims that remain unverified. Do not invent frame IDs, screen states, or approvals.

For the fictional worked example and the reasons behind these checks, read [references/recorded-workflow.md](references/recorded-workflow.md). Its product rules are case-specific, not defaults for other products.

## Build a route that can actually be shown

Follow a complete user scenario rather than the order of a canvas gallery: starting context → action → visible result → recipient or role change → follow-up → outcome. Show alternate outcomes briefly and identify them as alternatives, not successive states.

Before calling the script recording-ready, map each important spoken claim to a visible screen or explicitly label it as intended behavior. A compact working table is enough:

| Beat | Frame/link and target element | Claim or transition | Evidence status |
| --- | --- | --- | --- |
| Short beat name | Observed frame/node or supplied reference | What the viewer should see | Verified, intended behavior, missing, or unverified |

Check for the starting state, intermediate draft, created item, submission, recipient view, and final outcome where relevant. For variant comparisons, verify meaningful state differences; a row of differently named controls does not demonstrate attached media, comments, or created issues.

If visual inspection is available, make a small anchor map of 3–8 key elements: ID, source/viewport, approximate region, frame/node or element hint, observed fact, and intended narration. Verify legibility at recording zoom and keep cues tied to those anchors. If no visual inspection was possible, say so; text extraction alone is not visual QA.

When a state is missing, continue drafting the supported route. Clearly identify the gap outside the spoken copy. If it is peripheral, briefly label it as in progress and omit the gallery tour. If it is central to the requested demonstration, mark the script as a draft pending that state. Do not silently redesign Figma or describe an absent example as completed.

## Write for speaking while navigating

Use this lightweight shape, adapting the number of beats to the actual route:

```markdown
# Loom walkthrough — [topic]
Audience: [recipient]. Purpose: [what this update enables].
Estimated time: [range, including navigation pauses].

## 1 · [Concrete beat]
Show: [verified Figma link/frame] → [element or next screen].

- [Short, natural sentence that can be read aloud.]
- [What changed and why it matters, if relevant.]
- [Visible result or transition.]

[Pause to show the result.]

## Close
- [Accurate completion or approval status.]
- [One audience-appropriate next action.]
```

- Keep each bullet to one thought. Prefer short spoken sentences; use fragments for obvious navigation reminders. Avoid paragraphs disguised as bullets.
- Separate `Show:` and bracketed stage directions from spoken text. Use exact frame destinations instead of “go over there.”
- Explain the scenario, action, and consequence. Include rationale only where the viewer needs it to understand an approved change.
- Explicitly cue role changes: “Now we’re viewing this as the assigned person.” Keep example names and ownership consistent.
- Slow down at the key changed interaction. Point separately to existing history, a new input, and the saved result when those distinctions matter.
- For static mockups, direct movement between frames and describe intended behavior. Do not imply the prototype executed a save, sent a notification, or persisted data.
- Keep draft, submitted, completed, and approved states distinct. Match those semantics to the current product.
- Skip archived alternatives, dense maps, and design history unless requested.
- Use the requested duration. Otherwise aim for a concise 3–4 minute walkthrough as a starting assumption, not a fixed limit. Estimate speaking time at roughly 120–140 words per minute plus navigation pauses; label it an estimate. Confirm any Loom recording limit from current context rather than assuming a plan limit.

## Finish the script

Do one spoken-language pass and one route pass. Check that the opening fits the audience, every material claim has evidence or an explicit qualification, transitions can be followed, terminology is consistent, and the closing asks only for the next needed action. Cut repeated rationale and awkward sentences instead of growing the script.

Keep only a short “Before recording” note outside the copy when useful: starting frame, unresolved coverage, and critical distinctions. Save into the existing review/script location when one exists; return the script directly when no file is requested or appropriate. Avoid creating a new presentation system or several competing script versions.

Report the script path and whether the route was visually verified or remains a draft. Prepared speaker notes are not a recorded Loom; a countdown, attempted recording, or visible mail screen is not evidence of a completed upload or send. Stop when the requested script is delivered and checked.
