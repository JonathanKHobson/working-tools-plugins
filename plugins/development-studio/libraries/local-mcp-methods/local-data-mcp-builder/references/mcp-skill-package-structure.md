# MCP And Skill Package Structure

Use this reference when a local MCP, theme system, design library, workflow package, or knowledge tool needs clearer folder organization. The preferred model is a small skill package that can grow into an MCP when it needs tools, indexes, structured storage, and retrieval.

## Core Principle

Keep the root readable, keep reusable knowledge structured, and keep repeatable operations executable.

- Root files explain what the package is and when to use it.
- Markdown files carry human-readable rules and design intent.
- `references/` carries structured or machine-readable support material.
- `examples/` and `assets/` show the system what good output looks like.
- `scripts/` makes generation, validation, and evaluation repeatable.
- `agents/` stores role-specific review or analysis instructions.
- A package becomes MCP-shaped when it needs searchable state, callable tools, or reliable retrieval instead of loading everything into context.

## Recommended Folder Shape

```text
package-name/
  README.md
  SKILL.md
  AGENTS.md

  references/
    schema.md
    package-schema.json
    usage.md
    token-map.css
    retrieval-notes.md

  examples/
    README.md
    example-output.html
    example-record.json

    components/
      README.md
      component-examples.md
      component-library.fig

    tokens/
      README.md
      token-examples.md
      token-reference.fig

  assets/
    icons/
    screenshots/
    sample-files/

  agents/
    analyzer.md
    comparator.md
    grader.md

  scripts/
    generate_preview.py
    render_preview.sh
    run_eval.py

    validators/
      validate_schema.py
      validate_tokens.py
      validate_output.py

  evals/
    evals.json

  eval-viewer/
    generate_review.py
    viewer.html
```

Use only the folders the package needs. Do not create empty scaffolding just because the full structure exists.

## File Roles

| Location | Role |
| --- | --- |
| `README.md` | Human overview: what this package is, what it contains, and where to start. |
| `SKILL.md` | AI entrypoint: when to use the package and which files to load next. |
| `AGENTS.md` | Repo/package operating rules when multiple agents or coding tools may work inside it. |
| `references/` | Structured support files: schemas, JSON, CSS tokens, usage rules, parsing notes, retrieval maps. |
| `examples/` | Known-good outputs the AI can inspect or imitate, including HTML, JSON records, `.fig` files, and component examples. |
| `assets/` | Static source material or output assets: icons, screenshots, sample files, visual references. |
| `agents/` | Role prompts for analyzer, comparator, grader, researcher, reviewer, or other specialist passes. |
| `scripts/` | Executable generation and review operations: Python, shell, packaging, indexing, or eval runners. |
| `scripts/validators/` | Deterministic checks that prove the output followed the package rules. |
| `evals/evals.json` | Test prompts and expected outcomes for skill or package evaluation. |
| `eval-viewer/` | Include only when this package owns its own human review UI. Otherwise reference the shared viewer. |

## Theme Or Design-System Example

For themes, put the theme-specific design knowledge inside the theme folder and keep structured references below `references/`.

```text
themes/
  README.md
  SKILL.md
  AGENTS.md

  references/
    theme-index.md
    theme-schema.md
    token-schema.md

  theme_A/
    README.md
    theme.md
    colors.md
    typography.md
    spacing.md
    layout.md
    components.md
    interaction.md
    accessibility.md
    voice-and-tone.md

    references/
      theme.json
      tokens.css
      usage.md
      component-map.json
      figma-notes.md

    examples/
      README.md
      theme_A.html

      components/
        component-examples.md
        theme_A_components.fig

      tokens/
        token-examples.md
        theme_A_tokens.fig

    assets/
      swatches.png
      sample-screens/

    agents/
      analyzer.md
      comparator.md
      grader.md

    scripts/
      render_preview.sh
      generate_examples.py
      run_eval.py

      validators/
        validate_tokens.py
        validate_components.py
        validate_accessibility.py
```

## Dictation To Structure

When the user describes this casually, translate intent into concrete names and responsibilities.

- "Stuff for the AI to read first" -> `SKILL.md` or `README.md`
- "Extra docs / notes / different file types" -> `references/`
- "Examples it can copy" -> `examples/`
- "Figma files showing the pattern" -> `examples/.../*.fig` or `references/.../*.fig`, depending on whether it is an example or source of truth
- "Images, icons, screenshots" -> `assets/`
- "Different reviewers" -> `agents/analyzer.md`, `agents/comparator.md`, `agents/grader.md`
- "Scripts that make it reliable" -> `scripts/`
- "Checks that prove it worked" -> `scripts/validators/`
- "Searchable memory / less token load" -> SQL tables, JSON records, vector index, or retrieval notes under `references/`, plus MCP tools that retrieve only the needed slice

## Evaluation Reminder

When creating or improving a skill-like package and evaluation is in scope, add this to the working checklist:

> Create evals JSON and run `eval-viewer/generate_review.py` so the human can review test cases.

For simple subjective writing or exploratory planning, do not force a full benchmark. For repeatable transformations, code generation, data extraction, or workflow automation, prefer real evals plus human review before treating the package as done.
