> Historical source evidence with receiving-host-neutral locators. Listed configuration, availability, old observations and changes are not current facts or instructions for the recipient. Inspect actual callable capabilities and preserve active jobs before acting. No private config or corpus is supplied.

# Skill Provenance Catalog

Last refreshed: 2026-06-19, Round 10

This is a lightweight routing and provenance reference for Jonathan's
first-party Codex skills. It is not the authoritative runtime registry; the
runtime source of truth is the actual `SKILL.md` files under
`~/.codex/skills`.

Use this catalog when deciding whether a skill rule came from shipped local
practice, project-specific craft, platform/API documentation, maintenance and
debugging experience, external inspiration, deprecated compatibility, or an
uncertain origin that needs review.

## Provenance Classes

| Class | Meaning |
| --- | --- |
| `local-shipped-workflow` | Encodes a workflow Jonathan has used locally or repeatedly shipped through Codex. |
| `local-project-craft` | Encodes Jonathan-specific craft judgment, writing practice, design taste, or project methods. |
| `platform-api-docs` | Depends primarily on current official product, API, platform, or tool documentation. |
| `maintenance-debugging` | Encodes local machine, storage, MCP, browser, GitHub, or operational troubleshooting practice. |
| `external-inspiration` | Incorporates a named external framework, library, or externally inspired method. |
| `deprecated-compatibility` | Kept mainly so old routing still works while a newer local skill is preferred. |
| `needs-review` | Origin is not clear from the current `SKILL.md`; review before treating it as local policy. |

## First-Party Skill Rows

