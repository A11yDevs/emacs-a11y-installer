from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from emacs_a11y.install import planner, preflight, rollback, templates, validator, writer
from emacs_a11y.install.renderers import text as text_renderer
from emacs_a11y.models.install import (
    ConfirmationPolicy,
    InstallExecutionResult,
    InstallPlan,
    InstallRequest,
    PreflightResult,
    PreflightStatus,
    RuntimeValidationResult,
    RuntimeValidationStatus,
    TemplateValidationStatus,
)


@dataclass(slots=True)
class InstallPreview:
    request: InstallRequest
    preflight_result: PreflightResult
    plan: InstallPlan | None
    lines: list[str]
    emacs_executable: str | None


class InstallOrchestrator:
    def __init__(self, locator: templates.TemplateLocator | None = None) -> None:
        self.locator = locator or templates.TemplateLocator()

    def normalize_request(
        self,
        profile_name: str,
        mode: str,
        explicit_yes: bool,
        target_directory: Path | None = None,
    ) -> InstallRequest:
        if explicit_yes and profile_name == "minimal":
            policy = ConfirmationPolicy.EXPLICIT_YES_ALLOWED
        elif explicit_yes:
            policy = ConfirmationPolicy.DENY_UNSAFE_AUTOMATION
        elif mode == "interactive":
            policy = ConfirmationPolicy.INTERACTIVE_SELECTION
        else:
            policy = ConfirmationPolicy.PROMPT_REQUIRED

        return InstallRequest(
            profile_name=profile_name,
            mode=mode,
            confirmation_policy=policy,
            target_directory=target_directory or planner.resolve_default_target_directory(),
            explicit_yes=explicit_yes,
            allow_project_owned_overwrite=False,
        )

    def preview(self, request: InstallRequest) -> InstallPreview:
        preflight_check = preflight.build_preflight_check(
            profile_name=request.profile_name,
            target_directory=str(request.target_directory),
        )
        preflight_result = preflight.run_preflight(preflight_check)

        if preflight_result.status == PreflightStatus.CRITICAL_ABORT:
            return InstallPreview(
                request=request,
                preflight_result=preflight_result,
                plan=None,
                lines=text_renderer.render_preflight_abort(preflight_result),
                emacs_executable=None,
            )

        source = self.locator.resolve_source()
        template_validation, template = self.locator.validate_source(source)
        if template_validation.status != TemplateValidationStatus.VALID or template is None:
            message_lines = [*template_validation.message_lines]
            if template_validation.missing_items:
                message_lines.append(f"Itens ausentes: {', '.join(template_validation.missing_items)}")
            preflight_result.message_lines.extend(message_lines)
            preflight_result.exit_code = 1
            return InstallPreview(
                request=request,
                preflight_result=preflight_result,
                plan=None,
                lines=message_lines,
                emacs_executable=preflight_check.doctor_signals.get("emacs_version") and "emacs",
            )

        plan = planner.create_install_plan(request, template, preflight_result.message_lines)
        lines = text_renderer.render_install_plan(plan)
        emacs_executable = "emacs" if preflight_check.doctor_signals.get("emacs_version") else None
        return InstallPreview(
            request=request,
            preflight_result=preflight_result,
            plan=plan,
            lines=lines,
            emacs_executable=emacs_executable,
        )

    def execute(
        self,
        request: InstallRequest,
        auto_confirm: bool,
        confirm_callback: Callable[[str], bool] | None = None,
        prepared: InstallPreview | None = None,
    ) -> tuple[InstallExecutionResult, list[str]]:
        preview = prepared or self.preview(request)

        if preview.preflight_result.status == PreflightStatus.CRITICAL_ABORT:
            result = InstallExecutionResult(
                preflight_result=preview.preflight_result,
                runtime_validation=RuntimeValidationResult(RuntimeValidationStatus.SKIPPED),
                exit_code=2,
            )
            return result, text_renderer.render_preflight_abort(preview.preflight_result)

        if preview.plan is None:
            result = InstallExecutionResult(preflight_result=preview.preflight_result, exit_code=1)
            result.failed_items.append("Template ausente ou incompleto")
            return result, preview.lines

        if not auto_confirm:
            allowed = confirm_callback("Confirma instalação do perfil minimal?") if confirm_callback else False
            if not allowed:
                result = InstallExecutionResult(preflight_result=preview.preflight_result, exit_code=1)
                result.warning_items.append("Operação cancelada antes da escrita")
                return result, [*preview.lines, *text_renderer.render_cancelled()]

        write_result = writer.apply_install_plan(preview.plan)
        write_result.preflight_result = preview.preflight_result
        if preview.plan.personal_config_notices:
            write_result.warning_items.extend(
                [f"Configuracao pessoal preservada: {path}" for path in preview.plan.personal_config_notices]
            )

        failures = validator.validate_written_artifacts(preview.request.target_directory)
        if failures:
            write_result.failed_items.extend(failures)
            write_result.exit_code = 1

        write_result.runtime_validation = validator.validate_runtime(
            preview.emacs_executable,
            preview.request.target_directory,
        )

        if write_result.runtime_validation.status == RuntimeValidationStatus.FAILED:
            write_result.warning_items.append("Runtime validation falhou")

        write_result.rollback_guidance = rollback.build_rollback_instruction(
            write_result.created_items,
            write_result.copied_items,
        )

        if write_result.exit_code == 0:
            write_result.exit_code = 0

        return write_result, text_renderer.render_execution_summary(write_result)
