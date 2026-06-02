from pathlib import Path

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.install import preflight


runner = CliRunner()


class _Env:
    def __init__(self):
        self.emacs_version = "GNU Emacs"
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = True
        self.profile_accessible = True
        self.user_emacs_paths = []


def test_doctor_text_still_works_after_install_integration(monkeypatch):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env())
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code in (0, 1, 2)
    assert "Resumo" in result.stdout


def test_doctor_json_still_works_after_install_integration(monkeypatch):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env())
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code in (0, 1, 2)
    assert "report_version" in result.stdout
