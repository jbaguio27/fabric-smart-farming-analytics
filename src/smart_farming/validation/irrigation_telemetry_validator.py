"""
Validation helpers for irrigation telemetry events.

This module validates IrrigationTelemetryEvent instances before they are
published to downstream telemetry consumers.

The validator intentionally performs structural and domain validation
only. It does not modify event contents.
"""

from smart_farming.models import (
    IrrigationTelemetryEvent,
)


class IrrigationTelemetryValidator:
    """
    Validate irrigation telemetry events.
    """

    @staticmethod
    def validate(
        event: IrrigationTelemetryEvent,
    ) -> None:
        """
        Validate a single irrigation telemetry event.

        Args:
            event:
                Irrigation telemetry event.

        Raises:
            AssertionError:
                Raised when an event violates the telemetry contract.
        """

        assert event.event_id, (
            "Event ID must not be empty."
        )

        assert event.event_type == (
            "irrigation.telemetry"
        ), (
            "Unexpected irrigation event type."
        )

        assert event.event_timestamp is not None, (
            "Event timestamp is required."
        )

        assert event.facility_id, (
            "Facility ID must not be empty."
        )

        assert event.zone_id, (
            "Zone ID must not be empty."
        )

        assert (
            event.flow_rate_liters_per_minute >= 0.0
        ), (
            "Flow rate cannot be negative."
        )

        assert (
            event.pressure_kpa >= 0.0
        ), (
            "Pressure cannot be negative."
        )

        assert (
            event.irrigation_duration_seconds >= 0
        ), (
            "Irrigation duration cannot be negative."
        )

        assert (
            event.water_delivered_liters >= 0.0
        ), (
            "Delivered water cannot be negative."
        )

        assert (
            event.nutrient_solution_delivered_liters >= 0.0
        ), (
            "Delivered nutrient solution cannot be negative."
        )