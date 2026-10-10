# Format Editor Lens

Use for headings, lists, emphasis, tables, punctuation style, and destination syntax.

## Pass

1. Identify the destination: Markdown, MediaWiki, HTML, rich text, plain text, UI string, manuscript, or another system.
2. Validate heading case and hierarchy against the house style.
3. Remove mechanical bold, decorative emoji, repeated thematic breaks, and label-colon lists that do not aid scanning.
4. Convert tiny tables to prose and dense prose to tables only when repeated fields justify comparison.
5. Audit em-dash density and quote consistency without imposing a universal ban.
6. Search for mixed markup, fenced wrappers, literal bullet characters, broken links, and internal tool artifacts.
7. Validate destination objects such as templates, categories, component names, fields, and parameters.

## Output

Return `destination rule`, `violation`, `repair`, and `validation method`. Never change syntax inside code or data without checking its grammar.
