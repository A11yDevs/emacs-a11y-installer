from emacs_a11y.doctor import registry


def test_registry_loads_common_checks():
    checks = registry.load_checks("Linux")
    assert checks
    assert any(getattr(check, "__name__", "") == "check_system_info" for check in checks)


def test_registry_loads_platform_specific_checks_linux():
    checks = registry.load_checks("Linux")
    assert any(getattr(check, "__name__", "") == "check_linux_tts" for check in checks)


def test_registry_loads_platform_specific_checks_macos():
    checks = registry.load_checks("Darwin")
    assert any(getattr(check, "__name__", "") == "check_macos_tts" for check in checks)


def test_registry_loads_platform_specific_checks_windows():
    checks = registry.load_checks("Windows")
    assert any(getattr(check, "__name__", "") == "check_windows_tts" for check in checks)
