# Apple Foundation Model Toolkit

Use Apple’s native model for bounded text extraction, classification, rewriting and prototype workflows, with measured output checks. Start with “Check whether the Apple model is ready” or “Extract these fields locally and verify them against the source.”

[Apple model operations](skills/apple-model-operations/SKILL.md) owns readiness, CLI work, task fit and recovery. Its [CLI reference](skills/apple-model-operations/references/cli-operation.md) is for execution; [capabilities](skills/apple-model-operations/references/capabilities.md) separates on-device, Private Cloud Compute, SDK and Siri surfaces.

Requires a compatible Mac and Apple Intelligence readiness. The `fm` CLI is supplied by macOS 27; this plugin does not install macOS, download OS-managed model assets, accept terms by itself, or supply an MCP server. Administrator authentication may be required for machine-wide terms. Live access and successful inference are separate checks. On unsupported hosts, report the missing capability and use an authorized alternative. No provider account or personal machine binding is included.

A user request to analyze supplied text does not authorize executing model-generated file operations. Work Management owns cross-provider selection and coordination. This toolkit owns Apple-specific execution. Installed method files are not proof that the operating system model is ready.
