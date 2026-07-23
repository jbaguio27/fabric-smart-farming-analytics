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
    is_active: bool

    air_temperature_celsius: float
    humidity_percent: float
    water_ph: float
    electrical_conductivity: float
    simulation_cycle: int