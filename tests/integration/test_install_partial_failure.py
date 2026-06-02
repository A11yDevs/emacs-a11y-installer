from pathlib import Path

from emacs_a11y.install import planner, preflight
from emacs_a11y.install.orchestrator import InstallOrchestrator


class _Env:
    def __init__(self):
        self.emacs_version = "GNU Emacs"
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = False
        self.profile_accessible = False
        self.user_emacs_paths = []


def test_partial_failure_generates_failed_items_and_rollback(monkeypatch, tmp_path):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env())
    monkeypatch.setattr(planner, "resolve_default_target_directory", lambda: tmp_path / "profile")

    from emacs_a11y.install import writer

    original = writer.apply_install_plan

    def _broken(plan):
        result = original(plan)
        result.failed_items.append("simulated failure")
        result.exit_code = 1
        return result

    monkeypatch.setattr(writer, "apply_install_plan", _broken)

    orchestrator = InstallOrchestrator()
    request = orchestrator.normalize_request("minimal", "direct", explicit_yes=True)
    result, _lines = orchestrator.execute(request, auto_confirm=True)

    assert result.exit_code == 1
    assert result.failed_items
    assert result.rollback_guidance.paths_to_remove is not None
