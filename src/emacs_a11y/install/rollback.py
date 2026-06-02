from __future__ import annotations

from emacs_a11y.models.install import RollbackInstruction


def build_rollback_instruction(created_items: list[str], copied_items: list[str]) -> RollbackInstruction:
    paths = sorted(set(created_items + copied_items), key=len, reverse=True)
    return RollbackInstruction(
        paths_to_remove=paths,
        notes=[
            "Remova somente caminhos project-owned do perfil isolado.",
            "Nao remova ~/.emacs, ~/.emacs.d ou ~/.config/emacs.",
        ],
        future_command_hint="Comando futuro: emacs-a11y remove --profile minimal",
    )
