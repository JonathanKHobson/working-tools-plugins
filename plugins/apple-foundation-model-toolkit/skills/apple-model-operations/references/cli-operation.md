# Native CLI operation

Verified documentation: 2026-10-17. Recheck current `fm` help because OS releases and supported flags change.

## Readiness

Locate the system `fm` command and inspect `fm license --status`. If required, `fm license --show` displays terms without acceptance. Machine-wide acceptance is an administrator action, normally `sudo fm license`; require the user’s authorization and let the user authenticate locally when macOS requires their password. Never ask for the password in chat or change system files to bypass the license. Prior authorization to accept is sufficient; do not ask again merely because the operation is privileged.

After acceptance, inspect `fm --help` and `fm respond --help`. Run `fm available --model system` to check the on-device route; Apple Intelligence must be ready on a supported device. Distinguish unaccepted terms, disabled Apple Intelligence, assets not ready and an unsupported machine. Resolve the observed condition through supported settings or report the required action, without claiming inference succeeded.

## Bounded tasks

`fm respond` is the single-response route; `fm chat` is for interactive exploration. The documented default is on-device. Read current help for prompt input, instructions, schemas, output limits and explicit model selection. Run one short known-answer test before depending on the route. For a substantive task, provide only relevant text and impose a finite process timeout in the caller. Capture output, error text, exit status and elapsed time. Do not accept a successful exit with an empty response as completion.

The current CLI accepts prompt text on stdin: `fm respond --model system --no-stream --greedy < task.txt`. Use a task-owned file and a finite caller timeout. This keeps the prompt out of command arguments. Use supported stdin/file input for private text; otherwise do not place private prompts in process arguments. A caller can build an SDK-based route if the task warrants it, but do not install an SDK simply to avoid checking the installed CLI. For guided extraction, generate a schema with `fm schema object --name Result --string deadline --boolean recording_allowed --string room`, save it to a task-owned file, and pass `--schema /absolute/schema.json` to `fm respond`. The `schema` command supports guided output; use its current help, not an assumed JSON Schema compatibility claim. Check extracted fields against the source independently.

Private Cloud Compute is documented as a different route with usage limits; some installed builds expose only `system`. The installed command’s model list wins over broader product documentation. Do not switch from on-device to cloud silently. Confirm current selection and the task’s data-sharing authorization. Generated code and file-operation plans require the same task permissions and verification as code from any other model.

## Alternatives and recovery

The official Swift framework supports availability checks and integration into applications. Apple also provides a Python SDK for evaluation and prototyping on supported systems; use its official install requirements and an isolated environment when installation is authorized. Native Shortcuts may provide an Apple model action on supported OS versions. Verify its current action, selected model and actual output before claiming the route works. Use computer interaction only when a required setting or user-requested interface cannot be handled by the CLI, through the host’s supported computer-use tool. Never substitute Siri UI automation for a Foundation Models API.

On failure, retain the concrete error, correct one supported cause and retry once. Preserve other active model jobs. No global service restart, broad process kill or credential copying is part of routine recovery.

[Apple’s CLI and Python SDK walkthrough](https://developer.apple.com/videos/play/wwdc2026/334/) describes the native routes; [SystemLanguageModel](https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel) owns framework availability semantics.


## Other CLI capabilities to select only when needed

Current help exposes `count-tokens`, `chat`, `schema` and `serve` alongside `respond` and `available`. Use token counting to check a bounded prompt before a context-sensitive task. `respond` supports images, optional `ocr`/`barcode` tools, and `general`/`content-tagging` use cases. Enable only task-required tools; default guardrails remain in place. Check live flags before using them, and verify image/text results against the supplied evidence.

For an explicitly needed local application integration, `fm serve` exposes `/health`, `/v1/models` and `/v1/chat/completions`. The documented Unix socket transport is appropriate for local bindings; restrict socket permissions and retain a task-owned server handle. A loopback listener is another deliberate choice. Do not bind a network-wide host or install a background service merely to run a text task. Stop only the server this task started after use. Server availability is separate from model availability and successful inference.
