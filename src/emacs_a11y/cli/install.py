from __future__ import annotations

import threading
import time

import typer

from emacs_a11y.install.emacs import run_install_emacs_flow
from emacs_a11y.install.orchestrator import InstallOrchestrator


HEARTBEAT_INTERVAL_SECONDS = 5.0


def _start_assisted_execution_heartbeat() -> tuple[threading.Event, threading.Thread]:
    stop_event = threading.Event()

    def _heartbeat_worker() -> None:
        typer.echo("INFO: Execucao assistida iniciada. Aguarde...")
        started_at = time.monotonic()
        while not stop_event.wait(HEARTBEAT_INTERVAL_SECONDS):
            elapsed_seconds = int(time.monotonic() - started_at)
            typer.echo(f"INFO: Execucao assistida em andamento... {elapsed_seconds}s")

    thread = threading.Thread(target=_heartbeat_worker, daemon=True)
    thread.start()
    return stop_event, thread


def install_command(
    target: str | None = None,
    profile: str = typer.Option("minimal", "--profile", help="Perfil de instalação."),
    yes: bool = typer.Option(False, "--yes", help="Confirma execução sem prompt no caso explícito e seguro."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Mostra recomendacoes sem executar comandos externos."),
    execute: bool = typer.Option(False, "--execute", help="Solicita execucao assistida quando suportado."),
    method: str = typer.Option("auto", "--method", help="Metodo preferencial: auto, winget, brew, apt."),
) -> None:
    if target == "emacs-execute":
        target = "emacs"
        execute = True

    if target not in {None, "emacs"}:
        typer.echo(f"WARNING: Subcomando de install desconhecido: {target}.")
        typer.echo("NEXT STEP: Use 'emacs-a11y install emacs' para o assistente de instalacao do Emacs.")
        raise typer.Exit(code=1)

    if target == "emacs":
        if yes:
            typer.echo("WARNING: --yes nao faz parte do escopo da feature install emacs na v1.")
            raise typer.Exit(code=1)

        heartbeat: tuple[threading.Event, threading.Thread] | None = None
        if execute and not dry_run:
            heartbeat = _start_assisted_execution_heartbeat()

        try:
            result, lines = run_install_emacs_flow(
                execute=execute,
                dry_run=dry_run,
                method=method,
                confirm_callback=lambda prompt: typer.confirm(prompt, default=False),
            )
        finally:
            if heartbeat is not None:
                stop_event, thread = heartbeat
                stop_event.set()
                thread.join(timeout=0.2)
                typer.echo("INFO: Execucao assistida finalizada. Preparando resumo...")

        for line in lines:
            typer.echo(line)
        raise typer.Exit(code=result.exit_code)

    if profile != "minimal":
        typer.echo("WARNING: Apenas o perfil minimal esta em escopo nesta feature.")
        raise typer.Exit(code=1)

    if dry_run or execute or method != "auto":
        typer.echo("WARNING: --dry-run, --execute e --method sao aceitos apenas com 'install emacs'.")
        raise typer.Exit(code=1)

    orchestrator = InstallOrchestrator()
    request = orchestrator.normalize_request(profile_name=profile, mode="direct", explicit_yes=yes)

    if request.confirmation_policy.value == "DENY_UNSAFE_AUTOMATION":
        typer.echo("WARNING: --yes rejeitado para comando ambiguo ou fora de escopo.")
        raise typer.Exit(code=1)

    auto_confirm = yes
    result, lines = orchestrator.execute(
        request=request,
        auto_confirm=auto_confirm,
        confirm_callback=lambda prompt: typer.confirm(prompt, default=False),
    )

    for line in lines:
        typer.echo(line)

    raise typer.Exit(code=result.exit_code)
