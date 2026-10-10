import json
from pathlib import Path
import jsonschema


def test_example_and_source_registry_validate_against_schemas(sample_video) -> None:
    root=Path(__file__).resolve().parents[1]
    project=json.loads((root/'examples/music-slideshow/project.json').read_text())
    project_schema=json.loads((root/'schemas/video-project.schema.json').read_text())
    jsonschema.validate(project,project_schema)
    sources=json.loads((root/'research/sources.lock.json').read_text())
    source_schema=json.loads((root/'schemas/source-registry.schema.json').read_text())
    jsonschema.validate(sources,source_schema)
    from video_workflow.qa import validate_video
    qa=validate_video(sample_video(),expected_width=640,expected_height=360,expected_duration=8,deep=True)
    qa_schema=json.loads((root/'schemas/qa-report.schema.json').read_text())
    jsonschema.validate(qa,qa_schema)
