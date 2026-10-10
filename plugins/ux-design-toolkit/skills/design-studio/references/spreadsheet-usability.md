# Human-facing workbook design

Use with the primary Spreadsheets provider when people must operate or interpret a workbook. Raw machine tables and archives do not need a dashboard by default. Preserve formulas, data structure and traceability; add a user-facing view when a backend table must also serve recurring human work.

Start with the user's recurring decision and first useful view. Keep ordinary inputs/results close together while leaving calculations and source evidence reachable. Distinguish editable cells from computed cells through labels, structure and protection, not color alone. Show units, dates, active scenario, required inputs and source/assumption status where they affect interpretation.

Use validation and safe defaults to prevent plausible mistakes. Explain recovery from blanks, invalid dates, impossible values, stale data and conflicting assumptions. Group inputs by the user's task rather than formula dependencies. Avoid unnecessary merged cells, dense borders and hidden critical instructions. On narrow screens put the essential result and controls within a usable path.

For decision models expose the factors that can reverse the decision, uncertainty/ranges, downside and available buffers. Keep distinct capital needs and materially different regimes as explicit scenarios. This is presentation guidance; analytical, financial or legal judgments require their actual domain evidence.

Verify a realistic common task, an invalid-input case, a return-after-time-away case and traceability from result to assumption/source. Check keyboard/read order and meaning without color. The spreadsheet provider verifies calculations and file integrity; visual simplicity does not establish mathematical correctness. Deliver only the checks actually performed.
