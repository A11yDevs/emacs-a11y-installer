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


def test_install_emacs_missing_aborts_before_any_write(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))

    result = runner.invoke(app, ["install", "--profile", "minimal"])
    assert result.exit_code == 2
    assert "CRITICAL: Emacs nao encontrado" in result.stdout
    assert "Nenhum arquivo foi criado." in result.stdout
    assert not target.exists()


def test_install_emacs_present_creates_profile_after_confirmation(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs 30.0"))

    result = runner.invoke(app, ["install", "--profile", "minimal"], input="y\n")
    assert result.exit_code == 0
    assert (target / "early-init.el").exists()
    assert (target / "init.el").exists()
    assert (target / "custom.el").exists()
    assert (target / "logs").exists()


def test_install_cancel_before_write_creates_nothing(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs 30.0"))

    result = runner.invoke(app, ["install", "--profile", "minimal"], input="n\n")
    assert result.exit_code == 1
    assert "Instalação cancelada" in result.stdout
    assert not target.exists()


def test_minimal_init_contains_only_allowed_requires(monkeypatch, tmp_path):
    target = tmp_path / "profile"
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: target)
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs 30.0"))

    result = runner.invoke(app, ["install", "--profile", "minimal", "--yes"])
    assert result.exit_code == 0
    content = (target / "init.el").read_text(encoding="utf-8")
    assert "(require 'init-packages)" in content
    assert "(require 'init-core)" in content
    assert "(require 'init-dired)" in content
    assert "(require 'init-accessibility)" not in content
