# Editable FigJam workshop boards

Use for a requested FigJam board or its functional review. Workshop Facilitation owns agenda and decision process; UX Design owns hierarchy; Instructional Design owns learner alignment when this is a lesson. Those are optional collaborators, not prerequisites for a scoped editor task. This guide supplies authoring and verification, not a mandatory eight-stage template.

## Preserve the target and choose the actual tools

Resolve the requested file/page from current task evidence. Read existing nodes, text, links, bounds, and active collaboration state before writing. Record protected objects and source IDs. Place new work in a verified clear area unless revisions to existing content are authorized. A rebuild preserves original participant material and its links before changing presentation; normalization adds a labeled summary, never silently replaces the source.

Discover FigJam-compatible reads and writes. A Design-only metadata tool or auto-layout workflow is not evidence of FigJam support. If using `use_figma`, first read the installed `figma-use` skill and follow its font-loading, returned-ID, page-switch, and recovery contract. Native UI availability does not establish bridge availability. A supplied JSON manifest is authoring guidance unless the actual tool explicitly supports it as an import format.

Use editable sections, text, stickies, or shape-with-text cards. Inspect object types, text sublayers, supported sizing, and font mappings; do not assume every sticky behaves like a Design text node. A generated diagram or board image is not an editable workshop. Keep a logical-ID to actual-node-ID map with created versus preserved status. After an uncertain write, inspect returned IDs and existing objects before retrying; repair the affected batch rather than duplicating rooms. One writer owns a canvas region.

## Build one working view before multiplying it

Start with an orientation cue, one immediate question, a nearby response location, and a visible completion cue. Keep a short route and indexed evidence/parking links. Preserve original source questions in Reference rather than presenting the entire question bank as simultaneous assignments. Keep authority, constraints, and criteria available from the start. Future activities can be revealed in sequence; evidence and alternatives needed for the current task stay available together.

Build a representative section using realistic response length, then inspect it in the actual editor before repeating the pattern. Use a shallow reading order, meaningful object names, concise copy, and labeled semantic color. Expand or link detail when content overflows; do not shrink essential text to preserve arbitrary geometry. Canvas font units and whole-board fit do not establish laptop readability. Template dimensions, card counts, timing, and type sizes are starting choices to test.

## Presentation controls are not access controls

The following are documentation-based checkpoints, not claims of live support in the current account. Recheck only the capabilities the task uses.

| Capability | Check and honest fallback |
|---|---|
| Section reveal | The documented SectionNode property is `sectionContentsHidden`; use only if exposed by the current bridge and verify the editor result. Otherwise use the native UI. General node visibility, distance, and covering rectangles are not equivalent. If reveal cannot be verified, report that gap and use an explicit manual navigation plan. |
| Background-only lock | Check input editing **and containment**: record each intended child's `parent` ID and section membership before/after locking, then reveal and re-hide. An editable response alone does not pass this combination. If locking reparents content to the page, restore the intended membership and leave the staged background unlocked, reporting the tradeoff. A generic `locked` property or full lock is not proof of native background-only behavior. |
| Links and following | Home/Back/Next/Reference must use real targets. Navigation does not automatically reveal a section. Offer Spotlight/follow with opt-out where available; a local viewport change proves nothing about other participants' viewports. |
| Voting, when needed | Verify eligibility, candidate object type, vote count, result attribution, and explicit ending. Figma documentation describes choices concealed during voting and attributable afterward, with manual session ending. Do not promise anonymity, a facilitator-only control, automatic timer ending, or enforced one-vote-per-candidate without testing the claimed behavior. Use independent written candidate IDs followed by simultaneous submission as a disclosed nonanonymous fallback. |
| Keyboard and screen reader | Rehearse a meaningful contribution and linked navigation without precision dragging. Supply synchronized text/scribe access. Test the actual browser, role, and assistive technology before claiming support; a text companion does not itself pass a screen-reader test. |

Hidden sections are presentation controls, not confidentiality or a proven facilitator-only permission. Keep confidential facilitator notes in a separate unshared document. Do not widen sharing, publish a template, install widgets, purchase a plan, or alter a real active vote as an incidental workaround.

## Regressions observed in one live editor

