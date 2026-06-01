from __future__ import annotations

from emacs_a11y.doctor.checks import common, linux, macos, windows


def load_checks(os_name: str) -> list:
    checks = list(common.common_checks())

    normalized = os_name.lower()
    if normalized == "windows":
        checks.extend(windows.checks())
    elif normalized == "darwin":
        checks.extend(macos.checks())
    elif normalized == "linux":
        checks.extend(linux.checks())

    return checks
