# Output and review providers

Career Studio owns career evidence, positioning, packet choices, and application state. Use a provider only when the requested artifact needs it and its installed capability is actually discovered; load that provider's current skill at the point of work. If absent, use this studio's evidence map, 3–8 observed visual anchors with changed-anchor rechecks, and direct plain-language review. Report an unavailable export or render format rather than claiming it was inspected.

| Requested output or review | Current provider | Studio responsibility |
| --- | --- | --- |
| Editable Word document | `documents:documents` (or `doc` where that is the available host capability) | Supply reviewed career claims and compare final text to the evidence map. |
| PDF export or inspection | `pdf:pdf` | Inspect rendered pages, selectable text, links, and private metadata. |
| Editable slide deck | `presentations:presentations` | Preserve the same case facts, role, and artifacts used in the site and resume. |
| Website implementation | `build-web-apps:frontend-app-builder` or the existing project's framework | Supply case content and public-safe assets; preserve the owning checkout and current site language. |
| Sites preview or hosting, when requested | `sites:sites-building` and `sites:sites-hosting` | Verify the exact served route and employer-accessible links after publication. |
| UX and visual design review | `ux-design-toolkit:design-studio`; use `figma-design-workflow:design-visual-qa` for Figma source comparisons | Record 3–8 visual anchors and recheck the changed surfaces. |
| Narrative and prose quality | `writing-quality-studio:communication-crafter` | Keep the candidate's voice and every claim defensible. |

For Word, slides, sheets, and PDF tooling in Codex desktop, call `mcp__codex_app__load_workspace_dependencies` when runtime paths are needed. This Codex desktop helper is not a Claude Code or ChatGPT capability claim. These providers remain separate owners; this plugin does not copy their engines or infer authorization to publish, send, or submit.
