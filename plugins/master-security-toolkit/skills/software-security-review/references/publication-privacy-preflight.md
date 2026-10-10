# Local publication privacy preflight

Read this only when preparing an authorized public HTML page, local build folder, or email HTML for publication, sending, or hosting. This check belongs to the existing software-security-review owner; it adds no skill, hook, service, dependency, or universal approval gate.

Run the original [standard-library scanner](../../../scripts/publication_preflight.py) with explicitly supplied local files or the exact exported build directory, using a stable copy:

```bash
python3 /path/to/master-security-toolkit/scripts/publication_preflight.py /path/to/build
python3 /path/to/master-security-toolkit/scripts/publication_preflight.py --max-files 20 /path/to/page.html /path/to/local-script.js /path/to/email.html
```

Flags work before or after targets. No target defaults to the working directory or a personal vault. The scanner never follows linked assets, symlink path components, imports, commands or remote resources. Supply local HTML, CSS, JS/MJS/CJS, JSON, Markdown and TXT assets explicitly or inside the authorized build folder. It does not traverse named `vault`/`vaults`, `.obsidian`, `.git`, `node_modules`, or an Obsidian vault detected by its `.obsidian` marker. This is a conservative guard, not a registry of every personal data store: choose the target narrowly.

The run reads UTF-8 as data, including scripts, styles, comments and attributes. It checks raw text, up to three HTML-entity decoding rounds, and standard base64 tokens of 40–4096 characters that decode to printable UTF-8. Encoded findings point to the physical source line containing the encoding. It has no redaction mode and never modifies the target. It does not execute the source archive or generated content, fetch assets, send data, install anything, or inspect a parent directory's contents.

## Readback and disposition

Stdout is JSON containing rules, block/review tiers, source line and character offsets, source view, exact file SHA-256 and fingerprint. It omits excerpts, partial values and target filenames. `path_id` is `target-N:SHA256(relative-path-bytes)`; target numbers follow command argument order. A single file target uses the relative path `.`. A directory's child uses `./relative/name.ext`, with `/` separators and the filesystem's bytes. Confirm a private local file by computing SHA-256 of that relative path and of its bytes; do not copy private filenames or excerpts into a public report. For example, `python3 -c 'import hashlib; print(hashlib.sha256(b"./frame.html").hexdigest())'` computes a path identity without opening or executing the artifact. A finding fingerprint binds scanner version, rule, complete file hash and source character offset. Each physical source occurrence has its own line/fingerprint; repeated views of the same rule at the same offset are deduplicated. A base64 container contributes at most one finding per matched rule at its source offset, rather than a count of every decoded value inside it.

- **Block:** recognizable secret formats: private-key headers, AWS access keys, GitHub tokens, OpenAI/Anthropic keys, Stripe live keys, Slack tokens, legacy Google `AIza` keys, npm tokens and SendGrid keys. Remove an accidental secret from the publication artifact and address the exposed credential through its owning account; rerun the check. A synthetic example may be a false positive, but a raw match cannot establish that by itself.
- **Review:** email addresses, phone-like numbers, local user paths, credential-like assignments, URLs containing credentials, JWT-shaped tokens, confidentiality markers and printable base64. JWT-shaped text may be a public signed assertion or example, so its shape alone is not a block. Review exact private local context. Public contact information, deliberate examples and user-authorized names/content can remain. Record the disposition against the exact artifact SHA-256, rule and fingerprint, with a concrete reason such as "authorized public contact address." The scanner never silently accepts these items.
- **Incomplete:** unsupported types, binaries, non-UTF-8, excluded directories, symlinks, failures, changing files, empty target sets, limits and unscanned remainder are gaps. Review the named reason and record what was manually covered, intentionally excluded, or remains unverified. An image's presence means image contents require visual review; it is not itself a secret finding.

Exit `0`/`no-matches` means only no rule match among the eligible files with no recorded gaps. Exit `1` means block or review matches. Exit `2` means incomplete or invalid arguments, even if findings also exist. A review/incomplete run is never a clean run. After manual privacy review, exact finding dispositions and explicit gap/noncoverage rationale can support user-authorized publication. This reference does not add a blanket approval request when publication or sending is already authorized.

No global allowlist, wildcard exception, automatic acceptance, override or redaction CLI is implemented. A changed artifact invalidates an earlier disposition. Rerun after editing, and preserve actual scanner output with the exact published/sent artifact hash in the owning project record. Keep private reports local.

## Limits and verification

Defaults and hard ceilings are 1,000 supported files, 1,000,000 bytes per file and 20,000,000 total input bytes. Optional flags can lower these ceilings. Traversal also stops at 10,000 entries, depth 64 or 2,000 findings. Limits are reported as incomplete. The scanner uses held directory descriptors and no-follow opens on macOS/Unix; stable-copy review is still required because concurrent tree changes cannot be fully characterized.

This is a bounded heuristic privacy check, not security certification, general DLP or detection of every name, private statement, address, credential or image. Filenames are hidden from output but are not scanned for private meaning. It cannot interpret all prose, images, binaries, arbitrary encodings, runtime-generated text, concatenated/escaped JavaScript values or remote assets. Base64 is only one bounded static view; no recursive decoding is performed. Printable nested/HTML-encoded base64 payloads still produce a review finding, rather than a clean run, even when the inner secret format is not recognized. Unreadable or unusual payloads remain outside coverage. Rendered visual QA and manual review of authorized public content remain necessary.

After a scanner change, statically review its code, then run only the original synthetic [tests](../../../tests/test_publication_preflight.py):

```bash
python3 -B -m unittest discover -s /path/to/master-security-toolkit/tests -p test_publication_preflight.py -v
```

Tests exercise benign assets, known secret formats, script/style/comment/attribute contents, entity and base64 concealment, source lines, CLI ordering, no-target errors, symlink ancestors, vault refusal, limits, binary gaps, masked filenames, unchanged files and absent overrides. These tests verify deterministic behavior, not completeness of privacy detection.

Distinctive token rules are bounded heuristics, not issuer validation. Primary sources confirm the [npm token prefix and 36-character suffix](https://api-docs.npmjs.com/), [SendGrid key prefix/structure](https://www.twilio.com/docs/sendgrid/api-reference/api-keys/create-api-keys), and [Anthropic key prefix](https://platform.claude.com/docs/en/api/cli/beta/organization/api_keys/retrieve). Detection of legacy Google `AIza` keys does not cover every current Google format: Google's [official developer forum](https://discuss.ai.google.dev/t/api-key-to-start-with-aiza/169453) describes the transition toward `AQ` authentication keys. New formats require their own bounded review and tests.

## Source ideas and provenance

The user-supplied `local-legibility-preflight.zip` (SHA-256 `3b7ad26f684e99376868ce6974c8232a8faa19e847707881809b7d322c6c462c`) contained Larry Arnold's JavaScript preflight proposal and seven files. It was inspected as data, not executed or installed. No root license was present; this Python scanner, test suite and integration reference are original implementation, not copied source. The proposal informed the bounded publication check and separate secret/privacy tiers. The original archive remains private source evidence outside the plugin.

The integration avoids the proposal's skipped script/style content, missing encoded views, implicit source-walk assumptions, global allowlist, flag-order dependence, first-occurrence-only line reporting and output-modifying redaction. It preserves the useful narrow local preflight idea without adopting the original implementation or changing publish/send authorization.
