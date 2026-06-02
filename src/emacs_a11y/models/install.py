from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class TemplateSourceKind(str, Enum):
    PACKAGED_RESOURCE = "packaged_resource"
    DEVELOPMENT_PATH = "development_path"
    FROZEN_BUNDLE = "frozen_bundle"


class TemplateValidationStatus(str, Enum):
    VALID = "valid"
    INVALID = "invalid"
    INCOMPLETE = "incomplete"


class PreflightStatus(str, Enum):
    PASS = "pass"
    CRITICAL_ABORT = "critical_abort"


class InstallActionType(str, Enum):
    CREATE_DIRECTORY = "create_directory"
    COPY_TREE = "copy_tree"
    COPY_FILE = "copy_file"
    WRITE_FILE = "write_file"
    PRESERVE_EXISTING = "preserve_existing"
    SKIP = "skip"
    VALIDATE = "validate"


class RuntimeValidationStatus(str, Enum):
    VALIDATED = "validated"
    SKIPPED = "skipped"
    FAILED = "failed"


class ConfirmationPolicy(str, Enum):
    PROMPT_REQUIRED = "PROMPT_REQUIRED"
    INTERACTIVE_SELECTION = "INTERACTIVE_SELECTION"
    EXPLICIT_YES_ALLOWED = "EXPLICIT_YES_ALLOWED"
    DENY_UNSAFE_AUTOMATION = "DENY_UNSAFE_AUTOMATION"


@dataclass(slots=True)
class InstallProfile:
    name: str
    description: str
    enabled_modules: list[str]
    template_policy: str = "copy_template_and_filter_init"


@dataclass(slots=True)
class RequiredDependency:
    name: str
    required_for_profiles: list[str]
    status: str
    severity: str = "critical"


@dataclass(slots=True)
class TemplateSource:
    kind: TemplateSourceKind
    location: Path
    is_read_only: bool
    priority: int


@dataclass(slots=True)
class ProfileTemplate:
    root_path: Path
    early_init_path: Path
    init_path: Path
    lisp_root: Path
    available_modules: list[str]
    optional_modules: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TemplateValidationResult:
    status: TemplateValidationStatus
    message_lines: list[str] = field(default_factory=list)
    missing_items: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InstallRequest:
    profile_name: str
    mode: str
    confirmation_policy: ConfirmationPolicy
    target_directory: Path
    explicit_yes: bool = False
    allow_project_owned_overwrite: bool = False


@dataclass(slots=True)
class PreflightCheck:
    request: InstallRequest
    required_dependencies: list[RequiredDependency]
    doctor_signals: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True)
class PreflightResult:
    status: PreflightStatus
    missing_dependencies: list[str] = field(default_factory=list)
    message_lines: list[str] = field(default_factory=list)
    suggested_next_steps: list[str] = field(default_factory=list)
    exit_code: int = 0


@dataclass(slots=True)
class InstallPlanItem:
    path: Path
    item_type: str
    action_type: InstallActionType
    project_owned: bool
    source_path: Path | None = None
    reason: str = ""


@dataclass(slots=True)
class InstallPlan:
    request: InstallRequest
    template: ProfileTemplate
    items: list[InstallPlanItem]
    personal_config_notices: list[str] = field(default_factory=list)
    preflight_messages: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RuntimeValidationResult:
    status: RuntimeValidationStatus
    message_lines: list[str] = field(default_factory=list)
    command_preview: str | None = None


@dataclass(slots=True)
class RollbackInstruction:
    paths_to_remove: list[str]
    notes: list[str] = field(default_factory=list)
    future_command_hint: str | None = None


@dataclass(slots=True)
class InstallExecutionResult:
    created_items: list[str] = field(default_factory=list)
    copied_items: list[str] = field(default_factory=list)
    skipped_items: list[str] = field(default_factory=list)
    preserved_items: list[str] = field(default_factory=list)
    failed_items: list[str] = field(default_factory=list)
    warning_items: list[str] = field(default_factory=list)
    runtime_validation: RuntimeValidationResult = field(
        default_factory=lambda: RuntimeValidationResult(RuntimeValidationStatus.SKIPPED)
    )
    preflight_result: PreflightResult = field(
        default_factory=lambda: PreflightResult(PreflightStatus.PASS, exit_code=0)
    )
    rollback_guidance: RollbackInstruction = field(default_factory=lambda: RollbackInstruction(paths_to_remove=[]))
    log_paths: list[str] = field(default_factory=list)
    exit_code: int = 0


MINIMAL_PROFILE = InstallProfile(
    name="minimal",
    description="Perfil minimal seguro para Emacs Acessivel",
    enabled_modules=["init-packages", "init-core", "init-dired"],
)
