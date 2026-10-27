# Public runtime projections

- `hooks/hooks.json`: Only generic UserPromptSubmit editorial route is public; private author-host Gmail sender gate remains excluded.

The author-host Gmail sender gate and its private binding are not distributed. The default public hook routes final wording review only; it does not enforce sending authorization.

Claude loads `hooks/hooks.json` automatically. The public Claude manifest adds no second copy of these handlers. Shared commands resolve the installed Codex or Claude plugin root. Compatibility hook files remain templates; no private Gmail sender gate is included.
