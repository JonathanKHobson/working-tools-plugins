# Public runtime projections

- `plugin.portable.json`: Keep root Agent Plugins metadata from bypassing native hook discovery.

REA uses the recipient configured external runtime and integrity binding. No analysis engines, credentials or private host binding are bundled.

Claude loads `hooks/hooks.json` automatically. The public Claude manifest adds no second copy of these handlers. Shared commands resolve the installed Codex or Claude plugin root. Compatibility hook files remain templates; no private Gmail sender gate is included.
The shared SubagentStart command selects the existing generic input contract under Claude and preserves the explicit Codex parent-session contract under Codex. It adds no hook event or permission.
