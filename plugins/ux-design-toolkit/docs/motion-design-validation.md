# Motion design routing validation

## Baseline, 2026-10-05

Source is a non-Git plugin directory. `motion-and-performance` and its existing reference covered purpose, interruption, reduced motion, cost and measurement, while the entrypoint did not explicitly name the shared visual principles of motion design or distinguish UI-state ownership from title/styleframe and video-render work. `design-studio` already linked the motion reference.

| Request | Expected owner | Baseline observation |
| --- | --- | --- |
| Design the loading-to-results transition so state and focus remain clear | UX `motion-and-performance` | Matching route existed; motion-design vocabulary and visual handoff were implicit. |
| Review a modal opening, interruption, and reduced-motion path | UX `motion-and-performance` | Matching methods existed; no explicit shared-principles bridge. |
| Create styleframes and kinetic type for a channel intro | Graphic motion design and Video Production | UX entrypoint did not explicitly bypass this production work. |
| Render a narrated code-authored explainer | Video Production `create-motion-graphics` | UX entrypoint did not explicitly bypass this production work. |

## Changes and forward check

Made the UX `motion-and-performance` description and body explicitly own interactive state, feedback, interruption, focus and reduced motion. The existing Design Studio reference now bridges shared visual principles and has a bounded research-intake section. Replaying the four requests against current entrypoint descriptions and links yields:

| Request | Forward route | Result |
| --- | --- | --- |
| Loading-to-results transition | UX `motion-and-performance` | Pass: state, feedback and focus ownership explicit. |
| Modal opening/interruption/reduced motion | UX `motion-and-performance` | Pass: interaction and alternate-motion path explicit. |
| Channel intro styleframes/kinetic type | Graphic `motion-design`, then Video Production as needed | Pass: UX entrypoint explicitly bypasses standalone motion piece. |
| Narrated code-authored explainer | Video Production `create-motion-graphics` | Pass: UX entrypoint explicitly bypasses production. |

The changed UX skill passed `quick_validate.py`, and its local links resolved. This is a routing review, not an exercised interface, reduced-motion rendering check, or installed plugin discovery test. Canonical plugin installation and versioning were left to the integration owner.

## Supplied research intake — 2026-10-05

Gap: the sixteen original pattern briefs needed a conditional implementation chooser and correction of overly absolute technique rules. Added original `motion-technique-selection.md` based on primary docs linked in that file. No PDF arrived with the pasted report. No third-party skill procedure, code, assets or package was admitted, downloaded for execution, or installed. Sites provider is unchanged; Graphic's existing prompt guide routes implementation decisions here.

Review distinguishes public availability from license, quality, maintenance and tested behavior. The report's blanket “all free, verified” claim is not adopted. Candidate counts/component counts and duplicate claims are not independently established. None of these twenty candidates is runtime-tested in this intake.

| Supplied candidate | Disposition |
| --- | --- |
| yousuf-git motion-craft | Worker inspected pinned c92708a670c85fe3d85c198b964924c297e31609; overlaps owner. No import; numerical/taste rules not standards. |
| thedavidmurray claude-make-interfaces-feel-better | Worker inspected public repo; reports archived May 12, 2026, MIT. Overlapping reference, no import; archive/license report is not full dependency audit. |
| elninotarifa-creator motion | Deferred without source audit: current owner covers microinteractions/layout; no demonstrated remaining method gap. |
| hemel2002 View Transitions/scroll skill | Deferred without source audit: primary platform documentation used for the chooser. |
| keiseilab keiseikit motion-design | Deferred without source audit: current vector playback and motion owners cover these lanes. |
| manufarbkontrast auto-animate | Deferred without source audit: no project requiring automatic list animation selected. |
| mblode pattern-auto-animate-ui-elements | Deferred without source audit: same proposed lane; duplication not independently proven. |
| greysquirr3l react-spring-physics | Deferred without source audit: no React Spring implementation gap established. |
| omkarbachhav24-ux triphoria motion-primitives | Deferred without source audit: no component selected for adoption. |
| tromset lenis skill | Deferred without source audit: smooth-scroll replacement is outside this skill update. |
| axiestudio react-spring notes | Deferred without source audit: chooser uses primary sources instead. |
| theatre-js/theatre | Deferred without source audit: timeline editor/runtime installation not needed for guidance. |
| rroledo motion-primitives-website | Deferred without source audit: component count, license and runtime claims unverified here. |
| florash pinky-ui | Deferred without source audit: claimed transform-only behavior not verified; no component needed. |
| worldofhacks alex-style motion-primitives | Deferred without source audit: copied component collection not needed; rights/count unverified. |
| dotLottie 2.0 specification | Existing vector-playback owner retained; no spec/runtime import or version migration. |
| erebuzzz pixasso motion reference | Deferred without source audit: library comparison overlaps original chooser. |
| easings.net | Optional reference left unimported; easing visuals cannot establish a universal timing policy. |
| sevastijan View Transitions guide | Deferred without source audit: primary platform guide used instead. |
| pungrumpy review-animations STANDARDS | Worker received 404 at supplied path; do not substitute another repo or call it verified. |

