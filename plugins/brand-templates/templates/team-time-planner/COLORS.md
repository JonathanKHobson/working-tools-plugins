# Time Together · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #243746 | used style 22 font color |
| Input Surface | input-surface | #FFF2CC | used style 16 fill at Availability!A5, Availability!A6 |
| Surface | surface | #EBE4EE | used style 21 fill at Weekly plan!B7, Weekly plan!C7 |

## Functional states from conditional formatting

These colors appear only when the native workbook rule is met; they are separate from the base identity palette. Preserve the condition and a readable text label.

| Name | Role | sRGB hex | Condition | Source |
| --- | --- | --- | --- | --- |
| State surface / Over | conditional-fill | #FCE5E1 | Over; Unassigned | reference.xlsx conditional formatting: Weekly plan!B10:F10, Weekly plan!B14:F14, Weekly plan!B18:F18, Tasks!F5:F15 |
| State text / Over | conditional-text | #8B251A | Over; Unassigned | reference.xlsx conditional formatting: Weekly plan!B10:F10, Weekly plan!B14:F14, Weekly plan!B18:F18, Tasks!F5:F15 |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 12.28:1 | Normal-size text contrast threshold met |
| Text / Input Surface | 11.01:1 | Normal-size text contrast threshold met |
| Text / Surface | 9.86:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Team Time Planner: native colors](references/team-time-planner/COLORS.md)
