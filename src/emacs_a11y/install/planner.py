from __future__ import annotations

from pathlib import Path

from emacs_a11y.models.install import InstallActionType, InstallPlan, InstallPlanItem, InstallRequest, ProfileTemplate


def resolve_default_target_directory() -> Path:
    return Path.home() / ".emacs.d" / "emacs-a11y-profile"


def detect_personal_emacs_paths() -> list[str]:
    candidates = [Path.home() / ".emacs", Path.home() / ".emacs.d", Path.home() / ".config" / "emacs"]
    return [str(path) for path in candidates if path.exists()]


def is_path_within(base_dir: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(base_dir.resolve())
        return True
    except ValueError:
        return False


def create_install_plan(
    request: InstallRequest,
    template: ProfileTemplate,
    preflight_messages: list[str],
) -> InstallPlan:
    target = request.target_directory
    items = [
        InstallPlanItem(
            path=target,
            item_type="directory",
            action_type=InstallActionType.CREATE_DIRECTORY,
            project_owned=True,
            reason="Diretorio raiz do perfil isolado",
        ),
        InstallPlanItem(
            path=target / "lisp",
            item_type="directory",
            action_type=InstallActionType.CREATE_DIRECTORY,
            project_owned=True,
            reason="Diretorio de modulos Lisp",
        ),
        InstallPlanItem(
            path=target / "logs",
            item_type="directory",
            action_type=InstallActionType.CREATE_DIRECTORY,
            project_owned=True,
            reason="Diretorio de logs do perfil",
        ),
        InstallPlanItem(
            path=target / "early-init.el",
            item_type="file",
            action_type=InstallActionType.COPY_FILE,
            project_owned=True,
            source_path=template.early_init_path,
            reason="Materializar early-init canônico",
        ),
        InstallPlanItem(
            path=target / "init.el",
            item_type="file",
            action_type=InstallActionType.WRITE_FILE,
            project_owned=True,
            reason="Gerar init.el minimal com módulos permitidos",
        ),
        InstallPlanItem(
            path=target / "custom.el",
            item_type="file",
            action_type=InstallActionType.WRITE_FILE,
            project_owned=True,
            reason="Criar custom.el project-owned",
        ),
        InstallPlanItem(
            path=target / "lisp",
            item_type="directory",
            action_type=InstallActionType.COPY_TREE,
            project_owned=True,
            source_path=template.lisp_root,
            reason="Copiar lisp/ preservando estrutura",
        ),
    ]

    return InstallPlan(
        request=request,
        template=template,
        items=items,
        personal_config_notices=detect_personal_emacs_paths(),
        preflight_messages=preflight_messages,
    )
