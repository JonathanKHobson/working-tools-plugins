# Pinned native runtime provenance

Source: [pbakaus/impeccable at 114ea1d3838fca73b253af45f873b9c4f5f213c8](https://github.com/pbakaus/impeccable/tree/114ea1d3838fca73b253af45f873b9c4f5f213c8), Apache-2.0. The pinned source archive SHA-256 is `f12d358c640c33c90ad198d09b1dbe77ddc37286c72c74fc4e5b16ae70816b3d`. Apply [SOURCE-PATCHES.diff](SOURCE-PATCHES.diff), SHA-256 `bdd5c2364fd029b9e1b45feed99077289be68ed4dce656e4697c31565204b6ae`, before building. The patch marks our changes to live source reading, URL probes, and injection safety; it does not alter the tracked browser detector bundle.

Built on macOS arm64 with official Rust 1.98.1 arm64 distribution (`rust-1.98.1-aarch64-apple-darwin.tar.gz`, SHA-256 `cfc171d8120d401b10a1028c52646dd8e00e3e66852f949061ce087845f55afd`) verified against `channel-rust-stable.toml` and its official `.sha256` sidecar. The working compiler/linker was `/Library/Developer/CommandLineTools/usr/bin/clang`; no Xcode license change was made. The source `Cargo.lock` was used with `--locked` and two build jobs. Build caches and the toolchain stayed outside the installable plugin.

Rebuild in a trusted work directory containing the pinned source and verified ARM Rust toolchain:

```bash
export CARGO_HOME=/path/to/task-work/cargo-home
export CARGO_TARGET_DIR=/path/to/task-work/target
export CARGO_BUILD_JOBS=2
export CC=/Library/Developer/CommandLineTools/usr/bin/clang
export CXX=/Library/Developer/CommandLineTools/usr/bin/clang++
export CARGO_TARGET_AARCH64_APPLE_DARWIN_LINKER=/Library/Developer/CommandLineTools/usr/bin/clang
export DEVELOPER_DIR=/Library/Developer/CommandLineTools
export SDKROOT=/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk
export IMPECCABLE_NO_UPDATE_CHECK=1
/path/to/verified-arm-rust/bin/cargo build --release -p impeccable --locked
```

`bin/impeccable` is the resulting Mach-O arm64 engine, SHA-256 `46df08a23d806599660b8ccf588a5562e11d7b37c3ff2ed199fd686ed1acddc5`. Its CLI version is 4.0.0 (workspace crates are 0.1.6). The browser detector bundle tracked by upstream was embedded at native build time; it was not regenerated from Wasm. The native build emitted a non-fatal debug-stripping warning because the isolated Rust `rust-objcopy` could not resolve its `libLLVM.dylib`; the binary executed and passed the targeted tests and real browser pilot.

Run only through the UX Design Studio owned adapter, which checks the manifest hash, constrains project scope, disables update checks, and blocks the upstream installer/update/image-API verbs. `skill/` playbooks and agents are licensed reference data under the owning Studio policy. Upstream executable download launchers are omitted. License and third-party notice files are in this directory.

## Reviewed local reference amendment

`ASSET-PATCHES.diff` records one local amendment to `skill/reference/craft-floor.md`, introduced by the reviewed October 1, 2026 host refresh and reconciled with this manifest on October 9. The added States guidance requires a recognizable primary control, feedback on the control for pending/confirmed/no-op/retry states, accessible text/icon feedback, reduced motion, repeated-click checks and truthful confirmation. It is reference guidance only; neither the native engine nor executable browser scripts changed.

The retained upstream archive was rehashed against `source.archiveSha256`. All 54 packaged assets were compared to that archive, accounting for `SKILL.src.md` being packaged as `UPSTREAM-SKILL.src.md`. Exactly one file differs. The two restored `skill/reference/degraded/` files come byte-for-byte from the archive's `.agents/skills/impeccable/reference/degraded/` tree, which supplies the fallback bodies linked by `skill/reference/new-work.md` but absent from its `skill/` tree. Their source members and hashes are recorded in the release evidence. The reviewed refresh plan and apply receipt both record its original SHA-256 `d31766f5d4d1e9e2f510fa7b9214f57b678ece687ede90f3deb0973640d672a9` and amended SHA-256 `1a1cfea586ff703cad310823b07a654c25fab0d625a9a2cc4f6dea978546f340`. The upstream closure is preserved as `skillAssetsUpstreamSha256`; applying this separate asset patch reproduces `skillAssetsSha256`. Its patch digest is in `source.assetPatchSha256`. Keep `SOURCE-PATCHES.diff` for the original native source build; apply `ASSET-PATCHES.diff` only to the packaged skill assets after copying them.

The manifest had retained the upstream asset closure after the reviewed reference edit, causing the adapter to refuse all execution. The October 9 repair admits only the verified amendment and leaves the closure algorithm and refusal behavior intact. Any future asset addition, deletion, content change or symlink still fails verification until its exact change is reviewed and recorded. The private audit receipt with local source paths is outside this package.
