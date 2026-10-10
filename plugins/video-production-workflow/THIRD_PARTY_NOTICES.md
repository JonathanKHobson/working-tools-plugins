# Third-Party Notices and Research Attributions

This plugin is original implementation code released under MIT. It was informed by public documentation and open-source workflow examples listed in `research/sources.lock.json`.

The production implementation is original. The preserved Sora skill source under `libraries/sora/` is vendored with its own Apache-2.0 notice; the other projects below informed the workflow design unless their entry says otherwise:

- **browser-use/video-use** (MIT): transcript-first editing, staged FFmpeg rendering, output-timeline caption math, and self-review discipline.
- **bradautomates/claude-video** (MIT): scene-aware visual sampling, transcript fallback, and explicit fidelity/token budgets.
- **AgriciDaniel/claude-shorts** (MIT): candidate scoring, boundary snapping, vertical reframing, caption styles, and post-export validation.
- **DojoCodingLabs/remotion-superpowers** (MIT): decomposed production rules, audio-led timing, and role-specific production agents.
- **OpenAI Skills** (per-skill licensing; skill-creator is Apache-2.0): progressive disclosure, scripts/references/assets structure, and Codex plugin metadata.
- **Installed Sora skill** (Apache-2.0): the conditional generated-clip reference adapts shot-brief structure, cinematic/social formats, iteration, and artifact checks from its `SKILL.md` and `references/{prompting,cinematic-shots,social-ads,sample-prompts}.md`. The complete historical source, including the obsolete Videos API CLI, API tables, network notes and `LICENSE.txt`, is preserved under `libraries/sora/`. Its current provider adapter marks API execution unavailable; retained code is not an active service or instruction to invoke it.

Optional tools retain their own licenses. In particular, Remotion uses a custom source-available/commercial licensing model, Blender and some analysis tools are copyleft, and platform documentation changes. The plugin invokes or documents them; it does not relicense them.

Additional optional external tools reviewed for production use include MediaInfo (BSD-2-Clause), ExifTool (Perl Artistic/GPL choice), Netflix VMAF (BSD-2-Clause-Patent), Shaka Packager (BSD-3-Clause), MediaConch (verify current component licensing), and QCTools (GPL application with BSD-licensed BAVC code). They are not vendored.

**Payton Bilodeau's AI Video Editing Pack** (custom Free Use Terms): reviewed for
editor setup reuse, edition-aware control and editable project delivery. New
Resolve guidance is independently authored; no upstream templates, scripts,
assets or skill text are vendored or relicensed. Exact revision, source evidence
and adoption limits: [review](research/AI_VIDEO_EDITING_PACK_REVIEW.md).

## Additional retained method libraries

- Animate, cth9191, pinned `7e5eb56feb2dd573f890e1b7b34748af43d58263`: MIT, `libraries/animate-methods/LICENSE`. Original notices and source manifest retained.
- Charlie motion methods, charlie947, pinned `4cd156acdad0483884867c2d5a22268db66099d1`: MIT, `libraries/charlie-motion-methods/source/LICENSE`.
- HyperFrames, heygen-com, pinned `f6b38216263e0f9a8d67b4518a9b5dde71284169`: Apache-2.0, `libraries/hyperframes-methods/source/LICENSE`. The selected source and notices are preserved without code modification.
- YouTube method evidence, Jakeschincariol, pinned `a2feb2104981a375ffd4f87ee04f4f5344ac43c6`: MIT, `libraries/youtube-agent-methods/LICENSE`. Historical Python is inactive `.py.txt`.
- Animated diagram adaptations: preserve all four upstream license/notice files in `libraries/motion-diagram-methods/notices/`; no upstream runtime, font, icon or GSAP bundle is shipped.

First-party portability modifications are described in `PUBLIC_DISTRIBUTION.md`; retained third-party source code and license/notice bytes are unchanged. License grants for repository source do not authorize distribution of independently obtained reference pixels or outside assets.

Professional role-contract lineage preserves MIT notices from AgentLand Contributors (agency-agents `5baafd5f`), VoltAgent (voltagent-subagents `721e9734`) and Seth Hobson (wshobson-agents `46891e7e`) under `references/professional-agents/source-notices/`. Local responsibility and method routing are original adaptations; original vendor copyright is retained.

Loom Review Packet and Loom Walkthrough Scripting, their full references, agent metadata and original Python helper are first-party procedures by Jonathan Kyle Hobson, included under the root MIT grant. No Loom provider code, private recording or actual client/session evidence is copied. The private recorded-workflow case is replaced by a complete explicitly fictional worked scenario, with source/output hashes and transformation scope retained.
