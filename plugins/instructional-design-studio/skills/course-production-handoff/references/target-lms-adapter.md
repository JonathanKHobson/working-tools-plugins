# Target LMS adapter worksheet and learner test

Use only for an actual LMS delivery/package request. Reuse the asset register and states in [production guide](production-guide.md). This worksheet is unconfigured until populated with a real target. Nothing in this reference configures an LMS, supplies credentials, installs a runtime or establishes live compatibility.

## Adapter worksheet

Fill only known facts; unknown fields remain a delivery dependency rather than an inferred default.

| Field | Target-specific value / evidence |
| --- | --- |
| Destination | LMS product, tenant/test URL, environment, version/build, owner and authorized upload/import scope |
| Standard | Exact SCORM 1.2 or SCORM 2004 edition, xAPI/profile or other format; current target support/specification link and checked date |
| Package | Asset/register version, package filename + SHA-256, manifest/launch resource, authoring/export tool and settings, size limits and required files |
| Learner context | Disposable/test learner role and enrollment, browsers/devices, popup/frame/cookie requirements, permitted data and access prerequisites |
| Launch adapter | LMS launch mode and actual runtime/API discovery or profile endpoint; initialization, save/commit and exit behavior per target standard |
| Tracking map | Learning action → expected score scale/value → passing rule → completion/success states → target report field and timing |
| Attempt policy | New attempt/review/retry policy, reset permissions, aggregation/rollup if used, expected failed/pass outcomes |
| Resume map | Saved location/bookmark/state fields and limits, suspend/exit behavior, expected restore position and learner input |
| Access and media | Keyboard/AT checks, captions/transcripts, external asset rights/login/expiry, offline/error fallback where required |
| Release dependency | Named owner, accepted status, evidence, fallback and exact remaining step; package/import/test/release tracked separately |

Do not transplant data-model fields or limits between standards. In particular, completion and success may be separate states; use the actual target's specified mapping and readback. An xAPI statement accepted by an LRS alone does not prove LMS completion. Do not guess an endpoint or embed a credential in the worksheet/package.

## Execute only in the real authorized target

Use fictional test data and the smallest representative lesson/assessment first. Retain package hash, LMS settings, learner role, attempt ID (redacted), timestamp and expected-versus-observed evidence. An author preview or standards test harness can check a layer; it cannot replace the target learner launch.

| Check | Test action | Evidence required to pass |
| --- | --- | --- |
| Package/import | Check manifest/resources and import exact hash into the authorized test course | Import result, reported package identity/version and working resources; warnings resolved or documented |
| First launch | New test learner launches via the LMS entry | Course opens, initializes in intended frame/window, first activity/resources usable; actual API/init result if tooling exposes it |
| Score | Complete deterministic failed and passed examples or boundary cases required by the scoring rule | Known inputs produce expected score/scale, passing result and LMS report readback after save/exit; learner toast alone is insufficient |
| Completion | Leave a new attempt incomplete; complete required activity in another/reset authorized attempt | Expected incomplete/complete and success/failure states remain distinct and persist in the target report; rollup checked if applicable |
| Save/resume | Make identifiable progress, save/suspend using the normal exit, close and relaunch same attempt | Position, input/progress and score return correctly; logout/new session checked if required; no unintended new attempt |
| Retry/review | Use target's retry/review controls | Attempt count, reset/retained state and aggregation match the worksheet; no duplicate result masquerades as fresh completion |
| Failure/recovery | Interrupt one realistic save/network/resource path without changing production configuration | Honest failure/pending feedback, no false score/completion, documented recovery and authoritative result after retry |
| Access | Exercise affected keyboard/AT path and captions/download links in learner role | Actual traversal, names/errors/state and usable media/resources, with environment and untested combinations recorded |

After a fix or export-setting change, generate a new package hash, reimport and rerun the failed path plus affected tracking/resume checks with the same target conditions. Preserve the earlier failure. Record passed/failed/unverified/not applicable with reason; do not count unavailable target checks as passed.

## Handoff and source limits

Without target access/current specification, deliver the requested source/package, filled known worksheet fields and exact unexecuted tests. Say “target launch untested”; do not claim SCORM compliance, LMS compatibility or release. With access, compatibility wording names only the package hash, target version/configuration and tested learner paths. Standards conformance is a separate claim requiring its appropriate complete test method.

ADL's official [SCORM 2004 4th Edition Test Suite](https://github.com/adlnet/SCORM-2004-4ed-Test-Suite) distinguishes LMS, content-package, SCO and manifest tests. It is source context, not a dependency to install or a current execution recipe; its legacy prerequisites must be separately evaluated before use. On 2026-10-01, ADL's linked specification/guide PDF endpoints could not be retrieved in this maintenance pass. Consult the target's current documentation and obtain the exact authoritative edition before executing standard-specific checks; this reference supplies a practical test worksheet, not an unverified transcription of those PDFs.
