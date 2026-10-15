# Individual skill downloads

The Site offers a single skill entry with the supporting files from its released plugin. These are generated distribution files. They do not change canonical authoring, installed plugins, or the normal release command.

## Automatic maintenance

`complete_update.py --publish` and `--publish --reconcile-only` generate and verify skill downloads after importing the current plugin releases and before committing or deploying the Site catalog. Only a changed current plugin version needs new bundles. Unchanged products reuse their initial downloaded-byte verification only when the GitHub tag, asset digests, sizes, URLs and uploaded state still match. A failure prevents Site promotion and retains verified checkpoints for retry.

`catalog/skill-downloads.json` is a generated index, not another manually edited registry. Each product carries its exact parent plugin version, commit and ZIP hash. Each skill carries its frontmatter identity, original directory, ZIP URL, size and hash. Added/removed skills follow the released source tree. The Site projection checks the complete guide/download inventory before writing pages; a newly added skill without a guide is reported as a catalog gap, never silently omitted.

GitHub companion releases use `skill-bundles-v1/<plugin>/v<plugin-version>`. They preserve the original plugin release and every historical download. The format prefix versions the packaging contract without changing plugin versions. Never replace an existing asset. A deliberate future archive-format change requires a new format identity and corresponding Site support.

Initial backfill of already-published versions uses `python scripts/sync_skill_downloads.py --publish`; subsequent plugin publishes invoke the same code automatically. No watcher, per-skill release notes or separate routine upload is required.

## Contents and limits

Each archive has one top-level skill wrapper, a README and a file manifest. `.support/` retains the complete byte-exact reviewed plugin tree, including shared methods, scripts, assets, licenses and notices. This conservative choice keeps dynamic and relative references available without hand-maintained dependency lists. Some archives are larger than the selected skill's own folder.

The wrapper points to the original procedure and establishes `.support/` as the plugin root for package-root commands. Only that selected procedure is the entry point. Other skills are supporting material where referenced. Nested plugin/MCP/hook configuration is retained as source material, not registered or activated by extraction. External applications, accounts, providers and runtimes still require their own setup. Installing a standalone skill does not recreate full-plugin behavior.

The builder verifies source ZIPs against the exact Git tree, rejects unsafe archive paths and links, preserves executable modes, and round-trips all support hashes. Tests verify deterministic output, quoted names, differing directory/skill names, integrity failures, a real extracted fixture command, release no-ops, version updates and failure-before-Site-promotion. These establish file packaging and the release transaction; they do not certify every external service or skill task on every AI host.
