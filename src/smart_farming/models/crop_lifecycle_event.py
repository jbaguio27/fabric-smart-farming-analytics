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
from datetime import datetime
from typing import Optional

@dataclass(frozen=True, slots=True)
class CropLifecycleEvent:
    """
    Immutable Crop Lifecycle telemetry event.

    Attributes
    ----------
    event_timestamp:
        Simulation timestamp associated with the event.

    crop_batch_id:
        Unique crop batch identifier.

    zone_id:
        Growing zone containing the crop batch.

    crop_type:
        Human-readable crop variety.

    lifecycle_stage:
        Current biological lifecycle stage.

    age_days:
        Current biological age.

    health_score:
        Current biological health score.

    is_active:
        Indicates whether the crop batch is still active.

    air_temperature_celsius:
        Zone air temperature.

    humidity_percent:
        Zone humidity.

    water_ph:
        Nutrient solution pH.

    electrical_conductivity:
        Nutrient solution electrical conductivity.
    """

    event_timestamp: Optional[datetime]

    crop_batch_id: str
    zone_id: str
    crop_type: str

    lifecycle_stage: str

    age_days: float
    health_score: float
    is_active: bool

    air_temperature_celsius: float
    humidity_percent: float
    water_ph: float
    electrical_conductivity: float