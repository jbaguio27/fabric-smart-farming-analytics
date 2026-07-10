"""
Logging configuration for the HydroGrow Smart Farming Simulator.
"""

import logging

from smart_farming.config.settings import Settings

settings = Settings()

def configure_logging() -> None:
    """
    Configure the application's logging.

    This function should be called once during application startup.
    """

    root_logger = logging.getLogger()

    # Prevent duplicate handlers if logging is configured multiple times.
    if root_logger.handlers:
        return

    root_logger.setLevel(
        getattr(logging, settings.log_level.upper(), logging.INFO)
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    console_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Logger name, typically __name__.

    Returns:
        Configured logger instance.
    """

    return logging.getLogger(name)