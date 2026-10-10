# Create or revise a browser presentation

Use for an explicitly requested HTML/web presentation, PPTX-to-web conversion, or revision of an existing browser deck. Native document/slides providers remain the default when that is the requested editable output; do not turn a native deck request into HTML. Graphic Design owns deck composition/art direction; this procedure owns browser behavior and delivery checks. Follow the user's approved content and design rather than imposing a template.

## 1. Choose the mode and reading conditions

Identify new deck, conversion or enhancement. Infer purpose, audience, slide count/content, assets and speaker-led versus asynchronous reading from the brief; ask only when a missing answer changes the output. Speaker-led material usually needs one clear idea and larger type. Reading decks need enough context, evidence and captions to stand alone. Preserve mixed presenter/handout needs when requested instead of forcing a binary choice.

Decide whether the deliverable is a fixed-aspect-ratio presentation or a responsive reading artifact. A fixed stage (commonly 16:9) can scale uniformly and letterbox; its internal layout stays stable. A phone-readable report may reflow with preserved order. Do not silently replace one with the other or make scaled phone text illegible. Record the target stage/viewport and any separate accessible reading alternative.

## 2. Ground content and art direction

Inspect supplied assets and existing slides. Record each usable asset's actual subject, communication role, rights, crop and source; filenames alone do not establish visible content. Co-design the outline around real text and images. Keep exact names, amounts, quotations and other required facts under direct control. Missing information stays marked as unknown.

Use the existing design system and approved direction. When an unresolved visual direction materially benefits from alternatives, create a small set of genuinely different rendered slide examples using actual deck content. Do not force three previews or another approval round for a minor edit or an already chosen design. Keep workflow labels, source filenames and internal notes off the audience slides. After selection, expand that visual system consistently; do not substitute a new preset mid-deck.

## 3. Build the browser deck

Use the existing project/runtime, or a self-contained HTML file when that is the authorized portable output. Keep CSS/JS local or clearly disclose network assets. Do not require remote fonts, extra packages, a new service or a particular typography blacklist. Include only effects that serve meaning and respect reduced motion.

Make slide activation explicit: only the active slide receives pointer/keyboard interaction and accessibility exposure. Check that flex/grid layout rules cannot override the chosen visibility model and reveal every slide. Provide clear previous/next navigation, visible focus, slide position, suitable keyboard controls and optional touch controls; keyboard shortcuts must not capture normal text-entry behavior. Preserve a readable text route and avoid hover-only actions. Keep presenter notes separate from audience content.

If editing is part of the request, expose an explicit edit mode, escape edited plain text, preserve input focus/keyboard behavior, and verify save/reopen persistence. A control that merely changes the DOM is not a saved edit. Do not enable hidden editing, collect input or persist private text by default.

## 4. Convert or enhance faithfully

For PPTX conversion, use an existing reviewed extraction provider. Inventory slide order, text, images, notes, charts, tables and meaningful animations/transitions before building. Compare the extraction with rendered originals: text extraction alone misses layout, chart semantics or image content. Name unsupported features and choose a faithful static/interactive replacement within scope. Preserve required text and assets and keep transformations traceable. Speaker notes in HTML comments remain publicly readable; keep private notes out of shareable output unless expressly intended for that audience.

For an existing HTML deck, inspect its navigation, stage rules, content density and current source before edits. Preserve the approved style and behavior. Adding text/images requires checking the whole affected slide, not just the added element. Recompose or split overloaded slides when authorized; never solve overflow by shrinking text beyond usable size or hiding required content. Explain consequential sequence/content changes.

## 5. Verify and deliver

Inspect rendered slides at the target desktop stage and a relevant phone/short-height viewport. Check both overflow metrics and screenshots: panels can overlap without scroll overflow. Exercise navigation, focus, reduced motion, local assets and any edit/save/reopen path actually provided. Verify all slides appear once, in order; check final reveal states and media fallbacks. After a fix, recheck the affected slide and interaction.

For PDF, use the existing reviewed export toolchain. Verify page count/order, text readability, actual asset loading and every slide's final state. State whether the export is raster or selectable/vector text; a screenshot PDF loses interactivity and may lose accessibility. Do not promise universal fidelity or automatically download export runtimes.

Return the file/link, slide count, navigation and real edit/export limits. For a requested shareable, route through Work Management's existing single Shareables site procedure with a subpage and privacy/rights preflight; do not create a Vercel project or a new site automatically. Publishing and sending retain their actual authorization. Never deploy an entire working folder that may contain notes, source decks or credentials. Clean up only task-owned temporary previews when no longer needed.

Adapted from [Frontend Slides](https://github.com/zarazhangrui/frontend-slides/blob/9906a34d640d2111f724544cbc50f7f130569ae1/SKILL.md), MIT. [Notice](frontend-slides-LICENSE.txt). Retains mode selection, visual direction, density, fixed-stage option, conversion, revision and delivery checks. Omits upstream scripts/templates/assets, automatic installers/deployment, forced font bans, mandatory three-way previews, unconditional inline editing and fixed 16:9 for every artifact. Existing shared viewport guidance remains in design-reference-lookup; this adds the complete conditional browser-deck process.
