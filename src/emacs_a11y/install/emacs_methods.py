from __future__ import annotations

import shutil

from emacs_a11y.models.emacs_install import (
    EnvironmentDetectionResult,
    InstallCommand,
    InstallMethod,
    InstallationMethodRecommendation,
    PackageManager,
)


def _manual_recommendation(reason: str) -> InstallationMethodRecommendation:
    return InstallationMethodRecommendation(
        method=InstallMethod.MANUAL_GUIDANCE,
        package_manager=PackageManager.UNSUPPORTED,
        recommended_commands=[],
        manual_steps=[
            "Consulte a documentacao oficial do seu sistema para instalar GNU Emacs.",
            "Apos instalar, execute emacs-a11y doctor.",
            "Em seguida execute emacs-a11y install --profile minimal.",
        ],
        assisted_execution_supported=False,
        rationale=reason,
    )


def recommend_installation_method(
    environment: EnvironmentDetectionResult,
    requested_method: str = "auto",
) -> InstallationMethodRecommendation:
    requested_method = requested_method.lower().strip()

    if environment.operating_system == "windows":
        winget_available = shutil.which("winget") is not None
        if winget_available and requested_method in {"auto", "winget"}:
            command = InstallCommand(
                argv=["winget", "install", "-e", "--id", "GNU.Emacs"],
                display_text="winget install -e --id GNU.Emacs",
                requires_privilege=False,
                supported_for_assisted_execution=True,
                expected_effect="Instalar GNU Emacs via winget.",
            )
            return InstallationMethodRecommendation(
                method=InstallMethod.WINGET_GNU_EMACS,
                package_manager=PackageManager.WINGET,
                recommended_commands=[command],
                assisted_execution_supported=True,
                rationale="Windows com winget disponivel.",
            )
        return _manual_recommendation("Windows sem winget disponivel para execucao assistida.")

    if environment.operating_system == "macos":
        brew_available = shutil.which("brew") is not None
        if brew_available and requested_method in {"auto", "brew"}:
            command = InstallCommand(
                argv=["brew", "install", "--cask", "emacs-app"],
                display_text="brew install --cask emacs-app",
                requires_privilege=False,
                supported_for_assisted_execution=True,
                expected_effect="Instalar GNU Emacs com interface grafica via Homebrew cask.",
            )
            return InstallationMethodRecommendation(
                method=InstallMethod.HOMEBREW_CASK,
                package_manager=PackageManager.BREW,
                recommended_commands=[command],
                manual_steps=["Para abrir a interface grafica no macOS, use: open -a /Applications/Emacs.app"],
                assisted_execution_supported=True,
                rationale="macOS com Homebrew disponivel (instalacao grafica via cask).",
            )
        return _manual_recommendation("macOS sem Homebrew disponivel para execucao assistida.")

    if environment.operating_system == "linux" and environment.distribution in {"debian", "ubuntu"}:
        if requested_method not in {"auto", "apt"}:
            return _manual_recommendation("Metodo solicitado nao suportado para Debian/Ubuntu na v1.")

        commands = [
            InstallCommand(
                argv=["sudo", "apt", "update"],
                display_text="sudo apt update",
                requires_privilege=True,
                supported_for_assisted_execution=False,
                expected_effect="Atualizar indices de pacotes.",
            ),
            InstallCommand(
                argv=["sudo", "apt", "install", "emacs"],
                display_text="sudo apt install emacs",
                requires_privilege=True,
                supported_for_assisted_execution=False,
                expected_effect="Instalar GNU Emacs via apt.",
            ),
        ]
        return InstallationMethodRecommendation(
            method=InstallMethod.APT_GUIDANCE,
            package_manager=PackageManager.APT,
            recommended_commands=commands,
            manual_steps=["Debian/Ubuntu permanece guidance-only na v1."],
            assisted_execution_supported=False,
            rationale="Debian/Ubuntu com orientacao via apt sem execucao assistida.",
        )

    return _manual_recommendation("Plataforma nao suportada para automacao.")
