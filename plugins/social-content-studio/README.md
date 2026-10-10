# Social Content Studio

Create source-grounded social posts and derivatives, plan a calendar, review or preview copy, and carry an authorized publish or schedule through platform readback.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Draft one LinkedIn post from this finished case and my voice sample.” | Verified case facts and voice | Ready-to-review post with claim and link checks |
| “Adapt this article into a carousel and short-video script.” | Source article and target channels | Distinct formats preserving the original claim |
| “Schedule this approved post and verify the platform entry.” | Approved asset, account and time | Observed scheduled state or a precise blocker |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/social-content/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Use the [full task-to-skill map](docs/use-case-map.md). A single post uses social-content; calendar, adaptation, video, preview, review and publishing have distinct owners.

| Task / skill | What it produces |
| --- | --- |
| [channel-adaptation](skills/channel-adaptation/SKILL.md) | Repurpose a grounded source into platform-fit posts, threads, newsletters or carousel copy without changing its claim. |
| [content-calendar](skills/content-calendar/SKILL.md) | Plan social calendars and LinkedIn weeks, audit supplied post analytics, and coordinate source-linked course/video/article releases with verified publication states. |
| [professional-social-proof](skills/professional-social-proof/SKILL.md) | Package verified work into social proof campaigns and public derivatives with assets, links and follow-up tracking; Career owns LinkedIn profile positioning and section audits. |
| [short-form-video](skills/short-form-video/SKILL.md) | Write social reels and short-video scripts, or route animated and narration-led short-form stories into media production with captions and accessible handoff. |
| [social-content](skills/social-content/SKILL.md) | Draft grounded social posts, LinkedIn hooks, comments and reply threads from source facts and voice samples. Use the dedicated calendar, channel-adaptation, short-video, professional-proof, editorial-review, preview or publishing skill for those specific tasks. |
| [social-editorial-review](skills/social-editorial-review/SKILL.md) | Review social copy for source support, voice, channel fit, privacy, readability and actual publication readiness. |
| [social-preview](skills/social-preview/SKILL.md) | Render or review a social post mockup through the Studio’s Social Post Previewer app, using supplied assets or requested generated imagery. |
| [social-publishing](skills/social-publishing/SKILL.md) | Carry authorized social publishing or an established course/video/article handoff through account checks, native scheduling and verified readback. Distinguish drafts, reservations, schedules and publication; follow narrower user instructions first. |

## Recipient setup

Install this package into your Codex or Claude plugin host, then choose the matching skill from the task map. Supply your own source facts, voice samples, audience, platform account and authorization in your project. No personal account, sample, credential or posting policy is bundled. For the complete optional AIHumanizer social prose method, install and enable the official `aihumanizer@openai-curated-remote` plugin and load `aihumanizer:social-media` through the [provider handoff](references/social-methods/provider-social-prose.md). If it is unavailable, the first-party drafting and review methods still work and the response should identify that missing dependency. Other named Studios are optional specialist dependencies for their respective routes.


## Host compatibility

| Capability | Codex | Claude Code |
| --- | --- | --- |
| First-party skills and packaged methods | Native installation and synthetic first-use verified | Native installation and file parity verified; first-use behavior still needs a host test |
| AIHumanizer provider method | Separately install `aihumanizer@openai-curated-remote`; matching skill verified | That Codex marketplace identity is not a Claude installation route. Use the packaged first-party methods unless an authorized equivalent provider route is verified |
| Social Post Previewer | Requires the declared OpenAI app and an available connection; live rendering untested | The OpenAI app declaration does not supply a Claude app. Use an available preview tool only after checking the host, or deliver clearly labeled copy without claiming a rendered preview |

## Availability and recovery

This package has no `.mcp.json`. The optional Social Post Previewer app is declared separately in `.app.json`; verify its availability and rendering for a visual preview. Native publishing depends on the selected platform/account and authorization. A prepared draft or mockup is not scheduled or public; verify the actual platform state and URL for those claims. If a provider is unavailable, preserve the draft and exact next route.

See [project map](docs/project-map.md) and [use-case map](docs/use-case-map.md) for ownership and conditional methods. Private accounts, voice samples, platform policy, assets and receipts stay in the owning project. This directory is the maintained source for both local and public distributions; installed copies are generated. See [licensing](LICENSING.md) and [third-party notices](THIRD_PARTY_NOTICES.md).

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->
