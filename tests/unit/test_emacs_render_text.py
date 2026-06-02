from __future__ import annotations

from emacs_a11y.install.renderers.emacs_text import (
    build_consent_summary,
    render_consent,
    render_installed_emacs,
    render_recommendation,
)
from emacs_a11y.models.emacs_install import (
    EmacsDetectionResult,
    EnvironmentDetectionResult,
    InstallCommand,
    InstallMethod,
    InstallationMethodRecommendation,
    PackageManager,
    VersionSupportAssessment,
)


def _env() -> EnvironmentDetectionResult:
    return EnvironmentDetectionResult(
        operating_system="windows",
        distribution="unknown",
        architecture="x64",
        is_tty=True,
    )


def _recommendation() -> InstallationMethodRecommendation:
    return InstallationMethodRecommendation(
        method=InstallMethod.WINGET_GNU_EMACS,
        package_manager=PackageManager.WINGET,
        recommended_commands=[
            InstallCommand(
                argv=["winget", "install", "-e", "--id", "GNU.Emacs"],
                display_text="winget install -e --id GNU.Emacs",
                requires_privilege=False,
                supported_for_assisted_execution=True,
                expected_effect="instalar",
            )
        ],
        assisted_execution_supported=True,
    )


def test_renderer_includes_info_warning_command_next_step_markers() -> None:
    lines = render_recommendation(_env(), _recommendation())
    assert any(line.startswith("INFO") for line in lines)
    assert any(line.startswith("COMMAND") for line in lines)


def test_consent_renderer_contains_confirm_and_command() -> None:
    summary = build_consent_summary(_env(), _recommendation())
    lines = render_consent(summary)
    assert any(line.startswith("CONFIRM") for line in lines)
    assert any(line.startswith("COMMAND") for line in lines)


def test_render_installed_emacs_includes_extra_next_steps() -> None:
    lines = render_installed_emacs(
        EmacsDetectionResult(status="found", selected_path="/usr/local/bin/emacs", version_text="30.2"),
        VersionSupportAssessment(
            state="supported",
            detected_version="30.2",
            minimum_supported_version="29",
            message="ok",
        ),
        extra_next_steps=["Para abrir interface grafica: open -a /Applications/Emacs.app"],
    )
    assert any("open -a /Applications/Emacs.app" in line for line in lines)
