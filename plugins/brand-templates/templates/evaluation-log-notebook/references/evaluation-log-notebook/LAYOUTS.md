# Routes, sections and responsive layout

Source: `assets/source` · SHA-256 `0b64dc6d35a6b63998b3034b922c545d491af6852d2834c0b2ef989b6dbb9e3a` (relative filenames and bytes of CSS, JS, MJS, HTML, image and font files; excludes editable JSON/Markdown, package metadata, generated dist, host metadata). These are source observations; user-authorized changes may replace them.

HTML: index.html. Render modules: src/agent-tools.js, src/data.js, src/domain.js, src/main.js, src/view.js.

Section IDs: #app, #top, #log, #filters, #query, #status, #category, #selection, #download, #print, #records.

Responsive scopes: @media print, @media (max-width:850px), @media (max-width:540px).

- `body` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `button` · `base` · `assets/source/src/styles.css`: `{'padding': '.65rem .85rem', 'min-height': '44px'}`.
- `input,select` · `base` · `assets/source/src/styles.css`: `{'width': '100%', 'padding': '.7rem .6rem', 'min-height': '44px'}`.
- `p` · `base` · `assets/source/src/styles.css`: `{'margin': '.6rem 0 1.2rem'}`.
- `h1,h2,h3` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `h1` · `base` · `assets/source/src/styles.css`: `{'max-width': '19ch'}`.
- `main,header,section,aside,article` · `base` · `assets/source/src/styles.css`: `{'min-width': '0'}`.
- `.mast` · `base` · `assets/source/src/styles.css`: `{'padding': '1.25rem 4vw', 'display': 'flex', 'gap': '1rem', 'justify-content': 'space-between'}`.
- `.intro` · `base` · `assets/source/src/styles.css`: `{'padding': '3.5rem 4vw 2rem'}`.
- `.eyebrow` · `base` · `assets/source/src/styles.css`: `{'margin': '0 0 1rem'}`.
- `.question` · `base` · `assets/source/src/styles.css`: `{'max-width': '56ch', 'margin': '1.5rem 0 .8rem'}`.
- `.scope` · `base` · `assets/source/src/styles.css`: `{'max-width': '78ch', 'margin': '0 0 2rem'}`.
- `.runline` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'gap': '1rem 3rem'}`.
- `.workspace` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'grid-template-columns': 'minmax(240px,1fr) minmax(0,2.4fr)', 'max-width': '1600px', 'margin': 'auto'}`.
- `.rail` · `base` · `assets/source/src/styles.css`: `{'padding': '2.5rem 2.5vw 2.5rem 4vw'}`.
- `.totals` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.totals div` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'justify-content': 'space-between', 'padding': '.45rem 0', 'gap': '1rem'}`.
- `.totals dd` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.log` · `base` · `assets/source/src/styles.css`: `{'padding': '2.5rem 4vw 2.5rem 2.5vw'}`.
- `.section-heading` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'justify-content': 'space-between', 'gap': '1rem', 'align-items': 'baseline'}`.
- `.controls` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '1rem'}`.
- `.controls label` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'gap': '.5rem'}`.
- `.log-tools` · `base` · `assets/source/src/styles.css`: `{'margin': '1.25rem 0 2rem', 'display': 'flex', 'gap': '.75rem', 'align-items': 'center'}`.
- `.log-tools p` · `base` · `assets/source/src/styles.css`: `{'width': '100%', 'margin': '0 0 .3rem'}`.
- `.entry` · `base` · `assets/source/src/styles.css`: `{'padding': '1.8rem 0 2rem'}`.
- `.entry-meta` · `base` · `assets/source/src/styles.css`: `{'display': 'flex', 'gap': '.8rem 1.5rem', 'align-items': 'center'}`.
- `.state` · `base` · `assets/source/src/styles.css`: `{'padding': '.15rem .55rem'}`.
- `.category` · `base` · `assets/source/src/styles.css`: `{'margin': '.4rem 0 1.2rem'}`.
- `.evidence` · `base` · `assets/source/src/styles.css`: `{'display': 'grid', 'grid-template-columns': '8rem minmax(0,1fr)', 'gap': '.65rem 1rem'}`.
- `.evidence dd` · `base` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `summary` · `base` · `assets/source/src/styles.css`: `{'padding': '.8rem 0', 'min-height': '44px'}`.
- `.detail-body` · `base` · `assets/source/src/styles.css`: `{'padding': '.4rem 1rem'}`.
- `.empty` · `base` · `assets/source/src/styles.css`: `{'padding': '2rem 0'}`.
- `footer` · `base` · `assets/source/src/styles.css`: `{'padding': '2rem 4vw', 'display': 'grid', 'grid-template-columns': '1fr 2fr', 'gap': '2rem'}`.
- `footer p` · `base` · `assets/source/src/styles.css`: `{'margin': '0', 'max-width': '70ch'}`.
- `.skip` · `base` · `assets/source/src/styles.css`: `{'position': 'absolute', 'padding': '1rem'}`.
- `.boot,.error` · `base` · `assets/source/src/styles.css`: `{'padding': '3rem 4vw'}`.
- `.error` · `base` · `assets/source/src/styles.css`: `{'max-width': '65rem'}`.
- `.workspace` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr'}`.
- `.rail` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'padding': '2rem 5vw', 'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '1.5rem'}`.
- `.rail section` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.log` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'padding': '2rem 5vw'}`.
- `.intro` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'padding': '2.5rem 5vw 2rem'}`.
- `.mast` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'padding': '1rem 5vw'}`.
- `.to-top` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'display': 'none'}`.
- `footer` · `@media (max-width:850px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr', 'gap': '1rem'}`.
- `.rail` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr'}`.
- `.controls` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr'}`.
- `.evidence` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'grid-template-columns': '1fr', 'gap': '.2rem'}`.
- `.entry-meta` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'gap': '.65rem'}`.
- `.runline` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `.runline span` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `.log-tools button` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'width': '100%'}`.
- `button` · `@media (max-width:540px)` · `assets/source/src/styles.css`: `{'max-width': '100%'}`.
- `.mast` · `@media print` · `assets/source/src/styles.css`: `{'padding': '0 0 5mm'}`.
- `.intro` · `@media print` · `assets/source/src/styles.css`: `{'padding': '8mm 0'}`.
- `h1` · `@media print` · `assets/source/src/styles.css`: `{'max-width': 'none'}`.
- `.workspace` · `@media print` · `assets/source/src/styles.css`: `{'display': 'block'}`.
- `.rail` · `@media print` · `assets/source/src/styles.css`: `{'padding': '7mm 0', 'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '5mm'}`.
- `.rail section` · `@media print` · `assets/source/src/styles.css`: `{'margin': '0'}`.
- `.log` · `@media print` · `assets/source/src/styles.css`: `{'padding': '7mm 0'}`.
- `.controls,.log-tools button,.skip,.to-top` · `@media print` · `assets/source/src/styles.css`: `{'display': 'none'}`.
- `.log-tools` · `@media print` · `assets/source/src/styles.css`: `{'margin': '3mm 0'}`.
- `.entry` · `@media print` · `assets/source/src/styles.css`: `{'break-inside': 'avoid', 'padding': '5mm 0'}`.
- `.detail-body` · `@media print` · `assets/source/src/styles.css`: `{'padding': '0'}`.
- `.detail-body p` · `@media print` · `assets/source/src/styles.css`: `{'margin': '.3rem 0'}`.
- `.evidence` · `@media print` · `assets/source/src/styles.css`: `{'grid-template-columns': '23mm 1fr'}`.
- `footer` · `@media print` · `assets/source/src/styles.css`: `{'padding': '5mm 0', 'display': 'block'}`.
- `summary` · `@media print` · `assets/source/src/styles.css`: `{'padding': '2mm 0', 'min-height': '0'}`.
- `footer` · `@media print` · `assets/source/src/styles.css`: `{'display': 'none'}`.
