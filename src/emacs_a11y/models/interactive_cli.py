from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from emacs_a11y.models.emacs_install import InteractiveInstallContextState


class NavigationAction(str, Enum):
    STAY = "STAY"
    PUSH = "PUSH"
    POP = "POP"
    EXIT = "EXIT"


@dataclass(slots=True)
class CommandDefinition:
    name: str
    description: str
    kind: str = "action"
    target_context: str | None = None


@dataclass(slots=True)
class CommandContext:
    name: str
    prompt_label: str
    description: str
    parent: str | None
    commands: list[CommandDefinition] = field(default_factory=list)

    def command_map(self) -> dict[str, CommandDefinition]:
        result: dict[str, CommandDefinition] = {}
        for command in self.commands:
            result[command.name] = command
        return result


@dataclass(slots=True)
class CommandResult:
    status: str
    navigation: NavigationAction
    message_lines: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    next_context: str | None = None
    exit_code: int | None = None


@dataclass(slots=True)
class InteractiveSessionState:
    context_stack: list[str]
    contexts: dict[str, CommandContext]
    running: bool = True
    session_data: dict[str, object] = field(default_factory=dict)
    install_emacs_state: InteractiveInstallContextState = field(default_factory=InteractiveInstallContextState)

    @property
    def current_context(self) -> CommandContext:
        return self.contexts[self.context_stack[-1]]

    def push(self, context_name: str) -> None:
        self.context_stack.append(context_name)

    def pop(self) -> bool:
        if len(self.context_stack) == 1:
            return False
        self.context_stack.pop()
        return True
