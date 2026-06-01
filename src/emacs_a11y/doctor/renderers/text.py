from __future__ import annotations

from emacs_a11y.models.diagnostic import DiagnosticReport, DiagnosticResult, Severity


def _section_lines(title: str, items: list[DiagnosticResult]) -> list[str]:
    lines = [title]
    if not items:
        lines.append("- nenhum item")
        return lines

    for item in items:
        lines.append(f"- {item.severity.value} [{item.status.value}] {item.name}: {item.summary}")
        for ev in item.evidence:
            lines.append(f"  evidencia: {ev}")
    return lines


def render(report: DiagnosticReport) -> str:
    critical = [r for r in report.results if r.severity == Severity.CRITICAL]
    warning = [r for r in report.results if r.severity == Severity.WARNING]
    info = [r for r in report.results if r.severity == Severity.INFO]

    lines: list[str] = []
    lines.append("Resumo")
    lines.append(
        "- critical={0} warning={1} info={2} pass={3} fail={4} unknown={5}".format(
            report.summary.critical,
            report.summary.warning,
            report.summary.info,
            report.summary.pass_count,
            report.summary.fail,
            report.summary.unknown,
        )
    )
    lines.extend(_section_lines("Críticos", critical))
    lines.extend(_section_lines("Avisos", warning))
    lines.extend(_section_lines("Info", info))
    lines.append("Próximos passos")
    if report.next_steps:
        for step in report.next_steps:
            lines.append(f"- {step}")
    else:
        lines.append("- nenhum")
    return "\n".join(lines)
