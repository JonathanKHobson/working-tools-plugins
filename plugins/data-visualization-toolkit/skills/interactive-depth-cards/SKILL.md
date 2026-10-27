---
name: interactive-depth-cards
description: Build layered collectible depth cards from supplied art, with local HTML or project-local React, independent parallax, foil, finishes, flip and layer views. Use for interactive cards rather than quantitative charts or scroll stories.
---

# Interactive Depth Cards

Make an interactive card whose background, subject, live print, and light respond distinctly. Follow the user's existing identity, framework, and scope. An interactive request needs an actual working preview and rendered interaction review. A still image cannot demonstrate motion.

1. Establish the card's purpose, dimensions, text, and source rights. Use supplied local artwork when suitable. For new artwork, prepare separate environment and subject assets using the host's built-in image generation tool if available; follow [local art preparation](references/artwork-preparation.md). Do not add a separate API, connected app, CDN, or image dependency. Keep text and facts live rather than baking them into art.
2. Inspect alpha and 3–8 visual anchors: background, subject silhouette, quiet text areas, foreground edge, contrast, and narrow layout. Preserve attribution and actual asset provenance. A flat photo alone cannot reveal hidden scene content.
3. Choose the existing project's route. For a standalone file, prepare the [brief](references/input-and-review.md) and run `python3 scripts/build_depth_card.py --brief /absolute/brief.json --output /absolute/card.html`. This uses local Python and Pillow, embeds normalized images, and refuses an existing output unless `--overwrite` is explicit. The earlier one-to-five-layer brief remains accepted. For an existing React app, use [project-local React integration](references/react-integration.md); the three source files in `assets/react/` require only the host project's React setup.
4. Keep perspective, tilt, flip, and art planes separate. The background moves opposite the subject, print moves modestly, and depth strength is applied once. Zero depth neutralizes input rotation, displacement, lift and reactive light position. The optional exploded view is front-facing. Foil and finish are decorative and must preserve text contrast.
5. Verify the actual rendered card. Test pointer extremes, depth 0/50/100, all three finishes, foil on/off, drag versus tap, keyboard, flip and exploded state, touch scrolling, reduced motion, hidden-tab settling, narrow layout, clipping, and no mirrored back-face leak. Text and facts must remain understandable without animation. Use the [review contract](references/input-and-review.md) and the [design contract](assets/DESIGN.md).
6. Deliver the working preview first where a local preview surface is available, then editable source, assets, and source hashes. Distinguish generated code from visually reviewed output. Do not claim a browser check from static source inspection.

For analytical comparisons use [data visualization](../data-visualization/SKILL.md); for scroll-tied sequences use [visual stories](../visual-stories/SKILL.md). Neither route should be added to an ordinary card request.
