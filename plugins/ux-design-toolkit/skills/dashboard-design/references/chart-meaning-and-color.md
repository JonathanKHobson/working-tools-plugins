# Chart meaning and color

Choose the representation for the comparison. These defaults are adjustable with a stated reason, not a ban on expressive design.

| Task | Starting form | Meaning to preserve |
| --- | --- | --- |
| Category comparison | Bar or dot | Natural order where meaningful; zero baseline for magnitude bars; exact units |
| Time change | Line; columns for period totals | Chronology, elapsed spacing, missing observations and partial periods |
| Part of a whole | Stacked/100% bar; simple pie for few clear parts | Additive parts and denominator; overlapping groups are not a partition |
| Distribution | Histogram, box, density or individual points | Bin/kernel choices, sample size and valid summaries |
| Relationship | Scatter | Units and observed association; avoid causal claims without evidence |
| Many comparable groups | Small multiples | Comparable domains and stable encoding; label justified scale differences |
| Deviation from target | Dot/bullet/variance | Target source, zero/reference, whether more is favorable |
| Exact lookup | Table, optionally in-cell marks | Exact values, accessible headers, units and sorting |

Gaps stay gaps unless an explicit, defensible interpolation is labeled. Missing, zero, suppressed and not-applicable values need distinct treatment. Observed and forecast values need a visible boundary. Validate smoothing, stacked totals, normalized shares, negative values and domain clipping in the actual renderer. Material uncertainty belongs beside the estimate; explain interval type and method. Never invent bounds or reuse an aggregate interval for filtered groups.

## Color is a data contract

Keep separate tokens/maps for surfaces/text, categorical identity, magnitude, meaningful deviation, selection and status. Use a sequential scale for ordered amount. Use a diverging scale when the midpoint has a defensible interpretation (zero change, target or other declared reference), not merely because a palette is attractive. A dataset median is not automatically a neutral or desirable value. Missing data remains outside the numeric scale.

Map category ID to color, not visible array index; sorting or filtering must not swap identities. Equal peers may require equal emphasis. Focal-accent-plus-neutral is appropriate when there is a real focal question, not as a universal style. Reduce crowded categories through faceting or a better encoding rather than repeating confusable hues or silently merging nonadditive data.

Use palette databases as candidates. Review the actual mark size, background, adjacency, opacity, selected state and light/dark theme. Add direct labels, markers, line styles, patterns or text so meaning survives without hue. A redundant accessible table does not excuse an unreadable primary view. Imported brand colors may need an accessible chart variant; explain consequential substitutions.

For WCAG AA targets, normal text generally needs 4.5:1 contrast and large text 3:1. Essential graphical objects and control states covered by non-text contrast need 3:1 against adjacent colors, subject to that criterion's scope and exceptions. This is not a demand for 3:1 between every pair in a sequential ramp. Check actual required boundaries or add separating strokes/labels. Color-vision simulation and grayscale inspection add evidence but do not establish full accessibility conformance.

Sources: [ONS axes](https://service-manual.ons.gov.uk/data-visualisation/guidance/axes-and-gridlines), [uncertainty](https://service-manual.ons.gov.uk/data-visualisation/guidance/showing-uncertainty-in-charts), [chart color](https://service-manual.ons.gov.uk/data-visualisation/colours/using-colours-in-charts), [Carbon palettes](https://carbondesignsystem.com/data-visualization/color-palettes/), [W3C text contrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). These are original concise rules, not copied source examples or a licensed palette bundle.
