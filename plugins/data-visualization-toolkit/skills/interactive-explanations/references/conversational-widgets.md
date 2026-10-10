# Visualization widgets in conversations

Use when an explanation or data explorer includes controls whose meaning must survive a return to chat. This is maintained guidance, not a replacement for the full Visualize rendering/export procedure. General widget UX belongs to UX Design Studio; MCP transport and host integration belong to Build MCP Apps. A generated visual, standalone HTML and MCP App have different capabilities.

## Choose the interaction from the analytical question

Use direct controls for repeated, precise adjustments: filtering a cohort, comparing alternatives, exploring an assumption or inspecting evidence. Keep a clear static answer when interaction adds no useful decision. State which quantities are observations, estimates or hypothetical inputs. A simulation control must not silently alter the observed dataset or make a causal claim the data cannot support.

DynaVis (CHI 2024, 24 participants) found preference for a hybrid language-plus-widget visualization editing interface over its language-only condition. That supports trying persistent controls for repeated edits in similar tasks; it does not establish universal superiority for all widgets or validate this toolkit. [Primary study](https://www.microsoft.com/en-us/research/publication/dynavis-dynamically-synthesized-ui-widgets-for-visualization-editing/), checked 2026-10-06.

## Preserve meaning across the view and conversation

Before implementation, define the source dataset/revision, metric and units, transformations/aggregation, filters, selected stable IDs, sort/order, and hypothetical parameter values that determine the visible answer. State which are local exploration and which are saved. Keep a readable summary of active filters and assumptions near the result, including zero-result and unknown-data states.

Publish the settled semantic snapshot only through the actual supported provider. A local control change does not prove the assistant saw it. When the provider cannot share state, offer an explicit summary/copy action for the next turn. For MCP-backed views, follow Build MCP Apps' context/message capability checks; a context update and a request for another response are different operations. Include the current snapshot in a deliberate follow-up when synchronization cannot be established. Avoid sending private raw rows or full datasets merely to describe a chart selection.

Use stable IDs, not only row positions: “the second bar” changes meaning after sorting. Keep series identity, color meaning and scale changes clear. Preserve valid selection on refresh; explain when a selected item disappears. Do not animate continuous reordering beneath a pointer or replay a decorative entrance when an old chat view remounts.

## Access and motion

Provide keyboard controls, persistent labels/units, visible focus, and a non-drag adjustment path. Hover details need focus/touch equivalents. Maintain a text/table route to task-critical values. A chart may legitimately need two-dimensional exploration; surrounding labels, controls and explanations should still reflow. Do not force a library-carousel layout onto a chart or map.

Motion should explain correspondence between known states; preserve the same result and explanation with reduced motion. Provide pause or controlled refresh when automatic updates compete with reading. Coordinate meaningful status announcements with the host, avoiding an announcement for every frame or slider increment. Exact accessibility criteria and exceptions remain in the owning verification workflow; project touch-target defaults are not universal WCAG thresholds.

## Verify the whole question-to-answer path

Use known values to test a default state, an extreme parameter, reset, missing data and zero results. Check that filters update the chart, summary, export and shared context consistently. Exercise a rapid adjustment followed immediately by a chat question, sort then refer to a selected object, reopen/remount, denied context capability, narrow layout, enlarged text and reduced motion. Test keyboard and assistive technology where available; label untested paths.

Compare a proposed richer widget with a clear static chart or text baseline for the same task. Measure correct interpretation and recovery, not only preference or visual polish. Do not claim learning gains, usability gains, or model understanding from a screenshot or protocol acknowledgment.

Sources and limits: research package *Conversational MCP Widget Design*, 2026-10-06, UX27 and platform/state synthesis; [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview), [App context API](https://apps.extensions.modelcontextprotocol.io/api/classes/app.App.html#updateModelContext). Protocol support must be checked against the installed version and host; these are conceptual invariants, not copied API code.
