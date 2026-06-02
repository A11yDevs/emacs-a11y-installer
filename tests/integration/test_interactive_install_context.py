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


def test_interactive_install_minimal_with_emacs_present(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs"))

    result = runner.invoke(app, [], input="install\nminimal\nconfirm\nexit\n")
    assert result.exit_code == 0
    assert "emacs-a11y install>" in result.stdout
    assert "Plano de instalação" in result.stdout
    assert (target / "init.el").exists()


def test_interactive_install_missing_emacs_aborts_without_write(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))

    result = runner.invoke(app, [], input="install\nminimal\nexit\n")
    assert result.exit_code == 0
    assert "CRITICAL: Emacs nao encontrado" in result.stdout
    assert not target.exists()


def test_interactive_help_back_exit_still_work(monkeypatch):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))
    result = runner.invoke(app, [], input="install\nhelp\nback\nexit\n")
    assert result.exit_code == 0
    assert "help - ajuda de comandos" in result.stdout
