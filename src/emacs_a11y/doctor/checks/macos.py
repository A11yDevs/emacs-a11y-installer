from __future__ import annotations

import shutil

from emacs_a11y.models.diagnostic import DiagnosticResult, EnvironmentState, Severity, Status


def check_macos_tts(state: EnvironmentState) -> DiagnosticResult:
    say_cmd = shutil.which("say")
    if say_cmd:
        return DiagnosticResult(
            check_id="tts.macos",
            name="TTS macOS",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Comando de voz do macOS disponivel",
            evidence=[say_cmd],
        )

    return DiagnosticResult(
        check_id="tts.macos",
        name="TTS macOS",
        status=Status.UNKNOWN,
        severity=Severity.WARNING,
        summary="Nao foi possivel confirmar infraestrutura de voz do macOS",
        evidence=["comando say nao encontrado"],
        next_steps=["Valide vozes do sistema em Acessibilidade > Conteudo Falado."],
    )


def checks() -> list:
    return [check_macos_tts]
