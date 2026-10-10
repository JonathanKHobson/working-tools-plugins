# Date-binned activity calendars

Use an activity calendar when the question is **which local dates had how many qualifying records**, not when the reader needs a timed appointment schedule. Use the complete Visualize method for delivery and the bundled `viz-calendar` only for the latter. The [standalone example](../examples/activity-calendar.html) is an original, offline 14-day fixture.

1. Define the counted event, source record ID, timestamp field and deduplication rule. Declare whether a cell counts events, distinct days, people or another unit. A count is not a duration or a productivity score.
2. Convert each event timestamp into the named timezone before deriving the calendar date. State the date range and whether its endpoints are inclusive. The example counts distinct fixture record IDs by their `started_at` date in `America/Phoenix`; a UTC timestamp near midnight demonstrates why conversion matters.
3. Maintain a separate per-day coverage record. `0` means the source was checked for that day and no qualifying records were found. Missing means the source was not checked or was unavailable; never silently coerce it to zero. If partial coverage exists, label it and avoid pretending the count is complete.
4. Put the number or `—` in each cell, with a redundant legend and accessible day label. Expose exact contributing IDs on selection. Use a bounded palette and do not imply that a darker cell means better performance.
5. Reconcile displayed counts to the fixture/source, inspect narrow and wide renders, and exercise keyboard selection. Report whether source completeness was independently verified; a synthetic example only proves the aggregation and interaction pattern.
