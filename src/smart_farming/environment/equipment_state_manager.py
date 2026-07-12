"""
Equipment runtime state manager.

This module manages mutable runtime state for registered equipment assets.

The manager owns all state transitions, initialization, and runtime
updates. It intentionally separates business logic from the Equipment
and EquipmentState models.
"""

from smart_farming.environment import (
    EquipmentRegistry,
    EquipmentState
)
from smart_farming.models import EquipmentOperatingStatus
from smart_farming.utils import SimulationError

class EquipmentStateManager:
    """
    Manages routine state for registered equipment assets.
    """

    def __init__(
        self,
        registry: EquipmentRegistry,
    ) -> None:
        self._registry = registry
        self._states: dict[str, EquipmentState] = {}

    def initialize(self) -> None:
        """
        Create runtime state for every registered equipment asset.
        """

        self._states.clear()

        for equipment in self._registry.list_all():
            self._states[equipment.equipment_id] = EquipmentState()

    def get(
        self,
        equipment_id: str,
    ) -> EquipmentState:
        """
        Retrieve runtime state for an equipment asset.

        Raises:
            SimulationError:
                If runtime state has not been initialized.
        """

        try:
            return self._states[equipment_id]
        except KeyError as exc:
            raise SimulationError(
                f"No runtime state exists for equipment '{equipment_id}'."
            ) from exc
    
    def exists(
        self,
        equipment_id: str,
    ) -> bool:
        """
        Return whether runtime state exists.
        """
        return equipment_id in self._states

    def list_all(self) -> dict[str, EquipmentState]:
        """
        Return every equipment runtime state.
        """
        return dict(self._states)
    
    def set_operating_status(
        self,
        equipment_id: str,
        status: EquipmentOperatingStatus,
    ) -> None:
        """
        Update the operating status for an equipment asset.
        """
        self.get(equipment_id).operating_status = status

    def update_runtime(
        self,
        equipment_id: str,
        hours: float,
    ) -> None:
        """
        Increment accumulated runtime.
        """
        self.get(equipment_id).runtime_hours += hours

    def update_load(
        self,
        equipment_id: str,
        load: float,
    ) -> None:
        """
        Update equipment load.
        """
        self.get(equipment_id).current_load = load
    
    def update_health(
        self,
        equipment_id: str,
        health: float,
    ) -> None:
        """
        Update equipment health.
        """
        self.get(equipment_id).health = health