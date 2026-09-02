import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]

SCHEMA_PATH = ROOT / "core" / "semantic" / "schema" / "usl_representation_v1.schema.json"

EXAMPLE_PATH = ROOT / "core" / "semantic" / "examples" / "generated_usl_example_v1.json"


def load_json(path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def test_usl_schema_is_valid():
    schema = load_json(SCHEMA_PATH)

    Draft202012Validator.check_schema(schema)


def test_generated_usl_matches_schema():
    schema = load_json(SCHEMA_PATH)
    representation = load_json(EXAMPLE_PATH)

    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors(representation))

    assert errors == [], "\n".join(error.message for error in errors)
