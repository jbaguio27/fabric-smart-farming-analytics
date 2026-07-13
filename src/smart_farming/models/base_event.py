"""
Base event model shared by all Smart Farming simulator events.
"""

from dataclasses import dataclass, field, asdict
from smart_farming.config import (
    APPLICATION_NAME,
    SCHEMA_VERSION,
    FacilityId
)
from smart_farming.utils import (
    generate_event_id,
    utc_now
)


@dataclass(slots=True)
class BaseEvent:
    """
    Base event containing metadata shared by all simulator events.
    """

    event_type: str
    facility_id: FacilityId

    event_id: str = field(
        default_factory=generate_event_id,
        init=False,
    )

    timestamp: utc_now = field(
        default_factory= utc_now,
        init=False,
    )

    source: str = field(
        default=APPLICATION_NAME,
        init=False,
    )

    schema_version: str = field(
        default=SCHEMA_VERSION,
        init=False,
    )

    def to_dict(self) -> dict[str, object]:
        """
        Convert the event into a dictionary.

        Returns:
            Dictionary representation of the event.
        """

        return asdict(self)