"""
logger.py
---------
Centralised logging setup.
Import get_logger() in any module that needs logging.

Usage:
    from src.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened")
"""

import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

log_filename = f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger that writes to both the console and a timestamped log file.

    Parameters
    ----------
    name : str
        Logger name — pass __name__ from the calling module.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if get_logger is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s  %(levelname)s  %(name)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — writes to logs/pipeline_<timestamp>.log
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    # Console handler — prints to terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger