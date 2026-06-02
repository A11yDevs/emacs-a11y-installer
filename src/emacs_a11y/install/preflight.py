from __future__ import annotations

from emacs_a11y.doctor.checks.common import build_environment_state
from emacs_a11y.models.install import (
    PreflightCheck,
    PreflightResult,
    PreflightStatus,
    RequiredDependency,
)


def required_dependencies_for(profile_name: str, emacs_available: bool) -> list[RequiredDependency]:
    if profile_name != "minimal":
        return []

    return [
        RequiredDependency(
            name="emacs",
            required_for_profiles=["minimal"],
            status="available" if emacs_available else "missing",
            severity="critical",
        )
    ]


def build_preflight_check(profile_name: str, target_directory: str | None = None) -> PreflightCheck:
    state = build_environment_state()
    emacs_available = bool(state.emacs_version)
    dependencies = required_dependencies_for(profile_name, emacs_available)
    doctor_signals = {
        "emacs_version": state.emacs_version,
        "profile_path": state.profile_path,
        "profile_exists": state.profile_exists,
        "profile_accessible": state.profile_accessible,
        "user_emacs_paths": list(state.user_emacs_paths),
    }

    from emacs_a11y.models.install import ConfirmationPolicy, InstallRequest
    from pathlib import Path

    request = InstallRequest(
        profile_name=profile_name,
        mode="direct",
        confirmation_policy=ConfirmationPolicy.PROMPT_REQUIRED,
        target_directory=Path(target_directory or state.profile_path),
    )
    return PreflightCheck(request=request, required_dependencies=dependencies, doctor_signals=doctor_signals)


def run_preflight(check: PreflightCheck) -> PreflightResult:
    missing = [dep.name for dep in check.required_dependencies if dep.status == "missing"]
    if missing:
        return PreflightResult(
            status=PreflightStatus.CRITICAL_ABORT,
            missing_dependencies=missing,
            message_lines=[
                "CRITICAL: Emacs nao encontrado",
                "Nenhum arquivo foi criado.",
                "Nenhuma configuracao pessoal foi modificada.",
            ],
            suggested_next_steps=[
                "emacs-a11y install emacs",
                "emacs-a11y doctor",
                "emacs-a11y install --profile minimal",
            ],
            exit_code=2,
        )

    return PreflightResult(
        status=PreflightStatus.PASS,
        missing_dependencies=[],
        message_lines=["Preflight concluido: Emacs disponivel."],
        suggested_next_steps=[],
        exit_code=0,
    )
