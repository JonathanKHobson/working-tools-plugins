# Issue Desk · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #16252E | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #101B24 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #E3EEF6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Calculated Surface | calculated-surface | #F0F4F6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Editable field | input-surface | #FFF1D1 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Editable value | input-text | #0000CC | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |

## Functional states from conditional formatting

These colors appear only when the native workbook rule is met; they are separate from the base identity palette. Preserve the condition and a readable text label.

| Name | Role | sRGB hex | Condition | Source |
| --- | --- | --- | --- | --- |
| State surface / Scorable | conditional-fill | #E0EEE7 | Scorable | reference.xlsx conditional formatting: Scorecard!G10:G18 |
| State text / Scorable | conditional-text | #18563B | Scorable | reference.xlsx conditional formatting: Scorecard!G10:G18 |
| State surface / n.a. | conditional-fill | #FFF1D1 | n.a. | reference.xlsx conditional formatting: Scorecard!H10:I18 |
| State text / n.a. | conditional-text | #704000 | n.a. | reference.xlsx conditional formatting: Scorecard!H10:I18 |
| State surface / TIE | conditional-fill | #A4D8E2 | TIE | reference.xlsx conditional formatting: Scorecard!J10:J18 |
| State text / TIE | conditional-text | #101B24 | TIE | reference.xlsx conditional formatting: Scorecard!J10:J18 |
| State surface / WEIGHTS OK | conditional-fill | #FFC7CE | WEIGHTS OK | reference.xlsx conditional formatting: Scorecard!B6 |
| State text / WEIGHTS OK | conditional-text | #9C0006 | WEIGHTS OK | reference.xlsx conditional formatting: Scorecard!B6 |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 15.69:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 17.44:1 | Normal-size text contrast threshold met |
| Reading ground / Editable value | 11.22:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 13.32:1 | Normal-size text contrast threshold met |
| Reading ink / Calculated Surface | 14.18:1 | Normal-size text contrast threshold met |
| Reading ink / Editable field | 14.02:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 14.80:1 | Normal-size text contrast threshold met |
| Identity emphasis / Calculated Surface | 15.76:1 | Normal-size text contrast threshold met |
| Identity emphasis / Editable field | 15.57:1 | Normal-size text contrast threshold met |
| Supporting field / Editable value | 9.52:1 | Normal-size text contrast threshold met |
| Calculated Surface / Editable value | 10.14:1 | Normal-size text contrast threshold met |
| Editable field / Editable value | 10.02:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Evidence Audit Scorecard: native colors](references/evidence-audit-scorecard/COLORS.md)
