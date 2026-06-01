from __future__ import annotations

import json

from emacs_a11y.models.diagnostic import DiagnosticReport


def render(report: DiagnosticReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
