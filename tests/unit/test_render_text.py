from emacs_a11y.doctor.renderers import text
from emacs_a11y.models.diagnostic import (
    DiagnosticReport,
    DiagnosticResult,
    EnvironmentState,
    Severity,
    Status,
    SummaryCounts,
)


def _sample_report() -> DiagnosticReport:
    results = [
        DiagnosticResult("tool.python", "Python", Status.FAIL, Severity.CRITICAL, "Python ausente"),
        DiagnosticResult("tool.git", "Git", Status.FAIL, Severity.WARNING, "Git ausente"),
        DiagnosticResult("system.info", "Sistema", Status.PASS, Severity.INFO, "Linux x86_64"),
    ]
    return DiagnosticReport(
        report_version="1.0",
        generated_at="2026-06-01T00:00:00+00:00",
        environment=EnvironmentState(os="Linux", architecture="x86_64"),
        summary=SummaryCounts(critical=1, warning=1, info=1, pass_count=1, fail=2, unknown=0),
        results=results,
        next_steps=["Instale Python 3.11+"],
        exit_code=2,
    )


def test_text_renderer_contains_required_sections_in_order():
    rendered = text.render(_sample_report())
    positions = [rendered.index(section) for section in ["Resumo", "Críticos", "Avisos", "Info", "Próximos passos"]]
    assert positions == sorted(positions)


def test_text_renderer_contains_explicit_severity_tokens_and_no_color_codes():
    rendered = text.render(_sample_report())
    assert "CRITICAL" in rendered
    assert "WARNING" in rendered
    assert "INFO" in rendered
    assert "\x1b[" not in rendered
