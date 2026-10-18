# Benchmarking

Benchmarks should use authored, non-sensitive fixtures that resemble the recipient’s work. Label each fixture as synthetic or derived from a redacted project excerpt. Keep the fixture, rubric and raw output together in a private report; do not publish account names, machine paths, private source text or receipts.

Each run records:

- exact model key, quantization and runtime;
- host capability summary and date;
- context length, parallelism, output bound and temperature when supported;
- pre-load and post-unload process state;
- load and response durations, raw partial output and return code;
- per-task rubric result and observed failure mode.

Compare models on the same fixtures and bounds, one model at a time. Do not infer quality from speed alone. A strong recommendation requires repeated passes across at least four relevant task families and an explicit statement of unknowns.
