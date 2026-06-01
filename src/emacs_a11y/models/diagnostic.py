from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Callable


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class EnvironmentState:
    os: str
    architecture: str
    os_version: str | None = None
    path_entries: list[str] = field(default_factory=list)
    emacs_version: str | None = None
    git_available: bool = False
    python_available: bool = False
    profile_path: str = ""
    profile_exists: bool = False
    profile_accessible: bool = False
    user_emacs_paths: list[str] = field(default_factory=list)
    tts_signals: list[str] = field(default_factory=list)
    emacspeak_signals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, str | None]:
        return {
            "os": self.os,
            "os_version": self.os_version,
            "architecture": self.architecture,
        }


@dataclass(slots=True)
class DiagnosticResult:
    check_id: str
    name: str
    status: Status
    severity: Severity
    summary: str
    evidence: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    read_only: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "check_id": self.check_id,
            "name": self.name,
            "status": self.status.value,
            "severity": self.severity.value,
            "summary": self.summary,
            "evidence": self.evidence,
            "next_steps": self.next_steps,
            "read_only": True,
        }


@dataclass(slots=True)
class SummaryCounts:
    critical: int = 0
    warning: int = 0
    info: int = 0
    pass_count: int = 0
    fail: int = 0
    unknown: int = 0

    def to_dict(self) -> dict[str, int]:
        return {
            "critical": self.critical,
            "warning": self.warning,
            "info": self.info,
            "pass": self.pass_count,
            "fail": self.fail,
            "unknown": self.unknown,
        }


@dataclass(slots=True)
class DiagnosticReport:
    report_version: str
    generated_at: str
    environment: EnvironmentState
    summary: SummaryCounts
    results: list[DiagnosticResult]
    next_steps: list[str]
    exit_code: int

    def to_dict(self) -> dict[str, object]:
        return {
            "report_version": self.report_version,
            "generated_at": self.generated_at,
            "environment": self.environment.to_dict(),
            "summary": self.summary.to_dict(),
            "results": [result.to_dict() for result in self.results],
            "next_steps": self.next_steps,
            "exit_code": self.exit_code,
        }


@dataclass(slots=True)
class DiagnosticCheck:
    id: str
    name: str
    description: str
    platform_scope: list[str]
    run: Callable[[EnvironmentState], DiagnosticResult]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
