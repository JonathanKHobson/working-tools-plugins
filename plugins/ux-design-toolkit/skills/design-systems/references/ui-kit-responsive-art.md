# Responsive composition with integrated artwork

Use when illustration, photography, decorative frames or foreground objects share space with live UI. Existing [asset integration QA](../../../libraries/visual-asset-integration/references/responsive-image-qa.md) owns general crop, selection and delivery checks; this reference adds a composition contract for reusable kits.

## Define what must survive

Map three to eight anchors: the first useful action, title and reading field, important subjects/props, route/navigation, recognizable brand cue and the transition to following content. Record source, viewport, region, intended relation and acceptance scope. A user accepting a desktop or medium-width opening does not establish acceptance at every narrower width.

Specify live content, background scene, foreground decoration and interaction layers separately. Reserve both text-safe and subject-safe regions. Contrast alone cannot protect a face hidden by a button. Include the focus indicator's clearance, hover enlargement and long/pending labels in collision review.

Give decorative companions a spatial purpose: a grounded contact, a transition, a directional cue or a modest ending. Avoid repeating a mascot beside every question or treating every card as a new scene. Quiet task areas and expressive openings can share the same brand. Inspect continuity at intermediate widths where a subject can disappear or float even though the opening and narrowest screenshot look correct.

For reproducible collision checks, store normalized protected rectangles or polygons against each art source's intrinsic dimensions. Map them through the actual crop, scale and object position into viewport coordinates; compare visible control/text bounds. For cover sizing, the scale is max(container width/source width, container height/source height); contain uses min. Apply the real alignment offsets and clipping. Geometry supports review but does not judge aesthetics or identify every irregular shape automatically.

## Adapt the composition, not just the width

Use available space and content to determine layout transitions. Test intermediate widths around each transition, the narrowest supported width, and long/localized copy. Preserve meaningful reading order independently of visual art layers. Let content growth increase the available height or switch to a legible reading mode; do not move a CTA across a subject or shrink a hit target to rescue the artwork.

Where a landscape scene cannot preserve both subject and reading space, use an authored narrow composition, a deliberate crop, or a simpler decorative treatment. A narrow composition is art direction. Smaller resolutions of that same composition are delivery variants. These are separate decisions; `picture` and `srcset` do not design the layout for you.

An integrated visual direction should not accidentally become an endless stack of text blocks followed by disconnected full-width images. Evaluate the whole rhythm at ordinary phone size. Conversely, a text-enlargement accommodation may legitimately place extended text above art: task access takes priority over retaining the ordinary hero geometry. Name the accommodation and test it rather than presenting it as the default visual direction.

Inspect wrapping quality, not just horizontal overflow. Whole words, useful line lengths, readable labels and a clear primary action must survive. Reduce unnecessary gutters or switch display type to a reading role when appropriate. A root-font-size simulation is not the same check as browser zoom; record each method accurately.

## Responsive behavior beyond artwork

Navigation must work when entering narrow directly, entering wide directly, and resizing narrow → wide → narrow. Synchronize visible state, ARIA state, pointer interaction and focus ownership. A hidden disclosure must not leave desktop links inert. Test Escape immediately after opening, from within the panel, and after a pointer reopen.

For scrolling tabs or toolbars, verify first and last focused items are fully visible and the indicator is not clipped by the container. Include forced colors and any sticky layer. Do not infer a particular WCAG violation solely from a partly clipped ring; evaluate the relevant criterion and actual remaining indicator.

Use native/platform guidance for safe areas, software keyboards, touch and orientation as relevant. Desktop hover treatments require keyboard and touch equivalents. Verify actual devices when claiming device behavior; viewport emulation proves only its recorded browser environment.
