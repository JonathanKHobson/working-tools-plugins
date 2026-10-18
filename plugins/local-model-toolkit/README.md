# Local Model Toolkit

Local Model Toolkit helps a recipient use local language models through an installed runner such as LM Studio. It is CLI-first and keeps model selection tied to the task, available memory, context length, latency, output quality and demonstrated failure modes.

The toolkit does not bundle model weights, an account, a provider key, a machine path, a volume name or a background service. A recipient chooses an approved model source, configures the local runner, and accepts any provider terms themselves.

Start with `skills/local-operation/SKILL.md`. The CLI reference covers discovery, bounded loading, one-model-at-a-time execution and unload verification. The benchmark reference defines representative fixtures, rubrics and receipts. Computer-use guidance is conditional and never replaces a verified CLI path.

## Recipient onboarding

1. Install a supported local runner and confirm its official documentation and license.
2. Confirm available RAM, storage and accelerator support before downloading weights.
3. Discover compatible model variants in the runner. Treat “recommended” as a compatibility hint, not a quality guarantee.
4. Download one explicitly selected quantization, record its source and checksum when available, and test it, then unload it before adding another model.
5. Run the benchmark reference tasks with a bounded context and output limit. Keep raw receipts separate from this public toolkit.
6. Route only demonstrated task families to the model. Re-test after changing quantization, runtime, context, hardware or model version.

The toolkit’s public edition must remain recipient-agnostic. Host-specific findings belong in a private capability record or benchmark report.
