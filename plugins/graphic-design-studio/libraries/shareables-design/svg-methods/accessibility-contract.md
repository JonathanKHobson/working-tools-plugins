## Accessibility Contract

Classify every SVG before rendering:

| Role | Required handling |
| --- | --- |
| Decorative | `aria-hidden="true"` and no meaningful title dependency. |
| Meaningful | `role="img"`, `aria-labelledby`, plus `title` and `desc`. |
| Interactive | Keyboard reachable control, visible focus, readable label, and pointer target at least 24px or equivalent spacing. |
| Data visualization | Text summary and exact-value fallback when precision matters. |

Meaningful SVGs in the review gallery should use:

```html
<svg role="img" aria-labelledby="sample-title sample-desc" viewBox="0 0 100 100">
  <title id="sample-title">Review badge</title>
  <desc id="sample-desc">A rounded badge with a check mark and annotation line.</desc>
  ...
</svg>
```
