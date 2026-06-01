import json

from emacs_a11y.doctor.renderers import json as json_renderer
from emacs_a11y.models.diagnostic import (
    DiagnosticReport,
    DiagnosticResult,
    EnvironmentState,
    Severity,
    Status,
    SummaryCounts,
)


def test_render_json_contains_schema_fields():
    report = DiagnosticReport(
        report_version="1.0",
        generated_at="2026-06-01T00:00:00+00:00",
        environment=EnvironmentState(os="Linux", architecture="x86_64"),
        summary=SummaryCounts(critical=0, warning=0, info=1, pass_count=1, fail=0, unknown=0),
        results=[
            DiagnosticResult(
                check_id="system.info",
                name="Sistema",
                status=Status.PASS,
                severity=Severity.INFO,
                summary="ok",
            )
        ],
        next_steps=[],
        exit_code=0,
    )

    payload = json.loads(json_renderer.render(report))
    assert set(payload.keys()) == {"report_version", "generated_at", "environment", "summary", "results", "next_steps", "exit_code"}
    assert payload["results"][0]["read_only"] is True
