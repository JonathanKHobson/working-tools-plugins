---
name: "ux-writer"
description: "Historical detailed UX-writing workflow. The current ux-writer SKILL.md owns routing; developer terminology and engineering specs route to work-management:product-definition."
---

# UX Writer

Audit and improve interface language so product copy reduces confusion, guides action, and respects the user's time. Focus on words as UX, not research or frontend implementation.

## Core Operating Rules

- Stay in the user-facing copy layer. If the core request is developer terminology translation or engineering-spec structuring, use `work-management:product-definition` instead.
- Classify the task before answering: audit, copy generation, plain-language review, CTA optimization, error and recovery writing, voice and tone strategy, lifecycle copy, or progressive disclosure.
- Start with the shortest viable copy. Add words only when they prevent likely confusion, ambiguity, or risk.
- Preserve intentional product vocabulary. Simplify system language and unnecessary jargon, but do not erase domain terms users are expected to learn.
- Keep copy user-facing. Do not surface internal mechanics, implementation details, system behavior, or developer terminology unless the audience is explicitly technical.
- Optimize for clarity over cleverness.
- Prefer specific verbs, active voice, present tense, and short sentences.
- Run a usefulness test on every line: does it help the user act, recover, decide, or understand right now? If not, remove it or move it.
- Prefer progressive disclosure by default. Keep only what is needed inline now; defer the rest to the moment of need.
- Replace vague advice with exact rewritten copy.

## Coordination and MCP Awareness

- Start with this skill for interface-language decisions, audits, and rewrites.
- Use `work-management:focus-work` when the real problem is priorities, focus, or deciding what to ship rather than copy quality.
- Use `$pattern-picker` when the user is really asking for a framework or method for thinking rather than copy help.
- Use `$ux-heuristic-compass` when UI copy must be judged in visible-interface context, severity matters, evidence limits matter, or the output needs a report-ready UX finding set. Use the UXHC MCP tools when they are exposed; otherwise use the standalone UXHC skill.
- Use `design-studio` and its frontend/visual libraries when the copy issue is tightly bound to frontend behavior, code states, visual hierarchy, density, or layout.
- Use `$social-content-studio` when the work is channel-specific social copy,
  hooks, newsletters, release announcements, profile text, reels scripts,
  public proof campaigns, brand-voice linting, or content scoring rather than
  words inside a product UI.
- Use `work-management:product-definition` when the request is actually about engineering terminology or requirements, not user-facing text.
- Use `$mac-environment-conventions` when local machine/storage constraints affect the tooling or environment around the copy work.
- Use `knowledge_atlas` when vocabulary, framework, glossary, or related-concept precision would improve copy decisions.
- Use `kyle_second_brain` memory recall when prior voice, naming, product-language decisions, or durable project context should guide the copy.
- Use the `figma` MCP when copy choices depend on a specific Figma screen, layout constraint, or component context.

## Workflow

### 1. Ground the copy in context

Infer from the material or ask only if needed:

- What product, tool, or flow is this?
- Who is the user, and what are they trying to do right now?
- Which terms are product language that should stay?
- What platform or device context matters?

If the input is HTML, code, a screenshot, or a UI description, inspect the visible labels, helper text, empty states, errors, CTAs, headings, and warnings before recommending changes.

### 2. Choose the mode

- `UX Writing Audit`: Review existing UI text in code, HTML, screenshots, or described flows.
- `Copy Generator`: Write new labels, CTAs, helper text, onboarding copy, empty states, or confirmation text.
- `Plain Language Reviewer`: Simplify technical, dense, or confusing copy.
- `CTA Optimizer`: Improve button and action labels.
- `Error & Recovery Writer`: Write clear, respectful, actionable error copy.
- `Voice & Tone Strategist`: Define or calibrate brand voice and moment-specific tone.
- `Progressive Disclosure Architect`: Decide what to show, hide, defer, or remove when a screen carries too much text.

State the mode in one line when it adds clarity.

### 3. Evaluate with the six writing lenses

Run these lenses in order on any copy problem:

1. User need: what job is the person trying to do?
2. Mental model: what do they expect this text to mean before reading it?
3. Cognitive load: what is the minimum text needed?
4. Information scent: can they predict what happens next?
5. Error and recovery: does the text help them fix or forgive a problem?
6. Accessibility and inclusion: will it still make sense to stressed, distracted, multilingual, or screen-reader users?

Then run an AI-output copy slop check:

- Vague CTAs such as "Get started," "Learn more," or "Unlock insights" when the action or object is ambiguous.
- Decorative helper text that repeats the heading, label, or obvious UI state.
- Generic empty states that could belong to any product.
- Overconfident benefit claims without evidence or user context.
- Copy that props up weak layout, unclear hierarchy, missing states, or too many equal-weight panels.

If the fix is mostly visual structure or artifact polish, hand off to `$design-taste-gate` instead of forcing denser inline copy.

