# Sample UXHC Audit Output

This is a compact example shape for a lightweight skill-only audit. It is not a real report and should not be reused as evidence.

It shows two shapes: a basic landing page audit and a mission-context audit. The mission-context shape applies when audience constraints affect severity calibration.

---

## Example A — Basic Landing Page Audit

### UX Health Snapshot

Scope: one desktop landing page screenshot.

User goal: understand what the product does and choose a next step.

Overall read: the page appears visually organized, but the primary action competes with secondary links and the page does not make the next step obvious enough for a first-time visitor.

Top priority: clarify the primary call to action and reduce competing choices above the fold.

Evidence limits: this review cannot inspect hover, focus, error, loading, analytics, form submission, mobile layout, or real user behavior from a single screenshot.

### Top Issues

1. Primary action is not visually or verbally dominant.
   - Heuristic: H8 Aesthetic and Minimalist Design; H6 Recognition Rather Than Recall
   - Severity: 3, major
   - Evidence: multiple buttons and navigation links appear with similar weight near the first decision point.
   - Why it matters: users may pause or choose a secondary path before understanding the main intended action.
   - Fix: make one primary CTA visually dominant, move secondary links into a lower-priority treatment, and use action text that says what happens next.

2. The page does not clearly confirm what users can do after clicking.
   - Heuristic: H1 Visibility of System Status; H2 Match Between System and the Real World
   - Severity: 2, minor
   - Evidence: CTA language is generic and does not preview the result.
   - Why it matters: vague next steps increase hesitation and reduce confidence.
   - Fix: change the CTA to a user-centered action such as "Start a quick UX audit" or "Review my interface."

3. Support information may be too far from the decision point.
   - Heuristic: H10 Help and Documentation
   - Severity: 1, cosmetic
   - Evidence: explanatory text appears after the main actions instead of near the moment of choice.
   - Why it matters: users with questions may leave the primary path to search for reassurance.
   - Fix: add one short helper sentence near the CTA that explains what the user needs to provide.

### What Holds Up

- The visual structure appears calm and scannable.
- The page has enough hierarchy to support a quick first read.
- The issue is likely fixable through content and layout priority rather than a full redesign.

### What To Validate Next

- Check the mobile layout before shipping.
- Test whether a first-time user can say what the primary CTA does within 5 seconds.
- Inspect focus states, keyboard navigation, form states, and error recovery before assigning high confidence.

### Compact Recommendation

Before shipping, make the first decision point unmistakable: one primary action, one clear sentence explaining what happens next, and fewer competing links near the top of the page.

---

## Example B — Mission-Context Audit (Audience-Calibrated Severity)

Use this shape when audience context — surfaced through HIL questions — changes how findings should be scored. Include a Mission Context section at the top to frame the audit for the reader.

### Mission Context

This interface serves under-resourced learners accessing education on intermittent connections from low-end devices. Many users have limited screen time, limited data budgets, and limited prior experience with web apps. An issue that would score minor for a general consumer audience may score catastrophic for this audience — every lost session, failed load, or missing progress signal has real educational cost.

### UX Health Snapshot

Scope: desktop lesson player and learner profile, two pages.

User goal: complete a lesson and return to continue progress in a future session.

Overall read: the lesson experience is usable, but progress does not save for any user — including logged-in accounts. This breaks the core learning loop for an audience where returning to an unfinished lesson may not be possible.

Overall grade: C+ / 62% (audience-adjusted)

Top priority: fix progress persistence for authenticated users before any other change.

Evidence limits: review cannot inspect API behavior, offline mode, background sync, or real participant session data. Progress-loss finding was confirmed via live observation during authenticated session, not inferred.

### Top Issues

1. Progress does not save for authenticated users.
   - Heuristic: H6 Recognition Rather Than Recall; H7 Flexibility and Efficiency of Use
   - Severity: 4, catastrophic
   - Audience calibration: for general users this might score 3 (major). For learners with intermittent access and limited session windows, failing to persist progress may mean permanently losing work they cannot repeat.
   - Evidence: 0% progress ring observed after completing lesson steps while logged in. Confirmed across multiple lesson attempts.
   - Fix: implement server-side progress persistence keyed to authenticated user ID; confirm sync on session end and on reconnect.
   - Validate: log in, complete a lesson, log out, log back in, and verify progress is preserved.

2. Blank loading screen with no skeleton or spinner.
   - Heuristic: H1 Visibility of System Status
   - Severity: 3, major
   - Audience calibration: on slow connections, a 3–5 second blank screen causes users to abandon, thinking the page failed to load.
   - Evidence: 3–5 second blank white screen observed on lesson player load before Angular hydration. Page title shows "Loading | Oppia" during this window.
   - Fix: add a skeleton layout or branded spinner immediately on route change; update page title to the lesson name after load.

3. No exit or back button in lesson player header.
   - Heuristic: H3 User Control and Freedom
   - Severity: 3, major
   - Evidence: lesson player header does not show a visible exit control. Users who need to leave mid-lesson must use browser back button.
   - Fix: add a visible Back or Exit button in the player header. Confirm whether partial progress is preserved on early exit.

### What Holds Up

- Story metaphor (chapters, characters) aligns well with the mental model of learners (H2 strong).
- Error prevention on answer submission is adequate — no accidental submission risks observed.
- Visual design is calm and does not compete with lesson content.

### What To Validate Next

- Confirm progress persistence after the fix with authenticated sessions across devices.
- Test lesson loading on a throttled 2G connection to confirm skeleton load behavior.
- Review ARIA live regions and focus management with a screen reader on the lesson player.
