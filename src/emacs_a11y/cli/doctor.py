from __future__ import annotations

import typer

from emacs_a11y.doctor import orchestrator
from emacs_a11y.doctor.exit_codes import EXIT_INTERNAL_ERROR
from emacs_a11y.doctor.renderers import json as json_renderer
from emacs_a11y.doctor.renderers import text as text_renderer
from emacs_a11y.cli.install import install_command

app = typer.Typer(
    help="CLI acessivel para diagnostico e instalacao do Emacs Acessivel.",
    no_args_is_help=False,
    add_completion=False,
)


def execute_doctor_command(json_output: bool, emit=typer.echo) -> int:
    """Executa o diagnóstico e emite saída textual ou JSON."""

    try:
        report = orchestrator.run_diagnostic()
    except Exception as exc:  # pragma: no cover
        emit(f"Erro interno no diagnostico: {exc}")
        return EXIT_INTERNAL_ERROR

    if json_output:
        emit(json_renderer.render(report))
    else:
        emit(text_renderer.render(report))

    return report.exit_code


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Comandos principais do emacs-a11y."""

    if ctx.invoked_subcommand is not None:
        return

    from emacs_a11y.cli.interactive import run_interactive_session

    raise typer.Exit(code=run_interactive_session())


@app.command("doctor")
def doctor(json_output: bool = typer.Option(False, "--json", help="Mostra relatorio estruturado em JSON.")) -> None:
    """Executa diagnostico de ambiente em modo estritamente somente leitura."""

    raise typer.Exit(code=execute_doctor_command(json_output))


@app.command("install")
def install(
    target: str | None = typer.Argument(None, help="Subcomando de instalacao (ex.: emacs)."),
    profile: str = typer.Option("minimal", "--profile", help="Perfil de instalação."),
    yes: bool = typer.Option(False, "--yes", help="Confirma execução sem prompt no caso explícito e seguro."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Mostra recomendacoes sem executar comandos externos."),
    execute: bool = typer.Option(False, "--execute", help="Solicita execucao assistida quando suportado."),
    method: str = typer.Option("auto", "--method", help="Metodo preferencial: auto, winget, brew, apt."),
) -> None:
    """Instala perfil minimal em diretório isolado, com confirmação explícita."""

    install_command(target=target, profile=profile, yes=yes, dry_run=dry_run, execute=execute, method=method)


if __name__ == "__main__":
    app()
