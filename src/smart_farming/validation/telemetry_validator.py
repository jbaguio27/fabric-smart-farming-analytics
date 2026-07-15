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
5. Invalid telemetry is detected before downstream ingestion.

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