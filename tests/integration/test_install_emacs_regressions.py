from __future__ import annotations

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


def test_doctor_still_works() -> None:
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code in {0, 1, 2}


def test_doctor_json_still_works() -> None:
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code in {0, 1, 2}
    assert "report_version" in result.stdout


def test_install_profile_minimal_still_works(monkeypatch, tmp_path) -> None:
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs 30.1"))

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 0
    assert (target / "init.el").exists()
