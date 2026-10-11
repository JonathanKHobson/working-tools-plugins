# Reference-driven and original product prototypes

Use for URL-to-code, screenshot-to-code, original interactive prototypes, app bootstrap, mobile variants and preview handoff. This is a complete original UX method. It contains no vendor framework, browser wrapper, copied screenshot assets, hidden engine or automatic publishing. The output can be implemented with current file/code/browser tools and the receiving project's actual stack.

## Select the requested fidelity and evidence

Identify whether the task is faithful reconstruction of an authorized supplied design, learning from a reference for an original product, or a new concept. Record target viewport/device, content and behavior authority, desired editable format, assets and requested stage. Read [task context](product-task-context.md); for a URL's visual language also read [reference-site analysis](reference-site-analysis.md). For a Figma implementation use current Figma tools and its native source/node contract. A screenshot is visual evidence, not measured CSS or hidden behavior.

Use the currently callable browser interface. In a Codex host with computer-use support, begin with the exposed `cua` entrypoint for the given URL/tab/browser and read its documentation before actions. Other hosts use their supported browser inspection contract. Inspect the actual page at the target viewport and meaningful scroll positions; observe navigation and states only within the authorized scope. If live access is unavailable, continue from the supplied image/source and mark interactions, breakpoints and typography values as unverified. Do not claim a live clone from an image-only pass.

Map 3–8 anchors: ID, source URL/image/node, viewport/page, approximate region, selector/node if available, observed fact and intended action. Useful anchors include shell/header, primary task block, content density/type hierarchy, main action, a state-dependent control and narrow viewport. Record a few supported dimensions and colors where inspection exposes them; distinguish measured values from estimates. Screenshot-specific cropping, zoom, device scale and browser chrome can distort apparent sizes.

## Translate the source into an implementation contract

Inventory content, sections, components, states and assets. Preserve source wording and identity only within the user's authorized reproduction scope. Use supplied or appropriately licensed assets; do not extract private account data, reproduce a third-party logo as the project's identity, or imply ownership of a referenced design. Reference-inspired work should transfer principles such as grouping and hierarchy into original content and implementation.

Specify layout constraints, spacing/type/color tokens, component responsibilities, image fitting, overflow, responsive rules and control states. List what the reference does not establish: hover/focus, validation, loading, permissions, server result, mobile layout and persistence. Give those states deliberate behavior consistent with the task and incumbent system. Avoid invented backend success or production accounts in a visual demo. Document fixture data and mocked services.

## Bootstrap proportionately

For an existing app, inspect its source and package configuration first. Reuse its framework, components, tokens, assets and development commands. Change the smallest relevant owner; do not install a new framework to render one screen. For a standalone simple demo, semantic HTML, CSS and small JavaScript may suffice. For a multi-screen/stateful prototype, use the user's selected stack or the supported Development/Build Web workflow after checking available dependencies. Pin and inspect new dependencies as required by the project. No external method plugin is needed.

Keep expandable projects modular: entrypoint, components/layout, state/data, styling and assets where these responsibilities actually exist. A requested one-file mockup can stay one file. Use system/project fonts until rights and availability for another typeface are verified. Use Graphic Design's existing asset workflow only when an actual asset is needed. Keep API credentials out of source and demo data.

Build one complete vertical path first: entry, meaningful action, pending, authoritative or explicitly simulated result, recovery and return. Then fill supporting surfaces. A linked wireframe can test navigation; a high-fidelity mockup tests composition; a runnable prototype tests its implemented behavior. None establishes production service operation without that integration and check.

## Responsive and mobile behavior

Use content-driven constraints rather than copying one screenshot's absolute coordinates. Inspect at the source width and a requested narrow width; check intermediate width when the layout changes. Decide which groups wrap, stack or scroll, preserve reading/action order and keep useful content visible. Test long labels, empty/large content, zoom and reduced motion. Use the complete [Responsive Design method](../../responsive-design/SKILL.md) for touch, input mode, orientation, safe areas, virtual keyboard, platform navigation and locale. Native mobile mechanics use the real iOS/Android authoring/runtime owner; a web preview is not a native build.

For forms, test focus and keyboard paths, validation, loading, duplicate submit and failure recovery. For simulated asynchronous actions, disclose the simulation in the review context and use deterministic fixture states for acceptance. Do not put irrelevant implementation jargon in product copy. Use semantic links/buttons, meaningful names, visible focus and text-equivalent state indicators.

## Preview with the actual available runtime

Use the project’s normal build and preview command, or a bounded static server for a static artifact. Start only the needed task-owned process, record its session/port, open the actual preview in a supported browser and inspect console/build failures as relevant. A listening server alone is not a rendered pass. File openings through `open_in_codex` show saved artifacts; browser tabs show actual URLs. Do not invent an app preview API.

If browser execution is unavailable, save the editable artifact and run applicable source/build checks, clearly reporting that rendered and interaction QA remain unperformed. A pre-rendered image verifies only its visible output. If publishing is authorized, use the requested existing host (for example Sites' actual create/version/deploy/status tools after reading their contracts), then read back the deployed URL and exercise its intended path. Creating a site or version is not proof of deployment.

## Compare, correct and deliver

Reinspect the same anchors at the same viewport. Compare hierarchy, bounds, typography/wrapping, spacing, asset cropping and main-action/state visibility. Document material deviations: an unavailable asset/font, inaccessible reference, missing backend or unobserved mobile state. Fix defects that block the task or the requested fidelity. A pixel similarity impression cannot establish accessibility, behavior or usability.

Exercise entry-to-result, keyboard navigation, back/return, invalid input, empty/loading/error/retry where relevant, and the intended mobile state. Verify links and that results persist only as promised. For meaningful changes, run the project checks that actually cover the affected path. Rendered QA and source/build checks are separate evidence.

Deliver editable source, the working local or hosted preview requested, fixture/integration limits, verified anchors and paths, and unresolved defects. Maintain the source-grounded DESIGN.md when appropriate. Stop temporary task-owned helpers after review unless the user needs the continuing preview; preserve other jobs and browser sessions. An explicitly authorized publish request continues to live readback. A preview request ends at a verified preview.

## Worked fixture and acceptance

A supplied desktop screenshot shows a booking card with date, three slots and a Confirm button. The reconstruction records card/header/action anchors, preserves supplied text and uses fictional slot data. On mobile the slots wrap while the chosen date and Confirm stay adjacent. Selecting a slot activates Confirm; submission shows pending then simulated confirmation; the forced failure fixture retains the selection and offers Retry. A repeated click while pending does not create a second action.

Acceptance: (1) screenshot anchors checked at the source viewport, (2) narrow layout has no cropped required control, (3) keyboard can select and confirm, (4) failure retains input, (5) result is visibly labeled as a prototype in the review handoff, and (6) source/preview links work. Missing live availability is a disclosed integration limit, not a passing booking test.
