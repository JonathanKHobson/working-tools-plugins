# Capability Matrix: Existing AI Video Workflows vs. This Draft

**Reviewed:** 2026-07-22

Legend: **Strong** = first-class workflow; **Partial** = present but specialized; **Gap** = not a central capability.

| Capability | video-use | claude-video/watch | claude-shorts | remotion-superpowers | This draft |
|---|---:|---:|---:|---:|---:|
| Conversation-led strategy/approval | Strong | Partial | Strong | Strong | Strong |
| Source inventory/provenance | Partial | Partial | Partial | Partial | Strong |
| Transcript + word-level edit | Strong | Strong understanding | Strong | Partial | Strong/routed |
| Scene-aware visual inspection | Strong at decisions | Strong | Partial | TwelveLabs-oriented | Strong/routed |
| Music beat/energy/section analysis | Partial | Gap | Partial | Music generation/timing | Strong |
| Slideshow/mixed-orientation montage | Partial | Gap | Gap | Partial | Strong |
| Dialogue and multi-take editing | Strong | Understanding only | Short extraction | Partial | Strong |
| Typography/caption design | Strong examples | Gap | Strong presets | Strong Remotion | Strong/renderer-neutral |
| Motion-graphics engine selection | Strong multiple slots | Gap | Remotion | Remotion-focused | Strong multi-engine routing |
| Audio mix/loudness | Strong local rules | Gap | Partial | Strong integration | Strong standards-aware |
| Declarative renderer-neutral timeline | EDL-like | Gap | Segment JSON | Remotion compositions | Strong shared manifest |
| OTIO/EDL interchange | Gap | Gap | Gap | Gap | Strong |
| Multi-aspect/platform conform | Partial | Gap | Strong shorts platforms | Partial | Strong/reverify policy |
| Automated + visual QA | Strong cut review | Partial input inspection | Strong output validation | Review patterns | Strong evidence bundle |
| Cache/provenance/license governance | Strong transcript cache | Strong setup/cache ideas | Partial | Partial | Strong |
| Plugin evolution/evaluation | Gap | Gap | Gap | Partial | Strong |

## Interpretation

The existing ecosystem is not “missing video production.” It contains strong vertical slices. The unfilled need is the connective architecture: a shared editorial contract, cross-renderer routing, music-aware pacing, design/accessibility rules, interchange, provenance, and evidence-producing QA.

This draft should therefore be merged with or route to existing high-quality skills rather than replacing them wholesale. The handoff prompt explicitly asks Codex to inventory installed skills and choose extension, merge, orchestration, or new-plugin architecture.

## Resolve integration review — 2026-10-07

| Capability | Existing owner before change | Decision |
| --- | --- | --- |
| Editorial/audio/color/caption/motion craft | Existing stage skills and references | Keep; no duplicate pack family |
| Edition-aware native Resolve import/finishing | Gap | Add narrow `edit-davinci-resolve` owner |
| Editable import/save/reopen/export/reimport proof | Generic interchange only | Extend `exchange-video-timelines` |
| FCPXML generation/native MCP runtime | No verified local implementation | Defer; document limits and use supported import/UI route |

See [source/adoption review](AI_VIDEO_EDITING_PACK_REVIEW.md). Pack methods are
guidance only; runtime acceptance requires an editor test on the actual host.

## Original-motion default and reuse — 2026-10-07

Existing five stage owners now share a default art-direction contract. The supplied handoff adds controlled candidate comparison and project-owned accepted style evidence, without another skill, style catalog or required 3D runtime. See [adoption review](ART_DIRECTION_HANDOFF_REVIEW.md).
