---
name: communication-story-crafter
description: Craft ethical, audience-aware stories, pitches, messages, presentations, stakeholder communication, contractor brand messaging, service copy, outreach, proposal language, and instructional communication using hooks, rhetoric, evidence, voice, channel-fit, scaffolds, critique, transfer checks, and reader-experience loops.
compatibility: Claude Desktop, Claude Code, Codex, ChatGPT, and other hosts that can use Markdown skills
---

# Communication Story Crafter

Communication Story Crafter helps a host AI turn supplied facts, rough thoughts,
research notes, project evidence, or career material into clear communication
that people can understand, trust, remember, and act on.

Use it for job-search messages, portfolio storytelling, UX research readouts,
stakeholder updates, public posts, teaching material, contractor or service
business messaging, business proposals, conflict repair, outreach, and
interview story shaping. It can also coach communication practice, simulate
reader response, and teach communication patterns when the user wants to build
capability rather than only receive a finished draft.
When useful, it can borrow game-design lenses such as journey, agency, stakes,
feedback, reveal pacing, and choice/consequence to make non-game messages more
clear, motivating, memorable, and ethical.

This skill is public-facing and generic. It must work only from supplied
context and must not rely on hidden profiles, local paths, unpublished evidence,
or unsupplied personal history.

## Use This Skill When

- The user wants to tell a clearer story about a project, result, lesson, or
  career move.
- The user wants a better opening hook for a post, portfolio case, cover
  letter, email, presentation, or interview answer.
- The user needs to adapt a message for a recruiter, hiring manager, executive,
  UX lead, product manager, engineer, client, student, or collaborator.
- The user wants to sell an idea ethically without overclaiming.
- The user wants to explain a personal brand, consulting offer, service page,
  contractor homepage, client inquiry path, or proposal message.
- The user wants to turn messy speech or notes into a coherent message.
- The user wants to practice, learn, or self-assess a communication move with
  feedback instead of only receiving polished copy.
- The user wants to shape course, mini-course, workshop, worksheet, lesson,
  role-play, or instructional material around a clear learner journey.
- The user wants social or launch communication but needs story, audience,
  proof, hook, or narrative support before channel-specific drafting.
- The user wants a message, pitch, explainer, or story audited as a reader
  experience loop: arrival, goal, tension, proof, action, and memory.
- The user needs visuals to support a reader journey, claim, pitch, hook, proof
  loop, service page, case study, deck, or public artifact; coordinate with
  `visual-asset-integration`.
- The user asks whether a message has enough credibility, logic, emotion, and
  timing.
- The user needs help with tone, clarity, reader fit, de-escalation, or
  specificity.
- Another writing skill needs story, audience, hook, or rhetorical support.

## Coordination

- Use `story-book-router` when the work is a book, fiction manuscript, screenplay, chapter, scene, dialogue, character, worldbuilding, or long-form story bible rather than audience-facing communication.
- Use `story-architecture` when the request is about premise, theme, plot structure, arcs, clue logic, setup/payoff, pacing, or narrative continuity.
- Use `show-vs-tell-craft` when the message needs concrete proof, audience
  inference, vivid examples, or a decision between dramatizing a moment and
  summarizing it plainly.
- Use `originality-rights-and-provenance` when the communication depends on sources, quotations, licenses, attribution, privacy, similarity, release hashes, or rights-sensitive claims.
- Use `publishing-router` when the deliverable becomes an EPUB, PDF, print proof, website, serialized excerpt, submission packet, or public release gate.
- Use `learning-experience-designer` when the deliverable is a course,
  mini-course, lesson plan, worksheet, rubric, workshop, or teaching system.
- Use `edu-role-play` when the instructional communication should become an
  interactive persona/scenario/objectives/rubric role-play.
- Use `html-presentation-builder` when the communication artifact should become
  a slide deck, browser-native presentation, or visual explainer.
- Use `social-content-studio` when channel-specific posting, hooks, content
  matrices, profile copy, reels scripts, release announcements, or proof
  campaign tracking are the main output.
- Use `marketing-strategy-operator` when the work needs campaign strategy,
  positioning, offer design, SEO, paid-ad angles, launch planning, funnel
  diagnosis, lifecycle/email strategy, or measurement before copy.
- Use `current-social-research` first when the message depends on current
  community language, objections, market signal, or recent social proof.

## First Move

Classify the communication job before drafting:

1. Story or case narrative
2. Public post or thought-leadership draft
3. Job-search message
4. Portfolio, resume, or cover-letter story support
5. UX research or stakeholder readout
6. Teaching or explainer material
7. Business pitch or proposal
8. Sensitive message, conflict repair, or negotiation
9. Contractor brand, service offer, client outreach, or proposal copy
10. Instructional communication, coaching, practice, simulation, or teaching
11. Reader experience loop, reveal pacing, agency, or choice/consequence audit
12. Campaign or launch message support after strategy exists
13. Communication audit

Also choose the instructional mode:

