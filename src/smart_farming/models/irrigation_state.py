"""
Runtime state model for irrigation simulation.

This module defines the mutable runtime state representing the irrigation
system assigned to an individual growing zone.

The IrrigationState is owned by the IrrigationStateManager and is updated
once per simulation cycle.

Unlike telemetry event models, this runtime model represents the current
operational state of the irrigation subsystem inside the simulator.

Responsibilities
----------------
The runtime state tracks:

- Current irrigation activity
- Water delivery
- Nutrient solution delivery
- Irrigation duration
- Irrigation pressure
- Flow rate

Event formatting, serialization, validation, and telemetry generation are
handled by higher application layers.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class IrrigationState:
    """
    Mutable runtime irrigation state for a growing zone.

    One runtime instance exists for each growing zone.

    Attributes
    ----------
    zone_id:
        Zone serviced by the irrigation system.

    irrigation_active:
        Indicates whether irrigation is currently operating.

    flow_rate_liters_per_minute:
        Current irrigation flow rate.

    pressure_kpa:
        Current irrigation line pressure.

    irrigation_duration_seconds:
        Duration of the current irrigation cycle.

    water_delivered_liters:
        Total water delivered during the current cycle.

    nutrient_solution_delivered_liters:
        Nutrient solution delivered during the current cycle.
    """

    zone_id: str

    facility_id: str

    irrigation_active: bool

    flow_rate_liters_per_minute: float

    pressure_kpa: float

    irrigation_duration_seconds: int

    water_delivered_liters: float

    nutrient_solution_delivered_liters: float

    last_irrigation_cycle: int = 0

    next_irrigation_cycle: int = 0

    irrigation_interval_cycles: int = 0

    irrigation_end_cycle: int = 0