# Brand Templates picker design

Reference: the maintained compact Writing/Design/Activities chooser. Shared index, styles, bridge and application files are projected unchanged; Brand supplies only its adapter and data.

Keep the compact header with adjacent previous/next controls, search, optional filters, Sort, one horizontal preview row, secondary View and primary Use, and the separate detail/handoff views. Preserve query and selection on Back. Cards show the actual supplied brand-guide preview; kit typography and colors belong to content, not application chrome.

Change: brand title, category filter, source-aware detail fields and `prepare_brand_handoff` validation. Keep: common controls, disclosure, focus, theme and honest copy/send fallback. Defer: native host acceptance until installation and a fresh widget are observable.

Source anchors for same-viewport review: B1 `header` title/arrows, B2 `.toolbar` search/filter/sort, B3 `#cards` previews/actions, B4 `#detail-view` guide/source/rights, B5 `#handoff-view` prepared prompt/brief/status, B6 `#empty` and narrow layout. The complete visual rules of an individual brand are in its own `templates/{id}/DESIGN.md`.

Selected brands may supply `logoGallery`: labeled original artworks and exact-size icon renditions, placed before the existing guide in details. Reuse the shared `ui/logo-gallery.js/.css` controls: select, Previous/Next, visible caption/backing-field status, actual pixel-size row and optional larger preview. The modal closes with its visible button, backdrop or Escape and restores focus. No autoplay, new logo animation or favicon installation occurs. B7 `.brand-logo-gallery` is the added scoped review anchor. Artwork approval and larger-illustration roles come from the external collection, not this generic component.
