from emacs_a11y.models.diagnostic import (
    DiagnosticReport,
    DiagnosticResult,
    EnvironmentState,
    Severity,
    Status,
    SummaryCounts,
)


def test_report_to_dict_contains_expected_keys():
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

    payload = report.to_dict()
    assert payload["environment"]["os"] == "Linux"
    assert payload["summary"]["pass"] == 1
    assert payload["results"][0]["read_only"] is True
