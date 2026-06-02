from __future__ import annotations

import time

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.cli import install as install_cli


runner = CliRunner()


def _fake_result(status: str, exit_code: int, lines: list[str]):
    class _Result:
        def __init__(self):
            self.status = status
            self.exit_code = exit_code

    return _Result(), lines


def test_windows_with_winget_guidance(monkeypatch) -> None:
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake_result(
            "guidance_only",
            1,
            [
                "INFO: Plataforma detectada: windows (x64)",
                "COMMAND: winget install -e --id GNU.Emacs",
            ],
        ),
    )
    result = runner.invoke(app, ["install", "emacs"])
    assert result.exit_code == 1
    assert "winget install -e --id GNU.Emacs" in result.stdout


def test_execute_shows_confirmation_and_can_cancel(monkeypatch) -> None:
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake_result(
            "cancelled",
            1,
            [
                "CONFIRM: Metodo selecionado: WINGET_GNU_EMACS",
                "CANCELLED: Execucao assistida cancelada pela pessoa usuaria.",
            ],
        ),
    )
    result = runner.invoke(app, ["install", "emacs", "--execute"])
    assert result.exit_code == 1
    assert "CANCELLED" in result.stdout


def test_dry_run_never_executes(monkeypatch) -> None:
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake_result(
            "guidance_only", 1, ["INFO: DRY RUN - nenhum comando sera executado."]
        ),
    )
    result = runner.invoke(app, ["install", "emacs", "--dry-run"])
    assert result.exit_code == 1
    assert "DRY RUN" in result.stdout


def test_execute_unsupported_returns_exit_2(monkeypatch) -> None:
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake_result(
            "unsupported", 2, ["CRITICAL: Metodo/plataforma nao suportado para execucao assistida."]
        ),
    )
    result = runner.invoke(app, ["install", "emacs", "--execute", "--method", "apt"])
    assert result.exit_code == 2
    assert "CRITICAL" in result.stdout


def test_alias_emacs_execute_routes_to_execute_flow(monkeypatch) -> None:
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake_result(
            "cancelled",
            1,
            [
                "CONFIRM: Metodo selecionado: HOMEBREW_CASK",
                "CANCELLED: Execucao assistida cancelada pela pessoa usuaria.",
            ],
        ),
    )
    result = runner.invoke(app, ["install", "emacs-execute"])
    assert result.exit_code == 1
    assert "CANCELLED" in result.stdout


def test_unknown_install_subcommand_returns_clear_warning() -> None:
    result = runner.invoke(app, ["install", "emacs-foo"])
    assert result.exit_code == 1
    assert "Subcomando de install desconhecido" in result.stdout


def test_execute_shows_progress_feedback_when_command_is_slow(monkeypatch) -> None:
    monkeypatch.setattr(install_cli, "HEARTBEAT_INTERVAL_SECONDS", 0.01)

    def _slow_flow(execute, dry_run, method, confirm_callback=None):
        time.sleep(0.03)
        return _fake_result("success", 0, ["SUCCESS: Execucao assistida concluida com sucesso."])

    monkeypatch.setattr(install_cli, "run_install_emacs_flow", _slow_flow)

    result = runner.invoke(app, ["install", "emacs", "--execute"])
    assert result.exit_code == 0
    assert "Execucao assistida iniciada" in result.stdout
    assert "Execucao assistida em andamento" in result.stdout
    assert "Execucao assistida finalizada" in result.stdout
