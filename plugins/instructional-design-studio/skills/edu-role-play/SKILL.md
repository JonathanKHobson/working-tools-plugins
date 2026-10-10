---
name: edu-role-play
description: Create interactive learner-vs-AI role-play practice activities with personas, observable objectives, rubrics, debriefs, and optional SCORM/LMS handoff. Use when the user asks for a role-play, persona practice, sales simulation, customer conversation drill, compliance scenario, interview practice, stakeholder simulation, or AI-character training exercise.
---

# Edu Role Play

Build scenario-based practice activities, not generic chatbots. The output is a
single learner-facing role-play composition that can become bundled HTML through
the upstream `edu-role-play` CLI when a terminal and network are available.

This local skill was added from the 2026-06 harvest of
`minicoursegenerator/edu-role-play` and
`minicoursegenerator/skills-for-course-creators`. It keeps the useful
pedagogical structure and install path while adding local safety gates for
credentials, Cloudflare deployment, and public Shareables handoff.

Runtime smoke test: `npx -y edu-role-play@0.1.27 --help`, `init`, `lint`, and
`bundle` were verified locally on 2026-06-19. The package is MIT-licensed and
points to the reviewed upstream repo. The default bundle command uses a shared
public proxy unless `--proxy-url` is supplied; do not use that default for
private, sensitive, client, student, or production role-plays without explicit
approval.

## Use This Skill When

- A learner needs to practice a conversation with an AI persona.
- The user asks for sales, support, compliance, negotiation, interview,
  classroom, coaching, customer-success, or stakeholder simulation.
- A course or training asset needs measurable objectives and a rubric.
- A Shareables artifact should explain or host a role-play option.

Do not use this skill for ordinary fiction, open-ended brainstorming chatbots,
or therapy/medical/legal simulation as a substitute for qualified instruction.

## Hard Pedagogy Gate

Before writing the activity, confirm or infer these five pieces:

1. Learner role: who is practicing and what skill they are building.
2. Observable objectives: transcript-visible actions, not vague verbs.
3. Success criteria: what full credit looks like for each objective.
4. Rubric dimensions and weights: positive integers, total 1-20.
5. Persona goals and constraints: what the AI character wants and cannot do.

Forbidden objective verbs: understand, know, feel, appreciate, be aware,
familiarize, learn about. Replace them with ask, confirm, quantify, summarize,
handle, secure, surface, compare, disclose, escalate, or decide.

For substantial activities, summarize the plan before writing:

```markdown
Plan:
- Conversation:
- Learner role:
- Persona:
- Objectives:
- Difficulty / tone:
- Language:
```

Ask for confirmation only when the missing choice would materially change the
training. If the user told you to implement and the intent is clear, proceed
and record assumptions in the activity notes.

## Composition Shape

Create one folder per role-play:

```text
<slug>/
  <slug>.erp
  <slug>.html        # created only after bundle succeeds
  README.md          # short facilitator/author note when useful
```

Use `.erp` for the source composition so browsers do not mistake the raw source
for a finished artifact. The source contains:

- `<edu-persona>` with concrete name, role, background, goals, constraints, and
  speech patterns
- `<edu-scenario>` addressing the learner in the second person and naming the
  persona
- 2-4 `<edu-objective>` entries with stable ids
- `<edu-rubric>` with exactly one criterion per objective
- `<edu-termination>` with a turn cap and manual end by default
- `locale` on the root element when the UI should be non-English
- fallback notice explaining that the file is not bundled yet

## Avatar Choices

Use one of these only when it fits. Otherwise omit the avatar and allow the
runtime fallback.

- `middle-aged-man-friendly`
- `middle-aged-man-frustrated`
- `middle-aged-woman-professional`
- `young-woman-professional`
- `young-man-thoughtful`
- `older-woman-warm`

## Build And Verification

If `npx` is available and the user wants a source scaffold, run:

```bash
npx -y edu-role-play@0.1.27 init <slug>
```

If the user wants a runnable artifact, run:

```bash
npx -y edu-role-play@0.1.27 lint <slug>/<slug>.erp
npx -y edu-role-play@0.1.27 bundle <slug>/<slug>.erp
```

Fix every lint error. If network/package execution is unavailable or not yet
approved, leave the `.erp` source and README ready, and state that bundling was
not run.

Never ask the user for an API key for ordinary lint/bundle. Keys belong only in
an owned proxy or provider-side secret store, never in HTML.

For any real learner, client, student, internal, or sensitive scenario, prefer:

```bash
npx -y edu-role-play@0.1.27 bundle <slug>/<slug>.erp --proxy-url "$APPROVED_PROXY_URL"
```

Use the shared default proxy only for harmless demos when the user accepts that
the learner transcript may pass through a public third-party proxy.

## Proxy, SCORM, And LMS Gate

Deployment is a second step, not part of first draft creation.

Proceed only after the user says the role-play is ready to ship. Then:

- Explain that API keys stay in a Cloudflare Worker secret or approved backend.
- Use `edu-role-play-proxy` only as a reviewed optional deployment pattern.
- Do not use the CLI shared default proxy for sensitive or production sharing
  unless the user explicitly approves that boundary.
- Do not type Cloudflare credentials or API keys for the user.
- Do not embed any API key, token, or provider secret in the `.erp` or `.html`.
- If creating SCORM, run the upstream CLI only after lint and bundle pass.

## Shareables Handoff

When the role-play is part of a Shareables workflow:

- Use Shareables `packet` or `docs` for facilitator-facing explanation,
  source notes, rubric, safety boundaries, and deployment steps.
- Use Shareables `reel` only for a concise walkthrough, not for the role-play
  runtime itself.
- Keep learner transcript privacy visible near the proxy or deployment note.
- Link the final bundled HTML as a companion artifact rather than copying
  secrets or runtime internals into the shareable.

## Safety Rules

- Do not create manipulative, deceptive, coercive, or credential-harvesting
  scenarios.
- Do not simulate high-stakes medical, legal, financial, safety, or mental
  health advice without strong educational boundaries and professional review.
- Do not include real private client, student, prospect, patient, or employee
  data unless the user explicitly confirms it is approved and safe.
- Treat automated deployment, SCORM upload, and LMS integration as explicit
  runtime lanes with their own security review.

## Output Contract

Return:

```markdown
## Role-Play Built
- Folder:
- Source:
- Bundled HTML:
- Objectives:
- Rubric total:
- Verification:
- Remaining deployment gate:
```

If only drafting:

```markdown
## Role-Play Draft Ready
- Source:
- What is complete:
- What was not run:
- Next command:
```

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Workshop Facilitator. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