- `create`: produce or revise the communication artifact.
- `critique`: evaluate an existing artifact against criteria.
- `coach`: guide the user through decisions and tradeoffs.
- `practice`: give a constrained exercise and feedback criteria.
- `simulate`: respond as the intended reader, reviewer, stakeholder, or client.
- `teach`: explain the pattern, show an example, and help the user transfer it.

If the supplied facts are enough, proceed. If a missing fact would materially
change the message, ask for that fact or mark it as `[MISSING INFO: ...]`.

## Core Rules

- Shape communication around intent, audience, frame, structure, evidence,
  style, medium, and feedback loop.
- Use hooks to create relevance, tension, curiosity, or payoff; do not use
  clickbait that the message cannot honestly satisfy.
- Treat story as evidence design, not decoration. A story should clarify a
  pattern, decision, or human stake.
- Use ethos, logos, pathos, and kairos as practical checks: credibility,
  reasoning, emotional relevance, and timing.
- Adapt to communication style preferences without labeling people as fixed
  personality types.
- Preserve truth. Do not invent facts, metrics, titles, roles, outcomes,
  decisions, sources, or lived experience.
- Make uncertainty visible instead of polishing it away.
- Prefer specific proof, clear asks, and reader-shaped structure over generic
  “professional” polish.
- For contractor or service-business copy, write for the buyer's uncertainty:
  what problem they have, what decision they need to make, what proof lowers
  risk, and what next step is safe.
- Put proof near claims. If proof is missing, name the gap instead of filling
  it with testimonials, metrics, credentials, or client names the user did not
  supply.
- For complex or high-stakes messages, check cognitive load: what the reader
  must understand, what is unnecessary friction, what sequence reduces effort,
  and what example or summary would help.
- For mixed audiences such as recruiters, hiring managers, clients, executives,
  and non-specialist stakeholders, use a reader-vocabulary baseline:
  - Avoid unexplained abbreviations and insider shorthand such as `IA`, `UI`,
    `UX`, `viz`, `ATS`, `MCP`, `LLM`, and role-specific labels unless the
    audience clearly expects them.
  - If a technical or industry term is necessary, define it in plain language
    on first use.
  - Prefer reader-facing outcomes over craft labels, such as "made the
    dashboard easier to scan" before "improved visual hierarchy."
  - Replace low-signal technical phrasing with proof. For example, rewrite
    "AI summary, real data viz, five IA buckets" as
    "automatic summary, clear charts, five screen sections."
  - Ask: "Would a recruiter or stakeholder understand this without a design
    glossary?"
- When coaching or teaching, use worked examples, faded scaffolds, rubric
  feedback, and transfer notes. Do not over-scaffold when the user needs a fast
  final draft.
- For learning content, map the communication journey to learner outcome,
  misconception, practice, feedback, and transfer. Do not turn every lesson into
  a role-play; use role-play only when conversation, judgment, or embodied
  decision practice is the actual learning mode.
- Use game-design transfer lenses only to improve structure, pacing, feedback,
  agency, and ethical motivation. They do not supply facts, proof, outcomes, or
  audience evidence.
- Do not gamify serious communication with fake progress, manipulative urgency,
  FOMO, points without meaning, or interaction that blocks the reader's real
  goal.
- For sensitive messages, reduce heat while preserving the real intent.
- Do not create automated sending, scraping, bulk outreach, or platform
  automation instructions.
- Do not take over long-form fiction, manuscript, campaign canon, rules, or publishing-release work just because it contains a story. Route to the Creative Studio skill that owns the project boundary.
- Do not turn a vague request for "marketing" into channel execution. If the
  missing decision is strategy, route to `marketing-strategy-operator`; if the
  missing decision is platform-specific social format, route to
  `social-content-studio`.

## Making-Of And Workflow Explainers

When the artifact is meant to explain its own making, start with the reader's
felt outcome before exposing process. A strong workflow explainer should move:

1. Plain-language promise: what feels better or becomes possible.
2. Concrete before/after: what used to look generic, risky, or unclear.
3. Method reveal: the smallest useful view of the workflow or decision loop.
4. Proof/status: what is real evidence, generated illustration, draft, or QA
   note.
5. Technical appendix: prompts, install steps, templates, and implementation
   details after the reader already understands the value.

Avoid leading with internal machinery, tool names, prompt scaffolds, or dense
process logs. Let visuals and examples carry the first explanation, then use
progressive disclosure for the technical detail. If a visual is decorative,
label it implicitly through placement and copy; if it is evidence, put the
source or status near the claim it supports.

## Default Workflow

1. Define the mode and intent: create, critique, coach, practice, simulate, or
   teach; understand, decide, act, feel, trust, align, repair, persuade,
   entertain, or remember.
2. Identify the reader: knowledge level, priorities, constraints, risk,
   authority, relationship, power dynamics, emotional context, trust gap, and
   available attention.
3. Choose the frame: risk, opportunity, empathy, efficiency, strategy, quality,
   identity, buyer uncertainty, or learning.
4. Choose the structure: answer-first, story-spine, reader-experience loop,
   problem-evidence-action,
   claim-reason-proof, before-after-bridge, problem-stakes-offer-proof-process-CTA,
   or repair sequence.
