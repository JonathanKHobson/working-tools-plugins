# The Learning Plan · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Primary | primary | #35543B | Observed direct source color; this reusable accent role is an editorial choice, not an inferred original token. |
| Learning panel | surface | #E7EDE1 | Native reference.docx word/document.xml active shading/border value #E7EDE1; source visual and native-design-style-audit corroboration. |
| Panel rule | rule | #BCC8B9 | Native reference.docx word/document.xml active shading/border value #BCC8B9; source visual and native-design-style-audit corroboration. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Primary | 8.46:1 | Normal-size text contrast threshold met |
| Text / Learning panel | 17.60:1 | Normal-size text contrast threshold met |
| Text / Panel rule | 12.10:1 | Normal-size text contrast threshold met |
| Primary / Learning panel | 7.09:1 | Normal-size text contrast threshold met |
| Primary / Panel rule | 4.87:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Learning Workshop Proposal: native colors](references/learning-workshop-proposal/COLORS.md)
