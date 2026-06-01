from typer.testing import CliRunner

from emacs_a11y.cli import interactive
from emacs_a11y.cli.doctor import app


runner = CliRunner()


def test_doctor_navigation_root_to_doctor_and_back(monkeypatch):
    monkeypatch.setattr(interactive, "execute_doctor_command", lambda _json, emit: 0)
    result = runner.invoke(app, [], input="doctor\nback\nexit\n")
    assert result.exit_code == 0
    assert "emacs-a11y doctor>" in result.stdout
    assert "run - executa diagnóstico textual" in result.stdout


def test_doctor_context_run_json_and_explain(monkeypatch):
    def fake_execute(json_mode: bool, emit):
        if json_mode:
            emit('{"report_version":"1.0"}')
        else:
            emit("Resumo")
        return 0

    monkeypatch.setattr(interactive, "execute_doctor_command", fake_execute)
    result = runner.invoke(app, [], input="doctor\nrun\njson\nexplain\nexit\n")
    assert result.exit_code == 0
    assert "Resumo" in result.stdout
    assert '"report_version":"1.0"' in result.stdout
    assert "Explicações dos checks:" in result.stdout


def test_invalid_command_in_doctor_keeps_context(monkeypatch):
    monkeypatch.setattr(interactive, "execute_doctor_command", lambda _json, emit: 0)
    result = runner.invoke(app, [], input="doctor\njsoon\nexit\n")
    assert result.exit_code == 0
    assert "Comando inválido no contexto emacs-a11y doctor: jsoon." in result.stdout
    assert "emacs-a11y doctor>" in result.stdout
