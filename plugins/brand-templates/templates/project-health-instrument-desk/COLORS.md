# Project Instrument Desk · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #101B24 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #101B24 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #E3EEF6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Attention Surface | attention-surface | #FFF0D6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |

## Functional states from conditional formatting

These colors appear only when the native workbook rule is met; they are separate from the base identity palette. Preserve the condition and a readable text label.

| Name | Role | sRGB hex | Condition | Source |
| --- | --- | --- | --- | --- |
| State surface / 0 | conditional-fill | #FBE2DE | 0; Actual missing; Invalid actual; Duplicate ID; Missing ID; Check task / plan; Check state; Over planned | reference.xlsx conditional formatting: Review!C12:C15, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54 |
| State text / 0 | conditional-text | #972F2A | 0; Actual missing; Invalid actual; Duplicate ID; Missing ID; Check task / plan; Check state; Over planned | reference.xlsx conditional formatting: Review!C12:C15, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54, Task log!G5:G54 |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 17.44:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 17.44:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 14.80:1 | Normal-size text contrast threshold met |
| Reading ink / Attention Surface | 15.52:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 14.80:1 | Normal-size text contrast threshold met |
| Identity emphasis / Attention Surface | 15.52:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Project Health Instrument Desk: native colors](references/project-health-instrument-desk/COLORS.md)
