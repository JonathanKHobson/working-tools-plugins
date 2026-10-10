# Source and release architecture

Working Tools uses a hybrid: related reviewed workflow packages share this repository and marketplace, while independently maintained Compass runtimes, large datasets and provider implementations keep their own owners. A repository is not an installation unit; each directory under plugins is separately versioned and installable.

Public CI builds entirely from this repository. It never needs the maintainer's private source paths, accounts or corpus. PROVENANCE.json in each package records reviewed input hashes, transformations and exclusions. Public changes must be reconciled deliberately with the owning source before a later export. Do not overwrite a reviewed contribution with an old local copy.

catalog/packages.json drives both marketplace formats. Package tags use `package-id/vVERSION`. Release assets contain deterministic ZIPs and checksums. The catalog Site consumes a reviewed projection and links back to GitHub; it is not automatically synchronized.

Licenses belong to packages and files. The root license covers newly authored repository infrastructure and documentation only. Bundled third-party material keeps its own license and notices. Provider-owned services, client records, local authentication, restricted methods and private datasets are excluded. Release scope is recorded explicitly; a small subset is never presented as a complete Studio.
