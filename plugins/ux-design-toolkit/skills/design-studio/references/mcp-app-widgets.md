# Compact MCP library chooser

Read alongside [conversational widgets](conversational-widgets.md) when a person is choosing, browsing or inspecting a collection inside chat. This path remains for existing callers. The single-row carousel is a **library chooser pattern**, not a layout mandate for comparison tables, editors, result cards, maps or other widgets. Keep technical bridge, metadata and installation mechanics with the current MCP app provider.

## Inline choice and detail

- Present a short library title, compact search and useful filter, one horizontal row of previews with concise names, and a clear next action. Omit landing-page heroes, marketing copy, repeated instructions and an outer close control already supplied by the host.
- Place previous and next arrows together at the top right of the compact chooser, as a paired control. They should move a useful card or page, expose boundary state, and preserve predictable focus. Swipe or trackpad scrolling may supplement them. Do not create horizontal page overflow or make a long sideways strip the only way to find an item.
- Reveal less-used filters on demand; show active constraints and a clear action. Preserve query, filters, selection and position when returning from detail. Use named View and Back actions. Put full descriptions, evidence and configuration in the detail or supported expanded view instead of stacking panels beneath the row.
- Keep the common inline selection path compact without required inner vertical scrolling. A dedicated long detail view may scroll. Do not use a fixed height that clips enlarged text, errors or controls. At narrow widths show fewer cards or one card per page; if the host prevents an accessible layout, state that limit.
- Treat reference screenshots as topology evidence. Map heading, controls, row, arrows, action marker and detail transition; compare before and after at the same viewport. Do not assume the reference's host chrome or pixel size is portable.

## Actions, routing and continuity

Use a card menu for secondary actions only when it has hover, keyboard-focus and touch access. Make Use and View clear; labels, focus and dismissal must work without a mouse. Show a named Create template or Create activity action only when the owning library has a meaningful authoring route; do not replace that route with a generic unlabeled Create control. Edit and Delete require real supported actions and honest assistant-request labels when the widget merely prepares a request.

For a deliberate Use or Create handoff, validate source selection through the owning backend when supported, then use the host's text-message bridge only when advertised. Otherwise expose a copyable prompt and say whether it is prepared, copied or sent. A sent creation request is not evidence that an item was saved, registered or indexed. Keep the brief and status truthful through failure. Do not auto-submit on widget open or imply that a speculative menu action changed an artifact.

When sibling libraries share this pattern, maintain one chooser component and bridge with small adapters for titles, filters, preview, detail and handoff validation. Keep each catalog's data and source constraints in its adapter. Preserve selected `{id, view}` on a host remount only as a best-effort convenience; re-resolve against current data, keep private briefs and source contents out of session storage, and never promise recovery the host does not support.

AI-only search, ranking or handoff preparation uses structured backend tools without UI-opening metadata. Open the chooser when the human is intentionally browsing or selecting. Preserve the same IDs and source constraints in both paths, and keep optional search-miss logging separate from the widget.

## Review

Use Design Review on the actual rendered host widget. Map 3–8 anchors across the initial header and controls, row, arrows, menu and detail. Check normal, loading, empty, error and filtered states; common inline height; arrow boundaries; query/filter clear and return; keyboard and touch menu access; narrow and enlarged-text layouts; light and dark themes; and the actual Use/send/copy failure path. Verify separately that independent backend search does not open a widget. Record source/export checks separately from real-host results and mark untested assistive-technology or host modes explicitly.

For guided authoring in sibling libraries, keep the same named Create route through the shared brief and send/copy flow. Each adapter owns destination, authoring workflow and schema discovery, candidate requirements, registration fallback and a proportionate success check. A prompt sent to chat is not proof of a registered or visible library item.

When a user reports that the in-chat widget differs from an approved preview, first identify the exact visible instance and compare its header, controls and card topology. A stale host resource is a credible alternative to a design defect; hand release-freshness diagnosis to Build MCP Apps before changing the accepted component. Review the newest rendered instance after refresh. Record explicit appearance approval as visual acceptance, while keeping unexercised interaction paths unverified.

A prompt handoff must expose its useful payload before submission: entering Use or Create shows a populated selection-specific or authoring prompt without requiring a brief or sending a message. Put optional additional instructions after the prompt, update the visible payload when they change, and send/copy the text shown. Test empty-brief entry as a first-class path; a generic placeholder is not a prepared prompt. Distinguish Back to library from Return to chat, including a host-opened app tab and an honest fallback when inline return is unsupported.
