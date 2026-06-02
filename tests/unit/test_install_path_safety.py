from emacs_a11y.install import writer
from emacs_a11y.models.install import (
    ConfirmationPolicy,
    InstallActionType,
    InstallPlan,
    InstallPlanItem,
    InstallRequest,
    ProfileTemplate,
)


def test_writer_rejects_paths_outside_isolated_profile(tmp_path):
    target = tmp_path / "profile"
    request = InstallRequest(
        profile_name="minimal",
        mode="direct",
        confirmation_policy=ConfirmationPolicy.PROMPT_REQUIRED,
        target_directory=target,
    )

    template_root = tmp_path / "tpl"
    (template_root / "lisp").mkdir(parents=True)
    (template_root / "early-init.el").write_text("", encoding="utf-8")
    (template_root / "init.el").write_text("", encoding="utf-8")

    template = ProfileTemplate(
        root_path=template_root,
        early_init_path=template_root / "early-init.el",
        init_path=template_root / "init.el",
        lisp_root=template_root / "lisp",
        available_modules=[],
    )

    plan = InstallPlan(
        request=request,
        template=template,
        items=[
            InstallPlanItem(
                path=tmp_path / "outside" / "evil.txt",
                item_type="file",
                action_type=InstallActionType.WRITE_FILE,
                project_owned=True,
            )
        ],
    )

    result = writer.apply_install_plan(plan)
    assert result.failed_items
