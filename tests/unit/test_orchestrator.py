from emacs_a11y.doctor import orchestrator
from emacs_a11y.models.diagnostic import DiagnosticResult, Severity, Status


def test_orchestrator_aggregates_results(monkeypatch):
    class FakeState:
        os = "Linux"

    monkeypatch.setattr(orchestrator, "build_environment_state", lambda: FakeState())
    monkeypatch.setattr(
        orchestrator,
        "load_checks",
        lambda _os: [
            lambda _s: DiagnosticResult("a", "A", Status.PASS, Severity.INFO, "ok"),
            lambda _s: DiagnosticResult("b", "B", Status.FAIL, Severity.WARNING, "warn"),
        ],
    )

    report = orchestrator.run_diagnostic()
    assert report.summary.info == 1
    assert report.summary.warning == 1
    assert report.exit_code == 1
