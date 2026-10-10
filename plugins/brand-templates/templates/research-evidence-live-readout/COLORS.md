# Atlas Live Evidence · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FCFCF8 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #1E2933 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #13685F | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary Text | secondary-text | #475861 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #F2F4F5 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Evidence header | header | #233642 | Native ppt/slides/slide4.xml Observed in the fixture table tcPr. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Header labels | reverse-text | #FFFFFF | Native ppt/slides/slide4.xml Observed in the fixture run color. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 14.38:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 6.44:1 | Normal-size text contrast threshold met |
| Reading ground / Secondary Text | 7.20:1 | Normal-size text contrast threshold met |
| Reading ground / Evidence header | 12.17:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 13.40:1 | Normal-size text contrast threshold met |
| Reading ink / Header labels | 14.79:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 6.00:1 | Normal-size text contrast threshold met |
| Identity emphasis / Header labels | 6.62:1 | Normal-size text contrast threshold met |
| Secondary Text / Supporting field | 6.71:1 | Normal-size text contrast threshold met |
| Secondary Text / Header labels | 7.40:1 | Normal-size text contrast threshold met |
| Supporting field / Evidence header | 11.34:1 | Normal-size text contrast threshold met |
| Evidence header / Header labels | 12.52:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Research Evidence Live Readout: native colors](references/research-evidence-live-readout/COLORS.md)
