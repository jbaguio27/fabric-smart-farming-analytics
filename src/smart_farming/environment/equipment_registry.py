"""
Equipment registry.

This module manages the collection of persistent equipment assets used by
the Smart Farming simulator.

The registry acts as the central repository for equipment metadata and
provides lookup operations for generators and state managers.

Runtime characteristics such as equipment health, operating status,
runtime hours, and telemetry values are intentionally excluded. Those
responsibilities belong to the EquipmentStateManager.
"""

from collections import defaultdict
from smart_farming.models import Equipment
from smart_farming.utils import SimulationError

class EquipmentRegistry:
    """
    Stores and manages persistent equipment assets.

    Equipment objects are registered once during simulator
    initialization and reused throughout the simulation lifecycle.

    The registry is read-only after initialization unless equipment
    assets are intentionally added or removed.
    """

    def __init__(self) -> None:
        self._equipment: dict[str, Equipment] = {}

    def register(
        self,
        equipment: Equipment,
    ) -> None:
        """
        Register an equipment asset.

        Raises:
            SimulationError:
                If an equipment asset with the same ID is already
                registered.
        """

        if equipment.equipment_id in self._equipment:
            raise SimulationError(
                f"Equipment '{equipment.equipment_id}' is already registered."
            )
        
        self._equipment[equipment,equipment_id] = equipment

    def get(
        self,
        equipment_id: str,
    ) -> Equipment:
        """
        Retrieve an equipment asset.

        Args:
            equipment_id:
                Equipment_identifier.
        Returns:
            Registered equipment.
        Raises:
            SimulationError:
                If the equipment does not exist.
        """

        try:
            return self._equipment[equipment_id]
        except KeyError as exc:
            raise SimulationError(
                f"Equipment '{equipment_id}' is not registered."
            ) from exc
    
    def exists(
        self,
        equipment_id: str,
    ) -> bool:
        """
        Return whether an equipment asset is registered.
        """

        return equipment_id in self._equipment

    def list_all(self) -> list[Equipment]:
        """
        Return every registered equipment asset.
        """

        return list(self._equipment.values())

    def list_by_facility(
        self,
        zone_id: str,
    ) -> list[Equipment]:
        """
        Return all equipments within a facility.
        """
        return [
            equipment
            for equipment in self._equipment.values()
            if equipment.facility_id == facility_id
        ]

    def list_by_zone(
        self,
        zone_id: str,
    ) -> list[Equipment]:
        """
        Return all equipment within a growing zone.
        """
        return [
            equipment
            for equipment in self._equipment.values()
            if equipment.zone_id == zone_id
        ]
    
    def group_by_facility(self) -> dict[str, list[Equipment]]:
        """
        Group equipment by facility.
        """

        grouped: defaultdict[str, list[Equipment]] = defaultdict(list)

        for equipment in self._equipment.values():
            grouped[equipment.facility_id].append(equipment)

        return dict(grouped)

    def group_by_zone(self) -> dict[str, list[Equipment]]:
        """
        Group equipment by growing zone.
        """

        grouped: defaultdict[str, list[Equipment]] = defaultdict(list)

        for equipment in self._equipment.values():
            grouped[equipment.zone_id].append(equipment)

        return dict(grouped)

    def __len__(self) -> int:
        """
        Return the number of registered equipment assets.
        """

        return len(self._equipment)