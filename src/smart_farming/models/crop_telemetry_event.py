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
from .base_event import BaseEvent


@dataclass(slots=True)
class CropTelemetryEvent(BaseEvent):
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

    growth_rate:
        Current growth rate.

    biomass_grams:
        Total biomass in grams.

    water_consumption_liters:
        Water consumption in liters.

    nutrient_consumption_grams:
        Nutrient consumption in grams.

    environmental_stress_index:
        Index representing environmental stress.

    ambient_temperature_celsius:
        Current ambient air temperature.

    ambient_humidity_percent:
        Current relative humidity.

    water_ph:
        Nutrient solution pH.

    electrical_conductivity:
        Nutrient solution electrical conductivity.
    """

    simulation_cycle: int
    crop_batch_id: str
    zone_id: str
    crop_type: str
    lifecycle_stage: str
    age_days: float
    health_score: float
    growth_rate: float
    biomass_grams: float
    water_consumption_liters: float
    nutrient_consumption_grams: float
    environmental_stress_index: float
    ambient_temperature_celsius: float
    ambient_humidity_percent: float
    water_ph: float
    electrical_conductivity: float