from __future__ import annotations

import os
import sys
from pathlib import Path

from importlib import resources

from emacs_a11y.models.install import (
    ProfileTemplate,
    TemplateSource,
    TemplateSourceKind,
    TemplateValidationResult,
    TemplateValidationStatus,
)


REQUIRED_TEMPLATE_FILES = [
    "early-init.el",
    "init.el",
    "lisp/init-packages.el",
    "lisp/init-core.el",
    "lisp/init-dired.el",
]


class TemplateLocator:
    def resolve_source(self) -> TemplateSource:
        dev_path = os.environ.get("EMACS_A11Y_TEMPLATE_PATH")
        if dev_path:
            root = Path(dev_path).expanduser().resolve()
            if root.exists():
                return TemplateSource(
                    kind=TemplateSourceKind.DEVELOPMENT_PATH,
                    location=root,
                    is_read_only=False,
                    priority=0,
                )

        packaged_root = Path(str(resources.files("emacs_a11y.resources").joinpath("a11y-emacs")))
        if packaged_root.exists():
            return TemplateSource(
                kind=TemplateSourceKind.PACKAGED_RESOURCE,
                location=packaged_root,
                is_read_only=True,
                priority=1,
            )

        if getattr(sys, "frozen", False):
            frozen_root = Path(sys.executable).resolve().parent / "resources" / "a11y-emacs"
            if frozen_root.exists():
                return TemplateSource(
                    kind=TemplateSourceKind.FROZEN_BUNDLE,
                    location=frozen_root,
                    is_read_only=True,
                    priority=2,
                )

        raise FileNotFoundError("Template canônico não encontrado.")

    def validate_source(self, source: TemplateSource) -> tuple[TemplateValidationResult, ProfileTemplate | None]:
        missing_items: list[str] = []
        for rel_path in REQUIRED_TEMPLATE_FILES:
            if not (source.location / rel_path).exists():
                missing_items.append(rel_path)

        if missing_items:
            return (
                TemplateValidationResult(
                    status=TemplateValidationStatus.INCOMPLETE,
                    message_lines=["Template canônico incompleto."],
                    missing_items=missing_items,
                ),
                None,
            )

        lisp_root = source.location / "lisp"
        modules = sorted(path.stem for path in lisp_root.glob("*.el"))
        optional_modules = [name for name in modules if name == "init-accessibility"]

        return (
            TemplateValidationResult(
                status=TemplateValidationStatus.VALID,
                message_lines=["Template canônico validado."],
                missing_items=[],
                warnings=[],
            ),
            ProfileTemplate(
                root_path=source.location,
                early_init_path=source.location / "early-init.el",
                init_path=source.location / "init.el",
                lisp_root=lisp_root,
                available_modules=modules,
                optional_modules=optional_modules,
            ),
        )
