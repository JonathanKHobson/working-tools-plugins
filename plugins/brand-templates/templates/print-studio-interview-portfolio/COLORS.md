# Print Studio Notes · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #F1E9D8 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #24231F | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #15478C | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Accent | accent | #B92D19 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Ornamental accent | ornament | #EDAD39 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reversed labels | reverse-text | #FFFFFF | Native Native reference.pptx explicit run white; secondary reversed labels. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 13.02:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 7.52:1 | Normal-size text contrast threshold met |
| Reading ground / Accent | 5.04:1 | Normal-size text contrast threshold met |
| Reading ink / Ornamental accent | 7.97:1 | Normal-size text contrast threshold met |
| Reading ink / Reversed labels | 15.73:1 | Normal-size text contrast threshold met |
| Identity emphasis / Ornamental accent | 4.60:1 | Normal-size text contrast threshold met |
| Identity emphasis / Reversed labels | 9.08:1 | Normal-size text contrast threshold met |
| Accent / Reversed labels | 6.08:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Print Studio Interview Portfolio: native colors](references/print-studio-interview-portfolio/COLORS.md)
