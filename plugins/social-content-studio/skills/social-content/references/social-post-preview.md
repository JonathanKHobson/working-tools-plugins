# Social Post Previewer handoff

The existing Social Post Previewer app supplies image generation and post mockups when its tools are available. Discover its callable tools in the current tool inventory. Do not copy the app or infer a post was published from a preview.

## Select the correct operation

- When the user asks to **generate or create a new social media post** and the Social Post Previewer tools are available, call `social_post_previewer_generate_social_post_image` first with a concise visual headline and subheadline, brand name if known, and the target supported platform. It returns `imageUrl` and `altText`. Pass that exact `imageUrl` into `social_post_previewer_preview_generated_social_post` with the caption; do not alter or rehost it. If the user explicitly wants text only, provide that text or the explicit text-only mockup without generating an image.
- For **supplied image URLs or local images**, or an explicit **text-only mockup**, use `social_post_previewer_preview_social_post`. Pass supplied image URLs unchanged; use absolute paths for local images. A missing image is acceptable only for an explicit text-only preview.
- `social_post_previewer_get_preview_app_info` is a capability check, not a posting tool. Supported app preview platforms are `threads`, `instagram`, `facebook`, `twitter`, `youtube`, `tiktok`, and `instagram_story`; do not pretend that an unsupported platform has a native preview.

Keep post title, description, tag, author name/handle/avatar aligned with supplied or verified content. A preview may show cropped text or imagery; inspect the rendered result when available. Record 3–8 anchors: source/viewport, region, observed fact, and intended correction; verify changed anchors before signoff. Check readable headline, crop/safe area, account identity, CTA/link rendering, image order, contrast, and alt text. If the app cannot render or inspect the result, state that visual QA is unverified.

Never treat generate, preview, draft, schedule, and publish as the same state. Use `social-content-studio:social-publishing` for authorized platform actions and readback.

## Packaged app and host compatibility

Social Content Studio owns the app dependency `asdk_app_69457f83763881918ea06cc67fc9b6b0` through its root `.app.json`. Native Codex installation resolves its metadata; connection/authentication is separate. Its tools are `get_preview_app_info`, `generate_social_post_image`, `preview_generated_social_post` and `preview_social_post`. Read their current schemas and verify a live capability call before claiming availability. Supported platforms returned by the live info tool during the 2026-09-29 audit were Threads, Instagram feed, Facebook, X/Twitter, YouTube, TikTok and Instagram Story. LinkedIn was not in that list; a past receipt does not establish a current connection.

If installation reports `appsNeedingAuth`, complete the app connection through the host, then retry the read-only capability call. A package in the cache or a tool name in discovery is insufficient. Keep a canonical provider wrapper when the host requires it for execution; it is a provider dependency, not a second owner of this workflow. Before removing one, verify both the intended dependency and post-removal execution, and restore/reconnect it if the call fails.

For a newly generated visual post, the provider contract requires image generation first and the exact returned image URL passed to the generated-post preview. For supplied content/image or an explicitly text-only preview, use the supplied-content preview route; preserve supplied URLs/files and caption fields. Preview is not publishing. Do not send an actual post, schedule it or claim platform state from a mockup.

Claude does not ingest Codex `.app.json` declarations. The same complete preview workflow is installed there, but provider execution requires a genuinely available Claude connector or authorized browser route. Do not invent an MCP endpoint or pretend the Codex app was cloned. Provider-supported previews stay conditional on actual host capability.
