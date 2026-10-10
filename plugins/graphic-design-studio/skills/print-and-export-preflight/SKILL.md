---
name: print-and-export-preflight
description: Prepare and inspect final poster, flyer, and ad exports, including PDF page size, native image resolution, text, QR destinations, file size, and print requirements. Use before delivery or when an export looks wrong; mechanical checks complement rendered visual review.
---

# Print and export preflight

Use the job's actual dimensions, viewing context, printer or platform requirements, and delivery limit. Distinguish an editable master, screen proof, lightweight email file, and commercial-print file. Do not rename a proof “press ready” because it is a PDF.

For print, confirm trim dimensions, bleed if needed, safe area, frame overlap if applicable, font embedding, effective image resolution, color profile/output intent, and requested PDF standard. The printer's specification takes precedence over generic presets. A PDF/X preset alone does not certify a file. Do not blindly convert all content to an arbitrary CMYK profile or add crop marks a shop does not want.

Evaluate **effective PPI** from native pixels divided by placed inches. Exporting at 300 dpi or changing resolution metadata does not create missing detail. Upsampling may change pixel counts without restoring source detail; inspect the original and final image. Choose acceptable resolution for the actual asset, output method, and viewing distance rather than enforcing one number everywhere.

Keep exact type and QR construction deterministic when reliable editing and machine reading matter. For a standard QR Code, preserve at least four clear modules around every side. Select size from payload density, print capability, scan conditions, and available space. Inspect and decode the final export, compare the decoded URL with the intended destination, and separately confirm that destination serves the intended action. A code decoding in software is not a physical phone scan through frame glass.

## Optional PDF inspection helper

With Python/PyMuPDF available, run the bundled [pdf_preflight.py](scripts/pdf_preflight.py). QR checks additionally use Pillow and zxing-cpp. Use the environment's existing runtime; the script does not install dependencies.

```bash
python3 scripts/pdf_preflight.py poster.pdf --size-in 11 17 --max-mb 20 \
  --require-text "Saturday" --qr "https://example.org/event" \
  --render-dir /absolute/review/path --report /absolute/review/path/checks.json
```

Run from this skill folder or resolve the script relative to it. `--min-type-pt` and `--min-ppi` are optional job-specific thresholds. Sizes and thresholds are examples, not defaults for every graphic. Exit 0 means requested mechanical checks passed; 1 means a failed check; 2 means a requested check could not be performed. Read `limitations` even on exit 0.

The helper checks page dimensions, text bounds, requested text, optional size/type/PPI limits, and optionally QR payloads from rendered pages. It cannot certify color, PDF/X compliance, font licensing, source authenticity, visual balance, physical scanning, approval, or print-shop acceptance.

Reopen actual final bytes after compression or packaging. Inspect whole pages and changed details using [graphic-design-review](../graphic-design-review/SKILL.md). Verify delivered filenames, counts, and links; state exactly what was inspected and any unperformed physical or printer checks.

For a delivered design/template bundle, check that `DESIGN.md` is present, linked from its template `SKILL.md` when applicable, and that all supporting design files and declared source assets resolve after extraction. Match the specification to the actual retained source and output edition; documentation presence alone is not a visual fidelity pass.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Graphic Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
