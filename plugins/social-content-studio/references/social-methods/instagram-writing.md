# Instagram writing: captions and native copy

Use this method for an Instagram caption, a caption attached to a Reel or carousel, or a caption lint review. It adapts the upstream `ig-caption` procedure into the Studio's source, voice, privacy, accessibility, and draft-state boundaries. Source provenance: [Instagram agent review](../../libraries/instagram-agent/PROVENANCE.md).

## Establish the caption job

First decide whether the media already carries the hook.

- **Media-led caption:** a Reel or narrated Story already makes the opening promise in spoken or on-screen content. The caption supplies context, a useful detail, search language, and one reader action. Do not compete with a strong opening by repeating it as a second hook.
- **Caption-led post:** a photo, single image, or carousel needs the caption to earn the tap. Make the first visible unit concrete and complete enough to create a reason to continue. For a carousel, the cover and slides already carry part of the promise, so the caption should add context or a useful next step.

Record `job`, source/asset ID, intended audience, one action, voice basis, and publication state before drafting. A draft remains prepared until the owning project or platform records a later state.

## Caption structure

Use this shape as a starting point, then adjust to the reader and source:

```
VISIBLE OPEN    the first feed-visible unit; no greeting, hashtag, or decorative emoji opener
BODY            two to six short paragraphs, one idea per paragraph, with claim qualifiers beside claims
ONE ACTION      one clear action, such as save, answer, or request a supplied resource
TAGS            optional descriptive labels, kept within the platform's currently verified limit
ALT TEXT        supplied separately for the image or carousel, describing what is materially shown
```

The exact character cutoff, hashtag limit, and supported metadata fields are platform facts that can change. Verify them from a current official source or the live composer when the limit matters. Do not turn an observed limit into a universal performance claim. Keep the caption shorter when the media carries the explanation; length alone is not a quality signal.

## Search language and hashtags

Ask for two or three phrases a real reader might type. Place those phrases naturally in a sentence that remains useful to a human. Do not turn them into a keyword block. Hashtags are optional topic labels, not a guaranteed reach lever. Select only specific, relevant labels supported by the source and current account policy. Reject generic promises such as `#viral` or `#fyp` when they do not describe the post.

Do not place an unverified URL in the caption as though it were clickable. Use the approved bio, platform link field, Story link surface, or a prepared DM only when that destination and action are actually available. If a first comment is part of the user's approved handoff, label it separately and preserve its own state.

## Evidence and voice checks

- Keep names, amounts, dates, conditions, uncertainty, and chronology attached to the claims they qualify.
- Distinguish a proposal, shipped output, and measured outcome. Do not manufacture metrics, testimonials, firsthand participation, or audience response.
- Preserve the user's supplied voice sample. A named author or account does not establish an authentic voice sample.
- Use the existing `post-draft-gate.md`, `voice-files.md`, and bundled `provider-social-prose.md`. Use Writing Quality's `natural-prose-editor` for the final language pass when available, and identify when it was unavailable. This method does not install or claim an AI-authorship detector.
- Write alt text for a meaningful image. For a carousel, describe the cover and the information sequence or provide frame-level notes as the receiving workflow requires. Do not claim that caption text substitutes for image accessibility.
- If the post asks people to comment a keyword, the keyword must be supplied, easy to type, and tied to a resource the user can actually deliver. Do not gate a promised resource behind an undisclosed qualification step.

## Read-only lint and receipt

Use the bundled [caption diagnostic](../../skills/social-content/scripts/caption_check.py) for exact codepoint counts, an approximate text window, hashtag counts and optional keyword presence. It preserves the source string and emits JSON only. Run from the plugin root:

```sh
python3 skills/social-content/scripts/caption_check.py caption.txt --platform instagram --preview-budget 125
```

The preview budget is a simulation assumption, not an Instagram cutoff. Supply `--limit` or `--max-hashtags` only from current verified account/platform evidence. `--platform` is a label, never an automatic limit. This helper does not detect every CTA, verify a link, count graphemes, inspect alt text, render the feed or issue readiness verdicts. Those remain manual checks. Do not add unsupported facts or strip characters to satisfy a diagnostic.

Resolve actual factual or constraint failures and assess advisory observations. Explain material warnings that remain, especially when a source, platform, or accessibility fact is unavailable. Return the copy-ready block first, followed by this compact receipt:

```
CAPTION REVIEW
job: media-led | caption-led
source: <project source or asset ID>
action: one, <action>
search terms: <phrases and where they occur>
hashtags: <count and rationale, or none>
alt text: supplied | needed | not applicable with reason
prose review: natural-prose-editor completed | unavailable | not needed
lint: findings and warnings, advisory
state: prepared copy
```

Nothing here posts, schedules, sends a DM, or changes a profile.
