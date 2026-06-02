from __future__ import annotations

from typing import Callable
from pathlib import Path

from emacs_a11y.install.emacs_detector import detect_emacs, detect_environment
from emacs_a11y.install.emacs_executor import log_event, run_assisted_command
from emacs_a11y.install.emacs_methods import recommend_installation_method
from emacs_a11y.install.emacs_version import assess_emacs_version
from emacs_a11y.install.renderers.emacs_text import (
    build_consent_summary,
    render_assisted_outcome,
    render_cancelled,
    render_consent,
    render_installed_emacs,
    render_recommendation,
)
from emacs_a11y.models.emacs_install import (
    ConsentDecision,
    InstallExecutionMode,
    InstallationAttemptResult,
    status_to_exit_code,
)


def _is_homebrew_not_linked_output(output_summary: str, command_display_text: str) -> bool:
    normalized_summary = output_summary.lower()
    normalized_command = command_display_text.lower()
    if "brew" not in normalized_command:
        return False
    return "already installed" in normalized_summary and "not linked" in normalized_summary


def _is_homebrew_cask_reinstall_required(output_summary: str, command_display_text: str) -> bool:
    normalized_summary = output_summary.lower()
    normalized_command = command_display_text.lower()
    if "brew" not in normalized_command or "--cask" not in normalized_command:
        return False
    return "cannot be upgraded as-is" in normalized_summary


def _macos_gui_next_step() -> str:
    app_path = Path("/Applications/Emacs.app")
    if app_path.exists():
        return "Para abrir interface grafica: open -a /Applications/Emacs.app"
    return "Para usar interface grafica no macOS: brew install --cask emacs-app"