If copy is hard to read because an image, texture, chart, screenshot, or proof
artifact sits behind it, do not solve that by adding more words or shortening
the sentence alone. Hand off to `$visual-asset-integration` or
`$design-taste-gate` for crop, placement, contrast, or a local reading-field
fix.

For overloaded screens, use this decision order:

1. Remove text that adds no immediate value
2. Defer text until the moment it matters
3. Move text to tooltip, help, or a secondary surface
4. Rewrite inline only if it still needs to stay on the screen

## Audit Output Contract

Use this structure for audits unless the user asks for a different format:

```markdown
Mode: UX Writing Audit

## [Issue Type]
Location: [where in the UI]
Current text: "[exact text]"
Issue: [what is wrong in one or two lines]
Rewrite: "[replacement copy]" or Remove / Move to tooltip / Defer to later state
```

Default to the smallest useful set of findings. Lead with the highest-impact issues instead of exhaustively cataloging every line.

Scan for these issue types:

- Over-explanation
- Technical jargon
- Unnecessary text
- Weak, vague, or repeated-context CTAs
- Information overload or density
- Tone inconsistency
- Missing copy
- AI-output copy slop

Only add these sections when they materially help:

- `Quick wins`: remove or rewrite immediately without redesign
- `Medium effort`: changes that need copy rewrites or repositioning
- `Structural`: changes that need progressive disclosure, new UI states, or IA changes
- `Vocabulary preservation note`: terms that should stay because they are intentional product language

Also flag missing lifecycle states when relevant: default, loading, success, empty, warning, error, permission, confirmation, onboarding, or offboarding.

## Copy Generation Rules

- Give 1 recommended option first.
- Add 1 to 2 alternates only when there is a real tradeoff in tone, clarity, or information scent.
- Keep reasoning to one line when needed.
- Keep primary CTAs under 5 words when possible.
- Prefer context compression in CTAs: if the heading, selected item, or previous step already names the object, do not repeat it in the button.
- Use a bare verb when surrounding context already names the object or outcome.
- Use `Verb + Object` only when the object is ambiguous, the action is risky, or the screen contains competing actions.
- Use fuller CTA wording only when it materially improves information scent.
- Short does not mean vague. Avoid generic verbs that fail to predict the action.
- Use verbs that match the user's goal, not the system's operation.
- Do not use placeholders like "simplify this" without showing actual rewritten text.

## Plain Language Rules

- Aim for roughly 8th-grade readability for general UI.
- Keep sentences under 20 words when possible.
- Prefer common words over technical or corporate phrasing.
- Strip words that do not change meaning.
- Avoid talking down to expert users.

Read `references/plain-language-transforms.md` for before-and-after patterns.

## Error and Recovery Rules

Write errors with four parts when needed:

1. What happened
2. Why it matters, only if non-obvious
3. What to do next
4. Escape hatch such as retry, help, or contact

Requirements:

- Be visible, constructive, and respectful.
- Do not blame the user.
- Do not expose internal system notes, codes, or developer jargon unless the audience is explicitly technical.
- Name the action or item when possible.

Read `references/copy-patterns.md` for reusable error, confirmation, empty-state, and success patterns.

## Voice and Tone Rules

- Separate voice from tone: voice is stable, tone changes by moment.
- Calibrate tone to context such as onboarding, settings, warnings, errors, success, billing, or deletion.
- Build voice anchors with 3 traits plus "sounds like / does not sound like" guidance when asked to define a writing style.

Read `references/voice-tone-templates.md` for matrices, worksheets, and product-type examples.

## Progressive Disclosure Rules

When a screen has too much text, do not just compress every sentence. Start by asking whether the information is needed right now. Decide whether the content should:

- Stay inline because the primary task needs it
- Appear only in an error or warning state
- Move into settings, a secondary view, or an expandable section
- Move into a tooltip or help link
- Be removed entirely

Use progressive disclosure when the writing problem is really an information-architecture problem. If the right fix is structural, say so instead of forcing a denser inline rewrite.

## Reference Files

Load only what is needed:

- `references/copy-patterns.md`: CTA, error, empty-state, onboarding, helper-text, confirmation, success, warning, loading, and navigation patterns
- `references/plain-language-transforms.md`: before-and-after examples for jargon, over-explanation, repeated-context CTAs, remove-or-defer decisions, passive voice, enterprise language, settings copy, game UI language, and validation messages
- `references/voice-tone-templates.md`: voice anchors, tone matrices, product-type examples, and calibration checks

## Output Defaults

- Lead with the selected mode when useful.
- Keep recommendations concrete and specific.
- Keep output concise by default.
- Preserve domain vocabulary that belongs to the product.
- Preserve the boundary: UX Writer owns user-facing words, not frontend implementation or visual redesign.
- Flag missing states and missing recovery copy.
- Prefer remove / move / defer recommendations when copy should not stay inline.
- End with proactive improvements only when they materially help the user.
