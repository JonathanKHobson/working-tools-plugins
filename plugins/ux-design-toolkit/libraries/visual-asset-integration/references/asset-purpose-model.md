# Asset Purpose Model

Use purpose before style. The same image can be acceptable in one role and
misleading in another.

## Purpose Types

| Purpose | Job | Best Sources | Main Risk |
| --- | --- | --- | --- |
| `evidence` | Proves real work, behavior, people, artifact, gameplay, or outcome | screenshots, photos, exports, PDFs, videos, source files | generated or staged visuals pretending to prove reality |
| `identity` | Makes the brand or person recognizable | logo, avatar, portrait, favicon, social card | inconsistency, over-detail at small sizes |
| `interface` | Helps a user control or understand the UI | system icons, generated icons, state art, diagrams | decorative icons replacing familiar controls |
| `environment` | Establishes place, mood, world, or product context | textures, backgrounds, scenes, maps | contrast failure, visual clutter |
| `editorial` | Explains or supports an argument | charts, annotated screenshots, diagrams, article images | image decorates but does not clarify |
| `atmosphere` | Adds flavor and emotional texture | generated art, side flourishes, decorative scenes | mistaken for proof, overuse |

## Decision Rule

For each asset, ask:

1. What does this asset help the reader or user do?
2. What claim does it sit near?
3. Could a reasonable viewer think it proves something real?
4. If yes, is the source real enough for that role?
5. If no, should it be moved to atmosphere or environment?

## Promotion And Demotion

- Promote to `evidence` only when the source supports the adjacent claim.
- Demote to `atmosphere` when a visual is attractive but not source-backed.
- Use `editorial` for explanatory visuals that are not proof but improve
  comprehension.
- Use `identity` sparingly and consistently; do not redesign identity per
  section unless the product intentionally has sub-brands.
