"""
Lighting telemetry event model.

This module defines the normalized lighting telemetry event produced by
the HydroGrow Smart Farming Simulator.

Lighting telemetry represents the operational state of the artificial
grow-light system for an individual growing zone. The event captures the
lighting conditions experienced by crops and serves as the contract
consumed by downstream analytics platforms.
"""

from dataclasses import dataclass
from .base_event import BaseEvent


@dataclass(slots=True)
class LightingTelemetryEvent(BaseEvent):
    """
    Normalized lighting telemetry event.
    """

    zone_id: str
    lighting_enabled: bool
    lighting_intensity_percent: float
    photoperiod_hours: float
    daily_light_integral: float