from pathlib import Path

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.install import planner, preflight


runner = CliRunner()


class _Env:
    def __init__(self):
        self.emacs_version = "GNU Emacs"
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = True
        self.profile_accessible = True
        self.user_emacs_paths = []


def test_existing_profile_files_are_not_silently_overwritten(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    target.mkdir(parents=True)
    init_file = target / "init.el"
    init_file.write_text("existing", encoding="utf-8")

    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env())

    result = runner.invoke(app, ["install", "--profile", "minimal"], input="n\n")
    assert result.exit_code == 1
    assert init_file.read_text(encoding="utf-8") == "existing"
