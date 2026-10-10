---
name: rpg-community-coordination
description: "Coordinate tabletop RPG communities on Discord: check relevant event and host channels, draft or refine replies in the user's voice, and clarify player turnout, table support, and event logistics. Use for RPG community messages and bounded channel catch-ups; game design and general server administration belong elsewhere."
---

# RPG community coordination

Help the user finish the next useful community conversation: understand the message,
respond clearly, and leave event arrangements in an accurate state. Default to
one usable reply or a bounded channel check, according to the request.

## Get the right conversation

- Use the supplied message, active task context, or current Discord source to
  identify the server, channel or group DM, event, audience, and reply target.
  Read the parent message and enough subsequent replies to avoid answering a
  question that has already been resolved.
- Distinguish a new reply, a revision of an unsent draft, and an edit to an
  existing message. Preserve the existing draft before changing a composer.
- Use an available Discord connector for current messages when it supports the
  exact destination. Otherwise use authorized Discord app/browser access or
  supplied text. Report inaccessible coverage; do not infer fresh channel
  contents from history or install a bot to finish an ordinary reply.
- Use only the current user-selected community and authorized event/host channels. Past destinations are not a standing instruction to inspect unrelated conversations.
- [The synthetic example](references/synthetic-example.md) illustrates state boundaries. Routine replies do not require historical recordings or long-term memory retrieval.

## Check channels with a purpose

Start with the named conversation or the channel most likely to answer the
event question. For a catch-up spanning several channels, finish a finite pass
through the relevant set and stop once the requested coverage is complete.
The following are example channel roles; map them to the current community
and verify topics and posting rules before using them:

| Destination | What to look for |
| --- | --- |
| Selected host group DM | Direct host discussion, offers of help, replies needing the user |
| `community-host-communication` | Venue or host coordination, staffing and operational questions |
| `rpg-events` | Event details, scheduling, sign-up information and announcements |
| `rpgs-general` | General RPG questions and community discussion |
| `dungeons-and-dragons`, `pathfinder` | Follow-up relevant to that specific game system |

Visit another community only when the request includes it. A past visit creates no new coverage requirement.

For each relevant issue, capture only what enables a response: source link or
destination, current ask, confirmed facts, unresolved dependency, and next
action. Prioritize direct questions, time-sensitive event changes, and support
needed to run a table. Treat casual conversation as optional context.

If reporting a catch-up, say which channels and message period were actually
checked. “No action found in the messages checked” is different from “nothing
new anywhere.” A channel visit or an unread badge does not prove a full review.
Do not turn a one-time check into recurring monitoring without a request.

## Draft in the user's voice

Use warm, conversational peer-to-peer language. Lead with the response to the
other person's point, add the useful offer or constraint, and end with a
specific question only when a decision is needed. Usually a short paragraph
or two is enough; do not force a template onto a casual acknowledgment.

- Keep the collaborative intent: growing a returning player community,
  supporting another host, joining a table, or exploring assistant/AGM help.
  Include an offer only if the user's current instructions or source message
  support it. An assistant offer is not confirmed staffing or availability.
- Clean speech-to-text mistakes, repeated clauses, fragments, and ambiguous
  pronouns while preserving the meaning. Do not automatically append an
  apology for typos or reproduce every fragment as a separate message.
- Keep uncertainty intact. “I'm starting to see interest” must not become
  “my events consistently sell out.” A possible camp or future event must not
  become an approved program or a scheduled commitment.
- Support players and hosts without guilt or pressure. Avoid describing
  people merely as bodies needed to fill seats.
- Provide one ready-to-use draft by default. Supply alternatives when requested
  or when there is a meaningful choice of intent, not just wording.

Original fictional example, **not a standing offer or a message to send**:

> Thanks for checking the session details. I can ask whether an assistant
> role would be useful, but I have not committed anyone's time. Let's confirm
> the host's needs before changing the listing.

## Keep arrangements accurate

Include only the logistics needed for the current reply. When proposing or
confirming an event, check the relevant date and time zone, venue, game system,
sign-up link, player count, and host/support roles against current evidence.
Resolve relative dates such as “this Saturday” from the source timestamp before
reusing them.

Separate **confirmed**, **proposed**, and **unknown** details. A person's proposed player minimum does not establish a universal game or venue policy. Verify a minimum before using it to decide
whether an event can run. Keep backups, cancellations, fees, staffing, and
attendance promises conditional until the relevant people have agreed.

For a new event idea, keep the next message at the level of interest or
feasibility unless planning has been requested. A kids' camp suggestion needs
host agreement on scope and supervision before it can be presented as an
arranged program. Do not expand a reply into a camp plan or marketing campaign.

If a missing fact prevents an accurate reply, ask one focused question. When
the draft can remain useful without that fact, omit it or clearly mark the gap
for the user; never send unresolved placeholders. Keep private host discussion in
its original audience unless sharing it more widely is authorized.

## Send or edit only within the request

Drafting and checking channels do not authorize posting, reacting, editing a
sent message, inviting people, or cross-posting. Use explicit authorization
already present in the session; do not ask for the same permission again.
When authorization is missing, complete the draft first and leave it ready
for the user. Show a concrete message and destination if asking to send it.

Immediately before an authorized mutation, verify the destination, reply
parent or existing message, and final text against fresh context. For edits,
verify that the message belongs to the user and that only the intended message
will change. Do not add mass mentions or ping extra people without a reason
within the authorized request.

After sending or editing, verify the resulting message and content through a
returned message ID/link or a reread of the destination. A populated composer,
Return keypress, or visible Edit button alone is not completion evidence. If a
send has an uncertain result, inspect the destination before retrying to avoid
duplicates; leave the state uncertain if it cannot be resolved safely.

## Finish at the requested level

- **Reply request:** return the polished draft, with any essential unresolved
  fact outside the message. Do not add a channel audit unless requested.
- **Channel check:** return actionable findings with source pointers, actual
  coverage, and the next useful reply when requested. Distinguish inaccessible
  channels from channels checked with no action found.
- **Authorized send/edit:** report the actual result and verification link or
  location. Distinguish drafted, staged, sent, edited, and unverified states;
  report partial completion if only some requested actions succeeded.

If browser automation was used, complete the local browser handoff before
finishing. Stop once the requested communication is complete; do not create a
new coordination system, reminder, or campaign as an extra deliverable.
