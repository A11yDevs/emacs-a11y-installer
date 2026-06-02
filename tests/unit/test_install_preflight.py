from pathlib import Path

from emacs_a11y.install import preflight
from emacs_a11y.models.install import ConfirmationPolicy, InstallRequest, PreflightCheck


class _Env:
    def __init__(self, emacs_version: str | None):
        self.emacs_version = emacs_version
        self.profile_path = str(Path.home() / ".emacs.d" / "emacs-a11y-profile")
        self.profile_exists = False
        self.profile_accessible = False
        self.user_emacs_paths = []


def _request() -> InstallRequest:
    return InstallRequest(
        profile_name="minimal",
        mode="direct",
        confirmation_policy=ConfirmationPolicy.PROMPT_REQUIRED,
        target_directory=Path("/tmp/profile"),
    )


def test_missing_emacs_aborts_with_critical_and_next_steps(monkeypatch):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env(None))
    check = preflight.build_preflight_check("minimal")
    result = preflight.run_preflight(check)

    assert result.exit_code == 2
    assert "CRITICAL: Emacs nao encontrado" in result.message_lines[0]
    assert "emacs-a11y install emacs" in result.suggested_next_steps
    assert "emacs-a11y doctor" in result.suggested_next_steps
    assert "emacs-a11y install --profile minimal" in result.suggested_next_steps


def test_emacs_present_passes_preflight(monkeypatch):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs 30.0"))
    check = preflight.build_preflight_check("minimal")
    result = preflight.run_preflight(check)
    assert result.exit_code == 0
    assert result.missing_dependencies == []


def test_preflight_check_reuses_doctor_signals(monkeypatch):
    monkeypatch.setattr(preflight, "build_environment_state", lambda: _Env("GNU Emacs 30.0"))
    check = preflight.build_preflight_check("minimal")
    assert "emacs_version" in check.doctor_signals
    assert "profile_path" in check.doctor_signals


def test_no_package_manager_commands_in_preflight_path():
    request = _request()
    check = PreflightCheck(request=request, required_dependencies=[])
    result = preflight.run_preflight(check)
    joined = " ".join(result.message_lines + result.suggested_next_steps).lower()
    forbidden = ["winget", "brew", "apt", "dnf", "pacman", "sudo"]
    assert not any(token in joined for token in forbidden)
