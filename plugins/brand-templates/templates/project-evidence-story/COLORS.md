# Handoff Notes · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FAF7F0 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #1E2933 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #754838 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #EFE9E2 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary Text | secondary-text | #685D55 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Title brown | display-ink | #302924 | Native ppt/slides/slide1.xml Making volunteer handoffs visible. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Contribution header | header | #634338 | Native ppt/slides/slide3.xml Contributor table tcPr. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Header labels | reverse-text | #FFFFFF | Native ppt/slides/slide3.xml Contributor run color. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 13.82:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 7.16:1 | Normal-size text contrast threshold met |
| Reading ground / Secondary Text | 5.97:1 | Normal-size text contrast threshold met |
| Reading ground / Title brown | 13.37:1 | Normal-size text contrast threshold met |
| Reading ground / Contribution header | 8.21:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 12.27:1 | Normal-size text contrast threshold met |
| Reading ink / Header labels | 14.79:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 6.36:1 | Normal-size text contrast threshold met |
| Identity emphasis / Header labels | 7.66:1 | Normal-size text contrast threshold met |
| Supporting field / Secondary Text | 5.30:1 | Normal-size text contrast threshold met |
| Supporting field / Title brown | 11.87:1 | Normal-size text contrast threshold met |
| Supporting field / Contribution header | 7.29:1 | Normal-size text contrast threshold met |
| Secondary Text / Header labels | 6.39:1 | Normal-size text contrast threshold met |
| Title brown / Header labels | 14.30:1 | Normal-size text contrast threshold met |
| Contribution header / Header labels | 8.78:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Project Evidence Story: native colors](references/project-evidence-story/COLORS.md)
