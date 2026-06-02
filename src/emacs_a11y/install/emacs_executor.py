from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from emacs_a11y.models.emacs_install import InstallCommand


def _default_log_path() -> Path:
    return Path.home() / ".cache" / "emacs-a11y" / "logs" / "install-emacs.log"


def redact_sensitive_text(text: str) -> str:
    redacted = text
    redacted = re.sub(r"(?i)(token|password|secret)\s*[:=]\s*\S+", r"\1=[REDACTED]", redacted)
    redacted = redacted.replace(str(Path.home()), "~")
    return redacted


def log_event(event: str, details: str = "") -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    line = f"{timestamp} {event} {redact_sensitive_text(details)}".strip()
    log_path = _default_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return str(log_path)


def summarize_external_output(stdout: str, stderr: str) -> str:
    merged = "\n".join([part for part in [stdout.strip(), stderr.strip()] if part])
    if not merged:
        return "Sem saida adicional do comando externo."
    lines = [redact_sensitive_text(line) for line in merged.splitlines() if line.strip()]
    return " | ".join(lines[:3])


def run_assisted_command(command: InstallCommand) -> tuple[bool, str, int]:
    process = subprocess.run(
        command.argv,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    summary = summarize_external_output(process.stdout, process.stderr)
    return process.returncode == 0, summary, process.returncode
