"""
Utility functions and custom exceptions.
"""

from .datetime_utils import (
    utc_now,
    format_timestamp,
)

from .id_generator import generate_event_id
from .random_manager import RandomManager
from .exceptions import (
    SmartFarmingError,
    ConfigurationError,
    SimulationError,
    TelemetryGenerationError,
    ValidationError,
    DispatchError,
    EventSerializationError,
    DataValidationError,
    EventRegistrationError,
)

__all__ = [
    "utc_now",
    "format_timestamp",
    "generate_event_id",
    "SmartFarmingError",
    "ConfigurationError",
    "SimulationError",
    "TelemetryGenerationError",
    "ValidationError",
    "DispatchError",
    "EventSerializationError",
    "DataValidationError",
    "EventRegistrationError",
    "RandomManager",
]