"""
Base event model shared by all Smart Farming simulator events.
"""

from dataclasses import dataclass, field
from datetime import datetime

from smart_farming.config.constants import (
    APPLICATION_NAME,
    SCHEMA_VERSION,
)
from smart_farming.utils.datetime_utils import utc_now
from smart_farming.utils.id_generator import generate_event_id

@dataclass(slots=True)
class BaseEvent:
    """
    Base event containing metadata shared by all simulator events.
    """

    event_type: str
    facility_id: str

    event_id: str = field(default_factory=generate_event_id)

    timestamp: datetime = field(default_factory=utc_now)

    source: str = field(default=APPLICATION_NAME)

    schema_version: str = field(default=SCHEMA_VERSION)