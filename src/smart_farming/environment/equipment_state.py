"""
Equipment runtime state.

This module defines the mutable operational state associated with a
registered equipment asset.

Unlike the Equipment domain model, EquipmentState stores values that
change throughout the simulation, such as operating status, health,
runtime, and maintenance information.

Business logic is intentionally excluded. State transitions are managed
by the EquipmentStateManager.
"""

from dataclasses import dataclass
from datetime import datetime
from smart_farming.models import EquipmentOperatingStatus

@dataclass(slots=True)
class EquipmentState:
    """
    Represents the mutable runtime state of a registered equipment asset.

    This state changes during the simulation while the corresponding
    Equipment model remains immutable.

    Attributes:
        operating_status:
            Current operating condition.

        health:
            Overall equipment health percentage.

        runtime_hours:
            Accumulated operating hours.

        current_load:
            Current utilization expressed as a percentage.

        failure_probability:
            Probability of failure during the current simulation cycle.

        power_consumption_kw:
            Simulated equipment power draw in kilowatts.

        temperature_celsius:
            Simulated equipment operating temperature in degrees Celsius.

        vibration_mm_s:
            Simulated equipment vibration velocity in millimeters per
            second.

        last_maintenance_at:
            Timestamp of the most recent maintenance event.
    """

    operating_status: EquipmentOperatingStatus = (
        EquipmentOperatingStatus.ONLINE
    )

    health: float = 100.0

    runtime_hours: float = 0.0

    current_load: float = 0.0

    failure_probability: float = 0.0

    power_consumption_kw: float = 0.0

    temperature_celsius: float = 0.0

    vibration_mm_s: float = 0.0

    last_maintenance_at: datetime | None = None