# Source Coverage Map

This map accounts for every substantive section in the supplied 1,608-line capture of Wikipedia's “Signs of AI writing” page and the live page checked on 2026-07-21. The Humanizer converts those observations into editorial checks; it does not reproduce the article or treat the signs as authorship proof.

## Caveats

| Source section | Humanizer location |
| --- | --- |
| AI detection tools | `human-signals-and-false-positives.md` → Detector limits |
| Your detection ability | `human-signals-and-false-positives.md` → Human judgment limits |

## Content

| Source section | Humanizer location |
| --- | --- |
| Regression toward generic, positive descriptions | `content-patterns.md` → Generic smoothing |
| Undue emphasis on significance, legacy, and broader trends | `content-patterns.md` → Inflated significance |
| Broader debates and philosophical questions | `content-patterns.md` → Manufactured breadth |
| Generic ecology and conservation claims | `content-patterns.md` → Domain-shaped generic filler |
| Canned emphasis on notability, attribution, and media coverage | `content-patterns.md` → Coverage instead of content |
| “Active social media presence” language | `content-patterns.md` → Digital-presence boilerplate |
| Superficial analyses and trailing participial claims | `content-patterns.md` → Fact plus unearned interpretation |
| Promotional and advertisement-like language | `content-patterns.md` → Puffery and brochure voice |
| Cultural-heritage, corporate, and product-praise subtypes | `content-patterns.md` → Domain-shaped puffery |
| Vague attributions and overgeneralized opinions | `content-patterns.md` → Unnamed authority and inflated consensus |
| Outline-like “challenges and future prospects” conclusions | `content-patterns.md` → Canned tension and uplift |
| Leads treating lists or broad titles as proper nouns | `content-patterns.md` → Title-as-entity leads |

## Language and grammar

| Source section | Humanizer location |
| --- | --- |
| High density of “AI vocabulary” | `language-patterns.md` → Vocabulary clusters |
| Vocabulary shifts across model eras | `language-patterns.md` → Time- and model-sensitive cues |
| Avoidance of basic copulatives | `language-patterns.md` → Evasion of is, are, and has |
| Negative parallelisms | `language-patterns.md` → Contrast templates |
| “Not just X, but also Y” | `language-patterns.md` → Additive correction |
| “Not X, but Y” and “no X, just Y” | `language-patterns.md` → Dramatic negation |
| “X rather than Y” | `language-patterns.md` → Reversed contrast |
| Rule of three | `language-patterns.md` → Automatic tricolons |
| Lexical diversity and elegant variation | `language-patterns.md` → Synonym cycling |

## Style

| Source section | Humanizer location |
| --- | --- |
| Title case headings | `structure-and-formatting-patterns.md` → Heading case |
| Overuse of boldface | `structure-and-formatting-patterns.md` → Mechanical emphasis |
| Inline-header vertical lists | `structure-and-formatting-patterns.md` → Label-colon lists |
| Overuse of em dashes | `structure-and-formatting-patterns.md` → Em-dash audit |
| Emoji as formatting | `structure-and-formatting-patterns.md` → Decorative emoji |
| Unusual use of tables | `structure-and-formatting-patterns.md` → Tables that should be prose |
| Curly quotation marks and apostrophes | `structure-and-formatting-patterns.md` → Quote-style consistency |
| Skipping heading levels | `structure-and-formatting-patterns.md` → Heading hierarchy |
| Thematic breaks before headings | `structure-and-formatting-patterns.md` → Repeated separators |

## Communication intended for the user

| Source section | Humanizer location |
| --- | --- |
| Collaborative communication and canned helpfulness | `communication-and-markup-patterns.md` → Prompt-recipient residue |
| Advice about how to use or submit the generated text | `communication-and-markup-patterns.md` → Process instructions left in output |
| Knowledge-cutoff disclaimers | `communication-and-markup-patterns.md` → Model limitation residue |
| Speculation about gaps in sources | `communication-and-markup-patterns.md` → Unsupported absence claims |
| Phrasal templates and placeholder text | `communication-and-markup-patterns.md` → Unfilled scaffolds |
| Placeholder dates, URLs, publishers, and infobox comments | `communication-and-markup-patterns.md` → Placeholder scan |

## Markup

