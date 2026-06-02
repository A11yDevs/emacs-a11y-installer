from __future__ import annotations

from emacs_a11y.install.emacs import run_install_emacs_flow
from emacs_a11y.models.emacs_install import (
    EmacsDetectionResult,
    EnvironmentDetectionResult,
    InstallCommand,
    InstallMethod,
    InstallationMethodRecommendation,
    PackageManager,
)


def _env() -> EnvironmentDetectionResult:
    return EnvironmentDetectionResult(
        operating_system="macos",
        distribution="unknown",
        architecture="x86_64",
        is_tty=True,
    )


def _missing_emacs() -> EmacsDetectionResult:
    return EmacsDetectionResult(status="not_found", selected_path=None)


def _brew_recommendation() -> InstallationMethodRecommendation:
    return InstallationMethodRecommendation(
        method=InstallMethod.HOMEBREW_CASK,
        package_manager=PackageManager.BREW,
        recommended_commands=[
            InstallCommand(
                argv=["brew", "install", "--cask", "emacs-app"],
                display_text="brew install --cask emacs-app",
                requires_privilege=False,
                supported_for_assisted_execution=True,
                expected_effect="install",
            )
        ],
        assisted_execution_supported=True,
    )


def test_execute_success_but_not_detected_with_brew_not_linked_hint(monkeypatch) -> None:
    monkeypatch.setattr("emacs_a11y.install.emacs.detect_environment", lambda: _env())
    monkeypatch.setattr(
        "emacs_a11y.install.emacs.detect_emacs",
        lambda: _missing_emacs(),
    )
    monkeypatch.setattr(
        "emacs_a11y.install.emacs.recommend_installation_method",
        lambda _environment, requested_method: _brew_recommendation(),
    )
    monkeypatch.setattr(
        "emacs_a11y.install.emacs.run_assisted_command",
        lambda _command: (
            True,
            "Warning: emacs 30.2_2 is already installed, it's just not linked."
            " | To link this version, run: |   brew link emacs",
            0,
        ),
    )
    monkeypatch.setattr("emacs_a11y.install.emacs.log_event", lambda _event, _details="": "log")

    result, lines = run_install_emacs_flow(
        execute=True,
        dry_run=False,
        method="auto",
        confirm_callback=lambda _prompt: True,
    )

    assert result.status == "failed"
    assert result.exit_code == 3
    assert any("brew link emacs" in step for step in result.next_steps)
    assert any("brew link emacs" in line for line in lines)


def test_execute_failed_with_cask_upgrade_hint_returns_reinstall_step(monkeypatch) -> None:
    monkeypatch.setattr("emacs_a11y.install.emacs.detect_environment", lambda: _env())
    monkeypatch.setattr(
        "emacs_a11y.install.emacs.detect_emacs",
        lambda: _missing_emacs(),
    )
    monkeypatch.setattr(
        "emacs_a11y.install.emacs.recommend_installation_method",
        lambda _environment, requested_method: _brew_recommendation(),
    )
    monkeypatch.setattr(
        "emacs_a11y.install.emacs.run_assisted_command",
        lambda _command: (
            False,
            "Warning: The cask 'emacs-app' cannot be upgraded as-is."
            " | To fix this, run: brew reinstall --cask --force emacs-app",
            1,
        ),
    )
    monkeypatch.setattr("emacs_a11y.install.emacs.log_event", lambda _event, _details="": "log")

    result, lines = run_install_emacs_flow(
        execute=True,
        dry_run=False,
        method="auto",
        confirm_callback=lambda _prompt: True,
    )

    assert result.status == "failed"
    assert result.exit_code == 3
    assert any("brew reinstall --cask --force emacs-app" in step for step in result.next_steps)
    assert any("brew reinstall --cask --force emacs-app" in line for line in lines)
