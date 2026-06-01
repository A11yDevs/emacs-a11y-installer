from __future__ import annotations

import logging
from pathlib import Path


class RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        home = str(Path.home())
        if isinstance(record.msg, str):
            record.msg = record.msg.replace(home, "~")
        return True


def get_logger(name: str = "emacs_a11y.doctor") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    handler.addFilter(RedactFilter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger
