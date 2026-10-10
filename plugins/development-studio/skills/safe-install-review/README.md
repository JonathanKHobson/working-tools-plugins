# Safe Install Review

`safe-install-review` is a shareable skill for practical software safety
reviews before installing, running, wiring, copying, or adapting external code.
It is meant for evidence-based risk reduction, not formal penetration testing,
enterprise compliance, or a guarantee that something is safe.

## Included Files

- `SKILL.md` - the AI entrypoint and review workflow
- `references/threat-catalog.md` - durable threat patterns, review actions, and
  inspection command references

## When To Use

Use this skill for questions like:

- "Is this app safe to install?"
- "Can I run this curl install command?"
- "Review this MCP before I wire it into my agent."
- "Check this repo/package for malicious concerns before I copy from it."
- "Verify this download/checksum before I run it."

## How To Install

Copy the `safe-install-review` folder into the skill directory used by your AI
coding tool or agent environment. The final layout should look like this:

```text
safe-install-review/
  README.md
  SKILL.md
  references/
    threat-catalog.md
```

After copying it, start a new agent/chat session or reload skills if your tool
requires a restart before new skills are discovered.

## Review Output

The skill returns a practical verdict:

- `Proceed`
- `Proceed with caution`
- `Do not install yet`

Each review should also identify confidence, inspected evidence, checked threat
surfaces, risks found, unknowns, a safer path, commands run or not run, and a
final recommendation.

## Boundaries

This skill should inspect before running, mark uncertainty plainly, and avoid
broad reassurance. It should not install new scanners, create quarantine
folders, wire unreviewed MCPs, run unknown lifecycle scripts, or claim formal
security signoff unless the user explicitly asks for a separate security
workflow and provides the needed context.
