# Routes, sections and responsive layout

Source: `assets/source` · SHA-256 `d0648cba0f1b276196d028bcbb6add9fb82d2a18837355641579f312f7563c79` (relative filenames and bytes of CSS, JS, MJS, HTML, image and font files; excludes editable JSON/Markdown, package metadata, generated dist, host metadata). These are source observations; user-authorized changes may replace them.

HTML: . Render modules: src/assets.mjs, src/domain.mjs, src/png.mjs, src/render.mjs, src/sections.mjs.

Section IDs: #main, #top, #exhibition-title, #works, #chronology, #chronology-title, #viewing, #viewing-title.

Responsive scopes: @media (max-width:700px), @media (prefers-reduced-motion:reduce).

- `main` · `base` · `assets/source/styles/print.css`: `{'max-width': 'none', 'padding': '0'}`.
- `.skip,.masthead nav,.work-index,.next-link,footer` · `base` · `assets/source/styles/print.css`: `{'display': 'none'}`.
- `.masthead` · `base` · `assets/source/styles/print.css`: `{'min-height': '0', 'padding': '0 0 5mm'}`.
- `.introduction` · `base` · `assets/source/styles/print.css`: `{'padding': '8mm 0 0'}`.
- `.work` · `base` · `assets/source/styles/print.css`: `{'padding': '0'}`.
- `.caption` · `base` · `assets/source/styles/print.css`: `{'display': 'block'}`.
- `.artwork` · `base` · `assets/source/styles/print.css`: `{'max-height': '102mm', 'width': '100%', 'break-inside': 'avoid'}`.
- `.work-notes` · `base` · `assets/source/styles/print.css`: `{'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '8mm'}`.
- `details::details-content` · `base` · `assets/source/styles/print.css`: `{'display': 'block'}`.
- `details>*:not(summary)` · `base` · `assets/source/styles/print.css`: `{'display': 'block'}`.
- `dl div` · `base` · `assets/source/styles/print.css`: `{'break-inside': 'avoid'}`.
- `.unavailable` · `base` · `assets/source/styles/print.css`: `{'padding': '10mm 0'}`.
- `.chronology` · `base` · `assets/source/styles/print.css`: `{'padding': '0'}`.
- `.local-label` · `base` · `assets/source/styles/print.css`: `{'padding': '0 0 4mm'}`.
- `.chronology-intro` · `base` · `assets/source/styles/print.css`: `{'margin': '6mm 0'}`.
- `.event` · `base` · `assets/source/styles/print.css`: `{'grid-template-columns': '36mm 1fr', 'gap': '7mm', 'padding': '7mm 0 5mm', 'break-inside': 'avoid'}`.
- `.viewing` · `base` · `assets/source/styles/print.css`: `{'break-inside': 'avoid'}`.
- `.viewing>div` · `base` · `assets/source/styles/print.css`: `{'grid-template-columns': '1fr 1fr', 'gap': '8mm'}`.
- `.empty-chronology` · `base` · `assets/source/styles/print.css`: `{'padding': '7mm 0'}`.
- `.editorial-break` · `base` · `assets/source/styles/print.css`: `{'display': 'initial'}`.
- `body` · `base` · `assets/source/styles/screen.css`: `{'margin': '0'}`.
- `main` · `base` · `assets/source/styles/screen.css`: `{'max-width': '1536px', 'margin': '0 auto', 'padding': '0 var(--gutter)'}`.
- `p` · `base` · `assets/source/styles/screen.css`: `{'margin': '0'}`.
- `h1,h2,h3` · `base` · `assets/source/styles/screen.css`: `{'margin': '0'}`.
- `.skip` · `base` · `assets/source/styles/screen.css`: `{'position': 'fixed', 'width': '1px', 'height': '1px'}`.
- `.skip:focus` · `base` · `assets/source/styles/screen.css`: `{'width': 'auto', 'height': 'auto', 'padding': '12px'}`.
- `.masthead` · `base` · `assets/source/styles/screen.css`: `{'display': 'flex', 'justify-content': 'space-between', 'gap': '2rem', 'align-items': 'center', 'min-height': '90px', 'padding': '30px 0'}`.
- `.masthead nav` · `base` · `assets/source/styles/screen.css`: `{'display': 'flex', 'gap': '3.5rem'}`.
- `.introduction` · `base` · `assets/source/styles/screen.css`: `{'padding': '43px 0 31px'}`.
- `h1` · `base` · `assets/source/styles/screen.css`: `{'max-width': '1100px'}`.
- `.lead` · `base` · `assets/source/styles/screen.css`: `{'max-width': '1100px'}`.
- `.diagnostic` · `base` · `assets/source/styles/screen.css`: `{'max-width': '900px'}`.
- `.work-index` · `base` · `assets/source/styles/screen.css`: `{'display': 'flex', 'justify-content': 'space-between', 'gap': '2rem', 'padding': '28px 0 58px'}`.
- `.caption` · `base` · `assets/source/styles/screen.css`: `{'display': 'flex', 'justify-content': 'space-between', 'align-items': 'baseline', 'gap': '32px'}`.
- `.artwork` · `base` · `assets/source/styles/screen.css`: `{'display': 'block', 'width': '100%', 'height': 'auto'}`.
- `.work-notes` · `base` · `assets/source/styles/screen.css`: `{'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '60px'}`.
- `summary::-webkit-details-marker` · `base` · `assets/source/styles/screen.css`: `{'display': 'none'}`.
- `dl` · `base` · `assets/source/styles/screen.css`: `{'margin': '22px 0 0'}`.
- `dd` · `base` · `assets/source/styles/screen.css`: `{'margin': '3px 0 0'}`.
- `.unavailable` · `base` · `assets/source/styles/screen.css`: `{'padding': '36px 0'}`.
- `.local-label` · `base` · `assets/source/styles/screen.css`: `{'padding': '28px 0 32px'}`.
- `.chronology-intro` · `base` · `assets/source/styles/screen.css`: `{'margin': '34px 0 38px'}`.
- `.event` · `base` · `assets/source/styles/screen.css`: `{'display': 'grid', 'grid-template-columns': '240px 1fr', 'gap': '56px', 'padding': '48px 0 40px'}`.
- `.event h3` · `base` · `assets/source/styles/screen.css`: `{'margin': '0 0 16px'}`.
- `.empty-chronology` · `base` · `assets/source/styles/screen.css`: `{'padding': '40px 0'}`.
- `.viewing>div` · `base` · `assets/source/styles/screen.css`: `{'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '60px'}`.
- `footer` · `base` · `assets/source/styles/screen.css`: `{'display': 'flex', 'justify-content': 'space-between', 'gap': '24px', 'padding': '24px 0 42px'}`.
- `.recovery p` · `base` · `assets/source/styles/screen.css`: `{'margin': '28px 0'}`.
- `.masthead` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'align-items': 'flex-start', 'gap': '22px'}`.
- `.masthead nav` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'gap': '2rem'}`.
- `.editorial-break` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'display': 'none'}`.
- `.work-index` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'flex-direction': 'column', 'gap': '14px'}`.
- `.caption` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'display': 'block'}`.
- `.work-notes,.viewing>div` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'grid-template-columns': '1fr', 'gap': '28px'}`.
- `.event` · `@media (max-width:700px)` · `assets/source/styles/screen.css`: `{'grid-template-columns': '1fr', 'gap': '22px', 'padding': '32px 0'}`.
