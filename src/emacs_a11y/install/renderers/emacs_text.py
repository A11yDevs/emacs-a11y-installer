from __future__ import annotations

from emacs_a11y.models.emacs_install import (
    EmacsDetectionResult,
    EnvironmentDetectionResult,
    ExecutionConsentSummary,
    InstallationAttemptResult,
    InstallationMethodRecommendation,
    VersionSupportAssessment,
)


def render_recommendation(
    environment: EnvironmentDetectionResult,
    recommendation: InstallationMethodRecommendation,
    dry_run: bool = False,
) -> list[str]:
    lines: list[str] = []
    if dry_run:
        lines.append("INFO: DRY RUN - nenhum comando sera executado.")
    else:
        lines.append("INFO: Guidance-only ativo - nenhum comando sera executado automaticamente.")

    lines.append(f"INFO: Plataforma detectada: {environment.operating_system} ({environment.architecture})")
    if environment.distribution not in {"unknown", ""}:
        lines.append(f"INFO: Distribuicao detectada: {environment.distribution}")

    if recommendation.recommended_commands:
        for command in recommendation.recommended_commands:
            lines.append(f"COMMAND: {command.display_text}")
            if command.requires_privilege:
                lines.append("WARNING: Este comando pode exigir privilegios administrativos.")
    else:
        lines.append("WARNING: Nenhum comando automatico disponivel para este ambiente.")

    for step in recommendation.manual_steps:
        lines.append(f"NEXT STEP: {step}")

    return lines


def build_consent_summary(
    environment: EnvironmentDetectionResult,
    recommendation: InstallationMethodRecommendation,
) -> ExecutionConsentSummary:
    command_lines = [cmd.display_text for cmd in recommendation.recommended_commands]
    needs_priv = any(cmd.requires_privilege for cmd in recommendation.recommended_commands)
    return ExecutionConsentSummary(
        platform_line=f"CONFIRM: Plataforma detectada: {environment.operating_system} ({environment.architecture})",
        method_line=f"CONFIRM: Metodo selecionado: {recommendation.method.value}",
        command_lines=command_lines,
        privilege_line=(
            "CONFIRM: Pode exigir privilegios administrativos."
            if needs_priv
            else "CONFIRM: Nao requer privilegios administrativos."
        ),
        effect_line="CONFIRM: O comando exibido sera o unico comando executado.",
        cancel_line="CONFIRM: Digite nao para cancelar com seguranca.",
    )


def render_consent(summary: ExecutionConsentSummary) -> list[str]:
    lines = [summary.platform_line, summary.method_line]
    for command in summary.command_lines:
        lines.append(f"COMMAND: {command}")
    lines.extend([summary.privilege_line, summary.effect_line, summary.cancel_line])
    return lines


def render_cancelled() -> list[str]:
    return ["CANCELLED: Execucao assistida cancelada pela pessoa usuaria."]


def render_installed_emacs(
    emacs_detection: EmacsDetectionResult,
    version_assessment: VersionSupportAssessment,
    extra_next_steps: list[str] | None = None,
) -> list[str]:
    lines = ["INFO: Emacs ja esta disponivel no ambiente."]
    if emacs_detection.selected_path:
        lines.append(f"INFO: Caminho detectado: {emacs_detection.selected_path}")

    if version_assessment.state == "supported":
        lines.append(f"INFO: Versao detectada: {version_assessment.detected_version}")
    elif version_assessment.state == "unknown":
        lines.append("WARNING: Nao foi possivel identificar a versao do Emacs.")
    else:
        lines.append("WARNING: Versao do Emacs abaixo da politica minima suportada.")
        lines.append("WARNING: Atualizacao recomendada com consentimento explicito.")

    lines.append("NEXT STEP: emacs-a11y doctor")
    lines.append("NEXT STEP: emacs-a11y install --profile minimal")
    for step in extra_next_steps or []:
        lines.append(f"NEXT STEP: {step}")
    return lines


def render_assisted_outcome(result: InstallationAttemptResult) -> list[str]:
    lines: list[str] = []
    if result.status == "success":
        lines.append("SUCCESS: Execucao assistida concluida com sucesso.")
    elif result.status == "failed":
        lines.append("FAILED: Execucao assistida terminou com falha.")
    elif result.status == "unsupported":
        lines.append("SKIPPED: Execucao assistida nao suportada para este metodo/plataforma.")

    for command in result.executed_commands:
        lines.append(f"COMMAND: {command}")

    for step in result.next_steps:
        lines.append(f"NEXT STEP: {step}")

    return lines
