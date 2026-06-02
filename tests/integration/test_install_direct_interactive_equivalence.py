from pathlib import Path

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.install import planner, preflight


runner = CliRunner()


class _Env:
    def __init__(self):
        self.emacs_version = "GNU Emacs"
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = False
        self.profile_accessible = False
        self.user_emacs_paths = []


def test_direct_and_interactive_create_same_core_artifacts(monkeypatch, tmp_path):
    env = _Env()
    monkeypatch.setattr(preflight, "build_environment_state", lambda: env)

    target_direct = tmp_path / "direct"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target_direct)
    direct = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert direct.exit_code == 0

    target_interactive = tmp_path / "interactive"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target_interactive)
    interactive = runner.invoke(app, [], input="install\nminimal\nconfirm\nexit\n")
    assert interactive.exit_code == 0

    for rel in ["early-init.el", "init.el", "custom.el"]:
        assert (target_direct / rel).exists()
        assert (target_interactive / rel).exists()
