# Report Tokens

Tokens are the stable names behind the HTML renderer. Keep generated reports on
these tokens instead of ad hoc colors or spacing.

| Token | Value | Use |
| --- | --- | --- |
| `--uxhc-green` | `#0d6e6e` | Header, section accent, primary badges. |
| `--ink` | `#24292e` | Main text and footer background. |
| `--muted` | `#6a737d` | Metadata, helper text, secondary labels. |
| `--line` | `#e1e4e8` | Card borders and table rules. |
| `--bg` | `#f5f6fa` | Page background. |
| `--panel` | `#ffffff` | Card background. |
| `--danger` | `#cb2431` | Critical severity. |
| `--major` | `#c96a00` | Major severity. |
| `--medium` | `#b8860b` | Moderate severity and warning grades. |
| `--success` | `#22863a` | Strong scores and pass states. |

The renderer may expose these as CSS variables, but content authors should not
choose new colors.
