# Ground a diagram in actual repository behavior

Use when an architecture, sequence, dataflow or lifecycle diagram claims to explain real code. A conceptual proposal can instead label assumptions; never dress a proposal as observed behavior. Existing structural-diagrams owns notation and layout, and visualization-verification owns rendered acceptance.

## Inspect the smallest connected slice

1. Record the repository identity, revision and dirty state. Remove credentials/userinfo from remote URLs before recording them. Preserve the transport and path; an SSH/internal repository need not become a public link. A committed revision identifies committed bytes only. Cite changed working files with an explicit working-copy label and file hash, or inspect their committed versions; do not label dirty bytes as HEAD evidence. Keep source paths private when the output audience does not have access.
2. Locate the requested behavior using project instructions, manifests, registrations, entry points and configuration. Follow calls/imports from input through output or side effect. Do not inventory unrelated modules or create every discovered helper as a diagram node.
3. Distinguish the actor requesting work, the runtime executing it, the transform operating in memory, and the store receiving bytes. A controller owning a responsibility does not prove that it performs direct file/database I/O. Trace each reader/writer to the actual operation. Distinguish a configured provider, injected adapter, test stub, optional capability and running service.
4. Record exact relative paths and line ranges for each consequential node, relationship and boundary while reading. Check actual branch conditions, retries, fallback, errors, authorization enforcement and persistence. An exported but uncalled function does not establish a normal-path edge. A package description or configuration name alone is not a runtime trace.
5. Attach unresolved questions to the affected claim: observed write call versus unverified durability, optional provider versus unknown deployment, inferred relationship versus inspected call. Read the next relevant range only if it could resolve a consequential uncertainty. Stop once the requested responsibilities and relationships are supported; there is no target node/citation count.

## Author and verify

Choose the smallest notation that explains the question. Keep stable IDs and meaningful relation verbs, with an adjacent evidence list or source fields supported by the chosen format. Show the main path and necessary exceptional branches; preserve control ownership and behavior-changing conditions. A schema/example can teach shape, never supply repository facts. Keep external storage outside a control boundary unless enforcement evidence supports including it.

Check each asserted relationship against its cited source and conditions, then validate the selected notation/model. Inspect the rendered result at its intended size and a relevant narrow view; geometry or schema validation does not prove source truth or visual quality. For revisions, recheck changed entry points, dependencies and evidence. Deliver the diagram with observed/proposed/unknown distinctions and the actual checks performed.

Adapted from [Archify repository authoring](https://github.com/tt-a1i/archify/blob/7158026e852f3aa6578c741e673b46d7878c92c1/archify/references/repository-authoring.md), MIT. [Notice](archify-LICENSE.txt). This method does not install Archify, run its finalize/update checks, copy its renderer/brand assets, or impose its schema. Existing reviewed renderers remain available through the owning workflow.
