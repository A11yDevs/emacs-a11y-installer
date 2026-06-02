from __future__ import annotations

import subprocess
from pathlib import Path

from emacs_a11y.install.profile import ensure_no_accessibility_require, init_content_is_minimal
from emacs_a11y.models.install import RuntimeValidationResult, RuntimeValidationStatus


def validate_written_artifacts(target_dir: Path) -> list[str]:
    failures: list[str] = []

    required_paths = [
        target_dir / "early-init.el",
        target_dir / "init.el",
        target_dir / "custom.el",
        target_dir / "lisp",
        target_dir / "logs",
    ]

    for path in required_paths:
        if not path.exists():
            failures.append(f"Ausente: {path}")

    init_path = target_dir / "init.el"
    if init_path.exists():
        content = init_path.read_text(encoding="utf-8")
        if not init_content_is_minimal(content):
            failures.append("init.el nao esta no formato minimal esperado")
        if not ensure_no_accessibility_require(content):
            failures.append("init.el nao pode ativar init-accessibility")

    return failures


def validate_runtime(emacs_executable: str | None, target_dir: Path) -> RuntimeValidationResult:
    if not emacs_executable:
        return RuntimeValidationResult(
            status=RuntimeValidationStatus.SKIPPED,
            message_lines=["Runtime validation ignorada: Emacs indisponivel."],
        )

    command = [
        emacs_executable,
        "--batch",
        "--quick",
        "--eval",
        '(message "emacs-a11y runtime validation")',
    ]

    try:
        process = subprocess.run(command, check=False, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError) as exc:
        return RuntimeValidationResult(
            status=RuntimeValidationStatus.FAILED,
            message_lines=[f"Falha na runtime validation: {exc}"],
            command_preview=" ".join(command),
        )

    if process.returncode == 0:
        return RuntimeValidationResult(
            status=RuntimeValidationStatus.VALIDATED,
            message_lines=["Runtime validation concluida."],
            command_preview=" ".join(command),
        )

    return RuntimeValidationResult(
        status=RuntimeValidationStatus.FAILED,
        message_lines=["Runtime validation falhou."],
        command_preview=" ".join(command),
    )
