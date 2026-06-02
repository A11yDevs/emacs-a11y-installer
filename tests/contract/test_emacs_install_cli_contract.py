from __future__ import annotations

from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app
from emacs_a11y.cli import install as install_cli


runner = CliRunner()


def _fake(exit_code: int, lines: list[str]):
    return type("R", (), {"exit_code": exit_code})(), lines


def test_cli_contract_accepts_install_emacs_flags(monkeypatch) -> None:
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake(1, ["INFO: Guidance-only ativo"]),
    )

    result = runner.invoke(app, ["install", "emacs", "--dry-run", "--method", "auto"])
    assert result.exit_code == 1


def test_cli_contract_rejects_yes_for_emacs() -> None:
    result = runner.invoke(app, ["install", "emacs", "--yes"])
    assert result.exit_code == 1
    assert "--yes nao faz parte" in result.stdout


def test_contract_markers_presence(monkeypatch) -> None:
    lines = [
        "INFO: test",
        "WARNING: test",
        "CRITICAL: test",
        "COMMAND: test",
        "CONFIRM: test",
        "CANCELLED: test",
        "NEXT STEP: test",
        "SKIPPED: test",
        "SUCCESS: test",
        "FAILED: test",
    ]
    monkeypatch.setattr(
        install_cli,
        "run_install_emacs_flow",
        lambda execute, dry_run, method, confirm_callback=None: _fake(1, lines),
    )
    result = runner.invoke(app, ["install", "emacs"])
    for marker in [
        "INFO",
        "WARNING",
        "CRITICAL",
        "COMMAND",
        "CONFIRM",
        "CANCELLED",
        "NEXT STEP",
        "SKIPPED",
        "SUCCESS",
        "FAILED",
    ]:
        assert marker in result.stdout
