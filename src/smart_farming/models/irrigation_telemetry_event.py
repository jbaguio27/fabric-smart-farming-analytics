"""
Irrigation telemetry event model.

This module defines the telemetry contract representing the operational
state of the irrigation subsystem for a growing zone.

Unlike IrrigationState, which stores mutable runtime simulation data,
this event model represents an immutable telemetry record emitted by the
IrrigationTelemetryGenerator.

The resulting event is intended for downstream analytics platforms such
as Microsoft Fabric Eventstream, Eventhouse, Lakehouse, and Power BI.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class IrrigationTelemetryEvent:
    """
    Immutable irrigation telemetry event.

    Attributes
    ----------
    event_id:
        Globally unique telemetry event identifier.

    event_type:
        Event contract name.

    event_timestamp:
        Timestamp when the telemetry event was generated.

    facility_id:
        Facility identifier.

    zone_id:
        Growing zone identifier.

    irrigation_active:
        Indicates whether irrigation is currently operating.

    flow_rate_liters_per_minute:
        Current irrigation flow rate.

    pressure_kpa:
        Irrigation line pressure.

    irrigation_duration_seconds:
        Current irrigation duration.

    water_delivered_liters:
        Water volume delivered.

    nutrient_solution_delivered_liters:
        Nutrient solution volume delivered.
    """

    event_id: str

    event_type: str

    event_timestamp: datetime

    facility_id: str

    zone_id: str

    irrigation_active: bool

    flow_rate_liters_per_minute: float

    pressure_kpa: float

    irrigation_duration_seconds: int

    water_delivered_liters: float

    nutrient_solution_delivered_liters: float