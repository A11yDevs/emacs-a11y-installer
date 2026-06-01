from __future__ import annotations

import shutil

from emacs_a11y.models.diagnostic import DiagnosticResult, EnvironmentState, Severity, Status


def check_linux_tts(state: EnvironmentState) -> DiagnosticResult:
    evidence = []
    for cmd in ("speech-dispatcher", "spd-say", "espeak", "espeak-ng"):
        if shutil.which(cmd):
            evidence.append(cmd)

    if evidence:
        return DiagnosticResult(
            check_id="tts.linux",
            name="TTS Linux",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Sinais iniciais de TTS Linux detectados",
            evidence=evidence,
        )

    return DiagnosticResult(
        check_id="tts.linux",
        name="TTS Linux",
        status=Status.UNKNOWN,
        severity=Severity.WARNING,
        summary="Nao foi possivel confirmar infraestrutura de voz Linux",
        evidence=["speech-dispatcher/espeak nao encontrados"],
        next_steps=["Valide speech-dispatcher ou espeak no ambiente Linux."],
    )


def checks() -> list:
    return [check_linux_tts]
