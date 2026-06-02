from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path

from emacs_a11y.doctor.checks.common import build_environment_state, command_version
from emacs_a11y.models.emacs_install import EmacsCandidate, EmacsDetectionResult, EnvironmentDetectionResult


def detect_environment() -> EnvironmentDetectionResult:
    os_name = platform.system().lower()
    if "darwin" in os_name:
        operating_system = "macos"
    elif "windows" in os_name:
        operating_system = "windows"
    elif "linux" in os_name:
        operating_system = "linux"
    else:
        operating_system = "unknown"

    distribution = "unknown"
    if operating_system == "linux":
        distro_text = ""
        os_release = Path("/etc/os-release")
        if os_release.exists():
            distro_text = os_release.read_text(encoding="utf-8", errors="ignore").lower()
        if "ubuntu" in distro_text:
            distribution = "ubuntu"
        elif "debian" in distro_text:
            distribution = "debian"
        elif distro_text:
            distribution = "other_linux"

    return EnvironmentDetectionResult(
        operating_system=operating_system,
        distribution=distribution,
        architecture=platform.machine() or "unknown",
        is_tty=sys.stdin.isatty() and sys.stdout.isatty(),
        path_entries_visible=[entry for entry in os.environ.get("PATH", "").split(os.pathsep) if entry],
    )


def discover_emacs_candidates() -> list[EmacsCandidate]:
    candidates: list[EmacsCandidate] = []
    seen: set[str] = set()
    path_entries = [entry for entry in os.environ.get("PATH", "").split(os.pathsep) if entry]

    for idx, entry in enumerate(path_entries):
        candidate = Path(entry) / ("emacs.exe" if platform.system().lower().startswith("win") else "emacs")
        if candidate.exists() and os.access(candidate, os.X_OK):
            normalized = str(candidate)
            if normalized in seen:
                continue
            seen.add(normalized)
            candidates.append(EmacsCandidate(path=normalized, source="PATH", priority=idx))

    which_result = shutil.which("emacs")
    if which_result and which_result not in seen:
        candidates.append(EmacsCandidate(path=which_result, source="which", priority=len(candidates)))

    candidates.sort(key=lambda item: (item.priority, item.path))
    return candidates


def detect_emacs() -> EmacsDetectionResult:
    candidates = discover_emacs_candidates()
    if not candidates:
        doctor_state = build_environment_state()
        if doctor_state.emacs_version:
            return EmacsDetectionResult(
                status="found",
                selected_path=shutil.which("emacs"),
                candidates=[],
                version_text=doctor_state.emacs_version,
            )
        return EmacsDetectionResult(status="missing", selected_path=None, warnings=["Emacs nao encontrado no PATH."])

    selected = candidates[0]
    status = "multiple_found" if len(candidates) > 1 else "found"
    warnings: list[str] = []
    if len(candidates) > 1:
        warnings.append("Multiplos executaveis de Emacs encontrados; candidato de maior prioridade selecionado.")

    version = command_version(selected.path)
    return EmacsDetectionResult(
        status=status,
        selected_path=selected.path,
        candidates=candidates,
        version_text=version,
        warnings=warnings,
    )
