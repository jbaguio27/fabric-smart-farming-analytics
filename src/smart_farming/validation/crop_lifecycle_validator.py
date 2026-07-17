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

        assert event.crop_batch_id
        assert event.facility_id
        assert event.zone_id
        assert event.crop_type

        assert event.age_days >= 0.0

        assert 0.0 <= event.health_score <= 100.0

        assert event.lifecycle_stage in (
            "GERMINATION",
            "SEEDLING",
            "VEGETATIVE",
            "MATURE",
            "HARVESTED",
        )
        
        assert (
            event.air_temperature_celsius
            >= -20.0
        )

        assert (
            0.0
            <= event.humidity_percent
            <= 100.0
        )

        assert (
            0.0
            <= event.water_ph
            <= 14.0
        )

        assert (
            event.electrical_conductivity
            >= 0.0
        )