def run_install_emacs_flow(
    execute: bool,
    dry_run: bool,
    method: str,
    confirm_callback: Callable[[str], bool] | None = None,
) -> tuple[InstallationAttemptResult, list[str]]:
    environment = detect_environment()
    emacs_before = detect_emacs()

    recommendation = recommend_installation_method(environment, requested_method=method)

    if emacs_before.status in {"found", "multiple_found"}:
        version_assessment = assess_emacs_version(emacs_before.version_text)
        next_steps = ["emacs-a11y doctor", "emacs-a11y install --profile minimal"]
        extra_render_steps: list[str] = []
        if environment.operating_system == "macos":
            gui_step = _macos_gui_next_step()
            next_steps.append(gui_step)
            extra_render_steps.append(gui_step)
        result = InstallationAttemptResult(
            status="success",
            environment=environment,
            emacs_detection_before=emacs_before,
            version_assessment=version_assessment,
            recommendation=recommendation,
            mode=InstallExecutionMode.GUIDANCE_ONLY,
            next_steps=next_steps,
            exit_code=status_to_exit_code("success"),
        )
        log_path = log_event("install-emacs", "emacs already installed")
        result.logs.append(log_path)
        return result, render_installed_emacs(
            emacs_before,
            version_assessment,
            extra_next_steps=extra_render_steps,
        )

    if dry_run:
        result = InstallationAttemptResult(
            status="guidance_only",
            environment=environment,
            emacs_detection_before=emacs_before,
            version_assessment=None,
            recommendation=recommendation,
            mode=InstallExecutionMode.DRY_RUN,
            next_steps=["Revise o metodo sugerido e execute manualmente se desejar."],
            exit_code=status_to_exit_code("guidance_only"),
        )
        log_path = log_event("install-emacs", "dry-run mode")
        result.logs.append(log_path)
        return result, render_recommendation(environment, recommendation, dry_run=True)

    if not execute:
        result = InstallationAttemptResult(
            status="guidance_only",
            environment=environment,
            emacs_detection_before=emacs_before,
            version_assessment=None,
            recommendation=recommendation,
            mode=InstallExecutionMode.GUIDANCE_ONLY,
            next_steps=[
                "Execute o comando recomendado manualmente.",
                "Depois rode emacs-a11y doctor.",
                "Depois rode emacs-a11y install --profile minimal.",
            ],
            exit_code=status_to_exit_code("guidance_only"),
        )
        log_path = log_event("install-emacs", "guidance-only mode")
        result.logs.append(log_path)
        return result, render_recommendation(environment, recommendation)

    if not environment.is_tty:
        result = InstallationAttemptResult(
            status="unsupported",
            environment=environment,
            emacs_detection_before=emacs_before,
            version_assessment=None,
            recommendation=recommendation,
            mode=InstallExecutionMode.ASSISTED_EXECUTION,
            consent_decision=ConsentDecision.UNAVAILABLE_NO_TTY,
            next_steps=["Reexecute em sessao interativa (TTY) ou use guidance-only/dry-run."],
            exit_code=status_to_exit_code("unsupported"),
        )
        lines = ["CRITICAL: Sessao sem TTY nao pode executar instalacao assistida."]
        lines.extend(render_recommendation(environment, recommendation))
        log_path = log_event("install-emacs", "execute denied: no tty")
        result.logs.append(log_path)
        return result, lines

    if not recommendation.assisted_execution_supported or not recommendation.recommended_commands:
        result = InstallationAttemptResult(
            status="unsupported",
            environment=environment,
            emacs_detection_before=emacs_before,
            version_assessment=None,
            recommendation=recommendation,
            mode=InstallExecutionMode.ASSISTED_EXECUTION,
            next_steps=["Metodo/plataforma nao suportado para --execute. Use guidance-only."],
            exit_code=status_to_exit_code("unsupported"),
        )
        lines = ["CRITICAL: Metodo/plataforma nao suportado para execucao assistida."]
        lines.extend(render_recommendation(environment, recommendation))
        log_path = log_event("install-emacs", "execute denied: unsupported method")
        result.logs.append(log_path)
        return result, lines

    summary = build_consent_summary(environment, recommendation)
    consent_lines = render_consent(summary)
    allow = confirm_callback("CONFIRM: deseja executar o comando mostrado?") if confirm_callback else False

    if not allow:
        result = InstallationAttemptResult(
            status="cancelled",
            environment=environment,
            emacs_detection_before=emacs_before,
            version_assessment=None,
            recommendation=recommendation,
            mode=InstallExecutionMode.ASSISTED_EXECUTION,
            consent_decision=ConsentDecision.DECLINED,
            exit_code=status_to_exit_code("cancelled"),
        )
        log_path = log_event("install-emacs", "execute cancelled by user")
        result.logs.append(log_path)
        return result, [*consent_lines, *render_cancelled()]

    command = recommendation.recommended_commands[0]
    ok, output_summary, return_code = run_assisted_command(command)

    result = InstallationAttemptResult(
        status="success" if ok else "failed",
        environment=environment,
        emacs_detection_before=emacs_before,
        version_assessment=None,
        recommendation=recommendation,
        mode=InstallExecutionMode.ASSISTED_EXECUTION,
        consent_decision=ConsentDecision.CONFIRMED,
        executed_commands=[command.display_text],
        exit_code=status_to_exit_code("success" if ok else "failed"),
    )

    result.next_steps.append(f"Resumo do comando externo: {output_summary}")
    result.next_steps.append("Execute emacs-a11y doctor para validar o ambiente.")

    if not ok and _is_homebrew_cask_reinstall_required(output_summary, command.display_text):
        result.next_steps.append("Homebrew cask requer reinstalacao forcada para atualizar/reativar o app.")
        result.next_steps.append("Execute: brew reinstall --cask --force emacs-app")
        result.next_steps.append("Depois rode emacs-a11y doctor novamente.")

    if ok:
        emacs_after = detect_emacs()
        result.emacs_detection_after = emacs_after
        if emacs_after.status in {"found", "multiple_found"}:
            result.next_steps.append("Emacs detectado apos execucao assistida.")
            result.next_steps.append("Execute emacs-a11y install --profile minimal.")
            if environment.operating_system == "macos":
                result.next_steps.append(_macos_gui_next_step())
        else:
            result.status = "failed"
            result.exit_code = status_to_exit_code("failed")
            if _is_homebrew_not_linked_output(output_summary, command.display_text):
                result.next_steps.append(
                    "Homebrew indicou que o Emacs ja esta instalado, mas nao esta linkado no PATH."
                )
                result.next_steps.append("Execute brew link emacs e reabra o shell.")
                result.next_steps.append("Depois rode emacs-a11y doctor para confirmar deteccao.")
            else:
                result.next_steps.append(
                    "Comando retornou sucesso, mas Emacs nao foi detectado."
                    " Reabra o shell, verifique PATH ou rode emacs-a11y doctor."
                )

    log_path = log_event(
        "install-emacs",
        f"execute={'ok' if ok else 'failed'} return_code={return_code} command={command.display_text}",
    )
    result.logs.append(log_path)
    return result, [*consent_lines, *render_assisted_outcome(result)]
