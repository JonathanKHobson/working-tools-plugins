# Transcript evidence and learner reference workflow

Use this conditional procedure when auditing existing transcripts or adding claim-linked references. Course Production & Handoff owns integration; research/source review owns the quality of evidence. Reuse existing transcript components and project records. This method requires no new service, schema or top-level skill.

## 1. Establish the actual corpus

Read the current course identity, revision, video/lesson IDs, transcript text, timed cues, existing sources, glossary and exports. Inventory every supplied transcript and missing asset. Shared transcript UI does not establish that a course has been audited. For older courses, distinguish historical interface descriptions from claims intended to remain current.

Preserve the original spoken text and cue timing. Keep source errors or current corrections in clearly labeled editorial annotations. Do not silently rewrite speech to match new evidence. Untimed transcripts use stable paragraph or passage IDs; never invent timestamps. Audio accuracy requires listening checks and a separate stated scope.

For large corpora, partition deterministic cue/paragraph ranges. Record expected and observed IDs, counts, boundaries, overlap, omissions and zero-claim segments. Reject extraction with fabricated quotes, timestamps or missing coverage. Worker/model output proposes claims, not truth. Full segment coverage means every segment was screened, not that every factual error was discovered.

## 2. Audit consequential claims

For each candidate record its exact quote, video ID, cue/paragraph locator, claim, materiality, source candidates, disposition and uncertainty. Prioritize statistics, research findings, safety/access claims and changeable product behavior. Separate teaching advice, illustration, opinion and verifiable assertions. Keep broad thematic classifications in the audit record; only deliberate learner-facing decisions enter the course.

Open and assess the evidence. Prefer original research or official documentation when appropriate. Check the actual population, tool/version, comparator, outcome, timescale and scope. A report that someone made a claim is not independent proof of the event. Record secondary-only, abstract-only or inaccessible evidence honestly. Label background/context-only sources separately from sources that support a learner-facing claim. Do not attach a thematically related citation as proof of a specific unsupported assertion.

Use dispositions such as supported, supported with qualification, correction required, historical context, unsupported or unresolved. Keep the quoted claim distinct from the narrower statement justified by evidence. A material unresolved claim needs a visible editorial qualification or explicit course-owner decision, not just a private audit flag.

## 3. Present evidence without obscuring the transcript

Use stable source IDs internally and consistent numbered references within each video/transcript. Every displayed number resolves to the corresponding source entry at the end of that transcript. Reuse a source's number within the same scope. Preserve existing valid citations; renumber only through a complete mapping with all references checked.

Keep the transcript readable: attach a short, specific explanation at the relevant passage; put full source details and links in the end list. Distinguish support, qualification and correction. If several sources qualify one claim, give the full qualification once and concise source-specific notes on the additional references. Respect schema requirements without duplicating a paragraph beside every number.

Example: a spoken claim says “Everyone becomes twice as fast.” The editorial note can say “This study measured completion time on a bounded task in its sampled population; it does not establish a universal doubling [1].” A second study gets its own short scope note [2], not a duplicate correction. These are fictional examples, not empirical claims.

Place the source list at the end of the transcript, followed by the relevant glossary when the existing lesson design supports that order. Scope “In this transcript” terms to actual video content; label broader course glossary terms separately. Glossary definitions explain vocabulary and do not substitute for evidence. Confirm the glossary's relationship to the selected video rather than assuming it from appearance.

Keep plain and annotated exports distinct. Plain text preserves the source transcript; annotated text adds explicitly labeled notes and source references. Check actual downloaded files, not only generation code. If the product cannot represent an uncited editorial note, use an existing visible companion/guide location with a precise passage locator. Never create a fake source to satisfy the schema.

## 4. Integrate against current state

Use the existing course owner and import path. Read current state immediately before applying a scoped change; honor a single-writer or equivalent concurrency guard and revision checks. Refuse the wrong course, cue drift, missing source IDs and conflicting source definitions. Preserve unrelated lessons, exercises, guide text and existing evidence. Make replay idempotent. For intentional annotation repairs, replace only the identified old note and check the expected prior value.

Keep a baseline, scoped delta, rollback artifact and verification receipt in the owning project. An audit request does not itself authorize live publication. Apply only within the user's current authorization; prepare a concrete reviewable patch when publication is outside scope.

## 5. Verify and hand off

Check complete segment accounting, quote/locator validity, source-ID resolution, citation-number mapping, source URLs, annotation scope, glossary scope and unchanged speech/timing. Distinguish blocked automated URL access from a missing or dead source; a 403 response alone proves neither absence nor learner accessibility. Test representative multi-source notes and material unresolved claims. Reapply or simulate replay to prove no unintended duplicate edits.

For changed learner-facing content, map 3–8 anchors with IDs, source/viewport, region, selector if available, observed fact and intended action. Inspect the actual transcript, citation notes, end sources, glossary and exports in representative desktop/mobile learner views. Verify changed anchors after repairs. Rendered text inspection does not establish keyboard or screen-reader behavior; test those separately when claiming them.

Record saved revision, published version if authorized, fresh readback, tested viewports/roles, actual export hashes and remaining limits separately. A successful API save is not published verification. A final receipt supersedes older holds only for its expressly verified scope; retain historical receipts as history.

Return coverage, dispositions, exact artifact/revision, checks performed, visible unresolved issues and excluded checks. Separate source validation, technical integrity, rendered readability, human preference and learner outcomes. Positive feedback on presentation is not evidence of comprehension, retention or transfer.

## Reuse and method capture

For another course, repeat inventory and claim review against its own sources. Reuse the procedure and components, not the previous course's evidence judgments. Keep course identities, quotes, screenshots, private locators and approval history in the originating project. Capture one selected feedback-to-method checkpoint through the existing evidence owner, with provenance, allowed claims and missing proof. Changes to generic guidance, native installation and public release are separate states.
