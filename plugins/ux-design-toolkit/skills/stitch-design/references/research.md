# Research and adoption decisions

Reviewed **2026-09-08**. These methods contain original workflow text; upstream code and skill files are not vendored. This UX plugin is independent, not a Google product or endorsement. Capabilities and interfaces can change.

## Primary Google sources

- [Google Labs: Stitch skills](https://github.com/google-labs-code/stitch-skills): a maintained source of design/build/utility workflow examples under Apache-2.0. The repository's documented workflows require Stitch MCP. Adopt its useful separation of prompt refinement, design-system management, generation, and code reconciliation; provide an original browser workflow here instead of pretending MCP calls are available. Its own notice says it is not an officially supported Google product.
- [Stitch updates, May 19, 2026](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-updates/): richer contextual design, steering, and handoff possibilities. Treat each destination as something to verify in the current UI.
- [Stitch UI design, March 18, 2026](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/): canvas/context, design-system and prototype workflows inform the conditional system and flow methods.
- [DESIGN.md announcement, April 21, 2026](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/) and [spec repository](https://github.com/google-labs-code/design.md): current portable design-system work includes structured tokens and prose. Consult the live specification; do not assume an old Markdown-only skill template is sufficient.
- [Stitch prompting documentation](https://stitch.withgoogle.com/docs/learn/prompting/): useful official entry point, but text was not extractable in the research browser. No unverified detail from it is asserted here.

## Author-maintained community comparisons

- [Stitchflow](https://github.com/Leon-llb/stitchflow): manual browser-first process from brief to screenshot and export. Its profile-copying, browser-killing/debug-launch recipes, fixed selectors, and fixed model assumptions were not adopted. Use the user's existing supported browser session instead.
- [Stitch to Code](https://github.com/nassim-arifette/stitch-to-code): useful focus on reconciling generated screens, fonts, icons, and actual behavior. Reuse the principle, not framework-specific assumptions.
- [Stitch to Next.js](https://github.com/yshaish1/stitch-to-nextjs): illustrates implementation/render comparison; its MCP/Next.js requirements are not prerequisites for this plugin.

## Applied project lessons

- Preserve the user's draft and contextual attachments during screen selection/export.
- One theme/token source controls continuity; prompt text must not fight it.
- Shared global navigation and page-local navigation have separate roles.
- More authentic screenshots and concise supported claims improve evidence density; generated presentation art does not establish history or outcomes.
- Inspect actual exported files and implemented renders. A prototype is not a working form or verified delivery.
- Wait for fonts/images/layout after responsive or text-size changes; no-overflow checks do not prove every navigation destination is available.
- Respect project-specific icon/format rules without rewriting original historical screenshots.
- Keep review/QA material private and preserve source originals.
