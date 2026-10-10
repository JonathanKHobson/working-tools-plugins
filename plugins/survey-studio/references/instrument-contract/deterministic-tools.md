## Deterministic tools

Run commands from the skill directory.

```bash
# Validate canonical structure while loading
python scripts/survey_io.py  # library module; use through the commands below

# Methodological and structural audit
python scripts/survey_lint.py examples/product-experience-pulse.yaml --include-info

# Estimate respondent burden and identify hotspots
python scripts/estimate_burden.py examples/product-experience-pulse.yaml

# Generate a coded analysis dictionary
python scripts/generate_codebook.py examples/product-experience-pulse.yaml output/codebook.csv --format csv

# Export one synchronized instrument
python scripts/export_survey.py examples/product-experience-pulse.yaml output/survey.html --format html
python scripts/export_survey.py examples/product-experience-pulse.yaml output/survey.docx --format docx
python scripts/export_survey.py examples/product-experience-pulse.yaml output/survey.pdf --format pdf

# Create and validate Qualtrics TXT
python scripts/export_survey.py examples/product-experience-pulse.yaml output/qualtrics.txt --format qualtrics-advanced
python scripts/validate_qualtrics_txt.py output/qualtrics.txt

# Validate the complete installed skill
python scripts/validate_skill.py .
bash scripts/qa_all.sh
```

Use `--help` for flags. Treat the burden estimate as a planning heuristic, not a promise.
