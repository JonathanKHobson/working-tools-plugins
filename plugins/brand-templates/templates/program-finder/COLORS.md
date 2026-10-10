# The Programme Finder · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #F4F5EF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #16383A | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #316560 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Accent | accent | #AD4B16 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #E2ECE7 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Warning Surface | warning-surface | #FFF2DF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 11.53:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 6.06:1 | Normal-size text contrast threshold met |
| Reading ground / Accent | 5.05:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 10.47:1 | Normal-size text contrast threshold met |
| Reading ink / Warning Surface | 11.45:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 5.50:1 | Normal-size text contrast threshold met |
| Identity emphasis / Warning Surface | 6.02:1 | Normal-size text contrast threshold met |
| Accent / Supporting field | 4.58:1 | Normal-size text contrast threshold met |
| Accent / Warning Surface | 5.01:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Program Finder: native colors](references/program-finder/COLORS.md)
