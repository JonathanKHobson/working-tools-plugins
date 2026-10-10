---
name: video-templates
description: Browse video template families and exact examples, inspect staged style methods, or create and revise an editable storyboard before production.
---

# Video Templates

Use the existing `video-style-library` tools. Assistant-only discovery starts with `search_video_styles`, then `read_video_style`. Use `browse_video_styles` when the person is choosing visually. Families and distinct examples retain master hashes, review limits, rights, prerequisites and download availability. The seven `method/*` records are staged references, not finished films or production approvals.

Bind a selected family, exact example ID and current master hash through `prepare_video_style_handoff`. Reject stale selections. Read [DESIGN.md](../../DESIGN.md) before adapting the catalog or its chooser. Review [rights and dependencies](../../docs/rights.md); a download link is not a new license. Executable source and media remain in their originating packages/projects.

For storyboarding, create a useful shot draft with `create_video_storyboard`, then read and patch the saved revision. Open the populated editor for co-creation; autonomous production can use the same backend without opening it. Inspect per-shot media with `read_video_storyboard_media`. Preserve sketches/references, stable shot IDs and unrelated fields; default reads redact reference bytes, so use focused patches or `include_media=true` for deliberate whole-board replacement. Repeat operation IDs only for identical retries. Unsaved browser edits are not visible to the assistant.

`prepare_video_storyboard_draw_handoff` prepares a separate Draw and Think request. Creation and opening there remain separate verified steps, and later changes require explicit translation back into the source storyboard. There is no automatic synchronization.

Video Production Studio owns story timing, motion generation, editing, audio, captions, native editor handoff and render QA. Graphic Design owns art direction. Saving a storyboard or selecting a template is not finished film approval. Keep project media, private storyboard SQLite data and approval evidence external. [Onboarding](../../docs/onboarding.md) defines portable startup and external bindings.
