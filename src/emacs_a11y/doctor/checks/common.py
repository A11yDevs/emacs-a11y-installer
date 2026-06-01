from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from emacs_a11y.models.diagnostic import (
    DiagnosticResult,
    EnvironmentState,
    Severity,
    Status,
)


def command_path(cmd: str) -> str | None:
    return shutil.which(cmd)


def command_version(executable: str, flag: str = "--version") -> str | None:
    try:
        process = subprocess.run(
            [executable, flag],
            check=False,
            capture_output=True,
            text=True,
            timeout=1,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    output = (process.stdout or process.stderr or "").strip()
    if not output:
        return None
    return output.splitlines()[0][:200]


def build_environment_state() -> EnvironmentState:
    os_name = platform.system()
    profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
    profile = Path(profile_path)

    emacs_path = command_path("emacs")
    emacs_version = command_version(emacs_path) if emacs_path else None

    python_path = command_path("python") or command_path("python3")
    git_path = command_path("git")

    user_paths = [str(Path.home() / ".emacs"), str(Path.home() / ".emacs.d" / "init.el")]
    existing_user_paths = [p for p in user_paths if Path(p).exists()]

    emacspeak_paths = [
        Path.home() / ".emacs.d" / "emacspeak",
        Path("/usr/share/emacs/site-lisp/emacspeak"),
    ]
    emacspeak_signals = [str(p) for p in emacspeak_paths if p.exists()]
    if os.environ.get("EMACSPEAK_DIR"):
        emacspeak_signals.append(os.environ["EMACSPEAK_DIR"])

    return EnvironmentState(
        os=os_name,
        os_version=platform.version(),
        architecture=platform.machine() or "unknown",
        path_entries=[part for part in os.environ.get("PATH", "").split(os.pathsep) if part],
        emacs_version=emacs_version,
        git_available=git_path is not None,
        python_available=python_path is not None,
        profile_path=profile_path,
        profile_exists=profile.exists(),
        profile_accessible=os.access(profile, os.R_OK | os.X_OK) if profile.exists() else False,
        user_emacs_paths=existing_user_paths,
        tts_signals=[],
        emacspeak_signals=emacspeak_signals,
    )


def check_system_info(state: EnvironmentState) -> DiagnosticResult:
    return DiagnosticResult(
        check_id="system.info",
        name="Sistema operacional e arquitetura",
        status=Status.PASS,
        severity=Severity.INFO,
        summary=f"Sistema detectado: {state.os} ({state.architecture})",
        evidence=[f"os={state.os}", f"architecture={state.architecture}"],
    )


def check_emacs(state: EnvironmentState) -> DiagnosticResult:
    if state.emacs_version:
        return DiagnosticResult(
            check_id="tool.emacs",
            name="Emacs",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Emacs disponivel",
            evidence=[state.emacs_version],
        )

    return DiagnosticResult(
        check_id="tool.emacs",
        name="Emacs",
        status=Status.FAIL,
        severity=Severity.CRITICAL,
        summary="Emacs nao encontrado no PATH",
        evidence=["emacs ausente"],
        next_steps=["Instale Emacs e garanta que o executavel esteja no PATH."],
    )


def check_git(state: EnvironmentState) -> DiagnosticResult:
    if state.git_available:
        return DiagnosticResult(
            check_id="tool.git",
            name="Git",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Git disponivel",
            evidence=["git encontrado no PATH"],
        )

    return DiagnosticResult(
        check_id="tool.git",
        name="Git",
        status=Status.FAIL,
        severity=Severity.WARNING,
        summary="Git nao encontrado no PATH (nao bloqueante)",
        evidence=["git ausente"],
        next_steps=["Opcional: instale Git para fluxos de contribuicao e suporte."],
    )


def check_python(state: EnvironmentState) -> DiagnosticResult:
    if state.python_available:
        return DiagnosticResult(
            check_id="tool.python",
            name="Python",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Python disponivel",
            evidence=[f"python runtime={sys.version.split()[0]}"],
        )

    return DiagnosticResult(
        check_id="tool.python",
        name="Python",
        status=Status.FAIL,
        severity=Severity.CRITICAL,
        summary="Python nao encontrado no PATH",
        evidence=["python ausente"],
        next_steps=["Instale Python 3.11+ para usar a distribuicao canonica via pacote Python."],
    )


def check_profile(state: EnvironmentState) -> DiagnosticResult:
    if state.profile_exists and state.profile_accessible:
        return DiagnosticResult(
            check_id="profile.a11y",
            name="Perfil Emacs Acessivel",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Perfil do Emacs Acessivel presente e acessivel",
            evidence=[state.profile_path],
        )

    if state.profile_exists and not state.profile_accessible:
        return DiagnosticResult(
            check_id="profile.a11y",
            name="Perfil Emacs Acessivel",
            status=Status.FAIL,
            severity=Severity.WARNING,
            summary="Perfil encontrado, mas sem permissao de acesso",
            evidence=[state.profile_path],
            next_steps=["Revise permissoes de leitura/execucao do diretorio do perfil."],
        )

    return DiagnosticResult(
        check_id="profile.a11y",
        name="Perfil Emacs Acessivel",
        status=Status.UNKNOWN,
        severity=Severity.WARNING,
        summary="Perfil do Emacs Acessivel ainda nao criado",
        evidence=[state.profile_path],
        next_steps=["Siga o fluxo de instalacao quando o diagnostico estiver sem bloqueios criticos."],
    )


def check_user_config(state: EnvironmentState) -> DiagnosticResult:
    if not state.user_emacs_paths:
        return DiagnosticResult(
            check_id="user.config",
            name="Configuracao pessoal do Emacs",
            status=Status.UNKNOWN,
            severity=Severity.INFO,
            summary="Nenhuma configuracao pessoal padrao detectada",
            evidence=["~/.emacs e ~/.emacs.d/init.el ausentes"],
        )

    return DiagnosticResult(
        check_id="user.config",
        name="Configuracao pessoal do Emacs",
        status=Status.PASS,
        severity=Severity.INFO,
        summary="Configuracao pessoal existente detectada e preservada",
        evidence=state.user_emacs_paths,
        next_steps=["Nao sobrescreva arquivos pessoais; use perfil isolado do Emacs Acessivel."],
    )


def check_emacspeak(state: EnvironmentState) -> DiagnosticResult:
    if state.emacspeak_signals:
        return DiagnosticResult(
            check_id="tool.emacspeak",
            name="Emacspeak",
            status=Status.PASS,
            severity=Severity.INFO,
            summary="Sinais de instalacao do Emacspeak detectados",
            evidence=state.emacspeak_signals,
        )

    return DiagnosticResult(
        check_id="tool.emacspeak",
        name="Emacspeak",
        status=Status.UNKNOWN,
        severity=Severity.INFO,
        summary="Sem sinais claros de Emacspeak",
        evidence=["nenhum caminho padrao encontrado"],
        next_steps=["Opcional: valide manualmente o Emacspeak apos instalar o perfil do projeto."],
    )


def common_checks() -> list:
    return [
        check_system_info,
        check_emacs,
        check_git,
        check_python,
        check_profile,
        check_user_config,
        check_emacspeak,
    ]
