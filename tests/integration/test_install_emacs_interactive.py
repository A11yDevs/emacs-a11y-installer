from __future__ import annotations

import time

from typer.testing import CliRunner

from emacs_a11y.cli import interactive
from emacs_a11y.cli.doctor import app


runner = CliRunner()


def test_install_context_lists_emacs_command() -> None:
    result = runner.invoke(app, [], input="install\nhelp\nexit\n")
    assert result.exit_code == 0
    assert "emacs -" in result.stdout
    assert "profile" in result.stdout
    assert "minimal" in result.stdout


def test_interactive_emacs_guidance_flow(monkeypatch) -> None:
    monkeypatch.setattr(
        interactive,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: (
            type("R", (), {"exit_code": 1})(),
            ["INFO: Guidance-only ativo - nenhum comando sera executado automaticamente."],
        ),
    )
    result = runner.invoke(app, [], input="install\nemacs\nexit\n")
    assert result.exit_code == 0
    assert "Guidance-only" in result.stdout


def test_interactive_emacs_execute_shows_progress_feedback(monkeypatch) -> None:
    monkeypatch.setattr(interactive, "HEARTBEAT_INTERVAL_SECONDS", 0.01)

    def _slow_flow(execute, dry_run, method, confirm_callback=None):
        time.sleep(0.03)
        return type("R", (), {"exit_code": 0})(), ["SUCCESS: Execucao assistida concluida com sucesso."]

    monkeypatch.setattr(interactive, "run_install_emacs_flow", _slow_flow)

    result = runner.invoke(app, [], input="install\nemacs-execute\nexit\n")
    assert result.exit_code == 0
    assert "Execucao assistida iniciada" in result.stdout
    assert "Execucao assistida em andamento" in result.stdout
    assert "Execucao assistida finalizada" in result.stdout
