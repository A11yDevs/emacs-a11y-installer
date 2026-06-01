from __future__ import annotations

from emacs_a11y.doctor.checks.common import build_environment_state
from emacs_a11y.doctor.exit_codes import map_exit_code
from emacs_a11y.doctor.registry import load_checks
from emacs_a11y.models.diagnostic import (
    DiagnosticReport,
    DiagnosticResult,
    Severity,
    Status,
    SummaryCounts,
    utc_now_iso,
)


def _aggregate(results: list[DiagnosticResult]) -> SummaryCounts:
    summary = SummaryCounts()
    for result in results:
        if result.severity == Severity.CRITICAL:
            summary.critical += 1
        elif result.severity == Severity.WARNING:
            summary.warning += 1
        elif result.severity == Severity.INFO:
            summary.info += 1

        if result.status == Status.PASS:
            summary.pass_count += 1
        elif result.status == Status.FAIL:
            summary.fail += 1
        elif result.status == Status.UNKNOWN:
            summary.unknown += 1

    return summary


def _collect_next_steps(results: list[DiagnosticResult]) -> list[str]:
    unique: list[str] = []
    for result in results:
        for step in result.next_steps:
            if step not in unique:
                unique.append(step)
    return unique


def run_diagnostic() -> DiagnosticReport:
    state = build_environment_state()
    checks = load_checks(state.os)

    results = [check(state) for check in checks]
    summary = _aggregate(results)

    report = DiagnosticReport(
        report_version="1.0",
        generated_at=utc_now_iso(),
        environment=state,
        summary=summary,
        results=results,
        next_steps=_collect_next_steps(results),
        exit_code=map_exit_code(summary),
    )
    return report
