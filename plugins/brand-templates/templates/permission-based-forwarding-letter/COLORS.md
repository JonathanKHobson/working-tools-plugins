# With Permission · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #171B20 | used style Normal explicit text color |
| Scope slate | primary | #354653 | Native reference.docx word/styles.xml: style PFScope; text. |
| Notice slate | secondary-text | #47535D | Native reference.docx word/styles.xml: style PFNotice; text. |
| Title ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title, style PFSubject; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 17.30:1 | Normal-size text contrast threshold met |
| Background / Scope slate | 9.76:1 | Normal-size text contrast threshold met |
| Background / Notice slate | 7.89:1 | Normal-size text contrast threshold met |
| Background / Title ink | 21.00:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Permission Based Forwarding Letter: native colors](references/permission-based-forwarding-letter/COLORS.md)
