# Baseline Notes

Before the shared architecture, common failure patterns include:

- one-off FFmpeg commands with no editable project contract;
- renderer lock-in before creative decisions;
- equal-duration slideshows and blind beat cutting;
- transcript-only claims about visual content;
- source timestamps reused after edits, misaligning captions;
- overlays covering captions;
- hard audio cuts and unmeasured loudness;
- center-cropped vertical versions that lose subjects or text;
- successful process exit mistaken for a reviewed final video;
- copied skill text or installed tools without license/provenance strategy.

The test suite and scenarios should be expanded with evidence from the user’s prior video conversations when Codex performs the final merge/upgrade.

## Drive recording trim — September 30, 2026

Pre-change guidance inspection: no discoverable same-file Drive replacement path; no specific MP4 subtitle-copy duration check; validation required playback with sound without a user-requested silent-QA alternative. The actual project caught a copied subtitle stream extending the container past the trimmed A/V duration, corrected by explicit cue retiming and remuxing. Three pressure/routing scenarios above were added before the guidance change. This is a documented gap review, not a claim of an executed model-evaluation trial.

## Resolve edition and editable handoff — October 7, 2026

Pre-change inspection found generic install, dialogue and interchange guidance,
but no editor owner for edition-specific control, private setup reuse, native
timeline finishing or saved-project readback. Generic interchange calls for a
small round trip without specifying the Resolve project/reopen evidence. Four
scenarios were added before the guidance change. The built-in exporters are
limited: CMX3600 emits video-only hard cuts using integer non-drop-frame rates;
OTIO emits one sequential picture track and stores record starts as metadata.
Neither can be presumed to preserve full mixed productions. This is a source
gap review; runtime acceptance still requires a real editor smoke test.

## Art-directed motion defaults — October 7, 2026

User feedback reports repeated generic typography, bottom labels, static text and
weak stylistic distinction on another host. We have transcripts, not the offending
renders or reference playback; the precise visual cause remains unverified.
Pre-change inspection found detailed conditional motion grammar and font/reading
checks, but default planning/storyboard/type/motion steps could proceed without
a concrete visual thesis, photo integration, depth choice or a representative
craft comparison. Six pressure/boundary scenarios were added before edits.
Independent read-only review confirmed this default-contract gap. This is a
guidance gap diagnosis, not a baseline model trial or proof of improved videos.

## Supplied art-direction handoff — October 7, 2026

The first default-contract repair already covers type/photography/space/motion
and a representative passage. The supplied research adds a distinct method
gap: candidate comparisons need controlled content, and future reuse needs
an evidence-backed selected style record. Three scenarios were added before
these additions; no new universal style, duration, renderer or directory system
is warranted. The handoff is source material, not execution authorization.
