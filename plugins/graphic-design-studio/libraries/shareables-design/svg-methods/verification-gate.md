## Verification Gate

No Shareables MCP integration happens until this gate is complete.

1. Technical validation
   - SVG parses as XML.
   - Root element is SVG.
   - `viewBox` exists.
   - Centered alignment contract exists for generated sample icons.
   - A `data-art` group exists so browser QA can check art bounding boxes.
   - IDs are unique and safe.
   - No `image`, `script`, external href, private local path, or unsafe URL.
   - Accessibility role is declared and matched by markup.
   - Every used color is in the approved four-color palette.
   - Shape count stays within the tier budget.
   - Every sample has a concept ledger.

2. Visual validation
   - Gallery renders samples at display size plus 24, 32, 48, and 96.
   - Samples are readable at 32px or have a documented reason they are display-only.
   - Motifs read as one-color silhouettes at 24px.
   - Dark/light compatibility is checked where the style source requires it.
   - Similar samples differ by anatomy, not only color.
   - Major objects are visibly centered; off-center elements are rejected unless the asymmetry is intentional and clearly described.
   - Display-size details are pruned at 24px and 32px when they would become noise.

3. Style-source validation
   - Each style source has a utility control set.
   - Each style source has a personality set.
   - The personality samples express the style source without impersonating third-party brands or copying external assets.

4. AI failure review
   - Log common mistakes found during generation or repair.
   - Update this recipe when a recurring failure appears.

5. Kyle review stop point
   - Human review is required before promoting samples into resources, registry records, prompt recipes, or reusable production assets.

6. Pre-output self-check
   - Does every motif read at 24px?
   - Are all visible elements inside the viewBox safe zone?
   - Is every color in the style source palette?
   - Does every primary group measure centered in browser QA?
   - Does the result look deliberate, or merely technically valid?
   - If any answer fails, do not output the gallery.
