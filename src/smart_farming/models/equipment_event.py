"""
Equipment telemetry event model.

This module defines the event emitted by the Equipment Telemetry
Generator.

An EquipmentTelemetryEvent represents a snapshot of a single equipment
asset's operational condition at a specific point in simulated time.

The event combines immutable equipment metadata with mutable runtime
state managed by the EquipmentStateManager. It contains event data only
and intentionally excludes simulation behavior.
"""
from dataclasses import dataclass
from smart_farming.models import (
    BaseEvent,
    EquipmentOperatingStatus,
)

@dataclass(slots=True)
class EquipmentTelemetryEvent(BaseEvent):
    """
    Telemetry event representing the current operational state of a
    single equipment asset.

    This model is emitted by the EquipmentTelemetryGenerator and is
    intended to be streamed into Microsoft Fabric Eventstream.

    Attributes:
        equipment_id:
            Unique equipment identifier.

        facility_id:
            Identifier of the facility where the equipment is installed.

        zone_id:
            Identifier of the growing zone where the equipment operates.

        equipment_type:
            Equipment category defined in
            config.constants.EQUIPMENT_TYPES.

        operating_status:
            Current operating status.

        health:
            Current health percentage.

        runtime_hours:
            Total accumulated runtime.

        current_load:
            Current operating load expressed as a percentage.

        failure_probability:
            Calculated probability that the equipment will transition into a degraded
            operating state based on its current runtime condition.
    """

    equipment_id: str
    zone_id: str
    equipment_type: str
    operating_status: EquipmentOperatingStatus
    health: float
    runtime_hours: float
    current_load: float
    failure_probability: float