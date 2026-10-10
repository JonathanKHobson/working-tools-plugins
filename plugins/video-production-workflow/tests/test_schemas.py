import json
from pathlib import Path
import jsonschema


def test_example_and_source_registry_validate_against_schemas() -> None:
    root=Path(__file__).resolve().parents[1]
    project=json.loads((root/'examples/music-slideshow/project.json').read_text())
    project_schema=json.loads((root/'schemas/video-project.schema.json').read_text())
    jsonschema.validate(project,project_schema)
    sources=json.loads((root/'research/sources.lock.json').read_text())
    source_schema=json.loads((root/'schemas/source-registry.schema.json').read_text())
    jsonschema.validate(sources,source_schema)
    qa=json.loads((root/'examples/music-slideshow/output/qa-report.json').read_text())
    qa_schema=json.loads((root/'schemas/qa-report.schema.json').read_text())
    jsonschema.validate(qa,qa_schema)
