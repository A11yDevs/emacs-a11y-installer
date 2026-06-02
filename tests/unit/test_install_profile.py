from emacs_a11y.install import profile


def test_build_minimal_init_contains_only_three_expected_requires():
    content = profile.build_minimal_init()
    assert "(require 'init-packages)" in content
    assert "(require 'init-core)" in content
    assert "(require 'init-dired)" in content
    assert "(require 'init-accessibility)" not in content


def test_init_content_is_minimal_accepts_exact_expected_content():
    content = profile.build_minimal_init()
    assert profile.init_content_is_minimal(content)


def test_ensure_no_accessibility_require_rejects_forbidden_require():
    content = "(require 'init-packages)\n(require 'init-accessibility)\n"
    assert profile.ensure_no_accessibility_require(content) is False
