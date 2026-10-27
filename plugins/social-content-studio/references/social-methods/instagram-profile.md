# Instagram profile audit and rewrite

Use this method when the user asks to review, fix or rewrite an Instagram profile: name field, handle, bio, link, highlights, pinned posts, grid covers, category or contact options. It lives under `professional-social-proof` because the profile is the account's public proof surface. Career Studio still owns LinkedIn profile scoring and career positioning. If the request is really about job positioning, route it there and return here only for Instagram copy.

[Source and adaptation](../../libraries/instagram-agent/PROVENANCE.md): MIT `ig-profile` and `rubric.json`. The upstream 100-point rubric is **not** used as a score. Its weights are unvalidated, and no supplied evidence links any rubric item to follows, enquiries or sales.

## Boundaries

- **Use accessible evidence.** Accept supplied fields/screenshots/exports or inspect a profile through an available authorized read-only provider. Never collect credentials, scrape or start an unattended loop. If access is unavailable, request the missing fields without inventing them.
- **Drafting is not editing.** This method returns copy-ready field text and a change list. Changing the live profile is a separate action under `social-publishing`. If the current conversation already authorizes the exact profile edit, do not ask again; apply it through that owner and read it back. Resolve the requested state from the conversation; do not turn a supplied profile review into an unrequested live edit.
- **No fabrication.** Proof, client names, numbers, credentials and audience size come from the user's evidence or voice file. Where a fact is missing, write `{{proof: what you can verify}}` and list it.
- **Field limits are verified in the live editor.** Count the proposed text, but do not reuse unverified historical field limits. Check the current official guidance or live editor for the actual account before a change depends on a limit; report unavailable validation explicitly.
- **Search behavior is a hypothesis.** Upstream claims the name field is indexed by search. Treat it as plausible, not established. Put searchable words in the name field only where they read naturally and stay true.
- **No mandatory humanizer.** Review final copy with `social-editorial-review` as usual. Do not run AI-authorship scoring or strip characters. Keep the user's emoji, dashes, non-Latin script and RTL marks.
- **Private data stays in the project.** Do not create a home-folder profile store.

## Step 1: collect the profile snapshot

Ask once, in a single batch, for whatever is missing:

1. Name field (the bold line, not the handle) and handle.
2. Full bio text exactly as displayed, plus any line breaks.
3. Link(s), with where each one actually lands.
4. Highlight names, in order, with an approximate age of each.
5. Pinned posts and what each one is.
6. Top grid rows (a screenshot of the first two or three rows is enough).
7. Account type, category label and contact buttons shown.
8. The goal: what a good visitor does next (follow, enquire, buy, book, join a list), and who the visitor is.
9. Proof the user is willing to show publicly, from `voice-files.md` or the project.
10. Optional: profile visits, follows and link taps over a stated window, if they have them.

If the goal or audience is missing, ask. A profile cannot be judged without a destination. Proceed on the rest with visible placeholders.

Record what you received and what you did not:

```
SNAPSHOT  · supplied 2026-10-17 · source: 2 screenshots + pasted bio
received: name, handle, bio, link, 6 highlights, grid rows 1-2
missing:  pinned posts (not visible), category/contact, any metrics
goal:     enquiries from wedding planners (user-stated)
```

For a visual review, first map 3–8 observed anchors: source image/viewport, region, visible fact and intended correction. Verify changed anchors in the resulting native view or rendered candidate before visual signoff. Pasted text supports copy review only.

## Step 2: answer the decision question

Write one paragraph from the point of view of the stated visitor arriving from a single post. Answer two questions using only what is visible:

- Can they tell within the first glance what this account is and who it is for?
- Is the next step obvious and true?

Do this before itemizing. It keeps the audit about the visitor rather than a checklist.

## Step 3: itemized findings (no total score)

Assess each element as **Works / Weak / Missing / Unknown**. Each finding needs the observed evidence, why it matters to the stated goal, and the fix. "Unknown" means the element was not supplied; never score it as failing.

| Element | Question to answer |
|---|---|
| Name field | Name plus the plain words a target visitor would search, if true and natural? |
| Bio line 1 | Who it is for and what changes for them, in their words? |
| Bio remainder | One piece of verifiable proof or one specific offer? |
| Link | Lands on the page that matches the bio's promise? Works on mobile? Destination checked by the user? |
| Pinned posts | Do the pinned posts do distinct jobs (proof, offer explanation, introduction), or are they accidental? |
| Highlights | Named for questions a visitor actually asks; stale or contradictory items removed or moved? |
| Grid covers | Legible at thumbnail; topic recognizable without a tap? |
| Photo | Recognizable at small size; matches person vs brand identity? |
| Handle | Sayable and spellable; consistent with other channels if that matters to the user? |
| Category/contact | Matches the offer; contact route actually monitored? |
| Recency signals | Recent posting and replies visible? (Report what is observed; no fixed day threshold.) |
| Story presence | Is the visible current Story or highlight useful to the stated purpose? Absence is an observation, not a daily-posting failure. |
| Accessibility | Alt text on key images; text covers readable; no information carried only by emoji. |

