from __future__ import annotations

import typer

from emacs_a11y.doctor import orchestrator
from emacs_a11y.doctor.exit_codes import EXIT_INTERNAL_ERROR
from emacs_a11y.doctor.renderers import json as json_renderer
from emacs_a11y.doctor.renderers import text as text_renderer

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


if __name__ == "__main__":
    app()
