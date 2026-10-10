"""Atlas collection layout and stable IDs, independent of a host's private runtime."""
import re

COLLECTION_DIRS = {
    "patterns": "01 Patterns/Entries",
    "terms": "02 Terms/Entries",
    "biases": "03 Collections/Biases/Entries",
    "llm-biases": "03 Collections/Biases/LLM Biases/Entries",
    "ai-data-biases": "03 Collections/Biases/AI & Data Biases/Entries",
    "bias-mitigation": "03 Collections/Bias Mitigation/Entries",
    "ethical-dilemmas": "03 Collections/Ethical Dilemmas/Entries",
    "paradoxes-puzzles": "03 Collections/Paradoxes & Puzzles/Entries",
    "personas": "03 Collections/Personas/Entries",
    "task-templates": "03 Collections/Task Templates/Entries",
    "file-o-fun": "03 Collections/File-O-Fun/Cards",
}


def normalize_text(value):
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def slugify(value):
    text = normalize_text(value).lower().replace("&", " and ")
    text = re.sub(r"[\s_/]+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")