Rank by **likely impact on the stated goal × effort**, and say it is judgment, not measurement. Typical first fixes are bio line 1, the link destination and the pinned posts, because they are cheap and directly visible. Deviate whenever the evidence says otherwise.

Do not produce "38/100". If the user insists on a number, give a per-element count ("4 Works, 5 Weak, 2 Missing, 1 Unknown") and state that it is not a validated quality or conversion measure.

## Step 4: rewrite in fix-first order

For each field changed, provide two or three options that take different angles: audience-first, outcome-first and proof-first. Do not offer three paraphrases of one angle. Note the character count against the conservative target and flag anything within roughly 10% of it.

Templates:

```
NAME FIELD  (target ≤30, verify in editor)
A  Dana Ruiz | Wedding planner contracts      (39 - OVER, shorten)
B  Dana Ruiz | Planner contracts              (31 - check counter)
C  Dana · Contracts for planners              (28)

BIO
A  Contracts that get wedding planners paid on time.
   {{proof: e.g. used by N planners - only if verifiable}}
   Free clause pack ↓
B  For wedding planners tired of chasing deposits.
   Template contracts + the clauses in the supplied pack.
   Clause pack ↓
```

For pinned posts, name the three jobs and map existing posts to them. If no existing post fits a job, say "**needs a new post**" and hand it to `short-form-video` or `social-content`. Do not pretend a rewrite fills that slot.

For highlights, propose names and an order, and list which to archive. Archiving requires a specifically authorized platform action and verified current controls; a content review alone does not authorize it.

For the link, give one recommended destination with its reason. If multiple links remain, give the order and labels. Note that destination content and UTM choices are the user's (Marketing owns measurement design).

For grid covers, give concise cover text appropriate to the actual thumbnail and display time. Route visual production to Graphic.

## Step 5: before/after and residual work

```
PROFILE REVIEW  · goal: planner enquiries · evidence: screenshots 2026-10-17

DECISION READ  (before)
A planner arriving from the contract reel sees "Dana | lover of lists ☕" and
no mention of contracts. The link goes to a general linktree. Unclear next step.

FINDINGS  (impact x effort, judgment)
1 Bio line 1     Weak     no audience or outcome         -> rewrite A/B
2 Link           Weak     7-item menu, contract pack 5th -> single page
3 Pinned         Unknown  not in screenshots             -> please send
4 Name field     Weak     name + emoji only              -> options A-C
5 Highlights     Weak     "Random", "2023"               -> Pricing/Results/About
...

REWRITES  (copy-ready, fix-first)
...

MISSING PROOF  {{N planners}} - confirm or remove
NOT A REWRITE  pinned "proof" post does not exist yet; grid covers need design
STATE  prepared copy · no profile field changed
```

If follow or enquiry data was supplied, propose one measurement to revisit, with a window and denominator. Examples: follows per profile visit, or link taps per profile visit, over two comparable windows. State that a change in that measure after the edit is observational. Seasonality, posting volume and which posts sent visitors are confounds. Pass it to `content-calendar` for review rather than declaring success.

## Edge cases

- **Brand rather than person.** Swap "introduction to the person" for "who is behind this / how it works". Logo photos are appropriate here.
- **Personal or creator account without an offer.** The goal may be follows or community. Skip offer and link conversion, and keep the decision read.
- **Regulated claims** (health, finance, legal) or employer/NDA limits. Apply the off-limits list from the voice file. Prefer a description of the service over outcome claims.
- **Multilingual profile.** Keep the original script, directionality marks and line order. Never normalize characters.
- **The user asks for "viral" bio lines or keyword stuffing.** Decline the stuffing; keep searchable words natural.
- **Career-positioning request on Instagram** (job hunting). Use the Career Studio evidence record for facts and keep the copy here.
- **Screenshots conflict with pasted text.** Ask which is current. Do not guess.
- **The user authorized edits and the computer-use/native route is available.** Hand off to `social-publishing` with the final field values and read back each field. Report fields that differ from the intended text.

## Acceptance checks

- [ ] Goal and visitor stated or marked missing.
- [ ] Every element marked Works/Weak/Missing/Unknown with evidence; unsupplied elements are not failed.
- [ ] No total score presented as validated; no conversion or reach prediction.
- [ ] Every number, client or credential traces to user evidence or appears as a placeholder.
- [ ] Field lengths counted; any required limits verified in the current account or explicitly unverified.
- [ ] Options differ in angle; copy reviewed by `social-editorial-review`; no characters stripped.
- [ ] Items that need new content or design are listed separately from rewrites.
- [ ] Actual state reported (prepared / edited-and-read-back); no live edit without authorization.
- [ ] Nothing written outside the project.
