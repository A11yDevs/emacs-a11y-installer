from __future__ import annotations

import shutil
from pathlib import Path

from emacs_a11y.install import profile
from emacs_a11y.install.planner import is_path_within
from emacs_a11y.models.install import InstallActionType, InstallExecutionResult, InstallPlan


class InstallWriteError(RuntimeError):
    pass


def _safe_path_or_raise(target_root: Path, candidate: Path) -> Path:
    if not is_path_within(target_root, candidate):
        raise InstallWriteError(f"Caminho fora do perfil isolado: {candidate}")
    return candidate


def apply_install_plan(plan: InstallPlan) -> InstallExecutionResult:
    result = InstallExecutionResult(exit_code=0)
    target_root = plan.request.target_directory

    for item in plan.items:
        try:
            target = _safe_path_or_raise(target_root, item.path)

            if item.action_type == InstallActionType.CREATE_DIRECTORY:
                if target.exists():
                    result.preserved_items.append(str(target))
                else:
                    target.mkdir(parents=True, exist_ok=True)
                    result.created_items.append(str(target))

            elif item.action_type == InstallActionType.COPY_FILE:
                if item.source_path is None:
                    raise InstallWriteError("source_path ausente para COPY_FILE")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item.source_path, target)
                result.copied_items.append(str(target))

            elif item.action_type == InstallActionType.COPY_TREE:
                if item.source_path is None:
                    raise InstallWriteError("source_path ausente para COPY_TREE")
                target.mkdir(parents=True, exist_ok=True)
                for source_file in item.source_path.rglob("*"):
                    if source_file.is_dir():
                        continue
                    rel_path = source_file.relative_to(item.source_path)
                    destination = target / rel_path
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, destination)
                    result.copied_items.append(str(destination))

            elif item.action_type == InstallActionType.WRITE_FILE:
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.name == "init.el":
                    target.write_text(profile.build_minimal_init(), encoding="utf-8")
                elif target.name == "custom.el":
                    target.write_text(profile.build_custom_el(), encoding="utf-8")
                else:
                    target.write_text("", encoding="utf-8")
                result.created_items.append(str(target))

            elif item.action_type == InstallActionType.PRESERVE_EXISTING:
                result.preserved_items.append(str(target))

            elif item.action_type == InstallActionType.SKIP:
                result.skipped_items.append(str(target))

        except Exception as exc:  # pragma: no cover - defensivo
            result.failed_items.append(f"{item.path}: {exc}")

    if result.failed_items:
        result.exit_code = 1

    return result
