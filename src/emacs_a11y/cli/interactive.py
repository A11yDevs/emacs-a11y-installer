from __future__ import annotations

from difflib import get_close_matches
from typing import Callable

from emacs_a11y.cli.doctor import execute_doctor_command
from emacs_a11y.doctor.checks.common import build_environment_state
from emacs_a11y.doctor.registry import load_checks
from emacs_a11y.models.interactive_cli import (
    CommandContext,
    CommandDefinition,
    CommandResult,
    InteractiveSessionState,
    NavigationAction,
)


GLOBAL_COMMANDS = [
    CommandDefinition("help", "ajuda de comandos", kind="global"),
    CommandDefinition("back", "sair", kind="global"),
    CommandDefinition("exit", "sair", kind="global"),
]


def build_context_tree() -> dict[str, CommandContext]:
    root_commands = [
        CommandDefinition(
            "doctor",
            "Executa diagnóstico de ambiente em modo estritamente somente leitura.",
            kind="navigation",
            target_context="doctor",
        ),
        *GLOBAL_COMMANDS,
    ]
    doctor_commands = [
        CommandDefinition("run", "executa diagnóstico textual", kind="action"),
        CommandDefinition("json", "executa diagnóstico em JSON", kind="action"),
        CommandDefinition("explain", "explica checks de diagnóstico", kind="action"),
        *GLOBAL_COMMANDS,
    ]

    return {
        "root": CommandContext(
            name="root",
            prompt_label="emacs-a11y",
            description="Contexto raiz",
            parent=None,
            commands=root_commands,
        ),
        "doctor": CommandContext(
            name="doctor",
            prompt_label="emacs-a11y doctor",
            description="Contexto de diagnóstico",
            parent="root",
            commands=doctor_commands,
        ),
    }


def render_help(context: CommandContext) -> list[str]:
    lines = [f"Comandos do contexto {context.prompt_label}:"]
    for command in context.commands:
        lines.append(f"{command.name} - {command.description}")
    return lines


def suggest_commands(command: str, context: CommandContext) -> list[str]:
    names = [item.name for item in context.commands]
    return get_close_matches(command, names, n=3, cutoff=0.5)


def _run_doctor_text() -> tuple[list[str], int]:
    output_lines: list[str] = []

    def _capture(message: object) -> None:
        output_lines.append(str(message))

    exit_code = execute_doctor_command(False, emit=_capture)
    return output_lines, exit_code


def _run_doctor_json() -> tuple[list[str], int]:
    output_lines: list[str] = []

    def _capture(message: object) -> None:
        output_lines.append(str(message))

    exit_code = execute_doctor_command(True, emit=_capture)
    return output_lines, exit_code


def _explain_checks() -> list[str]:
    state = build_environment_state()
    checks = load_checks(state.os)

    lines = ["Explicações dos checks:"]
    for check in checks:
        check_name = getattr(check, "name", None) or getattr(check, "__name__", "check")
        check_description = getattr(check, "description", None) or "Sem descrição detalhada."
        lines.append(f"- {check_name}: {check_description}")
    return lines


def dispatch_command(state: InteractiveSessionState, raw_command: str) -> CommandResult:
    command = raw_command.strip().split()[0] if raw_command.strip() else ""
    if not command:
        return CommandResult(status="ok", navigation=NavigationAction.STAY)

    context = state.current_context

    if command == "help":
        return CommandResult(
            status="ok",
            navigation=NavigationAction.STAY,
            message_lines=render_help(context),
        )

    if command == "exit":
        return CommandResult(
            status="exit_requested",
            navigation=NavigationAction.EXIT,
            message_lines=["Sessão encerrada."],
            exit_code=0,
        )

    if command == "back":
        if context.parent is None:
            return CommandResult(
                status="exit_requested",
                navigation=NavigationAction.EXIT,
                message_lines=["Saindo do modo interativo."],
                exit_code=0,
            )
        return CommandResult(
            status="ok",
            navigation=NavigationAction.POP,
            message_lines=[f"Voltando para {state.contexts[context.parent].prompt_label}."],
            next_context=context.parent,
        )

    command_map = context.command_map()
    definition = command_map.get(command)

    if definition is None:
        suggestions = suggest_commands(command, context)
        message = [
            f"Comando inválido no contexto {context.prompt_label}: {command}.",
            "Use help para ver comandos disponíveis.",
        ]
        if suggestions:
            message.append(f"Sugestões: {', '.join(suggestions)}")
        return CommandResult(
            status="invalid",
            navigation=NavigationAction.STAY,
            message_lines=message,
            suggestions=suggestions,
        )

    if definition.kind == "navigation" and definition.target_context is not None:
        return CommandResult(
            status="ok",
            navigation=NavigationAction.PUSH,
            next_context=definition.target_context,
            message_lines=[f"Entrando em {state.contexts[definition.target_context].prompt_label}."],
        )

    if context.name == "doctor" and command == "run":
        lines, _ = _run_doctor_text()
        return CommandResult(status="ok", navigation=NavigationAction.STAY, message_lines=lines)

    if context.name == "doctor" and command == "json":
        lines, _ = _run_doctor_json()
        return CommandResult(status="ok", navigation=NavigationAction.STAY, message_lines=lines)

    if context.name == "doctor" and command == "explain":
        return CommandResult(status="ok", navigation=NavigationAction.STAY, message_lines=_explain_checks())

    return CommandResult(
        status="error",
        navigation=NavigationAction.STAY,
        message_lines=["Erro interno ao resolver comando."],
    )


def run_interactive_session(
    read_line: Callable[[str], str] | None = None,
    write_line: Callable[[str], None] | None = None,
) -> int:
    reader = read_line if read_line is not None else input
    writer = write_line if write_line is not None else print

    state = InteractiveSessionState(context_stack=["root"], contexts=build_context_tree())

    for line in render_help(state.current_context):
        writer(line)

    while state.running:
        try:
            raw = reader(f"{state.current_context.prompt_label}>")
        except EOFError:
            writer("Sessão encerrada.")
            return 0
        except KeyboardInterrupt:
            writer("Sessão interrompida.")
            return 0

        result = dispatch_command(state, raw)
        for line in result.message_lines:
            writer(line)

        if result.navigation == NavigationAction.PUSH and result.next_context:
            state.push(result.next_context)
            for line in render_help(state.current_context):
                writer(line)
        elif result.navigation == NavigationAction.POP:
            state.pop()
            for line in render_help(state.current_context):
                writer(line)
        elif result.navigation == NavigationAction.EXIT:
            return result.exit_code if result.exit_code is not None else 0

    return 0
