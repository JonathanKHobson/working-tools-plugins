# GSAP method provenance

Adapted from [GreenSock's official skill repository](https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760) at `aed9cfd3277740755f6bfc1155c7aa645403b760`. Copyright (c) 2026 GreenSock; full MIT notice in [LICENSE](LICENSE). The documentation license is distinct from the actual GSAP runtime's license and installation state.

Preserved complete selected core, timeline, React, ScrollTrigger and performance procedures, including their operative examples and checks. Changes remove broad default recommendations and safety claims; replace installer commands with a runtime boundary; scope teardown to owned objects; correct horizontal displacement units/`Max.max`, refresh-priority direction, callback cancellation claims and unsupported compositor/scrub performance claims. Timeline position descriptions now distinguish the recently added animation from the timeline end. Other framework/plugin/utility methods, examples, manifests and installer paths are excluded; use primary documentation when one is actually needed.

Original selected file SHA-256 values:

- `skills/gsap-core/SKILL.md`: `3887b47e050ab5afbe2a9a820f23d39fa02ab785e06a343be44c6f91d84d12b3`
- `skills/gsap-performance/SKILL.md`: `cb5408d6fba707aabcbfe3320317a14c1f8fca6070074e5261047930f50d441e`
- `skills/gsap-react/SKILL.md`: `88e2a5312b45e8cc7b3c496637ff5bc9af2ae9c925b555c8b235b34cbc989d74`
- `skills/gsap-scrolltrigger/SKILL.md`: `9351b6666a4749c0740406ea363aaccb99a087ff45cc5e8b99a0f367facf3ef4`
- `skills/gsap-timeline/SKILL.md`: `1a8b0f39cc4be3ed3d834b89672e4ae2f151b901dc3450bebf10bbc45379fe02`

## Added conditional plugin depth

`plugins-svg-text-flip.md` adapts the official SVG DrawSVG/MorphSVG/MotionPath, SplitText/ScrambleText and Flip methods for scoped UX implementation, focus, reduced motion and rendered QA. `plugins-svg-text-flip-official.md` retains the complete selected upstream sections and examples with three Flip option descriptions corrected against primary documentation (`nested`, `scale`, `simple`), plus two MotionPath cautions (`alignOrigin` default and `curviness` scope), without the unrelated plugin catalog or installer text. The original `skills/gsap-plugins/SKILL.md` SHA-256 is `5838b856c74c07fbc9fa99b6dfd1eee34ea554c3e530c30e0d58014b707d70a4`. The source is the same pinned GreenSock commit and MIT notice linked above. Its examples are documentary; confirm version-sensitive APIs and current runtime terms before applying them.
