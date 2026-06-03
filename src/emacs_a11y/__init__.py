"""Core package for emacs-a11y installer."""

from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]

try:
    __version__ = version("emacs-a11y-installer")
except PackageNotFoundError:
    __version__ = "0+unknown"
