"""
Facility Telemetry Event Model.

This module defines the immutable dataclass representing operational telemetry
and aggregated utilization metrics emitted by vertical farming facilities.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class FacilityEvent:
    """
    Telemetry event representing operational state and utilization of a vertical farm facility.

    Attributes:
        facility_id: Unique facility identifier (e.g. 'FAC-001').
        facility_name: Descriptive name of the vertical farm.
        operating_status: Current operational status ('ONLINE', 'WARNING', 'OFFLINE').
        active_zones_count: Number of active growing micro-location zones.
        total_equipment_count: Total installed equipment assets in the facility.
        average_equipment_health: Mean health score (0.0 to 100.0) across all facility equipment.
        total_power_consumption_kw: Aggregated facility electrical power demand in kW.
        total_water_consumption_lph: Aggregated nutrient water recirculation rate in liters/hour.
        timestamp: Event creation timestamp.
    """

    facility_id: str
    facility_name: str
    operating_status: str
    active_zones_count: int
    total_equipment_count: int
    average_equipment_health: float
    total_power_consumption_kw: float
    total_water_consumption_lph: float
    timestamp: datetime
