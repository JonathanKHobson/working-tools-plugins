---
name: plain-to-dev
description: Translate vague product, UX, business, or plain-English descriptions into precise developer terminology and buildable engineering requirements. Use when Codex needs to answer prompts like what do devs call this, translate this for engineering, how do I say this to a developer, what is the technical term for, or when a feature idea is too fuzzy for engineering because it lacks scope, rules, states, or acceptance criteria.
---

# Plain to Dev

Translate what someone means into language and structure an engineer can act on.

This skill covers two different gaps:
- vocabulary translation: the user described the right thing with the wrong term
- structural translation: the user has a real idea, but not yet a requirement
- beginner build translation/checkup: the user is non-technical, AI-assisted, or unsure whether an app idea/project is buildable and needs the next concrete step in plain language

## Coordination and MCP Awareness

- Start with this skill when the primary problem is translation into developer terminology or engineering-ready structure.
- Use `$focus-ops-manager` when the actual problem is focus, prioritization, or deciding what work matters now.
- Use `$prd-strategist` when the work needs broader product planning, phased scope, rollout thinking, or a full requirement pack.
- Use `$pattern-picker` when the user is really asking for the right framework or way to reason before translation begins.
- Use `$ux-heuristic-compass` when the request depends on bounded interface evaluation, UX audit framing, severity findings, or visible usability evidence rather than terminology.
- Use `$frontend-ux` when the answer materially depends on frontend implementation patterns, accessibility behavior, or state coverage in UI code.
- Use `$vibe-check` when the whole job is beginner app discovery, experience
  blueprinting, growth-loop thinking, or an AI-built project checkup. Use this
  skill when the user needs the shorter engineering translation of that work.
- Use `../local-data-mcp-builder/references/mcp-skill-package-structure.md` when the user is casually describing a reusable MCP, skill package, theme system, design library, validator set, or artifact pipeline and needs it translated into concrete folders and files.
- Use `knowledge_atlas` when you need stronger terminology verification, framework lookup, related concepts, or domain vocabulary beyond the bundled references.
- Use `kyle_second_brain` memory recall when the translation needs to align with prior conversation language, earlier requirements, saved notes, or an existing naming decision.

## Workflow

### 1. Classify the request

Pick one mode before answering:
- `Mode 1: Discipline-to-discipline`
  - Use for UX, marketing, PM, or business language that engineering names differently.
- `Mode 2: Plain description to technical term`
  - Use for colloquial descriptions of components, patterns, or behaviors.
- `Mode 3: Clarification-first translation`
  - Use when the description is too ambiguous to map confidently.
- `Mode 4: Idea to buildable requirement`
  - Use when the request is a feature idea, brief, or handoff that lacks inputs, rules, states, or done criteria.
- `Mode 5: Dictation to package structure`
  - Use when the user is speaking casually about folders, references, scripts, agents, examples, themes, or MCP/skill structure and needs clean file and responsibility names.
- `Mode 6: Beginner build translation/checkup`
  - Use when the user is new to building, is using AI to make an app/site/tool, or asks whether a project idea or AI-generated codebase "makes sense."
  - Keep the output plain-language and action-oriented; explain only the technical terms that change the next decision.
  - Tag idea evidence as `seen it`, `hunch`, or `guess` when that distinction
    materially changes what should be built first.

Modes can stack. A vague feature brief may need a few term translations plus a spec restructure.

### 2. Establish context before naming things

Resolve platform and implementation context first when it changes the answer:
- web or general product UI
- React, Vue, Angular, or component-library context
- iOS native: UIKit or SwiftUI
- Android native: Material Views or Jetpack Compose
- backend or general engineering terminology

If the request does not name a platform, infer it from context when possible. If the answer would materially change by platform, ask a short clarifying question instead of guessing.

### 3. Clarify only the ambiguity that matters

When the description could map to several concepts, ask targeted questions in this order and stop as soon as the term is identifiable:
1. Platform: website, iOS app, Android app, or cross-platform
2. Behavior: blocks the screen, slides in, appears inline, hovers, or disappears automatically
3. Trigger: button click, swipe, error, page load, or system event
4. Content: text, buttons, form fields, image, list of options, or mixed content

Do not ask broad discovery questions when one precise question will disambiguate the term.

### 4. Produce the right output contract

For translation tasks, use this exact structure:

```markdown
TERM: [precise technical term]
CONTEXT: [platform, framework, or layer]
ALSO CALLED: [aliases or platform variants]
DEV SEARCHABLE AS: [what a developer would search or ticket]
DEFINITION: [one sentence in plain language]
EXAMPLE IN USE: [one sentence showing how a developer would refer to it]
```

For idea-to-spec tasks, use this exact structure:

