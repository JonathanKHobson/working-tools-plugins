# DOCX Export

## Best for

Stakeholder review, tracked edits/comments, ethics or governance submissions, and editable print-oriented questionnaires.

## Not sufficient for

Platform execution or guaranteed layout across Word versions. A DOCX exported from a survey platform is not necessarily re-importable.

Generate:

```bash
python scripts/export_survey.py survey.yaml survey.docx --format docx
python scripts/export_survey.py survey.yaml respondent.docx --format docx --respondent-only
```

## Structure

Use real heading styles, list styles, tables only when necessary, meaningful alt text for images, page breaks around major sections, header/footer versioning, and researcher notes clearly distinguished from respondent copy. Do not simulate structure with tabs and spaces.

## QA

Open in Word and at least one alternate reader when important; render to PDF/images; inspect styles, page breaks, orphaned options, table widths, fonts, hyperlinks, comments/tracked changes, and accessibility checker results. Verify the ZIP/OOXML package is intact. Reconcile accepted edits back into canonical JSON/YAML before regenerating other formats.
