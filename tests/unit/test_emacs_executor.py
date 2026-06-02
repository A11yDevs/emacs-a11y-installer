from __future__ import annotations

from emacs_a11y.install.emacs_executor import redact_sensitive_text, run_assisted_command
from emacs_a11y.models.emacs_install import InstallCommand


def test_redaction_hides_sensitive_data() -> None:
    text = "token=abcd password:1234"
    redacted = redact_sensitive_text(text)
    assert "abcd" not in redacted
    assert "1234" not in redacted


def test_executor_uses_shell_false_and_argv_shape(monkeypatch) -> None:
    observed = {}

    class _Process:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def _fake_run(argv, check, capture_output, text, shell):
        observed["argv"] = argv
        observed["shell"] = shell
        return _Process()

    monkeypatch.setattr("emacs_a11y.install.emacs_executor.subprocess.run", _fake_run)

    command = InstallCommand(
        argv=["echo", "ok"],
        display_text="echo ok",
        requires_privilege=False,
        supported_for_assisted_execution=True,
        expected_effect="test",
    )
    ok, summary, return_code = run_assisted_command(command)
    assert ok is True
    assert return_code == 0
    assert observed["argv"] == ["echo", "ok"]
    assert observed["shell"] is False
    assert "ok" in summary
