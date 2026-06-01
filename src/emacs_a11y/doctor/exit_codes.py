from __future__ import annotations

from emacs_a11y.models.diagnostic import SummaryCounts


EXIT_READY = 0
EXIT_WARNING = 1
EXIT_CRITICAL = 2
EXIT_INTERNAL_ERROR = 3


def map_exit_code(summary: SummaryCounts) -> int:
    if summary.critical > 0:
        return EXIT_CRITICAL
    if summary.warning > 0:
        return EXIT_WARNING
    return EXIT_READY
