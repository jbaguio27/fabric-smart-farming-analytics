"""
Philippine Facility Profiles & Regional Configurations.
This module defines the FacilityProfile dataclass and the central registry
of 8 Philippine smart farming facilities (FAC-001 through FAC-008).
Facility profiles establish geographic locations, regional climate baselines,
target microclimates (temperature, humidity, pH, EC), agricultural domain foci,
and raw telemetry data anomaly profiles for Microsoft Fabric streaming ingestion.
"""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class FacilityProfile:
    """
    Immutable profile definition for a Philippine smart farming facility.
    Attributes:
        facility_id: Unique facility identifier (e.g. 'FAC-001').
        facility_name: Descriptive name of the facility.
        location: Specific municipality/city and province in the Philippines.
        region: Official administrative region in the Philippines.
        domain_focus: Primary agricultural domain or crop focus.
        target_temperature_celsius: Target climate baseline temperature in Celsius.
        target_humidity_percent: Target relative humidity percentage.
        target_ph: Target substrate/water pH level.
        target_ec: Target electrical conductivity in mS/cm.
        primary_crops: List of primary crops cultivated at the facility.
        operating_hours: Standard facility photoperiod or operational hours.
        anomaly_trait: Characteristic raw data anomaly profile for Bronze ingestion.
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