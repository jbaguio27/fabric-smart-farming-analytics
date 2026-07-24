"""
Facility State Manager.
This module provides the runtime state manager responsible for tracking
and updating the operational state of all Philippine hydroponics vertical farming facilities.
"""

from datetime import datetime, timezone
from typing import Final
from smart_farming.config import (
    PHILIPPINE_FACILITY_PROFILES,
    HEALTHY_FACILITY_THRESHOLD,
    ZONE_POWER_CONSUMPTION_KW,
    ZONE_WATER_RECIRCULATION_LPH,
)
from smart_farming.schemas import FacilityProfile
from smart_farming.models import FacilityEvent
from .equipment_state_manager import EquipmentStateManager
from .equipment_registry import EquipmentRegistry


class FacilityStateManager:
    """
    Manages operational state and aggregated metrics for all registered vertical farming facilities.
    """

    def __init__(
        self,
        equipment_state_manager: EquipmentStateManager | None = None,
        equipment_registry: EquipmentRegistry | None = None,
    ) -> None:
        """
        Initialize the FacilityStateManager.

        Args:
            equipment_state_manager: Optional EquipmentStateManager reference for health aggregation.
            equipment_registry: Optional EquipmentRegistry reference for facility equipment lookup.
        """

        self._profiles: Final[dict[str, FacilityProfile]] = PHILIPPINE_FACILITY_PROFILES
        self._equipment_state_manager = equipment_state_manager
        self._equipment_registry = equipment_registry

    def get_profile(
        self,
        facility_id: str,
    ) -> FacilityProfile:
        """
        Retrieve the facility profile for a given facility ID.

        Args:
            facility_id: Unique facility identifier (e.g. 'FAC-001').
        Returns:
            FacilityProfile dataclass instance.
        """

        if facility_id not in self._profiles:
            raise KeyError(f"Facility profile '{facility_id}' not found in registry.")

        return self._profiles[facility_id]

    def list_facility_ids(self) -> tuple[str, ...]:
        """
        Return a tuple of all registered facility IDs.

        Returns:
            Tuple of facility ID strings.
        """

        return tuple(self._profiles.keys())

    def get_all_profiles(self) -> tuple[FacilityProfile, ...]:
        """
        Return a tuple of all registered facility profiles.

        Returns:
            Tuple of FacilityProfile instances.
        """

        return tuple(self._profiles.values())

    def generate_facility_event(
        self,
        facility_id: str,
    ) -> FacilityEvent:
        """
        Generate a FacilityEvent snapshot for the specified facility.

        Args:
            facility_id: Facility identifier string.
        Returns:
            FacilityEvent dataclass populated with aggregated operational metrics.
        """

        profile = self.get_profile(facility_id)
        active_zones_count = len(profile.micro_locations)

        total_equipment = 0
        avg_health = 100.0
        active_alerts = 0
        total_power_kw = active_zones_count * ZONE_POWER_CONSUMPTION_KW

        # Determine effective equipment registry
        registry = self._equipment_registry
        if registry is None and self._equipment_state_manager is not None:
            registry = getattr(self._equipment_state_manager, "_equipment_registry", None)

        if registry is not None and self._equipment_state_manager is not None:
            facility_equipments = registry.list_by_facility(facility_id)
            if facility_equipments:
                total_equipment = len(facility_equipments)
                states = [
                    self._equipment_state_manager.get(eq.equipment_id)
                    for eq in facility_equipments
                    if self._equipment_state_manager.exists(eq.equipment_id)
                ]
                if states:
                    avg_health = sum(s.health for s in states) / len(states)
                    equipment_power = sum(s.power_consumption_kw for s in states)
                    if equipment_power > 0:
                        total_power_kw = equipment_power
                    active_alerts = sum(
                        1 for s in states
                        if str(getattr(s.operating_status, "value", s.operating_status)).upper() in ["WARNING", "DEGRADED", "ERROR", "OFFLINE"]
                    )

        operating_status = "ONLINE" if avg_health >= HEALTHY_FACILITY_THRESHOLD else "WARNING"
        total_water_lph = active_zones_count * ZONE_WATER_RECIRCULATION_LPH

        event = FacilityEvent(
            event_type="FacilityEvent",
            facility_id=profile.facility_id,
            facility_name=profile.facility_name,
            operating_status=operating_status,
            active_zones_count=active_zones_count,
            total_equipment_count=total_equipment,
            overall_health=round(avg_health, 2),
            power_draw_kw=round(total_power_kw, 2),
            water_circulation_lph=round(total_water_lph, 2),
            active_critical_alerts=active_alerts,
            region=getattr(profile, "region", ""),
            city=getattr(profile, "location", ""),
            latitude=getattr(profile, "latitude", 0.0),
            longitude=getattr(profile, "longitude", 0.0),
            elevation_m=getattr(profile, "elevation_m", 0.0),
            climate_zone=getattr(profile, "domain_focus", ""),
            water_source=getattr(profile, "water_source", ""),
            power_grid_redundancy=getattr(profile, "power_grid_redundancy", ""),
            max_zone_capacity=getattr(profile, "max_zone_capacity", 0),
        )
        return event