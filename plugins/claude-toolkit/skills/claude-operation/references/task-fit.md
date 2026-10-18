# Claude task fit

Use task fit as a routing hypothesis, not a permanent ranking.

- Opus is a starting choice for ambiguous architecture, difficult debugging,
  long-horizon synthesis, and consequential critique. Use higher effort only
  when the acceptance criteria justify the added cost or latency.
- Sonnet is a starting choice for well-specified implementation, extraction,
  routine drafting, and explicit-checklist review. Verify the actual model
  returned; live aliases and product documentation do not establish that a
  requested version was served.
- Claude's CLI is a good fit when the task needs code context, repository
  tools, or a bounded text-only independent worker. A text helper is a poor fit
  for web research or UI manipulation because those tools are intentionally
  disabled.

For each delegation, state the task, supplied evidence, allowed tools, output
shape, acceptance checks, and stop condition. Compare the result to the same
acceptance checks used for other providers. Do not claim that Claude is
inherently better at a domain from vendor benchmarks alone.
