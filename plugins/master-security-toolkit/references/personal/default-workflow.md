## Default Workflow

1. Classify the artifact and intended action.
   - Artifact: app bundle, CLI, MCP server, Claude/Codex plugin, browser
     extension, package, script, Docker image, repo, release artifact, checksum,
     update, or copied code.
   - Intended action: inspect only, download, install, run, wire into
     Claude/Codex, grant permissions, copy code, adapt patterns, or publish.

2. Verify the source before touching execution.
   - Prefer official sites, official package registries, signed releases,
     maintainer-linked repositories, release attestations, and publisher-owned
     documentation.
   - Treat search ads, SEO results, Discord/Reddit links, mirrored downloads,
     and AI-generated install instructions as untrusted until traced back to an
     official source.
   - For current advisories, releases, package metadata, or reputation checks,
     use live source verification instead of stale memory.

3. Inspect before running.
   - Read install instructions, manifests, and entrypoints before execution.
   - Inspect relevant files: `.mcp.json`, `plugin.json`, `manifest.json`,
     `package.json`, lockfiles, `pyproject.toml`, `setup.py`, requirements,
     shell scripts, Dockerfiles, GitHub Actions, plist files, LaunchAgents, and
     LaunchDaemons.
   - Never run the reviewed artifact, installer, lifecycle hook, MCP server, or
     binary as part of inspection unless the current user explicitly authorizes that step.

4. Apply the Evidence Hierarchy.
   - Rank trust signals by strength and explain what evidence is missing.
   - Popularity, stars, screenshots, social buzz, and AI recommendations are
     weak signals, not proof of safety.

5. Check the relevant threat surfaces.
   - Load `references/threat-catalog.md` and scan the rows for the surfaces in
     scope.
   - Include the important rows checked in the `Threats Checked` section of the
     output.

6. Run narrow checks when useful and available.
   - Verify checksums, signatures, notarization, and attestations when the
     publisher provides them.
   - Use ecosystem checks such as GitHub advisories, dependency review, secret
     scanning, static search, manifest diffing, `npm audit`, `pip-audit`,
     OpenSSF Scorecard, SLSA/GitHub/PyPI attestations, and package provenance
     when they fit the artifact.
   - Do not install new scanners or create new security infrastructure just to
     finish a quick review unless Jonathan explicitly asks for that.

7. Produce an MCP capability fingerprint for MCP reviews.
   - Use the template below before wiring or updating any external MCP.
   - Require re-review if the fingerprint changes after approval.

8. Decide and recommend.
   - Use one of three verdicts:
     - `Proceed`
     - `Proceed with caution`
     - `Do not install yet`
   - Name the concrete reason, not just a vibe.
   - If evidence is missing, mark it as an unknown and give the safest next step
     that would reduce the uncertainty.
