# CLI operation

LM Studio’s `lms` CLI is the preferred route when it is installed and connected to its local service. Resolve the executable from the recipient’s environment; do not hard-code a path in public instructions.

Use this lifecycle:

1. `lms ls` to record the exact installed model key and variant.
2. `lms ps --json` before loading. Stop if an unrelated model is loaded or a prior job is active.
3. `lms load MODEL --identifier OWNED_ID --context-length N --parallel 1 --ttl SECONDS -y` with a deliberately bounded context. Measure the load result and retain the output.
4. Run one bounded request at a time with `lms chat OWNED_ID --prompt PROMPT --dont-fetch-catalog --stats --ttl SECONDS -y` or the runner’s equivalent. Keep prompts free of secrets unless local handling is explicitly intended.
5. Save raw output and timing before interpreting it.
6. `lms unload OWNED_ID`, then `lms ps --json` to verify the model is gone.

Do not load several large models concurrently on a memory-constrained host. Do not use a failed load, a truncated output or a missing receipt as evidence of model quality. A load failure is runtime evidence and should be recorded separately from task quality.
