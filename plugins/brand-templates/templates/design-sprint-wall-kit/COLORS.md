# Frame to Test · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #562C30 | used style Heading1 explicit text color |
| Working slip | surface | #F5F2EC | Native reference.docx word/document.xml active shading/border value #F5F2EC; source visual and native-design-style-audit corroboration. |
| Slip border | rule | #C9C1B8 | Native reference.docx word/document.xml active shading/border value #C9C1B8; source visual and native-design-style-audit corroboration. |
| Reading ink | body-ink | #000000 | Native reference.docx word/styles.xml: style Title, style Normal, style KitTestBody; text. |
| Source link | link | #304D4A | Native reference.docx word/styles.xml: style KitLink; text. |
| Prompt amber | accent | #F2C467 | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |
| Prompt sage | secondary | #A9C4B9 | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |
| Prompt paper | motif-ground | #F8E9D0 | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 11.68:1 | Normal-size text contrast threshold met |
| Background / Reading ink | 21.00:1 | Normal-size text contrast threshold met |
| Background / Source link | 9.19:1 | Normal-size text contrast threshold met |
| Text / Working slip | 10.45:1 | Normal-size text contrast threshold met |
| Text / Slip border | 6.56:1 | Normal-size text contrast threshold met |
| Text / Prompt amber | 7.15:1 | Normal-size text contrast threshold met |
| Text / Prompt sage | 6.27:1 | Normal-size text contrast threshold met |
| Text / Prompt paper | 9.76:1 | Normal-size text contrast threshold met |
| Working slip / Reading ink | 18.79:1 | Normal-size text contrast threshold met |
| Working slip / Source link | 8.22:1 | Normal-size text contrast threshold met |
| Slip border / Reading ink | 11.80:1 | Normal-size text contrast threshold met |
| Slip border / Source link | 5.16:1 | Normal-size text contrast threshold met |
| Reading ink / Prompt amber | 12.87:1 | Normal-size text contrast threshold met |
| Reading ink / Prompt sage | 11.28:1 | Normal-size text contrast threshold met |
| Reading ink / Prompt paper | 17.56:1 | Normal-size text contrast threshold met |
| Source link / Prompt amber | 5.63:1 | Normal-size text contrast threshold met |
| Source link / Prompt sage | 4.94:1 | Normal-size text contrast threshold met |
| Source link / Prompt paper | 7.68:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Design Sprint Wall Kit: native colors](references/design-sprint-wall-kit/COLORS.md)