Candidate source URLs remain in the supplied conversation report. Selected review pointers: [motion-craft at reviewed revision](https://github.com/yousuf-git/claude-code-setup-forked/blob/c92708a670c85fe3d85c198b964924c297e31609/design/motion-craft/SKILL.md), [interface polish repository](https://github.com/thedavidmurray/claude-make-interfaces-feel-better), [unavailable standards path](https://github.com/pungrumpy/docker-doctor/blob/HEAD/.agents/skills/review-animations/STANDARDS.md). Revisit a candidate only for a specific missing behavior; pin and security-review its full reachable package before adoption.

Security: staged original technique reference scanned with Master Security Toolkit's local skillguard wrapper: 1 file, 0 active findings, 0 suppressed, digest 13868badea3bea6c709d5cc2dd5216b4174075c1f31a523e5193b3ad374b594f. Manual review: documentation links and original decision guidance only, no install commands, hooks, credentials or executable payload. Static scanning does not establish runtime safety, browser support, performance or licensing of the unadmitted candidates.

Behavioral checks for the guidance: interruptible tab switch may use CSS/WAAPI without forcing springs; equal point counts alone do not permit native path morphing; an image clipped toward collapse is hidden rather than revealed; an SVG event-triggered animation is possible; an eight-second repeat beside other content needs applicable playback control. These are instruction/source checks, not rendered demos. Visual QA is inapplicable to this text-only update; actual animation acceptance still requires playback and interface/graphic review.

Final changed-instruction scan: 4 files, 0 active findings, 0 suppressed; digest cf0028f161afb35893946758a2f2174db5b240a2479d035a1f5c5b328e1e32a2. Changed relative links and both affected skill validators passed.


## Part 2 intake — 2026-10-05

Received a pasted research summary; no attached PDF or full code/URL list was available. Updated the existing technique chooser and GSAP adapter only. Primary source checks support free former bonus plugins from GSAP 3.13, MorphSVG normalization, conditional FLIP scheduling, value-specific 3D flattening and SVG image restrictions. Sources are linked beside the decisions. No third-party code or skill body was imported; none of the proposed runtimes was installed.

Rejected as universal claims: guaranteed 60fps from transform/opacity, compositor-only clip-path/offset-distance everywhere, essential double-rAF for every FLIP, a fixed 200-point/node boundary, and static final keyframe regardless of real state. Retained the earlier reveal-direction correction. License scope remains distinct from price; the GSAP MIT method-source notice does not license its runtime.

All 23 new candidate labels remain deferred rather than verified/admitted. Exact identities, full URLs, licenses and runtime behavior were not supplied or audited here:
- Skills: svg-shape-morphing (anymotion); spring-physics-and-list-animation (orns-forge); motion-principles (motion-design-agent); anime-js-animations (rayspec); LOTTIE-RIVE guide (ultimate-animation-skill-pack); motion-canvas (claude-code-templates); genjutsu GSAP; claude-toolkit GSAP; gsap-motion (daovos). Existing pattern/GSAP/vector owners cover the stated lanes; exact source comparison awaits a concrete missing behavior and source.
- Libraries/tools: anime.js; Motion Canvas; Flubber; Vivus; react-flip-toolkit; FormKit auto-animate; canvas-confetti; Jitter. No selected implementation needs a new dependency. The claimed free status, versions and plans are not accepted without product-specific checks.
- References: MDN scroll-driven animations; MDN prefers-reduced-motion; Material 3 motion; Apple HIG motion; Paul Lewis FLIP; animate-anything. The exact Paul Lewis article was verified and linked; other proposed pages were not identified/loaded for this intake. No source package imported.

The Typed.js and KUTE.js exclusions remain source/version-sensitive research claims, not a global denylist. A read-only view of current Typed.js LICENSE.txt was obtained but no full version/use-specific licensing determination made. Neither tool is needed for this update.

Security and writing review: two staged original/maintained Markdown references scanned, 0 active and 0 suppressed findings; digest e5b0d5d93d720cb618f05b0d922439e47d14c0bc14cb81013ab481b2b2c64902. Manual review found no executable payloads, install commands, permissions, hooks or data transmission. Technical clarity review preserved conditional advice versus requirements, current semantic state and source/runtime license distinction. Static scan is not a runtime safety certificate. Text-only guidance: visual QA/design review inapplicable; no playback or performance test claimed.
