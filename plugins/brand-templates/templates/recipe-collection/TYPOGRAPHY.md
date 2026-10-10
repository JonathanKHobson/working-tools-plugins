# The Shared Table · typography

| Role | Source family | Included rendering family | Relationship | Files |
| --- | --- | --- | --- | --- |
| display | Rockwell | Zilla Slab | substitute | [regular](assets/fonts/zilla-slab/ZillaSlab-Regular.ttf), [semibold](assets/fonts/zilla-slab/ZillaSlab-SemiBold.ttf), [bold](assets/fonts/zilla-slab/ZillaSlab-Bold.ttf) |
| body | Noto Sans | Noto Sans | exact | [regular](assets/fonts/noto-sans/NotoSans-Regular.ttf), [bold](assets/fonts/noto-sans/NotoSans-Bold.ttf) |

## Font decisions

- display: Portable variant selected. Rockwell is a separately licensed/system font; not bundled. Open slab serif substitute for proprietary Rockwell. License: [OFL.txt](assets/fonts/zilla-slab/OFL.txt).
- body: Exact licensed source family for the source role. Exact OFL source family; official variable source is statically instanced. License: [OFL.txt](assets/fonts/noto-sans/OFL.txt).

The source family column describes the originating artifact. An included substitute is an intentional portable alternative, not an exact reproduction or a font-name alias. If a user supplies the licensed source family, retain the source family and recheck line wrapping. Outlined logo masters do not require the font to display.

Preserve display/body/support hierarchy and the source sizing relationships below. Do not shrink body copy merely to fit a specimen box. Test long headings, numerals, punctuation and language coverage with the final font; add a line or page when needed. Retain font license and attribution files with any redistributed binary.

- [Recipe Collection: native typography](references/recipe-collection/TYPOGRAPHY.md)
