from typer.testing import CliRunner

from emacs_a11y.cli.doctor import app


runner = CliRunner()


def test_no_args_enters_interactive_and_shows_root_help():
    result = runner.invoke(app, [], input="exit\n")
    assert result.exit_code == 0
    assert "emacs-a11y>" in result.stdout
    assert "help - ajuda de comandos" in result.stdout
    assert "doctor - Executa diagnóstico de ambiente em modo estritamente somente leitura." in result.stdout


def test_help_back_and_exit_in_root_context():
    result = runner.invoke(app, [], input="help\nback\n")
    assert result.exit_code == 0
    assert result.stdout.count("help - ajuda de comandos") >= 2
    assert "Saindo do modo interativo." in result.stdout


def test_invalid_command_in_root_is_clear_and_accessible():
    result = runner.invoke(app, [], input="doctro\nexit\n")
    assert result.exit_code == 0
    assert "Comando inválido no contexto emacs-a11y: doctro." in result.stdout
    assert "Use help para ver comandos disponíveis." in result.stdout


def test_eof_and_keyboard_interrupt_exit_cleanly(monkeypatch):
    sequence = [EOFError]

    def fake_input(_prompt: str) -> str:
        item = sequence.pop(0)
        if item is EOFError:
            raise EOFError
        return str(item)

    from emacs_a11y.cli import interactive

    exit_code = interactive.run_interactive_session(read_line=fake_input, write_line=lambda _msg: None)
    assert exit_code == 0
