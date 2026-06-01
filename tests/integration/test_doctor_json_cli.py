import json

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.doctor import orchestrator
from emacs_a11y.models.diagnostic import (
    DiagnosticReport,
    DiagnosticResult,
    EnvironmentState,
    Severity,
    Status,
    SummaryCounts,
)


runner = CliRunner()


def _json_report() -> DiagnosticReport:
    return DiagnosticReport(
        report_version="1.0",
        generated_at="2026-06-01T00:00:00+00:00",
        environment=EnvironmentState(os="Linux", architecture="x86_64"),
        summary=SummaryCounts(critical=0, warning=1, info=2, pass_count=2, fail=1, unknown=0),
        results=[
            DiagnosticResult("tool.git", "Git", Status.FAIL, Severity.WARNING, "Git ausente"),
            DiagnosticResult("system.info", "Sistema", Status.PASS, Severity.INFO, "Linux x86_64"),
            DiagnosticResult("tool.python", "Python", Status.PASS, Severity.INFO, "Python disponivel"),
        ],
        next_steps=["Opcional: instale Git"],
        exit_code=1,
    )


def test_doctor_json_outputs_valid_json(monkeypatch):
    monkeypatch.setattr(orchestrator, "run_diagnostic", _json_report)
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code == 1

    payload = json.loads(result.stdout)
    assert payload["report_version"] == "1.0"
    assert payload["summary"]["warning"] == 1
    assert payload["results"][0]["severity"] == "WARNING"


def test_doctor_text_and_json_semantic_parity(monkeypatch):
    monkeypatch.setattr(orchestrator, "run_diagnostic", _json_report)

    text_result = runner.invoke(app, ["doctor"])
    json_result = runner.invoke(app, ["doctor", "--json"])

    payload = json.loads(json_result.stdout)
    assert text_result.exit_code == json_result.exit_code == payload["exit_code"]
    assert "Git" in text_result.stdout
    assert any(item["name"] == "Git" for item in payload["results"])


def test_doctor_json_exit_code_determinism(monkeypatch):
    critical = _json_report()
    critical.summary.critical = 1
    critical.exit_code = 2

    monkeypatch.setattr(orchestrator, "run_diagnostic", lambda: critical)
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code == 2


def test_packaged_channel_parity_matrix_definition_exists():
    # Task artifact check: parity matrix protocol is documented in quickstart.
    from pathlib import Path

    content = Path("specs/001-doctor-cli/quickstart.md").read_text(encoding="utf-8")
    assert "paridade" in content.lower()
    assert "standalone" in content.lower()
