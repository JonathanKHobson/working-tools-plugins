# Source and release architecture

Working Tools uses a hybrid: related reviewed workflow packages share this repository and marketplace, while independently maintained Compass runtimes, large datasets and provider implementations keep their own owners. A repository is not an installation unit; each directory under plugins is separately versioned and installable.

Public CI builds entirely from this repository. It never needs the maintainer's private source paths, accounts or corpus. PROVENANCE.json in each package records reviewed input hashes, transformations and exclusions. Public changes must be reconciled deliberately with the owning source before a later export. Do not overwrite a reviewed contribution with an old local copy.

catalog/packages.json drives both marketplace formats. Package tags use `package-id/vVERSION`. Release assets contain deterministic ZIPs and checksums. The catalog Site consumes a reviewed projection and links back to GitHub; it is not automatically synchronized.

Licenses belong to packages and files. The root license covers newly authored repository infrastructure and documentation only. Bundled third-party material keeps its own license and notices. Provider-owned services, client records, local authentication, restricted methods and private datasets are excluded. Release scope is recorded explicitly; a small subset is never presented as a complete Studio.

## Release coverage gate

Use `python3 scripts/packages.py build` for a development archive. Publication requires `python3 scripts/packages.py release`; CI runs that stricter command for every push and pull request. It fails before building when an expected package, method or support file is missing, changed or unexplained.

The existing registry still owns package versions and both generated marketplaces. Two reviewed records protect its coverage:

- `catalog/coverage-baseline.json` preserves original audit IDs, current owners and explicit included, external, private, retired or blocked dispositions. Private identifiers are hashed; their named lineage stays in the maintainer's private audit.
- `catalog/source-inventory.json` pins every included file, component entrypoint and canonical source revision. Directory-based sources use a SHA256 tree revision, not an invented Git commit. Held scopes retain their count, tree hash, reason and capability effect.

Public CI checks this committed source snapshot. Before publication, the maintainer also runs `python3 scripts/packages.py release --canonical-root "$CANONICAL_PLUGINS"` against the canonical source directory. That detects new local packages, changed included files and drift in held scopes. Known owner-directory aliases can resolve locally; an explicitly declared external runtime alias is checked without copying its private destination.

A successful release build writes `dist/source-release-manifest.json`, mapping components, canonical revisions, file hashes, versions and public destinations. After downloading the release ZIPs into a separate directory, place that manifest alongside them and run `python3 scripts/packages.py verify-archives --output <download-directory>`. This checks archive and member hashes without extracting or executing files.

The [published source manifest for commit d9a56cd](https://github.com/JonathanKHobson/working-tools-plugins/releases/download/writing-quality-studio/v0.3.6/working-tools-source-release-manifest-d9a56cd.json) records all 31 packages and 10,528 distributable files. Each current public ZIP was checked against that inventory. Its SHA256 is `d2665470ae963fea832a31a04e1d3033a677b2089a8f0e9a7591b3fedb196e41`.

The reviewed inventory locks 31 canonical packages, including Research Toolkit. Writing Quality and UX match canonical source and the maintained personal installations. Discord and Oppia are excluded from current public source and discovery, with historical source and releases preserved in the [withdrawal record](compatibility.md#withdrawn-personal-offerings). Research Toolkit's author-supplied methods have an explicit public grant. Its released archive and all current package archives match the reviewed canonical file inventory; separate native-install and first-use results belong in the compatibility record. A passing source check does not establish every optional provider or model-generated result. Review each source relationship before changing the baseline; do not regenerate it from an incomplete public folder to make the gate pass.

The maintained [Working Tools website source](https://github.com/JonathanKHobson/working-tools-site) has its own repository and deployment history. Historical Compass repositories retain legacy source, routes and downloads; new catalog work belongs in Working Tools.

Human Writing is an authored method inside Writing Quality Studio 0.3.6. Its original text is preserved, and two newly authored support guides repair the missing local references. The original audit entry remains in the coverage baseline as included. Mental Health Navigation is explicitly private at its owner’s direction and is excluded from this public collection; its audit entry remains private rather than an unresolved publication requirement.

## Legal packaging gate

`python3 scripts/license_checks.py` checks each registered package's license documents, host manifest declarations and exact file scopes. A release also runs this check before writing archives. Every operative file needs a current hash, category and license entry in `LICENSE-SCOPE.json`; only the three inventory metadata files may omit self-referential hashes. New or changed material requires explicit rights review before its scope is updated. A passing check establishes packaging consistency, not authorship, license compatibility or legal clearance.

Individual skill builds check the verified source ZIP's license documents, manifest declarations and complete hashed scope before writing any bundle. The existing `.support/` tree retains every source license and notice byte. Existing published plugin and skill assets remain immutable; a correction belongs in a separately authorized later release.

Recorded source-rights questions live in the affected package registry row’s `licensing.releaseReview`. A held review blocks `release` even when structure and file-scope checks pass. A resolution records its reviewer, date, source basis and evidence, bound to exact file hashes; missing or changed bytes require fresh review. This is an internal maintainer release-readiness control. It adds no restriction to the source license and does not replace historical published assets.
