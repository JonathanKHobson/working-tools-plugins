# Depth card design contract

Owner: Interactive Depth Cards. Editable sources are `depth-card.html`, `../scripts/build_depth_card.py`, and the optional `react/` component, CSS and hook. This is a neutral adaptation surface, not a fixed brand identity.

- Composition: a portrait 5:7 card, bounded by a stable untransformed hit region inside an 1100px perspective stage. The front has independent background, optional particle and foreground art planes, optional local CSS sparkles, modest live print, rim, foil, and glare. The back uses live text. Explanatory copy and sourced facts sit outside the moving card.
- Spatial order: background depth around 8px, subject around 45px, print 58px, foil/light 63px. Background displacement is opposite foreground; all displacement uses already scaled pointer variables. Art should overscan its clipped plane; foreground may protrude but must stay inside the stage at input extremes.
- Interaction: pointer and arrow keys tilt; Home/Escape/0 reset; Enter/Space and click flip only when a back is supplied. Touch drag greater than 8px suppresses an accidental flip while vertical scrolling remains available. Exploded view separates planes and forces the front. The tilt and flipper are different wrappers.
- Finishes: holographic, gold, silver change rim, foil color and selected background grading. Foil and glare share pointer-driven light coordinates. At depth zero those coordinates stay centered and all input rotation, displacement and lift are neutral.
- Accessibility: title and facts remain live and readable without JavaScript. The inactive face is marked hidden to assistive technology; backface visibility prevents mirrored visual leakage. Focus is visible; controls expose pressed state. Reduced motion stops tilt and ambient orbit, removes flip/layer transitions, and retains immediate state changes. Print is static.
- Adaptation: apply the owning project's visual identity, supplied art, and factual content. Use local assets and avoid remote fonts, media and app services. Verify art contrast and alpha at neutral, extreme, flipped, separated and narrow views.

Verification details are in `../references/input-and-review.md`. Static source checks do not establish rendered quality.
