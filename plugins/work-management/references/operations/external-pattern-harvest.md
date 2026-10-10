## External Pattern Harvest

Use when a public repo, GitHub topic, skill marketplace, MCP example, agent
rulebook, or external workflow looks useful for Jonathan's local skills or
MCPs.

1. Default harvest is inspect-only. Do not install, run scripts, enable MCPs,
   wire configs, or copy executable code during the first pattern pass.
   Downloading/extracting source archives into a workspace cache for read-only
   review is allowed when Kyle explicitly asks for a thorough pass; executing
   anything from those archives is not.
2. Inventory the local target first: existing skill, MCP, protocol, or backlog
   file. Prefer improving an existing surface over creating a new one.
3. For a shallow pass, extract 5-8 reusable patterns as pattern cards with
   source, reusable pattern, local target, effort, impact, risk, first-pass
   action, and validation.
4. For a deep pass, inspect actual repo manifests, `SKILL.md` files, READMEs,
   command/mode docs, workflows, scripts, package manifests, MCP configs,
   examples, and tests. Compare them against all first-party local skills plus
   the relevant MCP workflow docs, not only the obvious target.
5. Prioritize low-effort, high-impact language and workflow tightening before
   new eval harnesses, validators, or MCP code.
   If the target is skill quality, trigger quality, or safety boundaries, use
   `skill-review-mini-rubric.md` before editing.
6. Patch at most one local artifact in a first pass unless the user asks for
   broader implementation. When Kyle explicitly asks for implementation, patch
   every owning surface needed to close the gap, including MCP workflow docs.
7. Create a new local skill only when the gap has no clear owner after checking
   existing skills, MCP docs, and backlog entries. Prefer a local wrapper skill
   over installing an external runtime when the external repo needs browser
   sessions, API keys, scrapers, or command execution.
8. Route any future copying, installing, executing, or MCP wiring through
   `personal-security-check` before touching the external artifact.
9. Verify with local discovery commands and record the result in
   `skill-mcp-improvement-backlog.md`. Capture durable memory only if the
   decision changes future work.
