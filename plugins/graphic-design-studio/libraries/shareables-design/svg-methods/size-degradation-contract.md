## Size-Degradation Contract

Each sample must define what survives at small sizes.

| Size | Required behavior |
| --- | --- |
| `24px` | Structural silhouette only. No text lines, glints, texture, or subtle decorative marks unless they remain unmistakable. |
| `32px` | Structural silhouette plus at most one supporting detail. |
| `48px` | Most semantic detail can appear if contrast holds. |
| Display size | Ornament may appear, but only if it has a named role and can be dropped without breaking the concept. |

Small-size variants should be pruned versions, not blind scaling of every display-size detail.
