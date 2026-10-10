# Citation Integrity

Use this guide whenever a draft contains factual claims, quotations, links, books, articles, identifiers, footnotes, or references.

## Contents

- Four-layer verification
- Unknown-source rule
- Link existence
- Identifier validation
- Metadata and claim match
- Book and page locators
- Reference placement and reuse
- Tracking and interface residue
- Date plausibility
- Citation case studies

## Four-layer verification

Verify each material citation at four distinct layers:

1. **Existence:** Does the source or identifier resolve?
2. **Identity:** Do author, title, publication, date, edition, DOI, ISBN, and URL describe the same source?
3. **Location:** Is there a page, section, timestamp, table, paragraph, or stable fragment that lets a reader find the support?
4. **Entailment:** Does the located passage actually support the draft’s exact claim and degree of certainty?

A real source can fail at layers 2–4. A resolving DOI is not enough.

## Unknown-source rule

When a source is unavailable and you cannot verify its content, treat both its existence and the attributed finding as unknown unless you have independent evidence for either. A source missing from the supplied material or unreachable in this environment is not thereby nonexistent or fabricated. A syntactically valid DOI, a citation in the draft, or a plausible topic does not establish what the source reports. Weakening an absolute claim to “some,” changing “proves” to “reports” or “may,” or appending “unverified” still invents a finding if no source supports it. Do not assert that a source reports any outcome you have not checked.

Omit the empirical finding from publication-ready prose, or leave a conspicuous evidence-needed placeholder for the author. A replacement may use only product facts independently supplied or verified for this task; the unsupported claim itself is not evidence of a feature or benefit. If no such facts are available, omit the sentence or use the placeholder. Do not supply a guessed result, direction, population, quotation, source assertion, product feature, or outcome.

**Synthetic contrast, with no source text available:**

- **Unsupported draft:** “The cited paper proves every learner became more confident.”
- **Still unsupported:** “A cited source (unverified) reports improved confidence among some learners.”
- **Safe working draft:** “[EVIDENCE NEEDED: verify the paper and its exact learner-confidence finding before making this claim.]” Omit the sentence if a placeholder is inappropriate for the destination.

## Link existence

Multiple dead links in a newly created document deserve investigation, especially if archives never captured them. But a failed request is not proof that a source is fictional.

Check for:

- institutional authentication or library access;
- geographic restrictions;
- bot blocking;
- a URL mangled by a citation tool;
- a missing start or end from manual copy/paste;
- a site move or redirect;
- an archived version;
- an identifier-based route such as DOI, PMID, ISBN, or report number.

Record `unreachable from this environment` separately from `confirmed nonexistent`.

## Identifier validation

### DOI

A DOI should match DOI syntax and resolve through `https://doi.org/`. Then compare the returned metadata with the citation.

**Failure:** the DOI resolves to an unrelated article with different authors and title.

**Repair:** find the correct DOI from the publisher or Crossref. If none can be verified, remove the DOI and mark the citation for source recovery.

### ISBN

Validate the ISBN-10 or ISBN-13 checksum after removing hyphens and spaces. Then compare title, author, edition, and publisher in a library catalog or publisher record.

An ISBN with a valid checksum can still identify the wrong book.

### Other identifiers

Validate PMID, arXiv ID, report number, court citation, patent number, or archival call number in its authoritative registry. Very low or generic identifiers attached to unrelated subjects may indicate a tool or copy/paste error.

## Metadata and claim match

Check every field against the source:

- author spelling and order;
- article or chapter title;
- journal, book, proceeding, or site;
- volume, issue, pages, and year;
- edition for books;
- publication date versus update or access date;
- quotation punctuation and omitted words;
- source type: press release, profile, news report, review, primary study, or commentary.

Do not turn:

- a press release into independent reporting;
- a passing mention into a profile;
- one critic into “critics”;
- a source’s quoted subject into the source’s own conclusion;
- correlation into causation;
- a proposal into an implemented program;
- an abstract claim into a result the paper did not test.

## Book and page locators

A whole-book citation is often too broad for a specific claim. Ask for a page, chapter, section, or searchable digital edition.

**Weak:** A general political book cited for a precise claim about Burke, with no page or a page that never mentions Burke.

**Better:** Give the page containing the passage and quote or paraphrase only what that passage supports.

No URL is not automatically an error; many legitimate books are offline or paywalled. The issue is whether a reader can verify the claim.

## Reference placement and reuse

Check destination-specific syntax for:

- a citation immediately following the supported claim;
- named reference defined once and reused correctly;
- every declared named reference used in the body;
- every reused name defined somewhere;
- no full duplicate citation after every sentence;
- no list of sources detached from the claims they supposedly support;
- no leftover back-reference arrows, footnote UI labels, or exported numbering.

In MediaWiki, a `<references>` list full of named definitions does not cite anything unless the names are invoked inline. In Markdown, a bibliography does not establish which sentence each source supports. In academic styles, follow the required note or author-date system.

## Tracking and interface residue

Review URLs containing:

- `utm_source=chatgpt.com`;
- `utm_source=openai`;
- `utm_source=copilot.com`;
- `referrer=grok.com`;
- `ppl-ai-file-upload`;
- temporary tokens, session IDs, or private download signatures.

Remove unnecessary tracking parameters after confirming the clean URL still reaches the same source. Tool involvement does not by itself prove that prose was generated, but the URL should be stable and privacy-conscious.

Also scan for internal citation artifacts listed in `communication-and-markup-patterns.md`.

## Date plausibility

Check:

- placeholder dates such as `2025-XX-XX`;
- impossible dates;
- an access date before publication;
- a future access date;
- multiple access dates suspiciously old relative to a newly created document;
- date-style inconsistency inside one document;
- a source update date presented as original publication.

Old access dates can be legitimate when citations were copied, research was conducted offline, or content moved between documents. Investigate before changing them.

## Citation case studies

### Case 1: DOI exists, source is wrong

**Draft claim:** A specific 1974 engineering paper established a limitation of Ohm’s law.

**Audit:** The DOI resolves, but the returned article has a different title and subject.

**Action:** Do not “fix” the title to match the DOI and keep the claim. Find a source that actually supports the limitation, or remove the citation and flag the claim.

### Case 2: Real book, unsupported page

**Draft claim:** A book frames modern politics through Burkean prescription.

**Audit:** The book exists, but the cited page does not mention Burke or the asserted framing.

**Action:** Search the book. If the idea is absent, remove the attribution. A plausible source is not a supporting source.

### Case 3: One article becomes broad consensus

**Draft claim:** Scholars widely interpret the event as a policy reversal.

**Audit:** One news analysis and one syndicated copy are cited.

**Action:** Write `Columnist Priya Sen described the event as a policy reversal` if accurate, or remove the consensus claim.

### Case 4: Source list without inline use

**Draft:** Four named references appear in a closing reference block; the body never invokes them.

**Action:** Attach each source to the exact supported sentence. Remove unused sources. Do not leave a decorative bibliography to imply research.

### Case 5: Placeholder URL

**Draft:** `url=PASTE_REPORT_URL_HERE` with a polished claim.

**Action:** Block release. Recover the report and verify it, or remove the claim. Never substitute a guessed URL.

### Case 6: Source performance in prose

**Weak:** The organization has been covered in numerous respected national outlets, demonstrating sustained significance.

**Better:** The regulator’s report says the organization processed 18 percent of the state’s claims in 2025.

The better sentence states what a source establishes, not that sources exist.
