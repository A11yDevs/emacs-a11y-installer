from __future__ import annotations

from emacs_a11y.install.emacs_version import (
    assess_emacs_version,
    parse_emacs_version,
    resolve_minimum_supported_version,
)
from emacs_a11y.models.emacs_install import status_to_exit_code


def test_parse_emacs_version_from_stdout_line() -> None:
    assert parse_emacs_version("GNU Emacs 30.1") == "30.1"


def test_parse_emacs_version_returns_none_when_missing() -> None:
    assert parse_emacs_version("sem versao") is None


def test_assess_emacs_version_supported(monkeypatch) -> None:
    monkeypatch.setenv("EMACS_A11Y_MIN_EMACS_VERSION", "29.1")
    assessment = assess_emacs_version("GNU Emacs 30.1")
    assert assessment.state == "supported"


def test_assess_emacs_version_unknown_when_unparseable(monkeypatch) -> None:
    monkeypatch.delenv("EMACS_A11Y_MIN_EMACS_VERSION", raising=False)
    assessment = assess_emacs_version("GNU Emacs ???")
    assert assessment.state == "unknown"


def test_assess_emacs_version_too_old(monkeypatch) -> None:
    monkeypatch.setenv("EMACS_A11Y_MIN_EMACS_VERSION", "29.1")
    assessment = assess_emacs_version("GNU Emacs 28.2")
    assert assessment.state == "too_old"


def test_minimum_version_fallback_on_invalid_env(monkeypatch) -> None:
    monkeypatch.setenv("EMACS_A11Y_MIN_EMACS_VERSION", "invalid")
    assert resolve_minimum_supported_version() == "29.1"


def test_status_to_exit_code_mapping() -> None:
    assert status_to_exit_code("success") == 0
    assert status_to_exit_code("guidance_only") == 1
    assert status_to_exit_code("cancelled") == 1
    assert status_to_exit_code("unsupported") == 2
    assert status_to_exit_code("failed") == 3
    assert status_to_exit_code("internal_error") == 4
