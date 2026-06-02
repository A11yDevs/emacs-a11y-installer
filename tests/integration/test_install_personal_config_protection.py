from pathlib import Path

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.install import planner, preflight


runner = CliRunner()


class _Env:
    def __init__(self, user_paths: list[str]):
        self.emacs_version = "GNU Emacs"
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = False
        self.profile_accessible = False
        self.user_emacs_paths = user_paths


def test_personal_config_paths_are_only_reported_not_modified(monkeypatch, tmp_path):
    fake_home = tmp_path / "home"
    (fake_home / ".emacs").parent.mkdir(parents=True)
    (fake_home / ".emacs").write_text("user", encoding="utf-8")
    (fake_home / ".emacs.d").mkdir(parents=True)
    (fake_home / ".config" / "emacs").mkdir(parents=True)

    env = _Env([
        str(fake_home / ".emacs"),
        str(fake_home / ".emacs.d"),
        str(fake_home / ".config" / "emacs"),
    ])
    monkeypatch.setattr(preflight, "build_environment_state", lambda: env)

    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 0
    assert "Configuracao pessoal preservada" in result.stdout
    assert (fake_home / ".emacs").read_text(encoding="utf-8") == "user"
