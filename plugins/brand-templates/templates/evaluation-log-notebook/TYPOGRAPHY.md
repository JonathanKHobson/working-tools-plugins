# Trial Ledger · typography

| Role | Source family | Included rendering family | Relationship | Files |
| --- | --- | --- | --- | --- |
| display | Menlo, Consolas, monospace | IBM Plex Mono | substitute | [regular](assets/fonts/ibm-plex-mono/IBMPlexMono-Regular.ttf), [semibold](assets/fonts/ibm-plex-mono/IBMPlexMono-SemiBold.ttf), [bold](assets/fonts/ibm-plex-mono/IBMPlexMono-Bold.ttf) |
| body | system-ui, sans-serif | Noto Sans | substitute | [regular](assets/fonts/noto-sans/NotoSans-Regular.ttf), [bold](assets/fonts/noto-sans/NotoSans-Bold.ttf) |

## Font decisions

- display: Portable variant selected. Menlo is an Apple/system font; not bundled. Exact OFL family from IBM's official static TTF package; semibold supports the source's IBM Plex Mono SmBld role. License: [OFL.txt](assets/fonts/ibm-plex-mono/OFL.txt).
- body: Portable variant selected. system-ui resolves to a host-dependent operating-system UI font; original family is not identifiable or bundled. Exact OFL source family; official variable source is statically instanced. License: [OFL.txt](assets/fonts/noto-sans/OFL.txt).

The source family column describes the originating artifact. An included substitute is an intentional portable alternative, not an exact reproduction or a font-name alias. If a user supplies the licensed source family, retain the source family and recheck line wrapping. Outlined logo masters do not require the font to display.

Preserve display/body/support hierarchy and the source sizing relationships below. Do not shrink body copy merely to fit a specimen box. Test long headings, numerals, punctuation and language coverage with the final font; add a line or page when needed. Retain font license and attribution files with any redistributed binary.

- [Evaluation Log Notebook: native typography](references/evaluation-log-notebook/TYPOGRAPHY.md)
