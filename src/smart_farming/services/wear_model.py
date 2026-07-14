"""
Wear model for equipment simulation.

Currently this class reproduces the existing wear calculation
performed inside EquipmentStateManager.

No behavior changes are introduced in this refactor.
"""

from smart_farming.environment.equipment_state import EquipmentState


class WearModel:
    """
    Calculates health degradation for equipment.
    """

    def apply(
        self,
        state: EquipmentState,
        degradation: float,
    ) -> None:
        """
        Apply health degradation.

        Parameters
        ----------
        state:
            Equipment runtime state.

        degradation:
            Amount of health to remove.
        """

        state.health = max(
            0.0,
            state.health - degradation,
        )