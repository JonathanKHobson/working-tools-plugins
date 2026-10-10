# Trace Practice · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Rendered source page 1 white reading ground. Mint is a secondary/reversed source color, not the whole page background. |
| Reading ink | text | #172D47 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Accent | accent | #EAC16F | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #AADCDD | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Table row | surface | #F1F5F7 | Native reference.docx word/document.xml active shading/border value #F1F5F7; source visual and native-design-style-audit corroboration. |
| Table rule | rule | #C7D4DA | Native reference.docx word/document.xml active shading/border value #C7D4DA; source visual and native-design-style-audit corroboration. |
| Mint support | support | #EAF3F1 | Native direct run color #EAF3F1; retain for supporting/reversed areas rather than assuming page fill. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 13.97:1 | Normal-size text contrast threshold met |
| Reading ink / Accent | 8.22:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 9.31:1 | Normal-size text contrast threshold met |
| Reading ink / Table row | 12.74:1 | Normal-size text contrast threshold met |
| Reading ink / Table rule | 9.22:1 | Normal-size text contrast threshold met |
| Reading ink / Mint support | 12.37:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Applied AI Workflow Case: native colors](references/applied-ai-workflow-case/COLORS.md)
