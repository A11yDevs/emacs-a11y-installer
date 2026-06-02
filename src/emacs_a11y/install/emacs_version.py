from __future__ import annotations

import os
import re

from emacs_a11y.models.emacs_install import VersionSupportAssessment

DEFAULT_MIN_EMACS_VERSION = "29.1"


def _version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def parse_emacs_version(version_text: str | None) -> str | None:
    if not version_text:
        return None
    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", version_text)
    if not match:
        return None
    return match.group(1)


def resolve_minimum_supported_version() -> str:
    raw = os.environ.get("EMACS_A11Y_MIN_EMACS_VERSION", "").strip()
    parsed = parse_emacs_version(raw)
    if parsed is None:
        return DEFAULT_MIN_EMACS_VERSION
    return parsed


def assess_emacs_version(version_text: str | None) -> VersionSupportAssessment:
    minimum = resolve_minimum_supported_version()
    parsed = parse_emacs_version(version_text)

    if parsed is None:
        return VersionSupportAssessment(
            state="unknown",
            detected_version=None,
            minimum_supported_version=minimum,
            message="Nao foi possivel identificar a versao do Emacs com seguranca.",
        )

    if _version_tuple(parsed) < _version_tuple(minimum):
        return VersionSupportAssessment(
            state="too_old",
            detected_version=parsed,
            minimum_supported_version=minimum,
            message="Versao detectada abaixo da politica minima suportada.",
        )

    return VersionSupportAssessment(
        state="supported",
        detected_version=parsed,
        minimum_supported_version=minimum,
        message="Versao do Emacs dentro da politica minima suportada.",
    )