| Source section | Humanizer location |
| --- | --- |
| Markdown used in a non-Markdown destination | `communication-and-markup-patterns.md` → Destination syntax mismatch |
| Mixed Markdown and wikitext | `communication-and-markup-patterns.md` → Mixed markup |
| Broken wikitext | `communication-and-markup-patterns.md` → Syntax and template validation |
| ChatGPT `contentReference`, `oaicite`, `oai_citation`, `turn0search0`, `attributableIndex` | `communication-and-markup-patterns.md` → Internal tool artifacts |
| Gemini `[cite: 1]`, span markers | `communication-and-markup-patterns.md` → Internal tool artifacts |
| Grok card tags | `communication-and-markup-patterns.md` → Internal tool artifacts |
| DeepSeek lenticular citation markers | `communication-and-markup-patterns.md` → Internal tool artifacts |
| Perplexity attachment and upload tags | `communication-and-markup-patterns.md` → Internal tool artifacts |
| `:::writing` wrappers | `communication-and-markup-patterns.md` → Internal tool artifacts |
| Non-existent or out-of-place categories | `communication-and-markup-patterns.md` → Destination object validation |
| Non-existent templates or parameters | `communication-and-markup-patterns.md` → Destination object validation |

## Citations

| Source section | Humanizer location |
| --- | --- |
| Broken external links | `citation-integrity.md` → Link existence and access caveats |
| Invalid DOI and ISBN values | `citation-integrity.md` → Identifier validation |
| Valid DOI leading to an unrelated article | `citation-integrity.md` → Metadata and claim match |
| Book citations without page numbers or URLs | `citation-integrity.md` → Locators and verification |
| Existing books whose cited pages do not support the claim | `citation-integrity.md` → Entailment check |
| Incorrect or unconventional reference reuse | `citation-integrity.md` → Placement and reuse |
| Return-arrow footnote residue | `citation-integrity.md` → Interface residue |
| `utm_source` and model referrer parameters | `citation-integrity.md` → Tracking-parameter review |
| Named references declared but unused or used but undefined | `citation-integrity.md` → Named-reference consistency |
| Pages without inline citations | `citation-integrity.md` → Claim-to-source placement |

## Comments, edit summaries, and workflow residue

| Source section | Humanizer location |
| --- | --- |
| Comment-specific policy misquotation and made-up shortcuts | `communication-and-markup-patterns.md` → Institutional overperformance |
| Long titled comments, misplaced maintenance banners, repeated assurances | `communication-and-markup-patterns.md` → Comment structure residue |
| Formal first-person edit-summary paragraphs | `communication-and-markup-patterns.md` → Summary proportionality |
| Canned assurances of policy adherence | `communication-and-markup-patterns.md` → Assurance without specifics |
| Mentions of “preserved” or “retained” unchanged content | `communication-and-markup-patterns.md` → Prompt-constraint residue |
| Overemphasis on the presence or reliability of citations | `communication-and-markup-patterns.md` → Source-count performance |

## Miscellaneous

| Source section | Humanizer location |
| --- | --- |
| Pronounced shift in writing style or English variety | `human-signals-and-false-positives.md` → Baseline and style drift |
| Submission statements in drafts | `communication-and-markup-patterns.md` → Reviewer-facing residue |
| Pre-placed maintenance or review templates | `communication-and-markup-patterns.md` → Workflow-state validation |
| Canned user/profile pages | `communication-and-markup-patterns.md` → Profile template residue |
| Permissions gaming | `human-signals-and-false-positives.md` → Behavior is outside a prose verdict |
| Differences between models and versions | `human-signals-and-false-positives.md` → Moving-target problem |

## Signs of human writing and ineffective indicators

| Source section | Humanizer location |
| --- | --- |
| Age of text relative to model availability | `human-signals-and-false-positives.md` → Provenance beats style |
| Ability to explain editorial choices | `human-signals-and-false-positives.md` → Revision ownership |
| Simple `is`/`has`, plain verbs, direct claims, natural hedges, isolated wordiness | `human-signals-and-false-positives.md` → Positive texture |
| Perfect grammar | `human-signals-and-false-positives.md` → Ineffective indicators |
| Mixed casual and formal register | `human-signals-and-false-positives.md` → Ineffective indicators |
| Bland, robotic, fancy, academic, or formal prose by itself | `human-signals-and-false-positives.md` → Ineffective indicators |
| Transition words in isolation | `human-signals-and-false-positives.md` → Ineffective indicators |
| Unsourced content by itself | `human-signals-and-false-positives.md` → Ineffective indicators |
| Bizarre or correct destination markup by itself | `human-signals-and-false-positives.md` → Ineffective indicators |

## Historical indicators

| Source section | Humanizer location |
| --- | --- |
| Didactic “important to note” disclaimers | `communication-and-markup-patterns.md` → Historical residue |
| “In summary” and conclusion restatements | `content-patterns.md` → Redundant endings |
| Prompt refusal and “as an AI language model” residue | `communication-and-markup-patterns.md` → Historical residue |
| Abrupt generation cutoffs | `communication-and-markup-patterns.md` → Truncation check |
| Old access dates inconsistent with creation date | `citation-integrity.md` → Date plausibility |
