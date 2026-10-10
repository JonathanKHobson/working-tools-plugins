# Woven Logic · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Synthesis purple | primary | #563B75 | reference.docx word/document.xml: 17 table header fills; source page 1 visible purple table header. |
| Table lavender | surface | #F0EBF5 | reference.docx word/document.xml: 42 body-cell fills. |
| Weave lavender | motif-ground | #E3DCEF | reference.docx word/media/image1.png: exact embedded woven-strip horizontal thread color. |
| Weave rust | accent | #B4643D | reference.docx word/media/image1.png: exact embedded woven-strip vertical thread color. |
| Weave charcoal | motif-ink | #2D3235 | reference.docx word/media/image1.png: exact embedded woven-strip vertical thread color. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Synthesis purple | 9.22:1 | Normal-size text contrast threshold met |
| Background / Weave charcoal | 12.97:1 | Normal-size text contrast threshold met |
| Text / Table lavender | 17.91:1 | Normal-size text contrast threshold met |
| Text / Weave lavender | 15.75:1 | Normal-size text contrast threshold met |
| Text / Weave rust | 4.83:1 | Normal-size text contrast threshold met |
| Synthesis purple / Table lavender | 7.86:1 | Normal-size text contrast threshold met |
| Synthesis purple / Weave lavender | 6.91:1 | Normal-size text contrast threshold met |
| Table lavender / Weave charcoal | 11.06:1 | Normal-size text contrast threshold met |
| Weave lavender / Weave charcoal | 9.73:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Cross Study Synthesis Atlas: native colors](references/cross-study-synthesis-atlas/COLORS.md)
