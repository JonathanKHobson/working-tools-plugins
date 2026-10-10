# Example: Single-File vs Expandable Web Deliverable

## User asks

> Make me a single HTML file I can send to someone.

Use single file:

```text
prototype.html
```

Keep sections clear:

```html
<style>
/* tokens */
/* layout */
/* components */
</style>

<script>
/* data */
/* behavior */
/* init */
</script>
```

## User asks

> Start a website for my game studio. It may eventually have game pages, devlogs, and a press kit.

Use expandable structure:

```text
studio-site/
  README.md
  index.html
  src/
    main.js
    pages/
    components/
    styles/
    assets/
  docs/
    project-map.md
```

Reason: future pages, reusable components, assets, and content updates need obvious homes.