The implementation handoff reported the following actual-editor findings; see [provenance and scope](sources.md#live-editor-regression-handoff). Use them as checks in the current environment, not universal FigJam behavior or a guarantee that a workaround will hold elsewhere.

- **Reveal and navigation:** authoring `sectionContentsHidden` produced a hatched closed-eye state; following the section's node link did not reveal it. The native eye control revealed and re-hid two working sections. Test navigation and reveal separately.
- **Locking versus membership:** native Lock background only left a response editable but moved contained objects to the page: their `parent` IDs changed and `section.children` became empty. This undermined section-based reveal/re-hide. Restoring parent membership and leaving staged section backgrounds unlocked was the chosen recovery. Recheck both containment and visible hide/reveal after changing a lock. Locking separate static objects is a possible alternative, still untested by this handoff; do not advertise it as a verified fix.
- **Hidden-section sizing:** resizing while hidden did not reliably persist through reveal. Revealing first, then using the UI's Resize to fit corrected containment in that environment. Recheck visible bounds and membership after reveal; do not trust a hidden-state size write alone.
- **ShapeWithText overflow:** fixed dimensions clipped realistic content. The reported repair used square shapes, measured text height, and room reflow. Choose the supported shape type that fits the task, measure actual wrapping, and recheck the containing room with a long response and an additional distinct idea. Do not assume dimensions that accepted a write will fit rendered text.
- **Quota boundary:** an authoring-tool quota stopped further API writes after partial completion. Preserve the node map and completed results; use an already authorized computer-use path for remaining editor work and QA when available. Record the exact blocked surface instead of claiming the whole editor is unavailable, looping the API, or changing accounts/plans.

## Verify and deliver

Create 3–8 anchors under the operating contract. Useful anchors cover opening orientation, current prompt/input, evidence route, simultaneous alternatives, decision/actions, and editor controls. Record actual viewport and zoom; inspect a small laptop view around 1366×768 and a larger view around 1440×900 where available, with normal editor chrome. Record deviations. These are practical test sizes, not universal benchmarks.

Use clearly labeled test data in an authorized rehearsal area/copy, preserving real participants and vote history. Exercise:

- Entry and return links; one native response edit; a long response and overflow contribution without clipping or loss.
- Reveal then restore a future section; verify intended parent IDs and membership, visible bounds, and editable inputs. If background protection is used, test it in combination with reveal. Record an unlocked-background fallback as a tradeoff, not a protection pass.
- Evidence/unknowns and all shortlisted options under the same criteria; a minority concern stays findable.
- Decision, explicit deferral, and an action with unconfirmed ownership; no invented consensus or accepted commitment.
- Relevant vote/follow behavior and a meaningful keyboard/non-drag route. Record the actual tested roles. A single account or screenshot cannot establish multiplayer behavior; unavailable participant/assistive-technology sessions remain `not tested`.

For each check record capability, `verified/pass`, `failed`, `not tested`, or `not available`, role/environment, action, observed result, evidence, and fallback. API readback verifies a property; actual editor interaction verifies a control. A failed required interaction is a readiness gap, not a pass because a fallback was described. Repeat only affected checks after fixes. Keep operator rehearsal separate from participant usability evidence.

Deliver real board/start/decision links where applicable, node map, working-scale screenshots, relevant test results, and a concise reveal/review/reset guide. At close, leave completed work usable in review mode with decisions and unresolved items findable. Reset only an unused master or authorized new-session copy; preserve historical contributions and results. Keep the participant text companion consistent with the final board.

## Evidence basis

Adapted from the supplied FigJam Collaboration Research Handoff (2026-10-03), particularly its implementation and acceptance-test guidance; see [source and verification scope](sources.md#figjam-collaboration-adoption). The later implementation handoff supplies bounded live observations above; this plugin-maintenance task did not independently operate the board. Neither the inherited report nor these checks establishes general effectiveness or participant accessibility.

Official references: [sections and native lock/reveal](https://help.figma.com/hc/en-us/articles/4939765379351-Organize-your-FigJam-board-with-sections), [SectionNode API](https://developers.figma.com/docs/plugins/api/SectionNode/), [voting](https://help.figma.com/hc/en-us/articles/9359912208663-Run-voting-sessions-in-FigJam), [StickyNode API](https://developers.figma.com/docs/plugins/api/StickyNode/), [font loading](https://developers.figma.com/docs/plugins/api/properties/figma-loadfontasync/), [Spotlight](https://help.figma.com/hc/en-us/articles/5025214483351-Facilitate-meetings-with-spotlight), [screen-reader guidance](https://help.figma.com/hc/en-us/articles/14477051168791-Use-FigJam-with-a-screen-reader). Product facts require current documentation and task-specific verification.
