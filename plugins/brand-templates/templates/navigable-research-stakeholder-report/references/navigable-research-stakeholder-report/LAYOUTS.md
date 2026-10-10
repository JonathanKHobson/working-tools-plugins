# Routes, sections and responsive layout

Source: `assets/source` · SHA-256 `6c40f3b6ca2d9b9802f99e70b03193ecfe8f94028cc0dd45fb45dd5deae3a20f` (relative filenames and bytes of CSS, JS, MJS, HTML, image and font files; excludes editable JSON/Markdown, package metadata, generated dist, host metadata). These are source observations; user-authorized changes may replace them.

HTML: . Render modules: src/app.js, src/components.mjs, src/render.mjs.

Section IDs: #main, #overview, #findings, #decisions, #study, #evidence, #expand-records, #collapse-records, #record-status.

Responsive scopes: @media (max-width:1000px), @media (max-width:760px), @media (max-width:380px), @media print.

- `body` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `p` · `base` · `assets/source/src/styles.css`: `{'margin': '.65rem 0 1rem'}`.
- `h1` · `base` · `assets/source/src/styles.css`: `{'margin': '.7rem 0 1.5rem', 'max-width': '25ch'}`.
- `h2` · `base` · `assets/source/src/styles.css`: `{'margin': '.65rem 0 1.1rem'}`.
- `h3` · `base` · `assets/source/src/styles.css`: `{'margin': '.5rem 0 1rem'}`.
- `button` · `base` · `assets/source/src/styles.css`: `{'padding': '.6rem .9rem', 'min-height': '44px'}`.
- `[hidden]` · `base` · `assets/source/src/styles.css`: `{'display': 'none'}`.
- `.skip-link` · `base` · `assets/source/src/styles.css`: `{'position': 'absolute', 'padding': '.8rem'}`.
- `.masthead` · `base` · `assets/source/src/styles.css`: `{'padding': '1.3rem max(1.5rem,calc((100vw - 1352px)/2))', 'display': 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'gap': '1rem'}`.
- `.fictional` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.page-shell` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'grid-template-columns': '210px minmax(0,1fr)', 'gap': '3.5rem', 'max-width': '1352px', 'margin': 'auto', 'padding': '2.5rem 1.5rem 4rem'}`.
- `.rail nav` · `base` · `assets/source/src/styles.css`: `{'position': 'sticky'}`.
- `.rail-label` · `base` · `assets/source/src/styles.css`: `{'margin': '0 0 1rem'}`.
- `.rail ol` · `base` · `assets/source/src/styles.css`: `{'padding': '0', 'margin': '0'}`.
- `.rail a` · `base` · `assets/source/src/styles.css`: `{'display': 'block', 'padding': '.55rem 0 .55rem 1rem'}`.
- `main` · `base` · `assets/source/src/styles.css`: `{'min-width': '0', 'max-width': '940px'}`.
- `.eyebrow` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.answer` · `base` · `assets/source/src/styles.css`: `{'padding': '1.4rem 1.6rem'}`.
- `.answer h2` · `base` · `assets/source/src/styles.css`: `{'max-width': '40ch'}`.
- `.answer-label` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'align-items': 'center', 'gap': '1rem', 'margin': '0 0 .7rem'}`.
- `.status` · `base` · `assets/source/src/styles.css`: `{'display': 'inline-block', 'padding': '.15rem .65rem'}`.
- `.metrics` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'grid-template-columns': 'repeat(3,minmax(0,1fr))', 'gap': '1.5rem', 'padding': '1.2rem 0 .25rem'}`.
- `.metrics p` · `base` · `assets/source/src/styles.css`: `{'margin': '.15rem 0 .7rem'}`.
- `.limit-strip` · `base` · `assets/source/src/styles.css`: `{'padding': '.1rem 1rem', 'margin': '1.2rem 0'}`.
- `.limit-strip p` · `base` · `assets/source/src/styles.css`: `{'margin': '.2rem 0 .3rem'}`.
- `.section-intro` · `base` · `assets/source/src/styles.css`: `{'max-width': '75ch'}`.
- `.finding` · `base` · `assets/source/src/styles.css`: `{'padding': '1.4rem 0 1.6rem'}`.
- `.finding h3` · `base` · `assets/source/src/styles.css`: `{'max-width': '58ch'}`.
- `dl` · `base` · `assets/source/src/styles.css`: `{'margin': '.7rem 0 1.3rem'}`.
- `.field` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'grid-template-columns': '165px minmax(0,1fr)', 'gap': '1.1rem', 'padding': '.6rem 0'}`.
- `.field dd` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.source-detail` · `base` · `assets/source/src/styles.css`: `{'padding': '.55rem 1rem'}`.
- `.source-detail p` · `base` · `assets/source/src/styles.css`: `{'margin': '.7rem 0'}`.
- `summary` · `base` · `assets/source/src/styles.css`: `{'min-height': '44px', 'padding': '.55rem 0'}`.
- `.decision` · `base` · `assets/source/src/styles.css`: `{'padding': '1.3rem 0'}`.
- `.decision-top` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'align-items': 'flex-start', 'justify-content': 'space-between', 'gap': '1rem'}`.
- `.decision-top h3` · `base` · `assets/source/src/styles.css`: `{'max-width': '50ch'}`.
- `.options` · `base` · `assets/source/src/styles.css`: `{'margin': '1rem 0', 'padding': '.5rem 1rem'}`.
- `.options li` · `base` · `assets/source/src/styles.css`: `{'padding': '.45rem 0'}`.
- `.study` · `base` · `assets/source/src/styles.css`: `{'padding': '1.3rem 1.5rem'}`.
- `.notice` · `base` · `assets/source/src/styles.css`: `{'padding': '.8rem 1rem'}`.
- `.js-controls` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'gap': '.6rem', 'align-items': 'center'}`.
- `.record` · `base` · `assets/source/src/styles.css`: `{'padding': '.4rem 0'}`.
- `.record-content` · `base` · `assets/source/src/styles.css`: `{'padding': '.2rem 1rem 1rem'}`.
- `.page-shell` · `@media (max-width:1000px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '170px minmax(0,1fr)', 'gap': '2rem'}`.
- `.wordmark span` · `@media (max-width:1000px)` · `assets/source/src/styles.css`: `{'display': 'block', 'margin': '0'}`.
- `.masthead` · `@media (max-width:1000px)` · `assets/source/src/styles.css`: `{'align-items': 'flex-start'}`.
- `.finding .field` · `@media (max-width:1000px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '140px minmax(0,1fr)'}`.
- `.page-shell` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'display': 'block', 'padding': '1.4rem 1.2rem 3rem'}`.
- `.masthead` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'padding': '1rem 1.2rem', 'gap': '.55rem'}`.
- `.rail ol` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'display': 'flex', 'gap': '.25rem .9rem'}`.
- `.rail a` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'padding': '.35rem 0', 'min-height': '44px'}`.
- `.rail-note` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'display': 'none'}`.
- `.answer` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'padding': '1.1rem 1.2rem'}`.
- `.metrics` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr', 'gap': '.85rem'}`.
- `.field,.finding .field` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `.decision-top` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `.study` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'padding': '1rem'}`.
- `.eyebrow span` · `@media (max-width:760px)` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `.metrics` · `@media (max-width:380px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr'}`.
- `.metrics>div` · `@media (max-width:380px)` · `assets/source/src/styles.css`: `{'display': 'flex', 'align-items': 'center', 'gap': '1rem'}`.
- `.metrics p` · `@media (max-width:380px)` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.metrics strong` · `@media (max-width:380px)` · `assets/source/src/styles.css`: `{'min-width': '6rem'}`.
- `.finding,.decision,.options,.study,h1,h2,h3` · `@media print` · `assets/source/src/styles.css`: `{'break-inside': 'avoid'}`.
- `.masthead` · `@media print` · `assets/source/src/styles.css`: `{'padding': '0 0 10pt'}`.
- `.wordmark span` · `@media print` · `assets/source/src/styles.css`: `{'display': 'inline'}`.
- `.rail,.skip-link,.js-controls,.overview-next` · `@media print` · `assets/source/src/styles.css`: `{'display': 'none'}`.
- `.page-shell` · `@media print` · `assets/source/src/styles.css`: `{'display': 'block', 'padding': '16pt 0 0', 'max-width': 'none'}`.
- `main` · `@media print` · `assets/source/src/styles.css`: `{'max-width': 'none'}`.
- `h1` · `@media print` · `assets/source/src/styles.css`: `{'max-width': 'none'}`.
- `.answer` · `@media print` · `assets/source/src/styles.css`: `{'padding': '12pt'}`.
- `.field,.metrics>div,.limit-strip` · `@media print` · `assets/source/src/styles.css`: `{'break-inside': 'avoid'}`.
- `.record-content` · `@media print` · `assets/source/src/styles.css`: `{'padding': '0 0 10pt'}`.
- `details>summary` · `@media print` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `details>*:not(summary)` · `@media print` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `details::details-content` · `@media print` · `assets/source/src/styles.css`: `{'display': 'block', 'height': 'auto'}`.
- `.field` · `@media print` · `assets/source/src/styles.css`: `{'grid-template-columns': '120pt minmax(0,1fr)', 'gap': '10pt', 'padding': '5pt 0'}`.
- `.record` · `@media print` · `assets/source/src/styles.css`: `{'break-inside': 'avoid'}`.
