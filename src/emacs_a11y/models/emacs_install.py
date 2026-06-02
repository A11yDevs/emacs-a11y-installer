from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PackageManager(str, Enum):
    WINGET = "WINGET"
    BREW = "BREW"
    APT = "APT"
    NONE = "NONE"
    UNSUPPORTED = "UNSUPPORTED"


class InstallMethod(str, Enum):
    WINGET_GNU_EMACS = "WINGET_GNU_EMACS"
    HOMEBREW_FORMULA = "HOMEBREW_FORMULA"
    HOMEBREW_CASK = "HOMEBREW_CASK"
    APT_GUIDANCE = "APT_GUIDANCE"
    MANUAL_GUIDANCE = "MANUAL_GUIDANCE"


class InstallExecutionMode(str, Enum):
    GUIDANCE_ONLY = "GUIDANCE_ONLY"
    DRY_RUN = "DRY_RUN"
    ASSISTED_EXECUTION = "ASSISTED_EXECUTION"


class ConsentDecision(str, Enum):
    CONFIRMED = "CONFIRMED"
    DECLINED = "DECLINED"
    UNAVAILABLE_NO_TTY = "UNAVAILABLE_NO_TTY"


@dataclass(slots=True)
class EnvironmentDetectionResult:
    operating_system: str
    distribution: str
    architecture: str
    is_tty: bool
    path_entries_visible: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EmacsCandidate:
    path: str
    source: str
    priority: int


@dataclass(slots=True)
class EmacsDetectionResult:
    status: str
    selected_path: str | None
    candidates: list[EmacsCandidate] = field(default_factory=list)
    version_text: str | None = None
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class VersionSupportAssessment:
    state: str
    detected_version: str | None
    minimum_supported_version: str
    message: str


@dataclass(slots=True)
class InstallCommand:
    argv: list[str]
    display_text: str
    requires_privilege: bool
    supported_for_assisted_execution: bool
    expected_effect: str


@dataclass(slots=True)
class InstallationMethodRecommendation:
    method: InstallMethod
    package_manager: PackageManager
    recommended_commands: list[InstallCommand]
    manual_steps: list[str] = field(default_factory=list)
    assisted_execution_supported: bool = False
    rationale: str = ""


@dataclass(slots=True)
class ExecutionConsentSummary:
    platform_line: str
    method_line: str
    command_lines: list[str]
    privilege_line: str
    effect_line: str
    cancel_line: str


@dataclass(slots=True)
class InstallationAttemptResult:
    status: str
    environment: EnvironmentDetectionResult
    emacs_detection_before: EmacsDetectionResult
    version_assessment: VersionSupportAssessment | None
    recommendation: InstallationMethodRecommendation
    mode: InstallExecutionMode = InstallExecutionMode.GUIDANCE_ONLY
    consent_decision: ConsentDecision | None = None
    executed_commands: list[str] = field(default_factory=list)
    emacs_detection_after: EmacsDetectionResult | None = None
    next_steps: list[str] = field(default_factory=list)
    exit_code: int = 0
    logs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InteractiveInstallContextState:
    pending_emacs_recommendation: InstallationMethodRecommendation | None = None
    pending_consent_summary: ExecutionConsentSummary | None = None
    pending_execute_method: str = "auto"
    last_status: str = ""


def status_to_exit_code(status: str) -> int:
    mapping = {
        "success": 0,
        "guidance_only": 1,
        "cancelled": 1,
        "unsupported": 2,
        "failed": 3,
        "internal_error": 4,
    }
    return mapping.get(status, 4)
