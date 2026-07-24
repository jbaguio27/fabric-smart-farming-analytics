"""
Immutable Crop Lifecycle telemetry event.

This module defines the canonical event emitted by the
CropLifecycleGenerator.

CropLifecycleEvent represents a snapshot of a crop batch at a specific
simulation instant. The event is immutable and is intended for
serialization to downstream telemetry sinks such as Microsoft Fabric,
Kafka, Event Hubs, or file-based outputs.

The model intentionally contains no business logic.
"""

from dataclasses import dataclass
from .base_event import BaseEvent

@dataclass(slots=True)
class CropLifecycleEvent(BaseEvent):
    """
    Immutable Crop Lifecycle telemetry event.
    """

    crop_batch_id: str
    zone_id: str
    crop_type: str
    lifecycle_stage: str
    age_days: float
    health_score: float
    environmental_stress_index: float
    harvest_cycle_days: int = 35
    target_biomass_g: float = 150.0
    is_active: bool = True

    air_temperature_celsius: float = 22.0
    humidity_percent: float = 65.0
    water_ph: float = 6.0
    electrical_conductivity: float = 1.8
    simulation_cycle: int = 0