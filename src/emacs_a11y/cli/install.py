from __future__ import annotations

import typer

from emacs_a11y.install.orchestrator import InstallOrchestrator


def install_command(
    profile: str = typer.Option("minimal", "--profile", help="Perfil de instalação."),
    yes: bool = typer.Option(False, "--yes", help="Confirma execução sem prompt no caso explícito e seguro."),
) -> None:
    if profile != "minimal":
        typer.echo("WARNING: Apenas o perfil minimal esta em escopo nesta feature.")
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
