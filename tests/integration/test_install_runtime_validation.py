from emacs_a11y.install import validator
from emacs_a11y.models.install import RuntimeValidationStatus


def test_runtime_validation_is_skipped_without_emacs(tmp_path):
    result = validator.validate_runtime(None, tmp_path)
    assert result.status == RuntimeValidationStatus.SKIPPED


def test_runtime_validation_reports_failure_for_invalid_emacs_binary(tmp_path):
    result = validator.validate_runtime("/nonexistent/emacs", tmp_path)
    assert result.status == RuntimeValidationStatus.FAILED
