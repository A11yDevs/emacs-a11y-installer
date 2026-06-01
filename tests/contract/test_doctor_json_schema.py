import json
from pathlib import Path

import jsonschema

from emacs_a11y.doctor.orchestrator import run_diagnostic


def test_doctor_json_schema_contract():
    schema_path = Path("specs/001-doctor-cli/contracts/doctor-report.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    payload = run_diagnostic().to_dict()
    jsonschema.validate(instance=payload, schema=schema)
