"""
Telemetry validation service.

This module contains validation logic for generated telemetry events.

The validator is intentionally separated from telemetry generators to
preserve single responsibility. Generators create events, while
validators verify event quality before downstream ingestion.

Initial validation focuses on equipment telemetry events and verifies:

1. Required identifiers exist.
2. Runtime metrics remain within expected ranges.
3. Sensor metrics are populated.
4. Sensor metrics remain physically plausible.
5. Event normalization rules are enforced.
6. Invalid telemetry is detected before downstream ingestion.

Future roadmap items may extend this validator with:

- anomaly detection validation
- missing telemetry detection
- schema compliance checks
- Fabric ingestion readiness checks
"""

from smart_farming.models import (
    EquipmentTelemetryEvent,
)


class TelemetryValidator:
    """
    Validates generated telemetry events.

    This service performs lightweight quality validation against emitted
    telemetry records. It does not mutate events and raises assertions
    when invalid telemetry is detected during verification.
    """

    def validate_runtime_consistency(
        self,
        event: EquipmentTelemetryEvent,
        state,
    ) -> None:
        """
        Validate that a telemetry event accurately reflects the
        runtime state from which it was generated.

        This validation protects the event contract by ensuring that
        telemetry generation remains a read-only projection of runtime
        state. Any mismatch indicates that the event generator is no
        longer faithfully emitting simulator state.

        Args:
            event:
                Generated equipment telemetry event.

            state:
                Runtime EquipmentState associated with the same
                equipment asset.

        Raises:
            AssertionError:
                Raised when event values diverge from runtime state.
        """

        assert (
            event.health
            == state.health
        )

        assert (
            event.runtime_hours
            == state.runtime_hours
        )

        assert (
            event.current_load
            == state.current_load
        )

        assert (
            event.failure_probability
            == state.failure_probability
        )

        assert (
            event.operating_status
            == state.operating_status
        )

        assert (
            event.power_consumption_kw
            == state.power_consumption_kw
        )

        assert (
            event.temperature_celsius
            == state.temperature_celsius
        )

        assert (
            event.vibration_mm_s
            == state.vibration_mm_s
        )

    def validate_sensor_profile_compliance(
        self,
        event: EquipmentTelemetryEvent,
        profile,
    ) -> None:
        """
        Validate that emitted sensor telemetry remains within the
        boundaries defined by the equipment type's sensor profile.

        This validation ensures that telemetry generation continues to
        respect the calibration contract established by
        EquipmentSensorProfile.

        Args:
            event:
                Generated equipment telemetry event.

            profile:
                Sensor profile associated with the equipment type.

        Raises:
            AssertionError:
                Raised when emitted telemetry falls outside the profile
                boundaries.
        """

        assert (
            profile.idle_power_kw
            <= event.power_consumption_kw
            <= profile.max_power_kw
        )

        assert (
            profile.base_temperature_celsius
            <= event.temperature_celsius
            <= profile.max_temperature_celsius
        )

        assert (
            profile.base_vibration_mm_s
            <= event.vibration_mm_s
            <= profile.max_vibration_mm_s
        )

    def validate_equipment_event(
        self,
        event: EquipmentTelemetryEvent,
    ) -> None:
        """
        Validate a single equipment telemetry event.

        Args:
            event:
                Generated equipment telemetry event.

        Raises:
            AssertionError:
                Raised when telemetry contains invalid or missing data.
        """

        assert event.equipment_id

        assert event.facility_id

        assert event.zone_id

        assert 0.0 <= event.health <= 100.0

        assert event.runtime_hours >= 0.0

        assert 0.0 <= event.current_load <= 100.0

        assert 0.0 <= event.failure_probability <= 1.0

        # Sensor telemetry validation

        assert event.power_consumption_kw > 0.0

        assert event.temperature_celsius > 0.0

        assert event.vibration_mm_s > 0.0

        # Physical plausibility validation

        assert event.temperature_celsius >= 0.0

        assert event.temperature_celsius <= 100.0

        assert event.vibration_mm_s <= 20.0

        assert event.power_consumption_kw <= 100.0

        # Event normalization validation

        assert event.health == round(event.health, 2)

        assert event.runtime_hours == round(event.runtime_hours, 2)

        assert event.current_load == round(event.current_load, 2)

        assert event.failure_probability == round(event.failure_probability, 4)

        assert (
            event.temperature_celsius
            == round(
                event.temperature_celsius,
                2,
            )
        )

        assert (
            event.vibration_mm_s
            == round(
                event.vibration_mm_s,
                3,
            )
        )