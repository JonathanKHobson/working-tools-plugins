# Room to Gather · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #243746 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #243746 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #EFF3F6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Editable field | input-surface | #FFF2CC | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |

## Functional states from conditional formatting

These colors appear only when the native workbook rule is met; they are separate from the base identity palette. Preserve the condition and a readable text label.

| Name | Role | sRGB hex | Condition | Source |
| --- | --- | --- | --- | --- |
| State surface / Missing | conditional-fill | #FCE5E1 | Missing; Over | reference.xlsx conditional formatting: Sessions!F5:F16, Sessions!F5:F16 |
| State text / Missing | conditional-text | #8B251A | Missing; Over | reference.xlsx conditional formatting: Sessions!F5:F16, Sessions!F5:F16 |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 12.28:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 12.28:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 11.01:1 | Normal-size text contrast threshold met |
| Reading ink / Editable field | 11.01:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 11.01:1 | Normal-size text contrast threshold met |
| Identity emphasis / Editable field | 11.01:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Capacity Ledger: native colors](references/capacity-ledger/COLORS.md)
