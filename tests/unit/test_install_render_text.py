from emacs_a11y.install.renderers import text
from emacs_a11y.models.install import InstallExecutionResult, PreflightResult, PreflightStatus


def test_render_preflight_abort_contains_critical_and_next_steps():
    result = PreflightResult(
        status=PreflightStatus.CRITICAL_ABORT,
        message_lines=["CRITICAL: Emacs nao encontrado"],
        suggested_next_steps=["emacs-a11y install emacs"],
        exit_code=2,
    )
    lines = text.render_preflight_abort(result)
    assert any("CRITICAL" in line for line in lines)
    assert any("NEXT STEP" in line for line in lines)


def test_render_execution_summary_exposes_canonical_markers():
    result = InstallExecutionResult(
        created_items=["a"],
        copied_items=["b"],
        skipped_items=[],
        preserved_items=[],
        failed_items=[],
        warning_items=[],
    )
    lines = text.render_execution_summary(result)
    markers = ["CREATED", "COPIED", "SKIPPED", "PRESERVED", "FAILED", "WARNING", "NEXT STEP"]
    for marker in markers:
        assert any(line == marker for line in lines)
