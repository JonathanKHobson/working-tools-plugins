# Local text hygiene and descriptive panels

Use only when the user requests a local text check, invisible-character inspection,
an explicit cleanup, or a descriptive before/after comparison. Ordinary editing
stays in Natural Prose Editor; actual personal voice matching stays in Voice and
Style. These tools are optional aids, never a compulsory pass before every post.

The stdlib-only scripts live in `../scripts/linkedin_text/` relative to this
reference. They have no network, provider, account, package installer, or personal
data store. Input and output are UTF-8; file reads preserve CRLF and a leading BOM.
No input file or existing destination is overwritten. Identical paths, symlink
aliases and hard-link aliases are rejected. Output files must use a new path.

## Preserve first

`humanize.py` preserves supplied text by default, including meaningful punctuation,
quotes, emoji sequences, joiners/non-joiners, right-to-left controls and spacing.
The name is retained for source/tool familiarity; it does not certify a human
writer or provide detector evasion. Lexical candidates are suggestions for a
contextual read, never replacements. The supplied 113 word/phrase entries remain
available; technical language and deliberate vocabulary may be correct unchanged.
An empty source suggestion is not an instruction to delete a phrase.

Run from the Natural Prose Editor skill directory:

```sh
python3 scripts/linkedin_text/humanize.py draft.txt --report
python3 scripts/linkedin_text/humanize.py draft.txt --json
python3 scripts/linkedin_text/humanize.py draft.txt --cleanup -o cleaned.txt --diff
python3 scripts/linkedin_text/humanize.py draft.txt --ascii-quotes -o ascii-quotes.txt
```

`--cleanup` is explicit and narrow: it removes a leading BOM and optionally a soft
hyphen or zero-width space between ASCII letters or next to an existing ASCII
whitespace boundary in unprotected prose. Zero-width spaces can distinguish words
in some languages; the option leaves other contexts unchanged. Even Latin-boundary
changes need review against the author's intended wording. It never deletes the
Unicode format category generally, word joiners, ZWJ/ZWNJ, directionality controls,
emoji tags, non-breaking spaces, or any other unlisted character. `--ascii-quotes`
changes only curly single/double quotes in unprotected prose. It does not replace
em/en dashes, ellipses, primes, bullets, arrows or vocabulary.

Protected spans include fenced and indented code, inline backtick code, URLs,
email addresses, bracketed placeholders/link labels, brace placeholders and HTML
tags. Protection is conservative rather than a complete Markdown parser: inspect
unusual or malformed markup manually and preserve exact source quotations when
needed. A leading BOM is the one file-level cleanup even before a protected span.
Default preservation is the appropriate choice for binding quotations, mixed
scripts, identifiers, source code, or uncertain boundaries.

Every applied change is reported on stderr, even without `--report`, with original
Unicode-character offset (zero-based), line/column (one-based), before/after and
reason. `--json` returns full before/after, exact changes and lexical candidates;
`--diff` also prints a unified comparison to stderr. With `-o`, the chosen text or
JSON format is written to the new destination. Stdin is selected by `-` or by
omitting the input argument. Nothing is uploaded or logged elsewhere.

## Observe without judging origin

```sh
python3 scripts/linkedin_text/detect.py draft.txt --json
python3 scripts/linkedin_text/detect.py before.txt after.txt --language en
python3 scripts/linkedin_text/detect.py - --language en --json
```

`detect.py` reports five descriptive panels, with no human score, pass/fail writing
verdict, detector result, authorship inference, release approval or engagement
forecast:

1. **Sentence variation:** approximate punctuation-delimited lengths and descriptive
   mean/spread. No target variation or preferred sentence count applies.
2. **Specificity candidates:** visible numbers and English capitalized-word
   candidates. They are neither verified facts nor verified names. Their absence
   does not establish vague writing; never add details or metrics to fill a panel.
3. **Stock terms:** literal matches with locators and report-only source suggestions.
   Keep appropriate terminology; optional synonyms may alter meaning or register.
4. **Typography/Unicode:** actual character names/counts. Format controls can support
   orthography, directionality, typography and emoji composition, and have no
   evidential relationship to authorship here.
5. **Voice cues:** English contractions, pronouns, bullet lengths and limited
   repeated-frame candidates. Formal prose, courtesy, contrast, repetition and
   punctuation can all be purposeful. This is not an authentic author baseline.

English-specific interpretation requires an explicit `--language en` context and
at least 25 approximate word tokens; sentence variation also requires at least
four approximate sentences. Otherwise those interpretations are `unknown`.
Language is supplied, never inferred from alphabet. Other panels can still report
literal observations, with their limitations. Tokenization and sentence boundaries
are heuristics, not linguistic validation. Short, mixed-language and non-English
samples need human/contextual review. Comparison shows the two panel sets without
an improvement score or presumption that fewer cues is better.

Both scripts accept a custom `--lexicon` containing `{"version":1,"terms":[...]}`.
Each entry needs `find`, `suggestion` and `family` strings. Terms are literal data,
not executable expressions; schema, size, duplicate and control-character checks
reject malformed input. Input is capped at 2 MiB; lexicons at 256 KiB/500 entries.
Invalid UTF-8, NUL input, missing files and unsafe output paths fail with an error.
A successful descriptive run exits 0 regardless of cue counts; invalid input exits 2.

## Adaptation and review

Adapted from the pinned MIT `Jakeschincariol/linkedin-agent-skill` li-human source;
the Studio's integration provenance retains the original source and license.
Kept: local tools, all 113 lexical candidates, locators, before/after, five-panel
organization. Rejected: invented human scores, detector-transfer claims, broad
format-character deletion, mechanical dash conversion, lexical replacement and
pressure to manufacture specificity or contractions. Existing evidence-first
editing, mutation checks, purposeful voice and false-positive protections govern
any subsequent revision. Tests cover preservation, script/emoji controls, protected
spans, Unicode cleanup, multiline bytes, invalid inputs, aliases and comparisons.