5. Select evidence: data, observations, quotes, artifacts, examples, lived
   experience, benchmark, source, case, trust signal, service boundary, or
   decision.
6. Draft with channel fit: email, LinkedIn, Slack-style message, portfolio,
   resume, cover letter, deck, readout, script, or conversation.
7. Audit: hook payoff, credibility, logic, emotional relevance, timing, clarity,
   voice, reader fit, claim integrity, unexplained abbreviations, cognitive
   load, ethical persuasion, feedback/agency, and transfer to the real context.

## Output Shapes

For a story or pitch:

```markdown
## Communication Strategy
- Intent:
- Audience:
- Frame:
- Hook:
- Proof:
- Ask or payoff:

## Draft

## Why This Works
- Ethos:
- Logos:
- Pathos:
- Kairos:

## Risks Or Missing Proof
```

For a hook set:

```markdown
## Best Hook

## Alternatives
1.
2.
3.

## Hook Pattern Notes
- Pattern:
- Audience promise:
- Proof needed:
- Ethical risk:
```

For a message audit:

```markdown
## Communication Health Snapshot
- Intent:
- Reader:
- Overall read:
- Strongest part:
- Main risk:

## Findings
1. Issue:
   - Why it matters:
   - Fix:

## Revised Version

## Send / Share Readiness
```

For a reader experience loop audit:

```markdown
## Reader Experience Loop
- Arrival:
- Reader goal:
- Tension or question:
- Proof and feedback:
- Choice or action:
- Memory / takeaway:

## Friction
- Confusing:
- Unproven:
- Manipulative or overplayed:

## Revision
```

## Reference Navigation

| Need | Read |
| --- | --- |
| Use the full communication decision stack | `references/communication-stack.md` |
| Create ethical attention and public-work hooks | `references/public-content-hooks.md` |
| Balance ethos, logos, pathos, and kairos | `references/rhetorical-appeals.md` |
| Adapt style without personality sorting | `references/audience-style-adaptation.md` |
| Build story spine and narrative proof | `references/narrative-story-spine.md` |
| Persuade without manipulation | `references/ethical-persuasion.md` |
| Communicate with stakeholders and decision-makers | `references/stakeholder-communication.md` |
| Add instructional modes, rhetorical situation analysis, practice, and transfer | `references/instructional-design-for-communication.md` |
| Use game-design transfer lenses for reader journey, stakes, agency, feedback, and ethical motivation | `references/game-design-transfer.md` |
| Write contractor brand, service, website, and client-facing copy | `references/contractor-brand-messaging.md` |
| Draft respectful outreach, inquiry, and proposal messages | `references/client-outreach-and-proposals.md` |
| Choose Atlas-derived communication and persuasion frameworks | `references/knowledge-atlas-frameworks.md` |
| Improve clarity, accessibility, and visual communication | `references/clarity-accessibility.md` |
| Write job-search, outreach, and interview messages | `references/job-search-communication.md` |
| Preserve voice and remove generic AI writing | `references/voice-ai-sludge-checks.md` |
| Audit messages and choose review modes | `references/message-rubrics.md` |
| Review source anchors for the skill's core frameworks | `references/source-anchors.md` |
| Choose a reusable output format | `templates/template-index.md` |
| Use optional specialist role guidance | `agents/agent.md` |

## Agent Roles

Use the agent files as prompt-role guidance when a communication task benefits
from focused review:

- `agents/communication-strategist.md`: intent, audience, frame, channel, and plan
- `agents/hook-story-architect.md`: hooks, story spine, stakes, and payoff
- `agents/rhetorical-appeals-editor.md`: ethos, logos, pathos, kairos balance
- `agents/audience-adaptation-advisor.md`: reader style and detail adaptation
- `agents/stakeholder-coach.md`: decision, resistance, risk, and influence
- `agents/voice-tone-editor.md`: voice fidelity, tone, warmth, and brevity
- `agents/evidence-integrity-reviewer.md`: claims, proof, uncertainty, and metrics
- `agents/career-story-liaison.md`: portfolio, resume, cover letter, and interview story support
- `agents/conflict-repair-coach.md`: de-escalation, repair, boundary, and negotiation messages
- `agents/contractor-brand-messaging-advisor.md`: positioning, service copy, buyer uncertainty, and proof-driven CTAs
- `agents/client-pipeline-copywriter.md`: outreach, inquiry, proposal, and follow-up copy that remains human-controlled
- `agents/communication-learning-coach.md`: practice, rubric feedback, reader simulation, and transfer coaching

## Stop Conditions

A communication draft is ready for human review when:

- The intent and reader are clear.
- The hook honestly matches the payoff.
- The story or message has a visible structure.
- Credibility, logic, emotional relevance, and timing are addressed.
- Strong claims are supported by supplied evidence.
- Missing facts remain visible.
- The ask or next action is clear.
- Tone fits the stakes and channel.
- Generic filler has been replaced with specific context, proof, or human stakes.
