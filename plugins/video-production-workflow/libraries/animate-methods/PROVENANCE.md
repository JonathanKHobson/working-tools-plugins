# Animate source provenance and static intake

Source: [cth9191/animate](https://github.com/cth9191/animate) at commit `7e5eb56feb2dd573f890e1b7b34748af43d58263` (`main`/`HEAD` observed 2026-10-06). Upstream manifest version: `0.4.0`. Source path: `plugins/animate/skills/animate/`. This directory preserves that skill's 107 files byte for byte, plus its repository MIT `LICENSE`, repository `README.md` as `README.upstream.md`, its referenced `docs/styles.png` overview, and marketplace/plugin manifests under `*.upstream.json`. The three root-level support files are renamed only to distinguish them from host entrypoints. The source's `docs/storyboard.png` (4.4 MB) is promotional media outside the reachable workflow and was not imported; `docs/styles.png` is included because `README.upstream.md` links to it. Seven `styles/*/sample.png` files are included because the style gallery and visual selection depend on them. No bulk footage, generated frames, or user reference media was copied. No symlinks occur in the selected upstream skill.

## Review and status

**Verdict for inactive source intake: Proceed with caution.** The source is MIT licensed, and the notice is retained. A static scan with the reviewed local `skillguard_scan.py` wrapper covered 76 eligible text files, found 0 active and 0 suppressed findings, and reported digest `826308d2d4dba07b5db2dba9d135c4de8c8d794ce4bfad54419bcaacf9dc5852`. This does not cover image bytes, dynamic behavior, dependency packages, or runtime network requests. I inspected the upstream skill, manifest, grammar, style cards and kits, demos, templates, and tool entrypoints. No upstream JavaScript or Python, install command, browser, renderer, voice model, or sample piece was executed during intake. The upstream source was fetched with Git; inspection, copying, checksum comparison, and the local static scanner were run.

The skill is **not discoverable as a host skill from this library**. The host's `create-motion-graphics` workflow owns any route into these methods, and the host's video QA/render contracts remain authoritative. Upstream instructions to require Claude, install Playwright globally, demand each of three check-ins, use `AskUserQuestion`, or delay an authorized deliverable are source behavior for adaptation, not host policy. Use the existing local toolchain and project-specific external-SSD workspace; check current runtime availability and the exact visual result before any future execution. Preserve user references locally, check rights to music/screenshots, and treat the optional ElevenLabs connector as separately configured and potentially credit consuming. The source's `new-style.md` describes a custom-look procedure; it is not an eighth installed style.

## Runtime and data boundaries for later integration

- Core contract: `piece.json` selects one `style`; `tools/build.mjs` concatenates `src/head.html`, `kit/core.js`, one style `kit.js`, scenes, bridges, `kit/morph.js`, board and score parts into `index.html`. `kit/morph.js` exposes `window.renderFrame`; score tail exposes `window.renderAudioWav` and `window.renderAudioStems`; storyboard exposes `window.renderBoard`. `TIMELINE` provides dimensions, fps, frames, shots, cuts/morphs, acts, safe areas and optional narration. A style implements `STYLE.paper`, `backdrop`, `window`, `blob`, `hero`, and optional hero outline/colour, `post`, `ones`.
- Output contract: Playwright Chromium calls the local HTML frame/audio functions; `export.mjs` writes PNG frames, WAV/stems, MP4 and optional SRT/caption preview; `review.mjs` reads video/audio and writes contact sheets and measured cut, text, anchor, loudness and pacing checks. Native tools require Node 18+, Playwright/Chromium and ffmpeg; optional word timing uses Python `faster-whisper`. No package lockfile or pinned dependency version is supplied. `faster-whisper` may obtain model files when later used; this was not tested.
- Network and credentials: `capture.mjs` navigates an arbitrary supplied URL in a fresh Playwright browser; do not use it on private/internal URLs or authenticated pages without task-specific authorization. Upstream voice instructions offer an ElevenLabs OAuth connector and per-character paid generation; no token or API key is bundled or requested by the source code. The other reviewed tools operate on local files, although unreviewed npm/PyPI/Chromium installation and model downloads would involve network. No telemetry, MCP launch definition, persistence hook, browser-profile access, or credential-reading code was found in the imported files.
- Untrusted piece input: `build.mjs` accepts `piece.json` `build` and `scenes` file paths, and recursively discovers local `styles/<name>/kit.js`; this is not a sandbox. It embeds every supported file directly in `<piece>/assets/` and checks assembled text with a URL regex and `vm.Script`, but that check is not a full security policy. Run only on trusted project files after inspecting generated parts and assets. `export.mjs` and `review.mjs` write under their resolved piece directories and execute local ffmpeg; `review.mjs` can read reference paths relative to the invocation cwd. Host integration should validate paths and keep task outputs in an owned project workspace.
- Artifact provenance: the repository MIT license covers the copied source as published. Upstream style notes mention studied references, but this review did not independently verify all underlying reference rights; keep reference pixels out of distributed output and preserve attribution for reused code.

## SHA-256 file inventory

Hashes below are of the staged files, excluding this provenance document. The 107 source skill files were byte-compared against the pinned checkout (`diff -qr` showed only added provenance and root support files). The `README.upstream.md`, `plugin.upstream.json`, and `marketplace.upstream.json` map to repository `README.md`, `plugins/animate/.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` respectively.

```text
fe0cbecb2244c397885aae6962df8a0b7d43805d663ee9cda344d05b87bd8625  LICENSE
a70aaa9cbcd8f464edf700aa211950b05e38f133d6b1bee158e31dacd4eaf3a4  README.upstream.md
1208ee4ab2458a4831a9816950cdba25d3869cbbd6a795c4fded995f88bc0761  SKILL.md
7bf4ec7fc81316a5d7d7fb67d8dc025118dc38ae6eaadc57df8fd411bcffe27e  craft.md
56b7b0380a77a00e4d9e5f7e7dacc22a2947811cc2801a9235ccee9b15ec4c3e  docs/styles.png
c4f2b3d295aeed783fd753884fa0931cf53916d9a77a1fb358145759aeae271a  examples/history-of-ai/brief.md
9ae0bdce90e1c310022c24d3014ed7aaee2e1cf8a6ab7e6a2c5201d3370ebdc2  examples/history-of-ai/piece.json
157bafdd047fbc57630c6115542be693e76b6617706b873f0f9358c842a1cb8c  examples/history-of-ai/src/bridges.js
fe07e4b3733782e16edefb96ecea4543c2255ea3d7c88e5de28a25a151edc1ba  examples/history-of-ai/src/head.html
fee87f87f0d38277d039b4c35aaf8345a98d9215fc91de81a199d72d716dea96  examples/history-of-ai/src/scenes.js
13dd29680a040b5eb18b3a4077a1e82d70fc0363cb8c28eaf3133b5b860ebf24  examples/history-of-ai/src/score.js
a4d028dfe78e1dda89b9508a156c65582461379256ca959e277b58522f7bf328  grammar/FORMATS.md
54f27f1cc5b61b2c97210b75f059d523b5cfb35ce90ab09f70857a9d96577665  grammar/FRAME.md
33f8fa0d2f6da78e9df1825ecabc7186f5a01f676328c165bbfe1cacb3646772  grammar/STORY.md
a5408cce5e2117c899fef6b329e670d060d72f844c81883333d96fa9ca6917c7  intake.md
b4245796208eba9d44dbdccae9af70d4857741631d6f0aeaef4ffb0674fb266b  kit/board.js
d791e21cdc1396d20bd7f1507a34693c64be9220a0d996cc4688149554967fc9  kit/core.js
08d1427f6b2044dedcca4487d92cc6f67a176834b6e9d020aca146ef1813209d  kit/morph.js
2dc73db24872366c7225f734761629712ab354edf5af5c1e8302e7fed47a0262  kit/score-head.js
554c065624508bf23fcc0a55581c1ebf3a92df461b72a8ed115dd1defbca9f3e  kit/score-tail.js
b82a3ccc3caef94636fc54d570663b87dd5562d6761a2acbdd9690c20df0b56c  marketplace.upstream.json
4ef30cf187ff1b1b3f501670b663396c44ce283d026e1cea76ef44899d9f2d2c  new-style.md
cd67961788d6058d17db1951adeee6f91095980526881cb7a609c8bc9114e762  plugin.upstream.json
4211463f82c631d859ca304dc9c0d325835ba5ba479b761d6f02f03421142fb5  styles/README.md
97a3cdfd418e9de66914708e9fd9b03cb20acb1b8ac0f327e46830f9b3937a82  styles/crosshatch/STYLE.md
c21ae6c28b72374a9020d906297f4dbbc3be105f286f87f18fe894f3849e5c63  styles/crosshatch/demo/piece.json
1cc6db03d883f917074f859eeedbb0fa76d9d3e3429c1d8b80b4dbddeb52f423  styles/crosshatch/demo/src/bridges.js
e514511bc44ea4e19e0845899a1129fe37e209d02aca8e26eddd63b9ddac010a  styles/crosshatch/demo/src/head.html
98ec5309ab5b44ba31e503ccbe27d5960985f41d67db915e78ea0377646a199a  styles/crosshatch/demo/src/scenes.js
b03ca36aa207cfbe330c1d1f2fea3b8c0bcc1c013a5ac62f93a3b780dec45ee7  styles/crosshatch/demo/src/score.js
a8c051c840e5a12c94984d37a9fa5db6be40938853197237d7f740312121822a  styles/crosshatch/kit.js
6a6c8445cc58eeeef43a88bef6631ef294fe935927c39e7b14b9ed72f56a42d0  styles/crosshatch/sample.png
84a706921678d0288be4500efd5ca8170427333a4849b4848bf75ebad7603a6a  styles/cut-paper/STYLE.md
498b17360f27fd65a5cddd6513584c8f3e5e91a18a758f4d6f26eb6a7d9a3a3d  styles/cut-paper/demo/piece.json
5b3ee1d625c8f165b069380bc5a32fef8a00b93783f881be37f97b4d31c0486a  styles/cut-paper/demo/src/bridges.js
2daa7df2a77528855a1bda2e9d3eb28066538cc55fd11cad6e5eb29e0d6b637f  styles/cut-paper/demo/src/head.html
17b3b6b938fc9d87cee6f558a8835f01bdefc17512d69b1e0d64e974fab9c831  styles/cut-paper/demo/src/scenes.js
5d2ef0d070179a0d72d1a16793179d920090e16f6d2e4ddd4584e62b18ee6454  styles/cut-paper/demo/src/score.js
f5791c4b6481407d4eba0eab69eca35d227481816b384967f6adf86c1ccd1a1e  styles/cut-paper/kit.js
378e45dadf1a42b9a6e96b6eddc7452ed1239f4da58aa77453c73ebd1ef45f4f  styles/cut-paper/sample.png
ce4d7cfdb19620abf0dd63da2f7ff88c89987042da4950d87403189f4c411095  styles/isometric/STYLE.md
32af19a37f7a93902f8cfbbdcb789f3158f1a274e8e2641784f3b9f741f272af  styles/isometric/demo/piece.json
a05964cb61d668491cd1f7152c3ab29df31b519d88578752e90585b8db7107df  styles/isometric/demo/src/bridges.js
1ef884579bd8366cdeb36e0dbdead04433aba1d5a67a36d6fa2dc00863c08fe3  styles/isometric/demo/src/head.html
96aeb3f37611c1db78b6eda8064a5a20018224d7a53d105d3d1b9895668604a4  styles/isometric/demo/src/scenes.js
30b29803a36fedde86046c7b026ea20167f438349c54f6d1eb60a68bccd358f4  styles/isometric/demo/src/score.js
b5e3027340ffbd34d908c086afad8941d8b9fa62513a9be032e1a3e2d7456c77  styles/isometric/demo-dark/dark.js
daaa90deabc1ed2e1d0dfeb857ec41ab970dc503e331e2e0a19203d7e61592e7  styles/isometric/demo-dark/piece.json
80de9daeec940abd0eb25a9fb865df328b477a41301099b6a61e50a5a4f7f37e  styles/isometric/kit.js
98f67dd5780a43c4e409b2fbe0062028013f252e22065dcc865b871e52ea02a4  styles/isometric/sample.png
28814f02d829e504ceb9bdfcfad123067b764fcba05588a10bc3215d6ca11ba2  styles/math/STYLE.md
941241e609880880383086637b704e7a1cd94387f064beea39299aaebc1daec7  styles/math/demo/piece.json
8c0dac6b99175c84462edffa9150c34840abca43cb27a62603eb4d392789ba10  styles/math/demo/src/bridges.js
b8435007c3b9217d622f0969604bb31d7b18bca7130163ff0393d50fbe068739  styles/math/demo/src/head.html
1be3ad658cc47827ae4f886d506b76551b51bcb96deb6d2be470b7cde8301034  styles/math/demo/src/scenes.js
18949ceb8efb7a2f1bb3f2d954241648968e05159fae2a4060b800b481929b62  styles/math/demo/src/score.js
314522b839515ef2ef4f98d4576a85acf12a9e954b73b9cd73a5a0341f14860e  styles/math/kit.js
133d4f1ff778fcb7fd70d3e9b48a14f94b3b5f4e96f77bf40883c475ee86443a  styles/math/sample.png
58712dbbb7628e486d943fcb4ce6a89abd5de0e545e123e5483abeaf792395ca  styles/pixel/STYLE.md
ac47a6cdd3ae71ce76d7df737d7ee5f1d4d9b15b0591498184923a9c0a2b1c9e  styles/pixel/demo/piece.json
7368810fe8c7f14bd5f10a2f803bbd3a67bc723fc36bf54a650d04030b9dfb95  styles/pixel/demo/src/bridges.js
34cc43e5f0844628c7a19d3f7f665ce1c6feb93b5d826f360d42d6802b5d2b75  styles/pixel/demo/src/head.html
e262ff298cae03bb706a017959fe1aa75ef8ae2eda168adb07927c8c14d196e9  styles/pixel/demo/src/scenes.js
c090864e79a91425e0ecefb71b86161a89f1257d3b34068f451e91ef9ab3c3c5  styles/pixel/demo/src/score.js
f5578749601de7b76c0572e65607d04e9233a7ae99ccd34d438d6dfd6b8806e2  styles/pixel/kit.js
78db9a4fadc0b89496305a0c91011759e68ad67b2e2aff0f1dd50a1576f5f1f9  styles/pixel/sample.png
89eaf579f69496e979e1b985a37fa9f52e0932a874b27cdc0cebec5d787947fe  styles/riso/STYLE.md
1aea3bee103a28d182a113e039b66014797ea93c6a3418ce63acbcbb663c123a  styles/riso/demo/piece.json
4551788f7c5d3c1a82da4a8fe904ec3bf6d6df96fbb368f7418ce0c0f34661f7  styles/riso/demo/src/bridges.js
cc99611f91cfd8593a31cd224f748748a89cd827d8b25bb920a3d404b64f1473  styles/riso/demo/src/head.html
086510b88e417fc6a77fb8dd807956bd7424f3965bf3e376d89314afb80851ac  styles/riso/demo/src/scenes.js
8d254e04be626b5f5db548d011be43045c7f755bd3a9dd1f4687d7b247de45dc  styles/riso/demo/src/score.js
0786f5db98abb592bcb1249b3558a6ff69d1a41afa4005f7b4d185758744791b  styles/riso/kit.js
288b1932f09e5a57e4d5a1dd1159d62987dc1aa440507b064d344efae273e20c  styles/riso/sample.png
3398e03719b6deb2ff68f6f1be52a47e370f1389f8b67be74af0887ad4ac9d5c  styles/sketchbook/STYLE.md
c7b45b1673ecc228c16dd6d0f448a21c795c36737abdbc5463be269c778a9741  styles/sketchbook/demo/piece.json
7924370bde0b4a3a08ccda806cfb686a2805146ca4d06abb849504179b381f29  styles/sketchbook/demo/src/bridges.js
769371c3cc878c5730234e7ef073cf176ba67575b6afb4145bc547f1dc05536b  styles/sketchbook/demo/src/head.html
2d671dc247896a4f10c0bf88de32995b5da52fce12d42741d0d72abf42a35f0c  styles/sketchbook/demo/src/scenes.js
2fd3653e0015b388999fb13169df18eae15cfc4cd2022f0944c6d245a3ea22c6  styles/sketchbook/demo/src/score.js
02ff4694da28f267920ddd5d2b01a9d9314c0fd33d0af679b2a8a1e99c86aca3  styles/sketchbook/kit.js
9aec4681282a744c8b09a17404bced48c0416d3f1888ff85721a42cf32c4f553  styles/sketchbook/sample.png
392e33a9aaeec8180c40aeb421d001f8a39a2853eba8adbabc840133d82fe437  templates/beat-cut/piece.json
50d0853f4f79968f1621adc1267baea70aeb461663d762fa05ac0070def89f56  templates/beat-cut/src/bridges.js
37952dc2395377e210ce91047343b3c5fa796df1b931c0e3d040ef4b176995ef  templates/beat-cut/src/head.html
cc5e8b8b3296d59867a885434059955a5f971949f3f7a3b916b0da5bcda3bf51  templates/beat-cut/src/scenes.js
1f88298b86e8ed28e42a69486c5f4c304b3197e613e5e0842818d1f49b946284  templates/beat-cut/src/score.js
5aa996b921cc77c336bdab5bb9d58a6478c8df4e161d4e740f47bd56fec12985  templates/piece/LOG.md
4c2a0fa85716b8ad56b178c5f98d03fd1227284973482507bcf270243a54d26f  templates/piece/brief.md
4f763beaf3deb651b79bc71cfc18ee966c4bb72ea7a8b4aea8dac7f9bf6a9fc2  templates/piece/piece.json
0c958e758d88e9cbee315e26d208a203ec2bcf2c0f97b3fd2c93e1e9c2b2383b  templates/piece/src/bridges.js
787f874220e936456626cf38bec78073c53ecbb47551d64c002c5e4ce9bc6cd6  templates/piece/src/head.html
540ead100c55ce17a8a99209c6149084a8ef0dc291b72b59b32e02bc88c19549  templates/piece/src/scenes.js
5d2ef0d070179a0d72d1a16793179d920090e16f6d2e4ddd4584e62b18ee6454  templates/piece/src/score.js
d350c393801d5f8a114393a9427f9d4871c97a9b3e7019d3294edead97f86a77  templates/style/kit.js
97ccfe3ab2547241d1facc90b43703a643a35cb9c89467c04984f55ff4b5582e  tools/beats.mjs
2209a54a41add2e4da103a0056fd60c994e07f06b2586eca901e0d051cfae202  tools/build.mjs
801db97ec5f6c94e2988a05fa6e625f71d7cadd5eb28761745ea0fa4cf8bb3e1  tools/capture.mjs
2eaef479fd44f78ab75e29c9b2f01ea8861909e6b8294559d9b31c5d485f7e1a  tools/compare.mjs
addf2fbe8a6c4ea1bb76544b76b824b4706fcbc04e1e5c251392d03c9f5a2e23  tools/export.mjs
ab2a2d1806ef115be08c7721ab0816eb2ea880fd2c5630bdfb1acf6ceb0f49ba  tools/framehash.mjs
620884b520b56be4e292b188949d4d99ddcdeda295d1af02091d69bb405ca293  tools/gallery.mjs
2ca101f6951be4a34519271d1c6166d9e55f385413b62d97e25782af3e73d280  tools/gpu.mjs
1ab59c2c2b3c10a014f178550826cc9348f8fa6b3b98f1e0137d7104beb1954e  tools/measure/refs.mjs
44d4cd254fcaed03f433389208a9aeecfdcc0d185ef0d2fa02456d21843be286  tools/measure/shotlog.py
7e03d692cc647562c03bed715b06e6ec8a7661e74fc5f392a269b04774b2c6ee  tools/review.mjs
801a6db91d4a1aff99fd1aac7ff94e7c03b7a5f0aa114f719ea1bd7eac879b64  tools/still.mjs
c8998cd90250c8aac67b5ba58a4ec124b494de61ae3d1273012b552a74875ed9  tools/storyboard.mjs
2462f31603f72f10e885bc921f11806f35bbf3bdebc12706fcd1f99f289ed991  tools/textcheck.mjs
a9e4bc642db7ba2ad48ab4a62583a12539d2450ade6fcfcc615dfb317038c5e9  tools/tile.mjs
123159fdaf3bc587addab6e0166718b90388c71dfa9f1e0c31ecada465b3e81a  tools/voice.mjs
e24bdae8ab3432910c932b2ea50c467f1a641f03f832aa7106e8ddbb94747808  tools/voice_words.py
```
