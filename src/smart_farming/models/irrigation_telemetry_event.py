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
from .base_event import BaseEvent


@dataclass(slots=True)
class IrrigationTelemetryEvent(BaseEvent):
    """
    Immutable irrigation telemetry event.
    """

    zone_id: str
    irrigation_active: bool
    flow_rate_liters_per_minute: float
    pressure_kpa: float
    irrigation_duration_seconds: int
    water_delivered_liters: float
    nutrient_solution_delivered_liters: float