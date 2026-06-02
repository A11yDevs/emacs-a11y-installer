from emacs_a11y.install.templates import TemplateLocator
from emacs_a11y.models.install import TemplateValidationStatus


def test_template_locator_finds_packaged_template():
    locator = TemplateLocator()
    source = locator.resolve_source()
    assert source.location.exists()


def test_template_validation_passes_for_packaged_template():
    locator = TemplateLocator()
    source = locator.resolve_source()
    validation, template = locator.validate_source(source)
    assert validation.status == TemplateValidationStatus.VALID
    assert template is not None
    assert (template.root_path / "early-init.el").exists()


def test_template_validation_reports_missing_items(tmp_path):
    broken = tmp_path / "a11y-emacs"
    (broken / "lisp").mkdir(parents=True)
    (broken / "early-init.el").write_text("", encoding="utf-8")

    from emacs_a11y.models.install import TemplateSource, TemplateSourceKind

    source = TemplateSource(
        kind=TemplateSourceKind.DEVELOPMENT_PATH,
        location=broken,
        is_read_only=False,
        priority=0,
    )
    locator = TemplateLocator()
    validation, template = locator.validate_source(source)

    assert validation.status == TemplateValidationStatus.INCOMPLETE
    assert template is None
    assert "init.el" in validation.missing_items
