from emacs_a11y.cli.interactive import build_context_tree, dispatch_command, render_help, suggest_commands
from emacs_a11y.models.interactive_cli import InteractiveSessionState, NavigationAction


def _state() -> InteractiveSessionState:
    return InteractiveSessionState(context_stack=["root"], contexts=build_context_tree())


def test_render_help_is_linear_and_without_color_codes():
    lines = render_help(build_context_tree()["root"])
    assert lines[0].startswith("Comandos do contexto")
    assert any("help - ajuda de comandos" in line for line in lines)
    assert all("\x1b[" not in line for line in lines)


def test_help_command_returns_context_help():
    result = dispatch_command(_state(), "help")
    assert result.navigation == NavigationAction.STAY
    assert any("doctor - Executa diagnóstico" in line for line in result.message_lines)


def test_invalid_command_has_clear_message_and_help_guidance():
    result = dispatch_command(_state(), "doctro")
    assert result.status == "invalid"
    assert "Comando inválido" in result.message_lines[0]
    assert "Use help" in " ".join(result.message_lines)
    assert len(result.suggestions) <= 3


def test_suggestions_are_capped_at_three():
    context = build_context_tree()["doctor"]
    suggestions = suggest_commands("j", context)
    assert len(suggestions) <= 3
