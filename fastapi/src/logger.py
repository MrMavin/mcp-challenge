"""Centralized logger configuration.

Usage:
    from .logger import get_logger
    logger = get_logger(__name__)

All loggers share the same console handler & format so output is consistent across the project.
"""

import logging
from functools import lru_cache

_CONSOLE_FORMAT = "% (asctime)s | %(levelname)s | %(name)s | %(message)s"

@lru_cache(maxsize=None)
def _get_console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(_CONSOLE_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    return handler

@lru_cache(maxsize=None)
def get_logger(name: str = "root", level: int = logging.INFO) -> logging.Logger:
    """Return a logger with a pre-configured console handler.

    Ensures we don't add duplicate handlers when the function is called multiple
    times for the same logger name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Ensure the console handler is attached only once.
    console_handler = _get_console_handler()
    if console_handler not in logger.handlers:
        logger.addHandler(console_handler)

    # Avoid propagating to root to prevent duplicate log lines when using uvicorn
    logger.propagate = False
    return logger