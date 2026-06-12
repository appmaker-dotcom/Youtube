"""
utils/__init__.py
-----------------
Shared utilities available to all modules.

Currently provides:
- get_logger(): returns a color-formatted logger for any module
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    import colorlog
    HAS_COLORLOG = True
except ImportError:
    HAS_COLORLOG = False


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger with:
    - Color output in the terminal
    - File output saved to logs/YYYY-MM-DD.log
    - Consistent format across all modules

    Args:
        name: Usually pass __name__ from the calling module.

    Returns:
        A configured Python logger instance.
    """
    logger = logging.getLogger(name)

    # Don't add duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # --- Terminal Handler (with color if available) ---
    if HAS_COLORLOG:
        terminal_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG":    "cyan",
                "INFO":     "green",
                "WARNING":  "yellow",
                "ERROR":    "red",
                "CRITICAL": "bold_red",
            }
        )
    else:
        terminal_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )

    terminal_handler = logging.StreamHandler(sys.stdout)
    terminal_handler.setLevel(logging.INFO)
    terminal_handler.setFormatter(terminal_formatter)

    # --- File Handler (plain text, saved to logs/) ---
    logs_dir = Path("./logs")
    logs_dir.mkdir(exist_ok=True)

    log_filename = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(terminal_handler)
    logger.addHandler(file_handler)

    return logger