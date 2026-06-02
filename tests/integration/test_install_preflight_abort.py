from pathlib import Path

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.install import planner, preflight


runner = CliRunner()


class _Env:
    def __init__(self):
        self.emacs_version = None
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = False
        self.profile_accessible = False
        self.user_emacs_paths = []


def test_preflight_abort_creates_no_profile_artifacts(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env())

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 2

    assert not target.exists()
    assert not (target / "early-init.el").exists()
    assert not (target / "init.el").exists()
    assert not (target / "custom.el").exists()
    assert not (target / "logs").exists()
