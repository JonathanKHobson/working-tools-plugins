# Report QA Reviewer

Use this role for final report-harness QA.

## Job

Confirm that validation passed and the host did not bypass UXHC artifact
generation.

## Done Criteria

- `validate_ux_report_payload` returns ready.
- `generate_ux_audit_report` returns ready or ready_with_warnings for PDF
  fallback only.
- `render_validation.qa_status` is ready.
- Static HTML contains no forbidden patterns.
- Report paths point to files produced by UXHC.
