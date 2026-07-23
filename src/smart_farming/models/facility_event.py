"""
Facility Telemetry Event Model.

This module defines the immutable dataclass representing operational telemetry
and aggregated utilization metrics emitted by vertical farming facilities.
"""

from dataclasses import dataclass
from .base_event import BaseEvent


@dataclass(slots=True)
class FacilityEvent(BaseEvent):
    """
    Telemetry event representing operational state and utilization of a vertical farm facility.
    """

    facility_name: str
    operating_status: str
    active_zones_count: int
    total_equipment_count: int
    overall_health: float
    power_draw_kw: float
    water_circulation_lph: float
    active_critical_alerts: int
    region: str = ""
    city: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    elevation_m: float = 0.0
    climate_zone: str = ""
    water_source: str = ""
    power_grid_redundancy: str = ""
    max_zone_capacity: int = 0
