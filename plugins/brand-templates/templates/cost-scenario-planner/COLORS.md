# Case & Cost · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Ledger white | background | #FFFFFF | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |
| Ledger ink | text | #211C19 | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |
| Section umber | primary | #5A2D22 | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |
| Calculated row | surface | #F4EBE6 | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |
| Editable field | input-surface | #FFF2CC | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |
| Input blue | input-text | #0000CC | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |
| Selection green | status | #006100 | Native workbook usedStyles and design/COLORS.md: exact role confirmed by cell references. |

## Functional states from conditional formatting

These colors appear only when the native workbook rule is met; they are separate from the base identity palette. Preserve the condition and a readable text label.

| Name | Role | sRGB hex | Condition | Source |
| --- | --- | --- | --- | --- |
| State surface / n.a. | conditional-fill | #FFC7CE | n.a.; Inputs complete | reference.xlsx conditional formatting: Cost planner!D9, Cost planner!D13, Cost planner!D17, Cost planner!D21, Cost planner!D25, Cost planner!F18, Cost planner!G16 |
| State text / n.a. | conditional-text | #9C0006 | n.a.; Inputs complete | reference.xlsx conditional formatting: Cost planner!D9, Cost planner!D13, Cost planner!D17, Cost planner!D21, Cost planner!D25, Cost planner!F18, Cost planner!G16 |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Ledger white / Ledger ink | 16.87:1 | Normal-size text contrast threshold met |
| Ledger white / Section umber | 11.46:1 | Normal-size text contrast threshold met |
| Ledger white / Input blue | 11.22:1 | Normal-size text contrast threshold met |
| Ledger white / Selection green | 7.75:1 | Normal-size text contrast threshold met |
| Ledger ink / Calculated row | 14.36:1 | Normal-size text contrast threshold met |
| Ledger ink / Editable field | 15.12:1 | Normal-size text contrast threshold met |
| Section umber / Calculated row | 9.75:1 | Normal-size text contrast threshold met |
| Section umber / Editable field | 10.27:1 | Normal-size text contrast threshold met |
| Calculated row / Input blue | 9.55:1 | Normal-size text contrast threshold met |
| Calculated row / Selection green | 6.60:1 | Normal-size text contrast threshold met |
| Editable field / Input blue | 10.06:1 | Normal-size text contrast threshold met |
| Editable field / Selection green | 6.95:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Cost Scenario Planner: native colors](references/cost-scenario-planner/COLORS.md)
