# Work in View · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading paper | background | #F7EDD7 | Native PPTX richSlides: masthead_work shapes blue; f1 text ink; accent shapes red; slide paper cream. |
| Editorial ink | text | #211F1B | Native PPTX richSlides: masthead_work shapes blue; f1 text ink; accent shapes red; slide paper cream. |
| Constructed blue | primary | #203B80 | Native PPTX richSlides: masthead_work shapes blue; f1 text ink; accent shapes red; slide paper cream. |
| Proof red | accent | #C14137 | Native PPTX richSlides: masthead_work shapes blue; f1 text ink; accent shapes red; slide paper cream. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading paper / Editorial ink | 14.14:1 | Normal-size text contrast threshold met |
| Reading paper / Constructed blue | 9.03:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Creative Practice Zine: native colors](references/creative-practice-zine/COLORS.md)
