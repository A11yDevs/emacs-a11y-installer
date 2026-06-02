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


def test_install_output_does_not_expose_common_secret_tokens(monkeypatch, tmp_path):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env())
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: tmp_path / "profile")

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 0
    lowered = result.stdout.lower()
    forbidden = ["password=", "token=", "secret=", "apikey", "authorization:"]
    assert not any(item in lowered for item in forbidden)
