# Three Small Investigations · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Response blue | primary | #183C52 | Native reference.docx word/styles.xml: style F24Response, style F24DialogueLast, style F24DialogueFirst; border. |
| Guide amber | surface | #FFF5D8 | Native reference.docx word/styles.xml: style F24DialogueLast, style F24DialogueFirst; shading fill. |
| Object paper | motif-ground | #FFF8E6 | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |
| Object gold | accent | #E6B944 | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Response blue | 11.62:1 | Normal-size text contrast threshold met |
| Text / Guide amber | 19.30:1 | Normal-size text contrast threshold met |
| Text / Object paper | 19.82:1 | Normal-size text contrast threshold met |
| Text / Object gold | 11.39:1 | Normal-size text contrast threshold met |
| Response blue / Guide amber | 10.68:1 | Normal-size text contrast threshold met |
| Response blue / Object paper | 10.97:1 | Normal-size text contrast threshold met |
| Response blue / Object gold | 6.30:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Museum Learning Trail: native colors](references/museum-learning-trail/COLORS.md)
