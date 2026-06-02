from pathlib import Path

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.install import planner, preflight


runner = CliRunner()


class _Env:
    def __init__(self, emacs_version: str | None):
        self.emacs_version = emacs_version
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = False
        self.profile_accessible = False
        self.user_emacs_paths = []


def test_contract_missing_emacs_outputs_critical_and_next_steps(monkeypatch, tmp_path):
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: tmp_path / "profile")
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))

    result = runner.invoke(app, ["install", "--profile", "minimal"])
    assert result.exit_code == 2
    assert "CRITICAL: Emacs nao encontrado" in result.stdout
    assert "emacs-a11y install emacs" in result.stdout
    assert "emacs-a11y doctor" in result.stdout
    assert "emacs-a11y install --profile minimal" in result.stdout


def test_contract_summary_contains_canonical_status_markers(monkeypatch, tmp_path):
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: tmp_path / "profile")
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs"))

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 0

    markers = ["CREATED", "COPIED", "SKIPPED", "PRESERVED", "FAILED", "WARNING", "NEXT STEP"]
    for marker in markers:
        assert marker in result.stdout


def test_contract_output_is_linear_without_ansi(monkeypatch, tmp_path):
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: tmp_path / "profile")
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))

    result = runner.invoke(app, ["install", "--profile", "minimal"])
    assert result.exit_code == 2
    assert "\x1b[" not in result.stdout
