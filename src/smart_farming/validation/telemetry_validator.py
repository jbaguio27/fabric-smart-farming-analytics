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
from dataclasses import dataclass
from smart_farming.models import (
    EquipmentTelemetryEvent,
)
from smart_farming.config import (
    MAX_EQUIPMENT_HEALTH,
    MIN_EQUIPMENT_HEALTH,
    MAX_EQUIPMENT_LOAD,
    MIN_EQUIPMENT_LOAD,
    MAX_FAILURE_PROBABILITY,
    MIN_FAILURE_PROBABILITY,
)


@dataclass(slots=True)
class ValidationStatistics:
    """
    Aggregated validation statistics produced during a verification run.

    The validator updates these counters whenever a validation rule
    successfully executes. The statistics are intended purely for
    observability and verification reporting.

    Attributes:
        validated_events:
            Number of equipment telemetry events validated.

        runtime_consistency_checks:
            Number of runtime-to-event consistency validations executed.

        profile_compliance_checks:
            Number of equipment sensor profile validations executed.
    """

    validated_events: int = 0

    runtime_consistency_checks: int = 0

    profile_compliance_checks: int = 0

class TelemetryValidator():
    """
    Validates generated telemetry events.

    This service performs lightweight quality validation against emitted
    telemetry records. It does not mutate events and raises assertions
    when invalid telemetry is detected during verification.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize validation statistics.

        Statistics are collected solely for verification reporting and
        have no impact on simulator behavior.
        """

        self.statistics = ValidationStatistics()

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
        ), (
            f"{event.equipment_id}: "
            f"health precision violation "
            f"({event.health})"
        )

        assert (
            event.runtime_hours
            == state.runtime_hours
        ), (
            f"{event.equipment_id}: "
            f"runtime hourse precision violation "
            f"({event.runtime_hours})"
        )

        assert (
            event.current_load
            == state.current_load
        ), (
            f"{event.equipment_id}: "
            f"current load precision violation "
            f"({event.current_load})"
        )

        assert (
            event.failure_probability
            == state.failure_probability
        ), (
            f"{event.equipment_id}: "
            f"failure probability precision violation "
            f"({event.failure_probability})"
        )

        assert (
            event.operating_status
            == state.operating_status
        ), (
            f"{event.equipment_id}: "
            f"operating status precision violation "
            f"({event.operating_status})"
        )

        assert (
            event.power_consumption_kw
            == state.power_consumption_kw
        ), (
            f"{event.equipment_id}: "
            f"power consumption kw precision violation "
            f"({event.power_consumption_kw})"
        )

        assert (
            event.operating_temperature_c
            == state.temperature_celsius
        ), (
            f"{event.equipment_id}: "
            f"temperature celcius precision violation "
            f"({event.operating_temperature_c})"
        )

        assert (
            event.vibration_vps
            == state.vibration_mm_s
        ), (
            f"{event.equipment_id}: "
            f"vibration mm/s precision violation "
            f"({event.vibration_vps})"
        )

        self.statistics.runtime_consistency_checks += 1

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
        ), (
            f"{event.equipment_id}: "
            f"power consumption outside profile range "
            f"({event.power_consumption_kw})"
        )

        assert (
            profile.base_temperature_celsius
            <= event.operating_temperature_c
            <= profile.max_temperature_celsius
        ), (
            f"{event.equipment_id}: "
            f"temperature celsius outside profile range "
            f"({event.operating_temperature_c})"
        )

        assert (
            profile.base_vibration_mm_s
            <= event.vibration_vps
            <= profile.max_vibration_mm_s
        ), (
            f"{event.equipment_id}: "
            f"vibration mm/s outside profile range "
            f"({event.vibration_vps})"
        )

        self.statistics.profile_compliance_checks += 1

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

        assert (
            MIN_EQUIPMENT_HEALTH 
            <= event.health 
            <= MAX_EQUIPMENT_HEALTH
        ), (
            f"{event.equipment_id}: "
            f"health outside profile range "
            f"({event.health})"
        )

        assert (
            event.runtime_hours 
            >= 0.0
        ), (
            f"{event.equipment_id}: "
            f"runtime hourse under 0.0"
            f"({event.runtime_hours})"
        )

        assert (
            MIN_EQUIPMENT_LOAD 
            <= event.current_load 
            <= MAX_EQUIPMENT_LOAD
        ), (
            f"{event.equipment_id}: "
            f"current load outside profile range "
            f"({event.current_load})"
        )

        assert (
            MIN_FAILURE_PROBABILITY
            <= event.failure_probability 
            <= MAX_FAILURE_PROBABILITY
        ), (
            f"{event.equipment_id}: "
            f"failure probability outside profile range "
            f"({event.failure_probability})"
        )

        # Sensor telemetry validation

        assert (
            event.power_consumption_kw 
            > 0.0
        ), (
            f"{event.equipment_id}: "
            f"power consumption under 0.0 "
            f"({event.power_consumption_kw})"
        )

        assert (
            event.operating_temperature_c 
            > 0.0
        ), (
            f"{event.equipment_id}: "
            f"temperature celcius under 0.0 "
            f"({event.operating_temperature_c})"
        )

        assert (
            event.vibration_vps 
            > 0.0
        ), (
            f"{event.equipment_id}: "
            f"vibration under 0.0 "
            f"({event.vibration_vps})"
        )

        # Physical plausibility validation

        assert (
            event.operating_temperature_c 
            >= 0.0
        ), (
            f"{event.equipment_id}: "
            f"temperature celcius under 0.0 "
            f"({event.operating_temperature_c})"
        )

        assert (
            event.operating_temperature_c 
            <= 100.0
        ), (
            f"{event.equipment_id}: "
            f"temperature celcius exceeded 100.0 "
        )

        assert (
            event.vibration_vps 
            <= 20.0
        ), (
            f"{event.equipment_id}: "
            f"vibration exceeded 20.0 "
            f"({event.vibration_vps})"
        )

        assert (
            event.power_consumption_kw 
            <= 100.0
        ), (
            f"{event.equipment_id}: "
            f"power consumption exceeded 100.0 "
            f"({event.power_consumption_kw})"
        )

        # Event normalization validation

        assert (
            event.health 
            == round(
                event.health, 
                2
            )
        ), (
            f"{event.equipment_id}: "
            f"health precision violation "
            f"({event.health})"
        )

        assert (
            event.runtime_hours 
            == round(
                event.runtime_hours, 
                2
            )
        ), (
            f"{event.equipment_id}: "
            f"runtime hours precision violation "
            f"({event.runtime_hours})"
        )

        assert (
            event.current_load 
            == round(
                event.current_load, 
                2
            )
        ), (
            f"{event.equipment_id}: "
            f"current load precision violation "
            f"({event.current_load})"
        )

        assert (
            event.failure_probability 
            == round(
                event.failure_probability,
                4
            )
        ), (
            f"{event.equipment_id}: "
            f"failure probability precision violation "
            f"({event.failure_probability})"
        )

        assert (
            event.operating_temperature_c
            == round(
                event.operating_temperature_c,
                2,
            )
        ), (
            f"{event.equipment_id}: "
            f"temperature celcius precision violation "
            f"({event.operating_temperature_c})"
        )

        assert (
            event.vibration_vps
            == round(
                event.vibration_vps,
                3,
            )
        ), (
            f"{event.equipment_id}: "
            f"vibration precision violation "
            f"({event.vibration_vps})"
        )

        self.statistics.validated_events += 1