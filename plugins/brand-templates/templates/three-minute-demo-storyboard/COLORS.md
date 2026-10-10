# Three Minute Story · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #121417 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #F5F0E6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Timing Accent | timing-accent | #F6BD60 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Structural rule | rule | #C8C3B9 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 16.24:1 | Normal-size text contrast threshold met |
| Reading ground / Timing Accent | 10.87:1 | Normal-size text contrast threshold met |
| Reading ground / Structural rule | 10.51:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Three Minute Demo Storyboard: native colors](references/three-minute-demo-storyboard/COLORS.md)
