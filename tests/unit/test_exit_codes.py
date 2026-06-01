from emacs_a11y.doctor.exit_codes import map_exit_code
from emacs_a11y.models.diagnostic import SummaryCounts


def test_exit_code_ready():
    summary = SummaryCounts(critical=0, warning=0)
    assert map_exit_code(summary) == 0


def test_exit_code_warning():
    summary = SummaryCounts(critical=0, warning=1)
    assert map_exit_code(summary) == 1


def test_exit_code_critical():
    summary = SummaryCounts(critical=1, warning=0)
    assert map_exit_code(summary) == 2
