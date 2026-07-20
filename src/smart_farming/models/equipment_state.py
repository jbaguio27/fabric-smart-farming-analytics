"""
Equipment runtime state.

This module defines the mutable runtime state associated with a
registered equipment asset.

Unlike the Equipment domain model, EquipmentState stores operational
values that evolve throughout the simulation, including equipment
health, operating status, utilization, runtime accumulation, simulated
sensor measurements, and maintenance history.

Business logic is intentionally excluded from this model. Runtime state
transitions are performed exclusively by the EquipmentStateManager.

Separating this runtime model from the Environment layer keeps the
domain model independent from orchestration logic and aligns the
equipment subsystem with the simulator's architecture used for CropState,
LightingState, and IrrigationState.
"""

from dataclasses import dataclass
from datetime import datetime

from smart_farming.models import EquipmentOperatingStatus


@dataclass(slots=True)
class EquipmentState:
    """
    Mutable runtime state for a registered equipment asset.

    An EquipmentState instance exists for every Equipment registered
    within the simulator. The state is continuously updated during each
    simulation cycle while the corresponding Equipment model remains
    immutable.

    This model intentionally contains only runtime data. Simulation
    behavior and state transitions are implemented by the
    EquipmentStateManager.

    Attributes
    ----------
    operating_status:
        Current simulated operating condition.

    health:
        Overall equipment health percentage.

    runtime_hours:
        Accumulated operating hours.

    current_load:
        Current operating utilization percentage.

    failure_probability:
        Calculated probability of failure for the current simulation
        cycle.

    power_consumption_kw:
        Simulated electrical power consumption.

    temperature_celsius:
        Simulated operating temperature.

    vibration_mm_s:
        Simulated vibration level.

    last_maintenance_at:
        Timestamp of the most recent maintenance activity.
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