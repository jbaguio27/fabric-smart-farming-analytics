"""
Crop Telemetry Event.

This module defines the immutable telemetry event emitted by the
CropTelemetryGenerator.

Unlike CropLifecycleEvent, which captures business lifecycle milestones,
CropTelemetryEvent represents the continuous biological condition of an
active crop batch at a particular simulation cycle.

Instances are immutable once created to ensure downstream consumers
receive a consistent snapshot of the simulated crop state.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class CropTelemetryEvent:
    """
    Immutable crop telemetry event.

    Attributes
    ----------
    event_timestamp:
        Simulation timestamp when the telemetry was produced.

    simulation_cycle:
        Simulation cycle number.

    crop_batch_id:
        Unique crop batch identifier.

    facility_id:
        Facility containing the crop batch.

    zone_id:
        Growing zone identifier.

    crop_type:
        Crop variety.

    lifecycle_stage:
        Current lifecycle stage.

    age_days:
        Crop age expressed in days.

    health_score:
        Overall crop health.

    air_temperature_celsius:
        Current zone air temperature.

    humidity_percent:
        Current relative humidity.

    water_ph:
        Nutrient solution pH.

    electrical_conductivity:
        Nutrient solution electrical conductivity.
    """

    event_timestamp: datetime

    simulation_cycle: int

    crop_batch_id: str

    facility_id: str

    zone_id: str

    crop_type: str

    lifecycle_stage: str

    age_days: float

    health_score: float

    air_temperature_celsius: float

    humidity_percent: float

    water_ph: float

    electrical_conductivity: float