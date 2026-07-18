"""
Crop Lifecycle Event Validator.

This module validates CropLifecycleEvent instances produced by the
CropLifecycleGenerator.

The validator guarantees that generated telemetry faithfully represents
the simulator runtime before events are emitted to downstream systems.

Validation intentionally remains read-only. No runtime state may be
modified by this component.
"""

from smart_farming.models import CropLifecycleEvent
from smart_farming.config import (
    CROP_LIFECYCLE_STAGES,
    EVENT_TYPE_CROP_LIFECYCLE,
)

class CropLifecycleValidator:
    """
    Validates crop lifecycle telemetry events.
    """

    def validate(
        self,
        event: CropLifecycleEvent,
    ) -> None:
        """
        Validate a crop lifecycle event.

        Raises
        ------
        AssertionError
            If any invariant is violated.
        """

        assert event.crop_batch_id, (
            "Crop batch identifier is required."
        )
        assert event.facility_id, (
            "Facility identifier is required."
        )
        assert event.zone_id, (
            "Growing zone identifier is required."
        )
        assert event.crop_type, (
            "Crop type is required."
        )

        assert (
            event.age_days >= 0.0
        ), (
            f"Crop age cannot be negative: "
            f"{event.age_days}"
        )

        assert (
            0.0 <= event.health_score <= 100.0
        ), (
            f"Health score must be between 0 and 100. "
            f"Received {event.health_score}"
        )

        assert (
            event.lifecycle_stage
            in CROP_LIFECYCLE_STAGES
        ), (
            f"Invalid lifecycle stage: "
            f"{event.lifecycle_stage}"
        )
        
        assert (
            event.air_temperature_celsius
            >= -20.0
        ), (
            f"Invalid air temperature: "
            f"{event.air_temperature_celsius} °C"
        )

        assert (
            0.0
            <= event.humidity_percent
            <= 100.0
        ), (
            f"Humidity must be between 0 and 100%. "
            f"Received {event.humidity_percent}."
        )

        assert (
            0.0
            <= event.water_ph
            <= 14.0
        ), (
            f"Water pH must be between 0 and 14. "
            f"Received {event.water_ph}."
        )

        assert (
            event.electrical_conductivity
            >= 0.0
        ), (
            f"Electrical conductivity cannot be negative. "
            f"Received {event.electrical_conductivity}."
        )

        assert (
            event.event_type == EVENT_TYPE_CROP_LIFECYCLE
        ),(
            f"Unexpected event type: "
            f"{event.event_type}"
        )

        assert event.simulation_cycle >= 0, (
            f"Simulation cycle cannot be negative. "
            f"Received {event.simulation_cycle}."
        )

        assert event.event_id, (
            "Event identifier is required."
        )

        assert event.event_timestamp is not None, (
            "Event timestamp is required."
        )