from __future__ import annotations

from pathlib import Path

from emacs_a11y.install import emacs_detector


def test_detect_environment_returns_required_fields() -> None:
    result = emacs_detector.detect_environment()
    assert result.operating_system in {"windows", "macos", "linux", "unknown"}
    assert result.architecture


def test_discover_emacs_candidates_prioritizes_path_order(monkeypatch, tmp_path) -> None:
    first = tmp_path / "bin1"
    second = tmp_path / "bin2"
    first.mkdir()
    second.mkdir()
    (second / "emacs").write_text("#!/bin/sh\n", encoding="utf-8")
    (first / "emacs").write_text("#!/bin/sh\n", encoding="utf-8")
    (first / "emacs").chmod(0o755)
    (second / "emacs").chmod(0o755)

    monkeypatch.setenv("PATH", f"{first}:{second}")
    monkeypatch.setattr(emacs_detector.platform, "system", lambda: "Linux")

    candidates = emacs_detector.discover_emacs_candidates()
    assert candidates
    assert Path(candidates[0].path).parent == first


def test_detect_emacs_missing(monkeypatch) -> None:
    monkeypatch.setattr(emacs_detector, "discover_emacs_candidates", lambda: [])

    class _State:
        emacs_version = None

    monkeypatch.setattr(emacs_detector, "build_environment_state", lambda: _State())
    result = emacs_detector.detect_emacs()
    assert result.status == "missing"
