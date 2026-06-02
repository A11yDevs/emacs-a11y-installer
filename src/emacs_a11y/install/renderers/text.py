from __future__ import annotations

from emacs_a11y.models.install import InstallExecutionResult, InstallPlan, PreflightResult


def render_preflight_abort(preflight: PreflightResult) -> list[str]:
    lines = [*preflight.message_lines]
    lines.append("NEXT STEP:")
    for step in preflight.suggested_next_steps:
        lines.append(f"- {step}")
    return lines


def render_install_plan(plan: InstallPlan) -> list[str]:
    lines = ["Plano de instalação (sem escrita ainda):"]
    lines.append(f"TARGET: {plan.request.target_directory}")
    for notice in plan.personal_config_notices:
        lines.append(f"INFO: Configuracao pessoal preservada: {notice}")
    for item in plan.items:
        source = f" <- {item.source_path}" if item.source_path else ""
        lines.append(f"PLAN: {item.action_type.value} {item.path}{source}")
    lines.append("Use confirm para continuar ou cancel para abortar.")
    return lines


def render_cancelled() -> list[str]:
    return ["WARNING: Instalação cancelada pelo usuário.", "Nenhum arquivo foi criado."]


def render_execution_summary(result: InstallExecutionResult) -> list[str]:
    lines: list[str] = []

    def _add_group(title: str, items: list[str]) -> None:
        lines.append(title)
        if items:
            lines.extend([f"- {item}" for item in items])
        else:
            lines.append("- (nenhum)")

    _add_group("CREATED", result.created_items)
    _add_group("COPIED", result.copied_items)
    _add_group("SKIPPED", result.skipped_items)
    _add_group("PRESERVED", result.preserved_items)
    _add_group("FAILED", result.failed_items)
    _add_group("WARNING", result.warning_items)

    if result.preflight_result.status.value == "critical_abort":
        lines.append("CRITICAL: Emacs não encontrado")

    lines.append("NEXT STEP")
    if result.preflight_result.suggested_next_steps:
        for step in result.preflight_result.suggested_next_steps:
            lines.append(f"- {step}")
    else:
        lines.append("- Revise o perfil isolado e execute emacs-a11y doctor.")

    if result.rollback_guidance.paths_to_remove:
        lines.append("Rollback guidance:")
        for path in result.rollback_guidance.paths_to_remove:
            lines.append(f"- remover {path}")

    return lines
