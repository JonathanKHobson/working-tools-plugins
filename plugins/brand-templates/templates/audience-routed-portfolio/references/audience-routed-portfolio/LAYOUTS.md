# Routes, sections and responsive layout

Source: `assets/source` · SHA-256 `55f21e8c544bf50e763d5560cfd720c9600b01598f165a07aa51f3f935d7bb25` (relative filenames and bytes of CSS, JS, MJS, HTML, image and font files; excludes editable JSON/Markdown, package metadata, generated dist, host metadata). These are source observations; user-authorized changes may replace them.

HTML: . Render modules: client/context.js, src/domain.mjs, src/pages.mjs, src/render.mjs.

Section IDs: #all-work, #main, #reading-context, #reading-routes.

Responsive scopes: @media print, @media (min-width:1400px), @media (max-width:1000px), @media (max-width:640px).

- `body` · `base` · `assets/source/styles/site.css`: `{'margin': '0'}`.
- `h1,h2,h3,p,dl,dd,figure` · `base` · `assets/source/styles/site.css`: `{'margin': '0'}`.
- `.page` · `base` · `assets/source/styles/site.css`: `{'width': 'min(100%,1648px)', 'padding': '0 3.6vw', 'margin': 'auto'}`.
- `.site-header` · `base` · `assets/source/styles/site.css`: `{'min-height': '82px', 'display': 'flex', 'gap': '2rem', 'align-items': 'center', 'justify-content': 'space-between'}`.
- `.site-header nav` · `base` · `assets/source/styles/site.css`: `{'display': 'flex', 'gap': '2.25rem', 'align-items': 'center'}`.
- `.site-header nav a` · `base` · `assets/source/styles/site.css`: `{'min-height': '44px', 'display': 'flex', 'align-items': 'center'}`.
- `.skip` · `base` · `assets/source/styles/site.css`: `{'position': 'absolute', 'padding': '.65rem'}`.
- `.index-intro` · `base` · `assets/source/styles/site.css`: `{'display': 'grid', 'grid-template-columns': '7fr 3.2fr', 'align-items': 'center', 'gap': '5vw', 'padding': '52px 0 46px'}`.
- `.audience-rail` · `base` · `assets/source/styles/site.css`: `{'display': 'grid', 'grid-template-columns': '1fr 1fr'}`.
- `.audience-rail>div` · `base` · `assets/source/styles/site.css`: `{'min-width': '0', 'padding': '22px 2.4vw 24px'}`.
- `.project-list` · `base` · `assets/source/styles/site.css`: `{'padding': '0', 'margin': '0'}`.
- `.project-row` · `base` · `assets/source/styles/site.css`: `{'display': 'grid', 'grid-template-columns': '9% 55% 1fr 30px', 'gap': '20px', 'align-items': 'center', 'padding': '19px 0 21px', 'min-height': '129px'}`.
- `.project-name` · `base` · `assets/source/styles/site.css`: `{'display': 'flex', 'flex-direction': 'column', 'min-width': '0'}`.
- `footer` · `base` · `assets/source/styles/site.css`: `{'display': 'flex', 'align-items': 'flex-start', 'justify-content': 'space-between', 'gap': '1.5rem', 'padding': '27px 0 29px'}`.
- `footer p` · `base` · `assets/source/styles/site.css`: `{'max-width': '65%'}`.
- `.back` · `base` · `assets/source/styles/site.css`: `{'display': 'inline-block', 'margin': '22px 0 18px'}`.
- `.case .page,.notes .page,.route .page` · `base` · `assets/source/styles/site.css`: `{'max-width': '1350px'}`.
- `.case-metadata` · `base` · `assets/source/styles/site.css`: `{'display': 'grid', 'grid-template-columns': '1fr 1fr 1fr', 'gap': '0', 'margin': '28px 0 27px'}`.
- `.case-section` · `base` · `assets/source/styles/site.css`: `{'display': 'grid', 'grid-template-columns': '23% minmax(0,1fr)', 'gap': '4%', 'padding': '25px 0'}`.
- `.case-section h2 span` · `base` · `assets/source/styles/site.css`: `{'display': 'block'}`.
- `.section-content` · `base` · `assets/source/styles/site.css`: `{'min-width': '0'}`.
- `.sample dl>div` · `base` · `assets/source/styles/site.css`: `{'display': 'grid', 'grid-template-columns': '29% minmax(0,1fr)', 'gap': '1.1rem', 'padding': '18px 20px'}`.
- `.case-end` · `base` · `assets/source/styles/site.css`: `{'display': 'flex', 'gap': '2.25rem'}`.
- `.empty-proof` · `base` · `assets/source/styles/site.css`: `{'padding': '18px'}`.
- `.route-reason` · `base` · `assets/source/styles/site.css`: `{'max-width': '850px', 'margin': '26px 0 40px'}`.
- `.after-route` · `base` · `assets/source/styles/site.css`: `{'display': 'flex', 'justify-content': 'space-between', 'gap': '2rem'}`.
- `.after-route p` · `base` · `assets/source/styles/site.css`: `{'max-width': '730px'}`.
- `.credits` · `base` · `assets/source/styles/site.css`: `{'padding': '28px 0'}`.
- `.credits p` · `base` · `assets/source/styles/site.css`: `{'max-width': '850px'}`.
- `.not-found .lead` · `base` · `assets/source/styles/site.css`: `{'margin': '30px 0'}`.
- `.not-found .audience-rail` · `base` · `assets/source/styles/site.css`: `{'margin': '45px 0'}`.
- `.not-found main` · `base` · `assets/source/styles/site.css`: `{'min-height': '70vh'}`.
- `.case .site-header` · `base` · `assets/source/styles/site.css`: `{'min-height': '68px'}`.
- `.home .project-row` · `@media (min-width:1400px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '9% 55% 1fr 42px'}`.
- `.home .index-intro` · `@media (min-width:1400px)` · `assets/source/styles/site.css`: `{'gap': '5.2vw'}`.
- `.site-header` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'gap': '1rem'}`.
- `.site-header nav` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'gap': '1.25rem'}`.
- `.index-intro` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '1fr', 'gap': '24px', 'padding': '36px 0'}`.
- `.index-intro p` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'max-width': '560px'}`.
- `.project-row` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '7% 53% 1fr 26px', 'gap': '13px'}`.
- `.sample dl>div` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '1fr', 'gap': '.35rem'}`.
- `.case-section` · `@media (max-width:1000px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '23% minmax(0,1fr)', 'gap': '3%'}`.
- `.page,.case .page` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'padding': '0 22px'}`.
- `.site-header` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'align-items': 'flex-start', 'flex-direction': 'column', 'gap': '.35rem', 'padding': '18px 0 10px', 'min-height': '100px'}`.
- `.site-header nav` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'width': '100%', 'gap': '1.15rem'}`.
- `.site-header nav a` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'min-height': '38px'}`.
- `.audience-rail` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '1fr'}`.
- `.audience-rail>div` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'min-width': '0', 'padding': '18px 0'}`.
- `.project-row` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '24px minmax(0,1fr) auto', 'gap': '10px', 'padding': '20px 0'}`.
- `.project-list li` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'min-width': '0'}`.
- `footer` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'display': 'block', 'padding': '22px 0'}`.
- `footer p` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'max-width': 'none'}`.
- `footer a` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'display': 'inline-block'}`.
- `.back` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'margin': '20px 0'}`.
- `.case-metadata` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '1fr', 'gap': '12px', 'margin': '28px 0'}`.
- `.case-metadata>div,.case-metadata>div+div` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'padding': '0', 'display': 'grid', 'grid-template-columns': 'minmax(0,.8fr) minmax(0,1.4fr)', 'gap': '12px'}`.
- `.case-section` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'grid-template-columns': '1fr', 'gap': '16px', 'padding': '22px 0'}`.
- `.case-section h2 span` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'display': 'inline'}`.
- `.section-content` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'padding': '0'}`.
- `.sample dl>div` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'padding': '15px'}`.
- `.case-end` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'gap': '20px'}`.
- `.after-route` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'display': 'block'}`.
- `.after-route a` · `@media (max-width:640px)` · `assets/source/styles/site.css`: `{'display': 'inline-block'}`.
- `.case .site-header` · `@media print` · `assets/source/styles/site.css`: `{'min-height': '35pt'}`.
- `.case footer` · `@media print` · `assets/source/styles/site.css`: `{'padding': '8pt 0', 'break-inside': 'avoid'}`.
- `.page,.case .page,.notes .page,.route .page` · `@media print` · `assets/source/styles/site.css`: `{'width': 'auto', 'max-width': 'none', 'padding': '0'}`.
- `.site-header` · `@media print` · `assets/source/styles/site.css`: `{'min-height': '35pt', 'padding': '0 0 10pt'}`.
- `.site-header nav` · `@media print` · `assets/source/styles/site.css`: `{'gap': '12pt'}`.
- `.site-header nav a` · `@media print` · `assets/source/styles/site.css`: `{'min-height': '0'}`.
- `.skip` · `@media print` · `assets/source/styles/site.css`: `{'display': 'none'}`.
- `.index-intro` · `@media print` · `assets/source/styles/site.css`: `{'padding': '24pt 0', 'gap': '20pt', 'grid-template-columns': '1fr'}`.
- `.project-row` · `@media print` · `assets/source/styles/site.css`: `{'grid-template-columns': '7% 52% 1fr 14pt', 'min-height': '0', 'padding': '13pt 0', 'gap': '10pt'}`.
- `.case-metadata` · `@media print` · `assets/source/styles/site.css`: `{'margin': '18pt 0'}`.
- `.case-section` · `@media print` · `assets/source/styles/site.css`: `{'padding': '9pt 0', 'grid-template-columns': '22% minmax(0,1fr)', 'gap': '4%', 'break-inside': 'avoid'}`.
- `.sample dl>div` · `@media print` · `assets/source/styles/site.css`: `{'padding': '9pt', 'gap': '8pt', 'grid-template-columns': '29% minmax(0,1fr)'}`.
- `footer,.case footer` · `@media print` · `assets/source/styles/site.css`: `{'padding': '16pt 0'}`.
- `.back` · `@media print` · `assets/source/styles/site.css`: `{'margin': '12pt 0'}`.
- `.project-list li` · `@media print` · `assets/source/styles/site.css`: `{'break-inside': 'avoid'}`.
- `.route-reason` · `@media print` · `assets/source/styles/site.css`: `{'margin': '18pt 0'}`.
- `.authored .case-section` · `@media print` · `assets/source/styles/site.css`: `{'padding': '7pt 0'}`.
- `.authored .case-metadata` · `@media print` · `assets/source/styles/site.css`: `{'margin': '12pt 0'}`.
- `.authored footer` · `@media print` · `assets/source/styles/site.css`: `{'padding': '8pt 0'}`.
