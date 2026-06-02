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


def test_yes_mode_works_with_emacs_present(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs"))

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 0
    assert (target / "init.el").exists()


def test_yes_mode_does_not_bypass_critical_preflight(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 2
    assert "CRITICAL: Emacs nao encontrado" in result.stdout
    assert not target.exists()
