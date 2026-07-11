"""
Logging configuration for the HydroGrow Smart Farming Simulator.
"""

import logging

from smart_farming.config.settings import Settings

def create_formatter() -> logging.Formatter:
    """
    Create the standard formatter used by application log handlers.

    Returns:
        Configured logging formatter.
    """

    return logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def create_console_handler(
    formatter: logging.Formatter,
) -> logging.Handler:
    """
    Create the application's console log handler.

    Args:
        formatter: Formatter applied to console log messages.
    
    Returns:
        Configured console log handler.
    """

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    return handler

def configure_logging(settings: Settings) -> None:
    """
    Configure the application's logging.

    Args:
        settings: Validated application settings.

    This function should be called once during application startup.
    """

    root_logger = logging.getLogger()

    # Prevent duplicate handlers if logging is configured multiple times.
    if root_logger.handlers:
        return

    root_logger.setLevel(
        getattr(logging, settings.log_level, logging.INFO)
    )

    formatter = create_formatter()

    console_handler = create_console_handler(formatter)

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

def log_application_start(
    logger: logging.Logger,
    settings: Settings,
) -> None:
    """
    Log application startup information

    Args:
        logger: Configured application logger.
        settings: Validated application settings.
    """

    logger.info(
        "Environment: %s | Log Level: %s",
        settings.environment,
        settings.log_level
    )

    logger.info(
        "Facilities: %d | Interval: %ds | Batch Size: %d",
        settings.total_facilities,
        settings.simulation_interval_seconds,
        settings.event_batch_size,
    )

def log_application_shutdown(
    logger: logging.Logger,
) -> None:
    """
    Log successful application shutdown.

    Args:
        logger: Configured application logger.
    """

    logger.info("HydroGrow Smart Farming Simulator stopped successfully.")

def log_unhandled_exception(
    logger: logging.Logger,
    message: str,
) -> None:
    """
    Log an unhandled application exception.

    Args:
        logger: Configured application logger.
        message: Exception message to record.
    """

    logger.exception(message)