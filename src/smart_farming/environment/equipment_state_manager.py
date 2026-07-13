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
from smart_farming.config import (
    HEALTH_DEGRADATION_PER_RUNTIME_HOUR,
    MAX_EQUIPMENT_HEALTH,
    MIN_EQUIPMENT_HEALTH,
)
from smart_farming.models import EquipmentOperatingStatus
from smart_farming.utils import SimulationError

class EquipmentStateManager:
    """
    Manages routine state for registered equipment assets.
    """

    def __init__(
        self,
        equipment_registry: EquipmentRegistry,
    ) -> None:
        """
        Initialize the equipment runtime state manager.

        Runtime state is automatically created for every registered
        equipment asset during construction. This guarantees that all
        registered equipment has mutable runtime state available before
        telemetry generation begins.

        Args:
            equipment_registry:
                Registry containing all persistent equipment assets.
        """
        self._registry = equipment_registry
        self._states: dict[str, EquipmentState] = {}
        
        self.initialize()

    def initialize(self) -> None:
        """
        Create runtime state for every registered equipment asset.

        Existing runtime state is cleared before rebuilding to ensure
        the manager remains synchronized with the equipment registry.
        Each registered equipment asset receives exactly one mutable
        runtime state object.
        """

        self._states.clear()

        for equipment in self._registry.list_all():
            self._states[equipment.equipment_id] = EquipmentState()

    def advance_runtime(
        self,
        hours: float,
    ) -> None:
        """
        Advance runtime for every registered equipment asset.

        Each simulation cycle contributes operating time to every
        equipment asset. Runtime accumulation is performed before any
        health degradation or operating status evaluation.

        Args:
            hours:
                Number of operating hours represented by the current
                simulation cycle.
        """

        for state in self._states.values():
            state.runtime_hours += hours

    def update_health(
        self,
        hours: float,
    ) -> None:
        """
        Update equipment health based on runtime accumulation.

        Equipment health decreases deterministically as runtime increases.
        The amount of degradation is controlled through application
        configuration to provide predictable simulation behavior.

        Health is constrained to the configured minimum and maximum limits
        to prevent invalid runtime state.

        Args:
            hours:
                Number of operating hours represented by the current
                simulation cycle.
        """

        degradation = (
            HEALTH_DEGRADATION_PER_RUNTIME_HOUR
            * hours
        )

        for state in self._states.values():
            state.health = max(
                MIN_EQUIPMENT_HEALTH,
                min(
                    MAX_EQUIPMENT_HEALTH,
                    state.health - degradation,
                ),
            )

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