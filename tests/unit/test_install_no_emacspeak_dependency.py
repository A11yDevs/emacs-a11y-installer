from emacs_a11y.install import profile


def test_minimal_profile_does_not_require_emacspeak_setup_file(tmp_path):
    init_path = tmp_path / "init.el"
    init_path.write_text(profile.build_minimal_init(), encoding="utf-8")
    content = init_path.read_text(encoding="utf-8")
    assert "emacspeak-setup.el" not in content


def test_minimal_profile_does_not_reference_dtk_or_emacspeak_symbols():
    content = profile.build_minimal_init()
    assert "dtk-" not in content
    assert "emacspeak-" not in content
