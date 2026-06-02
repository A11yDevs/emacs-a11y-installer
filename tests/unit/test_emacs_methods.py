from __future__ import annotations

from emacs_a11y.install.emacs_methods import recommend_installation_method
from emacs_a11y.models.emacs_install import EnvironmentDetectionResult


def _env(os_name: str, distribution: str = "unknown") -> EnvironmentDetectionResult:
    return EnvironmentDetectionResult(
        operating_system=os_name,
        distribution=distribution,
        architecture="x64",
        is_tty=True,
    )


def test_windows_with_winget_recommends_canonical_command(monkeypatch) -> None:
    monkeypatch.setattr(
        "emacs_a11y.install.emacs_methods.shutil.which",
        lambda cmd: "C:/winget" if cmd == "winget" else None,
    )
    recommendation = recommend_installation_method(_env("windows"))
    assert recommendation.recommended_commands[0].display_text == "winget install -e --id GNU.Emacs"
    assert recommendation.assisted_execution_supported is True


def test_windows_without_winget_falls_back_to_manual(monkeypatch) -> None:
    monkeypatch.setattr("emacs_a11y.install.emacs_methods.shutil.which", lambda _cmd: None)
    recommendation = recommend_installation_method(_env("windows"))
    assert recommendation.method.value == "MANUAL_GUIDANCE"
    assert recommendation.assisted_execution_supported is False


def test_macos_with_brew_recommends_brew(monkeypatch) -> None:
    monkeypatch.setattr(
        "emacs_a11y.install.emacs_methods.shutil.which",
        lambda cmd: "/opt/homebrew/bin/brew" if cmd == "brew" else None,
    )
    recommendation = recommend_installation_method(_env("macos"))
    assert recommendation.recommended_commands[0].display_text == "brew install --cask emacs-app"
    assert recommendation.method.value == "HOMEBREW_CASK"


def test_debian_ubuntu_is_guidance_only() -> None:
    recommendation = recommend_installation_method(_env("linux", "debian"))
    assert recommendation.assisted_execution_supported is False
    assert recommendation.recommended_commands[0].display_text == "sudo apt update"
