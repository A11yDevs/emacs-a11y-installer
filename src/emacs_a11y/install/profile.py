from __future__ import annotations

ALLOWED_REQUIRES = ["init-packages", "init-core", "init-dired"]


def build_minimal_init() -> str:
    return "\n".join([f"(require '{module})" for module in ALLOWED_REQUIRES]) + "\n"


def init_content_is_minimal(content: str) -> bool:
    expected = build_minimal_init().strip().splitlines()
    actual = [line.strip() for line in content.strip().splitlines() if line.strip()]
    return actual == expected


def ensure_no_accessibility_require(content: str) -> bool:
    return "(require 'init-accessibility)" not in content


def build_custom_el() -> str:
    return ";;; custom.el --- customizações locais do perfil minimal\n\n"
