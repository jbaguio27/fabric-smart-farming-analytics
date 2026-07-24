"""
Philippine Hydroponics Facility Profiles & Regional Configurations.

This module defines the FacilityProfile and ZoneMicroLocation dataclasses
for the 8 Philippine hydroponics vertical farming facilities (FAC-001 through FAC-008).

Facility profiles establish geographic locations, regional climate baselines,
target microclimates (temperature, humidity, pH, EC), vertical rack micro-locations,
and raw telemetry data anomaly profiles for Microsoft Fabric streaming ingestion.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ZoneMicroLocation:
    """
    Immutable representation of an internal vertical farming growing micro-location (zone/tier/rack).

    Attributes:
        zone_id: Zone identifier (e.g. 'ZONE-001').
        zone_name: Internal facility location or room description.
        dominant_crop_key: Primary crop key from CROP_GROWTH_PROFILES (e.g. 'butterhead_lettuce').
    """

    zone_id: str
    zone_name: str
    dominant_crop_key: str


@dataclass(frozen=True, slots=True)
class FacilityProfile:
    """
    Immutable profile definition for a Philippine hydroponics vertical farming facility.

    Attributes:
        facility_id: Unique facility identifier (e.g. 'FAC-001').
        facility_name: Descriptive name of the vertical farm.
        location: Specific municipality/city and province in the Philippines.
        region: Official administrative region in the Philippines.
        domain_focus: Primary hydroponics vertical farming subsystem or crop focus.
        target_temperature_celsius: Target climate baseline temperature in Celsius.
        target_humidity_percent: Target relative humidity percentage.
        target_ph: Target nutrient solution pH level.
        target_ec: Target electrical conductivity in mS/cm.
        primary_crops: List of primary crops cultivated at the facility.
        operating_hours: Standard facility photoperiod or operational hours.
        anomaly_trait: Characteristic raw data anomaly profile for Bronze ingestion.
        micro_locations: Tuple of internal growing zone micro-locations.
    """

    facility_id: str
    facility_name: str
    location: str
    region: str
    domain_focus: str
    target_temperature_celsius: float
    target_humidity_percent: float
    target_ph: float
    target_ec: float
    primary_crops: tuple[str, ...]
    operating_hours: str
    anomaly_trait: str
    latitude: float = 0.0
    longitude: float = 0.0
    elevation_m: float = 0.0
    water_source: str = ""
    power_grid_redundancy: str = ""
    max_zone_capacity: int = 0
    micro_locations: tuple[ZoneMicroLocation, ...] = field(default_factory=tuple)
