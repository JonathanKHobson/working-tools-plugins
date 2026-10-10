# Programme Desk · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #152B3A | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #1C457A | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #EFF3F4 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Editable field | input-surface | #FFF1CD | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary Text | secondary-text | #475B65 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |

## Functional states from conditional formatting

These colors appear only when the native workbook rule is met; they are separate from the base identity palette. Preserve the condition and a readable text label.

| Name | Role | sRGB hex | Condition | Source |
| --- | --- | --- | --- | --- |
| State surface / AND(D9<>"",ISERROR(SEARCH("!",D9))) | conditional-fill | #DBE9F1 | AND(D9<>"",ISERROR(SEARCH("!",D9))) | reference.xlsx conditional formatting: Timetable!D9:D20 |
| State text / AND(D9<>"",ISERROR(SEARCH("!",D9))) | conditional-text | #152B3A | AND(D9<>"",ISERROR(SEARCH("!",D9))); AND(E9<>"",ISERROR(SEARCH("!",E9))); AND(F9<>"",ISERROR(SEARCH("!",F9))); Outside | reference.xlsx conditional formatting: Timetable!D9:D20, Timetable!E9:E20, Timetable!F9:F20, Sessions!J10:J21 |
| State surface / ! | conditional-fill | #FADBDD | !; 0 | reference.xlsx conditional formatting: Timetable!D9:D20, Timetable!E9:E20, Timetable!F9:F20, Sessions!I10:I21 |
| State text / ! | conditional-text | #A4262C | !; AND($G10<>"",$G10<>"Valid"); 0; Ready | reference.xlsx conditional formatting: Timetable!D9:D20, Timetable!E9:E20, Timetable!F9:F20, Sessions!G10:G21, Sessions!I10:I21, Sessions!B7 |
| State surface / AND(E9<>"",ISERROR(SEARCH("!",E9))) | conditional-fill | #E4EBDD | AND(E9<>"",ISERROR(SEARCH("!",E9))) | reference.xlsx conditional formatting: Timetable!E9:E20 |
| State surface / AND(F9<>"",ISERROR(SEARCH("!",F9))) | conditional-fill | #EEE2DB | AND(F9<>"",ISERROR(SEARCH("!",F9))) | reference.xlsx conditional formatting: Timetable!F9:F20 |
| State surface / AND($G10<>"",$G10<>"Valid") | conditional-fill | #FDE4D5 | AND($G10<>"",$G10<>"Valid"); Ready | reference.xlsx conditional formatting: Sessions!G10:G21, Sessions!B7 |
| State surface / Outside | conditional-fill | #F6CF3E | Outside | reference.xlsx conditional formatting: Sessions!J10:J21 |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 14.60:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 9.63:1 | Normal-size text contrast threshold met |
| Reading ground / Secondary Text | 7.11:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 13.07:1 | Normal-size text contrast threshold met |
| Reading ink / Editable field | 13.01:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 8.62:1 | Normal-size text contrast threshold met |
| Identity emphasis / Editable field | 8.58:1 | Normal-size text contrast threshold met |
| Supporting field / Secondary Text | 6.37:1 | Normal-size text contrast threshold met |
| Editable field / Secondary Text | 6.34:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Festival Schedule Planner: native colors](references/festival-schedule-planner/COLORS.md)
