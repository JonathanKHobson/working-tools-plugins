# Interpret audio checks before choosing a repair

Use when a recording or edited clip is flagged for room noise, silence, omitted filler, clicks or level changes. Reuse available measurements and the original audio; this procedure adds no detector or runtime.

1. Identify whether the file is a raw recording, processed master or final excerpt. Note known gating, denoising, compression and intentional silent tails. A processed master cannot reliably reveal the original room floor.
2. Inspect the interval behind a noise-floor estimate. If a gate has replaced quiet passages with digital silence, report the original floor and related signal-to-noise estimate as unavailable, not exceptionally clean. If speech or music is continuous, a quiet-window estimate may still contain signal; do not diagnose room noise from that number alone. Retain method, window, units and applicability.
3. Treat click and level-step detections as review locations. Inspect the waveform and neighboring edit, then listen when permitted. Consonant attacks can resemble clicks; an intentional speaker change can explain a level shift. For quiet-testing requests, measure and inspect silently and explicitly leave listening unverified.
4. A transcript may omit hesitations, breaths or short speech-like sounds. An energy burst absent from the transcript is a candidate for inspection, not a confirmed filler word or permission to delete it. Conversely, no detected filler does not prove none exists.
5. Use the transcript to locate a passage, then verify actual cut boundaries against audio and frames. Choose padding, crossfades and room tone for the observed material. Do not require silence-only cuts when continuous speech, music or a deliberate J/L cut calls for another boundary.
6. Choose the smallest repair justified by the defect, preserve the source, and compare before/after. Reuse existing authorization for reversible edits; honor explicit review holds without adding a mandatory approval to every filter.

Output: affected interval; observed evidence; interpretation and confidence; proposed/performed action; final checks; remaining listening or source-data limits. A loudness pass does not certify intelligibility, lack of distortion or natural cadence.

Acceptance example: gated interview, zero-valued digital-silence tail, and a click flag near “t”. Exclude the intentional tail, mark original room noise unavailable, review the consonant/cut, and do not apply blanket denoising or claim a listening pass from numbers alone.

Method provenance: original local guidance prompted by Bloom Studio 0.1.0 noise-check and tightening limitations, reviewed 2026-10-02. No upstream detector, thresholds or code imported; no accuracy or performance improvement claimed.
