---
name: skill-authoring
description: Maintain the recipient's local skill routing, ownership, and evidence when creating, consolidating, or updating skills and plugins. Use the bundled skill-creator for general authoring mechanics; this adds local integration rules.
---

# Recipient Skill Maintenance

Use the available `skill-creator` for general authoring. This file contains only
recipient-specific integration rules. Prefer improving the existing owner over a
new skill, plugin, router, hook, or runtime.

## Ownership and size

- Read the full entrypoint of each skill being changed. Distinguish source,
  installed cache, and standalone copies before editing. Update the source and
  reinstall through the supported plugin path; do not patch vendor caches.
- A new skill needs a distinct trigger, output, or operational boundary.
  Package related skills together for distribution without merging every
  workflow into one prompt. Keep only one authoritative implementation.
- Keep names/descriptions short and specific. Keep shared constraints in the
  entrypoint; put substantial conditional detail in a reference with a clear
  read trigger. Remove generic tutorials and duplicated global instructions.
- Use scripts for repeated deterministic work. Do not create a new runtime
  merely to route Markdown or a validator that only matches its own wording.
- Extract lessons from finished task evidence: failure, corrected behavior,
  proof, and scope. Keep product-specific facts in a project reference; do not
  turn one incident into a universal rule or old approval into new authority.

## Routing and validation

When a common entrypoint or next hop changes, update only the affected family
in `../../references/skill-routing-index.md` and `.json`.
Prefer 1–3 meaningful neighbor links over catalog copies in every skill.
Run:

```sh
python3 ${RECIPIENT_ROUTING_AUDIT}
```

Use the skill-creator's `quick_validate.py` for changed entrypoints, check local
reference targets, and run changed scripts with representative inputs. On this Mac,
run these validators with
`${SKILL_VALIDATION_PYTHON}`
(native Python with PyYAML). The system Python shim may require Xcode license
acceptance; do not accept a license to run a content validator. If this runtime
is missing, report the dependency rather than substituting an unvalidated check. For a
substantial routing or delegation change, have an independent worker try a few
realistic tasks, including a task that should bypass the skill. Check decisions
and observable outputs, not just frontmatter. Report untested behavior honestly.

## External adoption

Inspect primary source, license, exact files, hooks, dependencies, credential
access and network behavior before importing. Start with useful patterns in
the existing skill. Use `personal-security-check` before executing or wiring
external code; the user's existing authorization governs whether further
permission is needed. No unrequested telemetry, persistent agent, paid runtime,
account mutation, or browser-profile access.

For a broader harvest, use only the External Pattern Harvest section of
`../../libraries/focus-ops-manager/references/codex-operating-protocols.md`. Record a short
adopt/defer/reject decision with sources in the existing improvement backlog.
Do not add a second catalog or a recurring maintenance job without need.

## Onboarding changes

For a plugin or skill introduction, discovery description, first-use flow, support-file route or MCP help change, apply the maintained Work Management [human and agent onboarding standard](../../references/plugin-maintenance.md#human-and-agent-onboarding). Keep purpose and selection metadata brief, explain when each support file is needed, and verify human guidance separately from installed/runtime capability.

Apply `writing-quality-studio:natural-prose-editor` and its technical-clarity
reference to authored instructions. That method owns economical wording and
the progression from startup description through orientation and procedure to
conditional depth. Review repetition and negative instructions while preserving
the conditions and checks needed for the task. Verify selection and execution
after shortening.

The receiving host must supply `RECIPIENT_ROUTING_AUDIT` and `SKILL_VALIDATION_PYTHON` before the illustrated host-specific validators can run. A missing validator is reported as unverified. No validator, global hook or recurring job is installed by this method.
