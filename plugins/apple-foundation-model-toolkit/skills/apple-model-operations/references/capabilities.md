# Capabilities and task fit

Evidence reviewed 2026-10-17. Apple documents `fm` in macOS 27, with single response, interactive chat and guided structured output. On-device and Private Cloud Compute are distinct selections; the latter is larger and subject to usage limits. The Python and Swift SDKs support application integration and explicit tool calling. Source: [Apple WWDC26 session](https://developer.apple.com/videos/play/wwdc2026/334/).

Start with short extraction, classification, rewriting or supplied-context summaries when privacy, offline operation or low overhead matters. These are evaluation candidates, not established superiority over Claude, Gemini or downloaded models. Test dates, negation, missing values, instruction following and truncation on representative inputs. If an on-device model loses essential meaning, use a better verified route rather than repairing its answer without counting the repair cost.

Siri’s assistant behavior, App Intents, Shortcuts actions and the general Foundation Model are different capabilities. Access to one does not grant arbitrary control through the others. A physics or code answer still needs independent domain tests. A file-classification result should produce a reviewable plan before an authorized caller applies mutations.

Keep per-host available model choices and benchmark results outside the portable plugin. Do not infer exact parameter count, context limits, offline availability or performance from a marketing name; inspect current platform documentation and actual runtime responses.