```markdown
PROBLEM: [user or business problem being solved]
USER: [who experiences it, in what context]
OUTCOME: [what should change and how success is judged]
RULES: [allowed, forbidden, conditional, role-based, validated behavior]
DONE MEANS: [ship-ready acceptance criteria]
OPEN QUESTIONS: [only the missing decisions that materially block implementation]
```

For beginner build translation/checkup tasks, use this exact structure:

```markdown
WHAT YOU ARE BUILDING: [plain-English product/tool/app description]
WHO IT HELPS: [primary user and situation]
FIRST WORKING VERSION: [smallest useful slice]
BUILDABLE PIECES: [screens, data, integrations, rules, and states]
RISKS TO CHECK: [auth, payments, privacy, storage, APIs, deployment, cost, or maintenance]
NEXT ACTION: [one concrete file, command, question, or repo inspection step]
DO NOT TOUCH YET: [scope that would distract from the first working version]
```

### 5. Translate ideas into engineering-ready structure

When using `Mode 4`, convert outcome language into buildable requirements:
- replace vague adjectives like `easy`, `smart`, `intuitive`, or `seamless` with measurable conditions
- identify missing inputs, outputs, rules, states, dependencies, and acceptance criteria
- separate user problem from proposed UI solution
- flag open questions explicitly instead of filling gaps with confident-sounding guesses

Minimum spec coverage:
- user and context
- entry point and main flow
- role or permission differences
- validation and limits
- loading, success, error, empty, and edge states
- analytics, accessibility, or integration constraints when the request implies them

When using `Mode 6`, reduce the project to a checkable first slice:
- name whether the task is idea clarification, project checkup, error recovery, or handoff preparation
- identify the struggling moment, one primary user, one differentiator, and the
  minimum table stakes required for a switchable V1
- translate terms like local, GitHub, staging, production, API key, database, environment variable, deploy, build, and test when they materially affect the next step
- if a codebase already exists, inspect the project map and entrypoints before proposing a rewrite
- route to `$project-structure-architect` for file/folder organization, `$local-mcp-debugging` for local tool failures, `$frontend-ux` for visible app behavior, or `$prd-strategist` for broader roadmap/scope only when the current next action requires it
- keep the user focused on one shippable slice, not a full platform plan

### 6. Translate dictated system structure into concrete folders

When the user dictates a folder or package idea, preserve their intent but replace casual wording with stable implementation language:
- "stuff the AI reads first" -> `README.md`, `SKILL.md`, or `AGENTS.md`
- "extra docs / references / other formats" -> `references/`
- "examples it can copy" -> `examples/`
- "figma files showing the pattern" -> `.fig` files under `examples/` or `references/`
- "assets / images / screenshots" -> `assets/`
- "different reviewers or roles" -> `agents/analyzer.md`, `agents/comparator.md`, `agents/grader.md`
- "scripts that make it reliable" -> `scripts/`
- "validators / checks" -> `scripts/validators/`
- "less token load / searchable memory" -> SQL, JSON records, vector indexes, schemas, and MCP tools that retrieve only the needed slice

For reusable MCP, theme, skill, design-system, or artifact-pipeline structures, use `../local-data-mcp-builder/references/mcp-skill-package-structure.md` as the default folder model. Include the evaluation reminder when applicable: Create evals JSON and run `eval-viewer/generate_review.py` so the human can review test cases.

### 7. Keep the boundary with UX writing clear

Use this skill when the core problem is translation into developer language or engineering structure.

Do not use this skill when the user mainly needs:
- better microcopy
- improved CTA labels
- error messages
- onboarding copy
- tone or voice calibration

Those stay in `$ux-writer`.

## Output Rules

- Lead with the selected mode when helpful.
- Prefer the precise term over the familiar but sloppy one.
- Include platform-specific names when they differ materially.
- Preserve intentional domain vocabulary when the product truly uses it.
- When a request is ambiguous, translate as far as you confidently can, then ask the smallest clarifying question needed.
- When restructuring ideas, name missing requirements as open questions instead of inventing policy.

## Reference Files

Load only the relevant reference:
- `references/discipline-glossary.md`
  - UX, PM, marketing, and business terminology mapped to engineering language
- `references/component-glossary.md`
  - plain component descriptions mapped to platform-specific technical terms
- `references/idea-to-spec.md`
  - structural checklist, vague-adjective translations, failure modes, and acceptance framing
- `references/beginner-build-translation.md`
  - Vibe Check-derived beginner build translation, evidence tags, glossary,
    first-slice framing, and checkup-mode translation
- `../local-data-mcp-builder/references/mcp-skill-package-structure.md`
  - folder architecture for skill-like MCP packages, themes, examples, scripts, validators, agents, and eval review

## Default Behaviors

- If the input is a single phrase, answer with the translation contract.
- If the input is a list, return one entry per item and mark ambiguous items clearly.
- If the input is a brief or feature request, use the idea-to-spec contract first, then add any key term translations that unblock implementation.
- End with only the follow-up questions that materially affect buildability.
