## SVG Construction Rules

- Every standalone SVG has `xmlns` and `viewBox`.
- Prefer `viewBox="0 0 100 100"` for icon and personality samples unless a specific format needs otherwise.
- Use a visible 100x100 center contract: major frames, faces, and icon bodies should balance around x=50 and y=50 unless the brief explicitly calls for asymmetry.
- Keep all reusable icon anatomy inside a safe zone around x=14..86 and y=14..86, with personality marks allowed to use y=88..94 only for a shadow.
- Keep a stable family anatomy: frame or base, primary shape, motif slot, detail marks, optional highlight.
- Let the motif carry meaning; do not randomize every point.
- Use simple primitives before complex paths.
- Use 1-2 accent colors plus neutral structure.
- Avoid external images, remote fonts, scripts, unsafe URLs, filters that hide structure, and pasted third-party marks.
- Keep IDs unique and stable.
- Escape user-provided text before insertion.
- Avoid stray decorative dots, unexplained marks, weak translucent rings, and off-center plates unless they have a semantic purpose that remains readable at 32px.
- Anchor every primary art group with an explicit center such as `transform="translate(50 50)"`; do not rely on scattered absolute coordinates for primary composition.
- No generated color may appear unless it is one of the style source's four approved palette colors or a documented opacity of one of those colors.
- Do geometry deliberately. For example, a warning triangle with points `(50,19)`, `(85,79)`, and `(15,79)` has an x-centroid of `50`; an exclamation stem with `x=46.5` and `width=7` spans `46.5..53.5`, centered on `50`.

For future avatar SVGs, use the reference character anatomy before inventing symbols:

```text
shadow
-> soft body silhouette
-> highlight
-> semantic motif slot
-> eyes
-> pupils
-> glints
-> cheeks
-> smile or expression
```

For the next sample run, do not generate avatars yet. Generate mark and motif samples first. Avatar work is a later tier after simple marks pass.
