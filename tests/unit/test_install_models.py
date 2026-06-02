from pathlib import Path

from emacs_a11y.models.install import (
    ConfirmationPolicy,
    InstallExecutionResult,
    InstallRequest,
    PreflightResult,
    PreflightStatus,
    RequiredDependency,
    RuntimeValidationStatus,
)


def test_required_dependency_for_minimal_marks_emacs_critical():
    dep = RequiredDependency(name="emacs", required_for_profiles=["minimal"], status="missing")
    assert dep.name == "emacs"
    assert dep.required_for_profiles == ["minimal"]
    assert dep.severity == "critical"


def test_preflight_critical_result_has_exit_code_2_and_missing_dependency():
    result = PreflightResult(
        status=PreflightStatus.CRITICAL_ABORT,
        missing_dependencies=["emacs"],
        exit_code=2,
    )
    assert result.status == PreflightStatus.CRITICAL_ABORT
    assert result.exit_code == 2
    assert result.missing_dependencies == ["emacs"]


def test_install_execution_result_can_represent_safe_abort_without_writes():
    result = InstallExecutionResult(
        preflight_result=PreflightResult(status=PreflightStatus.CRITICAL_ABORT, exit_code=2),
        exit_code=2,
    )
    assert result.created_items == []
    assert result.copied_items == []
    assert result.preflight_result.status == PreflightStatus.CRITICAL_ABORT


def test_install_request_explicit_yes_policy_is_modelled():
    request = InstallRequest(
        profile_name="minimal",
        mode="direct",
        confirmation_policy=ConfirmationPolicy.EXPLICIT_YES_ALLOWED,
        target_directory=Path("/tmp/profile"),
        explicit_yes=True,
    )
    assert request.profile_name == "minimal"
    assert request.confirmation_policy == ConfirmationPolicy.EXPLICIT_YES_ALLOWED
    assert request.explicit_yes is True


def test_runtime_validation_default_is_skipped_in_execution_result():
    result = InstallExecutionResult()
    assert result.runtime_validation.status == RuntimeValidationStatus.SKIPPED
