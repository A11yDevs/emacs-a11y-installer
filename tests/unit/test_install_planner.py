from pathlib import Path

from emacs_a11y.install import planner
from emacs_a11y.models.install import ConfirmationPolicy, InstallRequest, ProfileTemplate


def _request(tmp_path: Path) -> InstallRequest:
    return InstallRequest(
        profile_name="minimal",
        mode="direct",
        confirmation_policy=ConfirmationPolicy.PROMPT_REQUIRED,
        target_directory=tmp_path / "profile",
    )


def _template(tmp_path: Path) -> ProfileTemplate:
    root = tmp_path / "tpl"
    (root / "lisp").mkdir(parents=True)
    (root / "early-init.el").write_text("", encoding="utf-8")
    (root / "init.el").write_text("", encoding="utf-8")
    (root / "lisp" / "init-packages.el").write_text("", encoding="utf-8")
    return ProfileTemplate(
        root_path=root,
        early_init_path=root / "early-init.el",
        init_path=root / "init.el",
        lisp_root=root / "lisp",
        available_modules=["init-packages"],
    )


def test_plan_is_generated_without_writing(tmp_path):
    request = _request(tmp_path)
    template = _template(tmp_path)
    plan = planner.create_install_plan(request, template, ["ok"])

    assert plan.items
    assert not request.target_directory.exists()


def test_path_safety_helper_accepts_only_paths_within_target(tmp_path):
    base = tmp_path / "profile"
    inside = base / "init.el"
    outside = tmp_path / "outside" / "x"

    assert planner.is_path_within(base, inside)
    assert not planner.is_path_within(base, outside)
