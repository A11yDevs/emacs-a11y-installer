import subprocess
from pathlib import Path

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


def _report_with_levels() -> DiagnosticReport:
    return DiagnosticReport(
        report_version="1.0",
        generated_at="2026-06-01T00:00:00+00:00",
        environment=EnvironmentState(os="Linux", architecture="x86_64"),
        summary=SummaryCounts(critical=1, warning=1, info=1, pass_count=1, fail=2, unknown=0),
        results=[
            DiagnosticResult("tool.python", "Python", Status.FAIL, Severity.CRITICAL, "Python ausente"),
            DiagnosticResult("tool.git", "Git", Status.FAIL, Severity.WARNING, "Git ausente"),
            DiagnosticResult("system.info", "Sistema", Status.PASS, Severity.INFO, "Linux x86_64"),
        ],
        next_steps=["Instale Python"],
        exit_code=2,
    )


def test_doctor_text_sections_are_linear_and_accessible(monkeypatch):
    monkeypatch.setattr(orchestrator, "run_diagnostic", _report_with_levels)
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 2
    output = result.stdout
    expected = ["Resumo", "Críticos", "Avisos", "Info", "Próximos passos"]
    positions = [output.index(item) for item in expected]
    assert positions == sorted(positions)
    assert "CRITICAL" in output
    assert "WARNING" in output
    assert "INFO" in output
    assert "\x1b[" not in output


def test_doctor_does_not_trigger_writes_or_install_commands(monkeypatch):
    monkeypatch.setattr(orchestrator, "run_diagnostic", _report_with_levels)

    def denied_write(*_args, **_kwargs):
        raise AssertionError("write operation attempted")

    monkeypatch.setattr(Path, "mkdir", denied_write)
    monkeypatch.setattr(Path, "write_text", denied_write)

    original_run = subprocess.run

    def guarded_run(cmd, *args, **kwargs):
        raw = " ".join(cmd) if isinstance(cmd, (list, tuple)) else str(cmd)
        forbidden = ["pip install", "apt", "brew install", "curl", "wget", "sudo"]
        assert not any(token in raw for token in forbidden)
        return original_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", guarded_run)

    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 2


def test_doctor_help_is_useful_and_linear():
    result = runner.invoke(app, ["doctor", "--help"])
    assert result.exit_code == 0
    assert "diagnostico" in result.stdout.lower()
    assert "--json" in result.stdout


def test_root_help_includes_doctor_command():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "doctor" in result.stdout
