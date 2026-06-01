from emacs_a11y.doctor.checks import common
from emacs_a11y.models.diagnostic import EnvironmentState, Severity, Status


def test_check_git_non_blocking_warning():
    state = EnvironmentState(os="Linux", architecture="x86_64", git_available=False)
    result = common.check_git(state)
    assert result.status == Status.FAIL
    assert result.severity == Severity.WARNING


def test_check_python_critical_when_missing():
    state = EnvironmentState(os="Linux", architecture="x86_64", python_available=False)
    result = common.check_python(state)
    assert result.status == Status.FAIL
    assert result.severity == Severity.CRITICAL


def test_check_profile_permission_denied_warning():
    state = EnvironmentState(
        os="Linux",
        architecture="x86_64",
        profile_path="/tmp/profile",
        profile_exists=True,
        profile_accessible=False,
    )
    result = common.check_profile(state)
    assert result.status == Status.FAIL
    assert result.severity == Severity.WARNING


def test_build_environment_state_multiple_emacs_paths(monkeypatch, tmp_path):
    emacs_file = tmp_path / ".emacs"
    init_file = tmp_path / ".emacs.d" / "init.el"
    init_file.parent.mkdir(parents=True)
    emacs_file.write_text("", encoding="utf-8")
    init_file.write_text("", encoding="utf-8")

    monkeypatch.setattr(common.Path, "home", lambda: tmp_path)

    def fake_command_path(cmd: str):
        mapping = {
            "emacs": "/usr/bin/emacs",
            "python": "/usr/bin/python3",
            "git": "/usr/bin/git",
            "python3": "/usr/bin/python3",
        }
        return mapping.get(cmd)

    monkeypatch.setattr(common, "command_path", fake_command_path)
    monkeypatch.setattr(common, "command_version", lambda *_args, **_kwargs: "GNU Emacs 29.3")

    state = common.build_environment_state()
    assert str(emacs_file) in state.user_emacs_paths
    assert str(init_file) in state.user_emacs_paths


def test_check_emacspeak_unknown_without_signals():
    state = EnvironmentState(os="Linux", architecture="x86_64", emacspeak_signals=[])
    result = common.check_emacspeak(state)
    assert result.status == Status.UNKNOWN
    assert result.severity == Severity.INFO
