# Instagram engagement: comments, replies, and DMs

Use this method for a supplied Instagram comment, a reply set under the user's post, a comment on another account's post, or a one-person DM draft. It is a writing and triage method only. Source provenance: [Instagram agent review](../../libraries/instagram-agent/PROVENANCE.md).

## Operating boundary

The input is pasted text, a supplied screenshot, a project-owned export, or a verified native record already available to the user. Do not scrape a feed or inbox, harvest contacts, collect passwords, operate a browser loop, auto-like, auto-comment, bulk-DM, or schedule replies. A prepared response is not sent. Any external action remains with `social-publishing`, its current provider capability, exact account authorization, and native readback. An approved provider feature for a person who already interacted is a separate capability and must be verified before use.

Use the existing Writing Quality final pass for the exact authored text. Preserve the user's voice, authentic quotations, source facts, and no-em-dash preference where applicable. Never claim that a style check proves human authorship or predicts reach.

## Comment on another account's post

Read the supplied post or Reel, account handle, and relevant context. If only a URL is supplied and the content is unavailable, ask for pasted content or a screenshot. Choose the comment type from the actual post:

| Type | Use when | Shape |
| --- | --- | --- |
| Add a datum | You have a source-backed number or observation | one specific addition with its condition |
| Add a missing case | The post is right but bounded | agreement, then the missing condition |
| Respectful disagreement | You have a supported counterpoint | name the valid part, then the precise fork |
| Extend one line | One line deserves useful development | quote only what is needed, then add substance |
| Ask the real question | An important decision point is missing | one answerable question |
| Receipt | You actually did the described work | a concise, attributable account |
| Correction | There is a material factual error | kind, brief, sourced correction |
| Reframe | Facts are sound but the framing hides a tradeoff | explain the alternative frame |
| One-liner | The post needs only a short truthful response | fewer than ten words when possible |

Write one to three sentences, one idea, and no pitch. Do not restate the Reel, open with generic praise, use emoji-only text, or mention a product, link, or profile unless the post itself makes that directly relevant and the user has a clear reason. Provide two meaningfully different options and recommend one with a source-grounded reason. Do not use unsupported “early comment” or visibility claims as a promise.

## Batch comments

When given several posts, return one distinct comment per supplied post, preserving its URL/ID, account, comment type and source basis. Account for every input, including skips and missing context. Review repeated phrasing, repeated-account contacts and duplicated points across the set; reduce formulaic repetition without inventing facts. Respect the requested batch size, not a compulsory quota. Reuse an existing project engagement record if one exists; no home-directory log or new contact store is required. Batch drafting still grants no batch-send authority.

## Reply under the user's own post

Triage every supplied comment and report counts before drafting. Use these buckets:

| Bucket | Treatment |
| --- | --- |
| Correction/safety concern | Address a material correction or safety concern promptly before routine engagement |
| Keyword/resource request | Deliver the promised resource or explain the verified handoff |
| Lead/problem | Answer publicly first, then offer one bounded next step |
| Substance | Give the most complete supported answer |
| Question | Answer the question; flag a future Reel only as a candidate |
| Support | Acknowledge briefly or leave a reaction if the user chooses |
| Noise/abuse/bait | Skip, hide, or moderate only within authorized native controls; explain the recommendation |

Answer the actual question, match the commenter’s length, use a handle once when useful, and keep a criticism response factual. Do not promise a call, file, referral, discount, or private help without authorization. Never bulk-DM people who did not initiate contact. A question can become a Reel candidate, but this method does not create or publish that Reel.

Return every supplied comment ID, classification, copy-ready response, skipped reason, and uncertainty. Make the sum of categories account for all supplied items. Keep a private engagement record only in the owning project if the user already has one; do not create a global home log.

## One-person DMs

Classify the trigger before writing:

1. **Hand raised:** the person commented a keyword, replied to a Story, answered an interaction, or asked for a resource.
2. **Warm approach:** there is a genuine, recent conversation or contribution history.
3. **Specific collaboration or brand proposal:** a concrete idea, fit, and requested contribution.

Without a real trigger, label it cold outreach. If the user already requested that message, draft it without another permission question; otherwise keep it a recommendation. Never invent familiarity, a mutual, or prior viewing. Career outreach uses Career Studio; ordinary Instagram community conversations stay here.

For a keyword delivery draft, put the resource first, include one useful usage line, and optionally end with one easy question. For a warm approach, use two to four sentences, reference the specific post or exchange, give something useful before asking, and make one small ask. Keep links and calendars out of the first message unless the user specifically needs them and the destination is verified. A collaboration pitch states what was observed, the concrete idea, what the recipient receives, and what is requested.

Prepare follow-ups only within the requested scope and when a new, truthful reason exists; choose a bounded cadence from context rather than a universal count or delay. Label their proposed dates relative to the first message, never as scheduled sends. The close-the-loop message should release pressure. Stop when the person declines, opts out, or does not engage after the bounded sequence.

## Output contract

```
INSTAGRAM ENGAGEMENT REVIEW
surface: comment | reply | DM
source/account: <supplied identifier>
classification: <type or bucket>
options/replies: <copy-ready text>
DM character count: <exact count of final draft, advisory; verify any actual limit>
follow-up: <only if requested, proposed date/timezone and new reason, never scheduled>
recommendation: <one option and evidence-based reason>
external action: none; user/provider must send if authorized
prose review: completed | unavailable
uncertainties: <missing context, policy or capability>
state: prepared
```

