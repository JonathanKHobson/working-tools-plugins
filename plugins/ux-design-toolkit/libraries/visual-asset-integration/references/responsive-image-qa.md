# Responsive Image QA

Run rendered QA whenever visual assets affect a visible surface.

## Minimum Checks

- Desktop screenshot at a representative wide viewport.
- Mobile screenshot at a narrow viewport.
- No horizontal overflow.
- No unintended clipping, overlap, or bleed.
- Hero and detail media do not create excessive scroll.
- Text remains readable over images or texture at the exact rendered placement.
  Check whether letters cross complex shapes, similar-value colors, map lines,
  props, faces, or high-contrast texture. If they do, repair with crop/position,
  a local translucent reading field, or a deliberate overlay.
- Important text is at least 16px unless the format genuinely requires smaller
  labels.
- Images load without broken paths.
- Alt text exists and matches image purpose.
- Width and height or stable aspect ratio are defined.
- Lazy/eager loading is intentional.
- Reduced motion is respected when assets animate.

## Crop Checks

- Important subject remains visible on mobile.
- Proof details are not cropped out.
- Backgrounds do not hide UI controls or text.
- Text-safe negative space remains text-safe after responsive cropping and image
  repositioning.
- Right-side hero art stays within the designed hero height.
- Repeated images are intentional and limited.

## Publish Checks

- Verify the actual destination repo/path before pushing.
- Smoke-test public URLs after publish.
- Check cache-busted URLs when recent changes may be cached.
- Confirm the public surface has no internal placeholder labels, production
  prompt notes, source scaffolding, or temporary editorial text. Preserve
  historical proposal/prototype labels needed to interpret real evidence.

## Responsive Selection And Proof Fidelity

- Preserve original evidence bytes and provide a normal original-file link for
  close inspection. Optimize derivatives, not the only source copy. Do not
  cosmetically repair historical UI or crop away a relevant qualification.
- Use `srcset` widths capped at native resolution, without upscaling. A native
  428px phone capture needs an honest 428px candidate; a 1440px filename cannot
  create missing detail. Use `sizes` that matches the actual layout, including
  mobile padding and desktop columns. Preserve alpha where the asset needs it.
- Set intrinsic dimensions or a stable aspect ratio. Load the likely opening
  proof/hero eagerly; lazy-load genuinely secondary images. Do not defer the
  main case-opening image merely because a shared helper defaults to lazy.
- Inspect `currentSrc`, rendered width, viewport, DPR, and source dimensions in
  the browser at representative phone and desktop sizes. Compare actual text
  legibility against the original, especially small labels and dense evidence.
  Supply native essential findings alongside source images when raster text
  cannot carry the meaning accessibly; keep enough real imagery to prove the work.
- Compare full-page unique selected-image bytes separately from initial-viewport
  loading. Include newly added identity assets and document previews. Report
  CSS/JS bytes separately and state cache/transfer assumptions. A predicted byte
  saving is not a measured load time, LCP, or Core Web Vitals result.

## Scoped Interaction And Accessibility Check

- Inspect exact rendered contrast pairs for body text, captions, dark panels,
  buttons, and focus/hover states against the applicable accessibility threshold.
  A passing body-text sample does not verify every component or certify the site.
- Test 200% zoom and narrow reflow for clipping, unintended horizontal scroll,
  reading order, sticky elements, controls, and captions. Verify touch targets
  and keyboard focus at the same placements used in the visual anchor map.
- Disable JavaScript: navigation, source-image anchors, and file links must retain
  useful behavior. With enhancement enabled, test focus return, Escape, actual
  backdrop versus interior padding, and a real broken-image response.
- After authorized publication, verify served source and derivative URLs plus
  important downloads by content/type and bytes or hashes. HTTP 200 alone can
  hide a stale asset or an HTML error page. Report the scope actually verified.
