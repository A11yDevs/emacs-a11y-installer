from __future__ import annotations

from emacs_a11y.models.diagnostic import DiagnosticResult, EnvironmentState, Severity, Status


def check_windows_tts(state: EnvironmentState) -> DiagnosticResult:
    signals = []
    for marker in ("SAPI", "OneCore", "Narrator"):
        if marker.lower() in " ".join(state.path_entries).lower():
            signals.append(marker)

    if signals:
        return DiagnosticResult(
            check_id="tts.windows",
            name="TTS Windows",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Sinais iniciais de TTS Windows detectados",
            evidence=signals,
        )

    return DiagnosticResult(
        check_id="tts.windows",
        name="TTS Windows",
        status=Status.UNKNOWN,
        severity=Severity.WARNING,
        summary="Nao foi possivel confirmar TTS Windows com seguranca",
        evidence=["sinais SAPI/OneCore/Narrator nao encontrados"],
        next_steps=["Valide manualmente Narrador e vozes instaladas no Windows."],
    )


def checks() -> list:
    return [check_windows_tts]
