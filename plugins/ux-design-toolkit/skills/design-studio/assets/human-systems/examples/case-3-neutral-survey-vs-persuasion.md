# Case 3 — Neutral survey versus persuasion, same facts (synthetic)

**Labels:** synthetic. No survey was fielded and no promotion was sent. Owners: survey instruments belong to Survey Studio (`survey-studio:survey-strategist`), which is referenced by L11 and L25 but wasn't inspected by this lane. Respondent-facing wording polish belongs to `natural-prose-editor` via L25. Promotional copy belongs to marketing-strategy-studio / lane05. This case shows the **boundary**; it doesn't add a new survey method.

## Shared facts

These are the same as case 1: S04 has enrollment 14 of 30 and a rating of 4.6 from 5 responses. The coordinator has two separate goals:

- **(a) Research:** learn why S04 enrolled poorly.
- **(b) Promotion:** raise enrollment for S04's next run.

## "Before": one merged instrument (illustrative)

> 1. How much did you love our acclaimed Data Storytelling workshop, rated 4.6 stars by participants?
> 2. Was the timing and location convenient? (Yes / No)
> 3. Don't you agree more colleagues should attend?
> 4. Why didn't you tell others about this great session?
> 5. Share this workshop with a friend → [link]

### Baseline-style critique (illustrative)
"Make the survey shorter to improve completion; add a progress bar; make the Share button more prominent (Fitts' law)."

That critique tunes completion and conversion. It leaves the measurement problems untouched and misapplies Fitts' law to promotion salience (HS-01 "when not to use").

## Upgraded critique

| ID | Item | Problem | Evidence | Fix |
|---|---|---|---|---|
| S1 | Q1 | Leading and loaded ("love", "acclaimed"). It embeds a claim (4.6) from only 5 responses | X09 p. 264 #6; U13 [0006] | "How would you rate the workshop overall?" on a labelled scale, with a "Did not attend" filter first |
| S2 | Q2 | Double-barrelled (timing *and* location), and a forced yes/no | X09 p. 264 #7, #5; U13 [0005], [0009] | Split into two items with exhaustive options that include "Not applicable" |
| S3 | Q3 | Invites agreement and asks for an opinion on other people's behavior | X09 #6; the chapter flags acquiescence (p. 263) | Drop it. It serves (b), not (a) |
| S4 | Q4 | Presupposes the respondent didn't tell others and that the session was "great" | X09 #6; U13 [0009] ("Why do you support such an unfair policy?") | If word of mouth matters: "Did you mention this workshop to anyone? (Yes / No / Don't remember)", with a skip-logic follow-up |
| S5 | Q5 | A persuasion action inside a research instrument. It changes the respondent's role and the survey's purpose | X09 p. 263 framing (the questionnaire scripts a researcher–respondent conversation); research contract "keep neutral research separate from marketing" | Remove it. Offer sharing, if at all, *after* the survey is submitted and clearly separate from it |
| S6 | Overall | Missing the decision the research serves: *why* enrollment was low. Nothing asks about awareness, scheduling conflicts, relevance or prerequisites | L11 lines 5–7 (start from the decision); X09 p. 264 order advice | Put a filter first ("Were you aware of this workshop before it ran?"), then awareness, timing and relevance items, grouped by topic and moving from general to specific. Target non-enrolled invitees too, because attendees can't explain non-enrollment. Survey Studio owns sampling |

### Neutral research draft (for handoff to Survey Studio; not a fielded instrument)

1. Before today, were you aware that the "Data Storytelling Basics" workshop was offered in week 3? (Yes / No / Not sure)
2. *[If yes]* Which, if any, of the following affected whether you enrolled? Select all that apply. (Schedule conflict / Topic not relevant to my work / Unclear what the workshop covered / Cost or approval / I did enroll / Other: ___ / None of these)
3. *[If enrolled]* How would you rate the workshop overall? (1 Very poor – 5 Very good, labelled; Prefer not to say)
4. Is there anything else about how workshops are scheduled or described that we should know? (optional, open)

Two further requirements: keep the item IDs stable, and have Survey Studio QA the draft and own the version before it is fielded (L25).

### Separate promotion (for lane05 / marketing; not sent)

- A claim like "rated 4.6 out of 5" must disclose the base: "4.6 out of 5 from 5 participants". Without the base it overstates the evidence, and the benchmark brief forbids implying significance.
- Research responses aren't marketing assets. Quoting a respondent in promotion needs consent that the survey never asked for, so quoting is excluded by default.
- Promotional urgency must be true. "Only 16 seats left" is technically true of 14/30 enrollment, but it frames low demand as scarcity, so this packet flags it as misleading. That's lane05's call.

**What changed between critiques (same facts):** the baseline optimized completion and sharing. The upgraded critique separates the two goals. One neutral instrument serves the enrollment question (a); promotion (b) moves to its own channel with the evidence base disclosed. Both are routed to their existing owners.
