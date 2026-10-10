# Narration, pronunciation and translated audio

Use this conditional procedure for synthesized narration, replacement spoken lines or a requested language version. Ordinary recorded-audio cleanup stays in the normal mix workflow. This is independently authored, provider-neutral production guidance. It does not install VoiceStudio, a speech model, dictation capture, a microphone monitor or an agent bridge.

## Establish the production contract

Read the current approved script and delivery brief. Identify source language, requested target language/dialect, audience, voice choice, pronunciations, duration constraints and whether the picture may change. For teaching content, preserve demonstrations, instructions, warnings, quantities, quoted material and on-screen labels. A translated performance can adapt natural phrasing; it cannot silently change the taught action or promise.

Use an already available, authorized tool. Confirm the selected operation and model can actually perform the requested language/voice task; a platform's broad language count does not establish quality for that engine. For cloning, record whose voice it is and the consent covering this use; keep reference recordings and consent private in the project. Voice consent, source-recording rights, model terms and output-use rights are separate checks. If they are missing, use an authorized stock voice or hold the affected voice choice. Provider limits do not authorize new billing, uploads or model downloads.

## Keep editorial text distinct from spoken rendering

Maintain the approved display/transcript wording separately from pronunciation input. Put only confirmed unusual names, abbreviations, technical terms and desired readings into the project's existing lexicon. Record original spelling, intended spoken form, language/dialect and a reviewed sample. Test a short phrase containing the term and a neighboring ordinary word; replacements must not damage substrings or compound terms. Numbers, dates, units and negations require contextual review. Do not replace source captions with phonetic respellings.

For a translation, keep stable segment IDs with source text, approved target text, speaker, source in/out times, available speaking time, voice setting and take status. Review text before generation, especially terminology, instructions and cultural assumptions. A provider's returned segment must match the expected ID; missing, duplicated or reordered segments fail the handoff. Reuse the existing project manifest rather than creating a second project database.

## Fit speech to the actual timeline

Speech units and subtitle display units serve different purposes. Segment spoken performance at meaningful sentence/phrase boundaries and speaker changes. A subtitle reading-speed ceiling does not justify chopping narration into single-word TTS jobs. Derive subtitles later from the accepted delivery timeline.

For a course, aim first for intelligible, meaning-preserving teaching audio; perfect voice resemblance or lip-sync is not required unless the delivery brief requires it. Fix incorrect instructions, changed quantities, misleading on-screen references and clipped speech before release. Naturalness defects can remain visible in a clearly labeled pilot when they do not obstruct learning. Generate a representative 30–60 second pilot before a long run. Measure the produced speech, including meaningful pauses; estimated character counts alone do not establish duration. For a timing miss, prefer one bounded revision of the target phrasing that preserves meaning, then regenerate and measure the affected segment. If it still misses, make an explicit editorial choice: a justified pause/picture extension, a modest verified speed adjustment, a shorter approved reading, or leave that segment unresolved. Do not silently truncate speech, compress it until unintelligible or loop regeneration indefinitely. Preserve the original take and changed settings so comparison is meaningful.

When changing text, voice, language, pronunciation or timing, mark dependent takes stale. Regenerate only affected segments when the tool supports it, but invalidate downstream captions/mix/exports that rely on them. A cached take belongs to a specific text/voice/settings revision. Resume an existing generation job by its ID when supported; do not resubmit on a disconnected stream until its actual state is known. An interrupted stream is not evidence of completed audio.

## Mix and export

Retain separate dialogue, music/effects and combined stems when the source permits. Protect original ambience, avoid doubling original and dubbed speech accidentally, and apply fades at boundaries. Follow the normal loudness/true-peak workflow; larger bit depth or fewer signal warnings do not prove a more natural voice. Do not remove an existing synthetic-media provenance mark or claim watermark detection establishes consent.

Name target-language audio tracks and set the intended default track explicitly when exporting multiple tracks. Captions must match the delivered words and final timing. Source-language word timestamps are not valid target-language word alignment; if estimated timing is used, label it and avoid presenting approximate karaoke highlights as measured alignment. Save transcript/caption sidecars and preserve a source-to-output segment mapping in the existing asset record.

## Acceptance and handoff

Listen to the pilot and changed segments for intelligibility, pronunciation, speaker continuity, clipped words, pauses, artifacts and meaning; inspect beginning, joins and end against picture. A translation needs review by someone capable of assessing the target language before making a language-quality claim. Probe final duration, sample rate/channels, track labels/default flags and caption offset; then use validate-video-quality for delivery acceptance. If quiet testing was requested, perform the permitted signal/decoder checks and explicitly leave listening unverified.

Report separately: script approved, translation reviewed, voice use authorized, job completed, file downloaded, technically checked, listened/reviewed, and delivery accepted. Keep any missing stage visible. No generated clip or model was exercised merely by installing this method.

## Source and admission boundary

The review of [VoiceStudio](https://github.com/debpalash/VoiceStudio/tree/befc0a6f5b552b0b99e6eea574bc3c55e3d0519a) identified useful operational issues in docs/electron-dubbing.md, docs/dubbing/export.md, docs/audio-quality-handoff.md and backend/services/pronunciation.py. This new procedure expresses our own production contract; no upstream implementation, document prose, model or sample voice is bundled. VoiceStudio is AGPL-3.0-only with separate model terms; future runtime or redistribution decisions require their own source/license review. Full audit and source hashes remain in the owning project, not in a shared runtime skill.