| Skill | Path | Primary lane | Provenance class | Basis/source note | Review status |
| --- | --- | --- | --- | --- | --- |
| `chatgpt-apps` | `~/.codex/skills/chatgpt-apps/SKILL.md` | ChatGPT Apps SDK build and troubleshooting | `platform-api-docs` | Docs-first OpenAI Apps SDK workflow with local scaffold conventions. | seeded |
| `chronicle` | `~/.codex/skills/chronicle/SKILL.md` | Chronicle screen-history access | `needs-review` | Skill exists locally, but provenance and policy source should be reviewed before broad reuse. | needs-review |
| `cloudflare-deploy` | `~/.codex/skills/cloudflare-deploy/SKILL.md` | Cloudflare deployment | `platform-api-docs` | Platform deployment guidance grounded in Cloudflare products and docs. | seeded |
| `communication-story-crafter` | `~/.codex/skills/communication-story-crafter/SKILL.md` | Audience-aware storytelling and stakeholder communication | `local-project-craft` | Local communication craft extracted from Jonathan's recurring story, pitch, and stakeholder work. | seeded |
| `cover-letter-crafter` | `~/.codex/skills/cover-letter-crafter/SKILL.md` | Cover letter writing and audit | `local-project-craft` | Local job-search writing practice with truthfulness and evidence constraints. | seeded |
| `critical-compass` | `~/.codex/skills/critical-compass/SKILL.md` | Critical-thinking audit and reasoning checks | `external-inspiration` | Compass-family reasoning framework influenced by critical-thinking libraries and local workflow. | seeded |
| `current-social-research` | `~/.codex/skills/current-social-research/SKILL.md` | Recent public/community sentiment and current-source research | `external-inspiration` | Round 9 local wrapper inspired by current-web/social research skills such as `last30days`, with local safety, citation, and Shareables gates instead of external runtime install. | seeded |
| `design-taste-gate` | `~/.codex/skills/design-taste-gate/SKILL.md` | Design-quality review | `local-project-craft` | Local visual craft gate for frontend and artifact polish. | seeded |
| `develop-web-game` | `~/.codex/skills/develop-web-game/SKILL.md` | Web-game implementation loop | `local-shipped-workflow` | Local Playwright-backed game development and verification workflow. | seeded |
| `discord-bot-mcp-setup` | `~/.codex/skills/discord-bot-mcp-setup/SKILL.md` | Discord bot plus MCP setup | `maintenance-debugging` | Local token, invite, and MCP wiring practice for Discord-backed servers. | seeded |
| `doc` | `~/.codex/skills/doc/SKILL.md` | `.docx` document work | `local-shipped-workflow` | Local document-generation workflow using `python-docx` and render checks. | seeded |
| `figma` | `~/.codex/skills/figma/SKILL.md` | Figma MCP read and design context | `platform-api-docs` | Figma MCP workflow plus local design-to-code conventions. | seeded |
| `figma-implement-design` | `~/.codex/skills/figma-implement-design/SKILL.md` | Figma-to-code implementation | `platform-api-docs` | Figma MCP screenshot/context workflow for production implementation. | seeded |
| `frontend-ux` | `~/.codex/skills/frontend-ux/SKILL.md` | UX-aware frontend implementation review | `local-project-craft` | Local frontend UX judgment, accessibility, and state-coverage practice. | seeded |
| `game-designer` | `~/.codex/skills/game-designer/SKILL.md` | Game systems design and critique | `external-inspiration` | Uses established game-design concepts adapted into a local skill. | seeded |
| `gh-address-comments` | `~/.codex/skills/gh-address-comments/SKILL.md` | GitHub review or issue-comment handling | `maintenance-debugging` | Local `gh` CLI workflow for addressing open PR feedback. | seeded |
| `gh-fix-ci` | `~/.codex/skills/gh-fix-ci/SKILL.md` | GitHub Actions CI diagnosis | `maintenance-debugging` | Local `gh` CLI workflow for checks and log-driven fixes. | seeded |
| `imagegen` | `~/.codex/skills/imagegen/SKILL.md` | OpenAI image generation and editing | `platform-api-docs` | OpenAI Image API CLI workflow with local credential boundary. | seeded |
| `github-conventions` | `~/.codex/skills/github-conventions/SKILL.md` | Jonathan's GitHub account and repo conventions | `maintenance-debugging` | Jonathan-specific GitHub account, repo, branch, and upload practice. | seeded |
| `mac-environment-conventions` | `~/.codex/skills/mac-environment-conventions/SKILL.md` | Mac storage and runtime placement | `maintenance-debugging` | Jonathan-specific Mac and external-drive placement conventions. | seeded |
| `mac-troubleshooter` | `~/.codex/skills/mac-troubleshooter/SKILL.md` | Mac app and process troubleshooting | `maintenance-debugging` | Local Mac process, window, cache, and relaunch recovery workflow. | seeded |
| `obsidian-vault-router` | `~/.codex/skills/obsidian-vault-router/SKILL.md` | Obsidian vault routing and edits | `maintenance-debugging` | Jonathan-specific vault, graph, metadata, and routing conventions. | seeded |
| `storage-memory-manager` | `~/.codex/skills/storage-memory-manager/SKILL.md` | Disk, cache, and memory cleanup triage | `maintenance-debugging` | Local Mac storage/memory cleanup and external-drive safety practice. | seeded |
| `focus-ops-manager` | `~/.codex/skills/focus-ops-manager/SKILL.md` | Focus, sequencing, accountability, and project routing | `local-shipped-workflow` | Jonathan-specific operating-manager rules for shipping over scaffolding. | seeded |
| `prompt-playbook` | `~/.codex/skills/prompt-playbook/SKILL.md` | Jonathan's recurring prompt patterns | `local-project-craft` | Local prompt-writing patterns and corrections. | seeded |
| `lavish-axi` | `~/.codex/skills/lavish-axi/SKILL.md` | Local HTML artifact review-loop pilots and Shareables annotation/layout-gate adaptation | `external-inspiration` | Round 10 local wrapper inspired by `kunchenguid/lavish-axi`, preserving sandbox, safety-review, and no-runtime-export boundaries instead of installing the external CLI by default. | seeded |
| `local-data-mcp-builder` | `~/.codex/skills/local-data-mcp-builder/SKILL.md` | Local data-backed MCP design and hardening | `local-shipped-workflow` | Local MCP builder practice from Compass, storage, Atlas, and KSB hardening. | seeded |
| `local-mcp-debugging` | `~/.codex/skills/local-mcp-debugging/SKILL.md` | Local MCP attach, launcher, and agent-behavior debugging | `maintenance-debugging` | Local Codex/Claude MCP failure modes and repair patterns. | seeded |
| `local-storage-mcp` | `~/.codex/skills/local-storage-mcp/SKILL.md` | Local file/storage evidence lookup | `maintenance-debugging` | Local storage catalog and machine-convention retrieval workflow. | seeded |
| `native-macos-app-builder` | `~/.codex/skills/native-macos-app-builder/SKILL.md` | Native macOS app building | `platform-api-docs` | Apple/Xcode/Swift implementation guidance with local build preferences. | seeded |
| `openai-docs` | `~/.codex/skills/openai-docs/SKILL.md` | OpenAI API and product documentation | `platform-api-docs` | Official OpenAI docs-first workflow. | seeded |
| `pattern-picker` | `~/.codex/skills/pattern-picker/SKILL.md` | Thinking-framework selection | `external-inspiration` | Framework library and reasoning-pattern selection method. | seeded |
| `pdf` | `~/.codex/skills/pdf/SKILL.md` | PDF reading, generation, and visual review | `local-shipped-workflow` | Local PDF extraction/generation/rendering workflow. | seeded |
| `personal-security-check` | `~/.codex/skills/personal-security-check/SKILL.md` | External artifact security review | `maintenance-debugging` | Local practical security gate for apps, MCPs, packages, repos, and scripts. | seeded |
| `plain-to-dev` | `~/.codex/skills/plain-to-dev/SKILL.md` | Translate fuzzy ideas into engineering terms | `local-project-craft` | Local product-to-engineering translation practice. | seeded |
| `playwright` | `~/.codex/skills/playwright/SKILL.md` | Browser automation from terminal | `platform-api-docs` | Playwright CLI/browser automation workflow with local cleanup expectations. | seeded |
| `playwright-interactive` | `~/.codex/skills/playwright-interactive/SKILL.md` | Persistent browser/Electron interaction | `local-shipped-workflow` | Local iterative UI debugging, screenshot, and browser-handoff workflow. | seeded |
| `portfolio-crafter` | `~/.codex/skills/portfolio-crafter/SKILL.md` | Portfolio case-study writing and audit | `local-project-craft` | Local career/portfolio writing practice with evidence and confidentiality constraints. | seeded |
| `prd-strategist` | `~/.codex/skills/prd-strategist/SKILL.md` | PRDs, roadmaps, and product specs | `external-inspiration` | Product-management frameworks adapted to local delivery planning. | seeded |
| `resume-crafter` | `~/.codex/skills/resume-crafter/SKILL.md` | Resume writing and audit | `local-project-craft` | Local job-search writing practice with ATS and evidence constraints. | seeded |
| `safe-install-review` | `~/.codex/skills/safe-install-review/SKILL.md` | External install and command safety review | `maintenance-debugging` | Compatibility/sibling safety-review skill; compare with `personal-security-check` before extending. | seeded |
| `screenshot` | `~/.codex/skills/screenshot/SKILL.md` | OS-level screenshot capture | `maintenance-debugging` | Local capture fallback for desktop/system screenshots. | seeded |
| `sora` | `~/.codex/skills/sora/SKILL.md` | OpenAI Sora video generation workflow | `platform-api-docs` | OpenAI video API CLI workflow with local credential boundary. | seeded |
| `speech` | `~/.codex/skills/speech/SKILL.md` | OpenAI speech/audio generation | `platform-api-docs` | OpenAI Audio API CLI workflow with local credential boundary. | seeded |
| `transcribe` | `~/.codex/skills/transcribe/SKILL.md` | Audio/video transcription | `platform-api-docs` | OpenAI transcription workflow with optional diarization conventions. | seeded |
| `ux-heuristic-compass` | `~/.codex/skills/ux-heuristic-compass/SKILL.md` | UX heuristic audits and reports | `external-inspiration` | Compass-family UX heuristic framework and local report workflow. | seeded |
| `ux-oracle` | `~/.codex/skills/ux-oracle/SKILL.md` | Legacy UX routing | `deprecated-compatibility` | Deprecated compatibility router; prefer newer UX skills named in its description. | seeded |
| `ux-writer` | `~/.codex/skills/ux-writer/SKILL.md` | Product microcopy and UX writing | `local-project-craft` | Local UX writing judgment and product-copy practice. | seeded |

## Review Notes

- This catalog intentionally uses coarse labels. A skill may combine local
  practice and external ideas; the class names the dominant provenance signal
  visible from the current skill body.
- This seed began with the first-party inventory command used in the harvest
  test plan. Symlinked external skill roots, such as externally hosted package
  skills, are out of scope for this first-party catalog. Round 10 adds
  `lavish-axi` as an external-inspiration wrapper for a real uncovered review
  loop while keeping external runtime adoption separate from skill routing.
- `needs-review` is a safety label, not a defect. Use it when provenance is
  unclear instead of inventing a source.
- Before changing a skill because of this catalog, use
  [skill-review-mini-rubric.md](skill-review-mini-rubric.md) and fix only
  critical or major issues by default.
