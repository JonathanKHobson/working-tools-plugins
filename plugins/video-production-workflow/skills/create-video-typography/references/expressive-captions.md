# Expressive captions and reversible style changes

Use for emphasized words, kinetic captions or a requested caption-style revision, in any format. A course, interview, screen demonstration, product film and text-led animation need different intensity. A supplied demonstration prompt is a menu of possible techniques, not a requirement to apply every effect or copy its wording, palette, person or font.

## Preserve the text and timing first

Keep a reviewed transcript and stable cue/word IDs separate from presentation. Fix transcription and map cues to the final output timeline after edits; use verified word alignment for word-level animation. Do not guess timing from character counts. If only phrase timing is reliable, emphasize a phrase or review the recording before adding precise word reveals. Do not split away negation, units, numbers, conditions or speaker attribution to isolate an exciting word.

Distinguish three roles: complete accessible captions; a decorative emphasis duplicate; and a diagram/object label. The caption track retains the whole spoken meaning and meaningful non-speech sounds where needed. A keyword-only graphic is not a replacement caption. A silent demonstration needs appropriate explanatory text; do not invent speech just to create captions.

## Build a small semantic style system

In the existing project style/slot brief, define a readable base style, an accent treatment and an optional stronger treatment for a truly consequential word or phrase. These are editorial roles, not mandatory levels or new manifest fields. Select emphasis because it changes the viewer's understanding, not because a word is long or every phrase needs a highlight.

- Color can distinguish a key term, but meaning must survive without color. Weight, a stable outline/background or restrained size change may supply the additional cue.
- Use bold, italic or a different font style only when supported by the chosen licensed family and language. A bounded alternate family can serve a deliberate role; avoid random per-word font cycling. Preserve readable letterforms and verify fallback glyphs.
- Strong emphasis may combine measured size, weight, timing or placement. Do not apply every dimension at once by default. Keep sufficient hold time and a predictable reading path; a position change must not make viewers chase text across the frame.
- Font/weight/size changes affect real glyph widths. Remeasure the full cue at its largest/extreme state, including outline and shadow, against line breaks, safe areas and nearby UI. Reserve layout space or deliberately keyframe the move; don't let each emphasized word recenter the entire sentence.
- Coordinate emphasis with the spoken point, demonstrated action or payoff. Preserve contrasts such as “not approved” rather than enlarging only “approved.” Use a quieter style for dense explanations and protect space around a cursor, chart or important control.

Typography may suggest vocal stress, but changing its appearance does not change the audio. Preserve recorded delivery unless a performance edit is authorized. For requested re-recording, dubbing or synthetic delivery changes, use Mix Video Audio's narration-and-dubbing method with speaker/voice authorization, exact meaning, pronunciation and timing review. Do not infer voice-cloning permission from a request for bold captions.

## Restyle without rebuilding the edit

Store the text, timing, emphasis spans and style roles separately in the existing editable tool/asset. Change style tokens or the caption template, retain cue IDs and reviewed wording/times, then remeasure font metrics, line wraps, extrema, clipping and local contrast for each aspect ratio/language. Style-only revision need not invalidate transcription or audio alignment; font/layout changes invalidate visual QA. If the request also changes words or timing, revalidate the affected caption alignment and meaning.

SRT and platform caption tracks may not retain the richer presentation of a rendered kinetic/ASS layer. Keep a complete plain-text timed sidecar where supported and verify the destination's actual behavior. Treat unsupported per-word font/position features as a compositor or editor task; do not invent fields in the current editorial manifest. See [compositing capability boundaries](../../create-motion-graphics/references/tracked-layer-compositing.md#execution-boundary).

## Check the final composite

Inspect longest cues, strongest emphasis, scene changes and caption entry/exit at the actual target size and phone-sized playback. Check full-speed reading, muted comprehension, changing background contrast, localization, font fallback and platform reservations. Keep essential captions above the final foreground/graphics. If a title is intentionally behind another element, preserve its required meaning visibly elsewhere; use the [layering method](../../create-motion-graphics/references/tracked-layer-compositing.md) for that graphic. Avoid flashing and relentless movement; use a stable alternative when motion competes with access. Record rendered checks separately from intended styling.

Basis: generalized from the user's supplied editing example and preferences, 2026-10-02. This is a maintained editorial method, not a measured engagement claim. Existing caption timing, font-rights and accessibility procedures remain in force.
