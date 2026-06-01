from pathlib import Path


def test_bootstrap_scripts_are_wrappers_without_business_rules():
    script_files = [
        Path("scripts/bootstrap-doctor.sh"),
        Path("scripts/bootstrap-doctor.ps1"),
    ]
    forbidden = [
        "def check_",
        "class Diagnostic",
        "pip install",
        "apt install",
        "brew install",
    ]

    for script in script_files:
        content = script.read_text(encoding="utf-8")
        assert "emacs-a11y doctor" in content
        assert all(token not in content for token in forbidden)
