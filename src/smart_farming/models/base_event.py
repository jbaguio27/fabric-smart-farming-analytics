"""
Base event model shared by all Smart Farming simulator events.
"""

from dataclasses import dataclass, field, asdict
from smart_farming.config.constants import (
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

    operator_contact: str = field(
        default="",
        init=False,
    )

    operator_phone: str = field(
        default="+639175551234",
        init=False,
    )

    def __post_init__(self) -> None:
        facility = str(self.facility_id).lower() if self.facility_id else "fac-001"
        self.operator_contact = f"tech.{facility}@smartfarm.ph"
        
        facility_phones = {
            "fac-001": "+639178452190",
            "fac-002": "+639183920411",
            "fac-003": "+639209518342",
            "fac-004": "+639284031955",
            "fac-005": "+639985721048",
            "fac-006": "+639082496103",
            "fac-007": "+639196308274",
            "fac-008": "+639271845920",
        }
        self.operator_phone = facility_phones.get(facility, "+639178452190")

    def to_dict(self) -> dict[str, object]:
        """
        Convert the event into a dictionary.

        Returns:
            Dictionary representation of the event.
        """

        return asdict(self)