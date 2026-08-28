import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]

SCHEMA_PATH = ROOT / "semantic" / "schema" / "usl_representation_v1.schema.json"
EXAMPLE_PATH = ROOT / "semantic" / "examples" / "generated_usl_example_v1.json"


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8-sig") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}")
        sys.exit(1)
    except OSError as exc:
        print(f"ERROR: Could not read {path}: {exc}")
        sys.exit(1)


def main():
    schema = load_json(SCHEMA_PATH)
    representation = load_json(EXAMPLE_PATH)

    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(representation),
        key=lambda error: list(error.path)
    )

    if errors:
        print("USL representation: INVALID")
        print()

        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            print(f"- {location}: {error.message}")

        sys.exit(1)

    print("USL representation: VALID")
    print(f"Schema:  {SCHEMA_PATH}")
    print(f"Example: {EXAMPLE_PATH}")


if __name__ == "__main__":
    main()
