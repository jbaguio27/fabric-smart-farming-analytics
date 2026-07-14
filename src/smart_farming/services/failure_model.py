"""
Failure model for equipment simulation.

This service will eventually contain all probability and
operating-state calculations.

During the structural refactor it simply mirrors the current
EquipmentStateManager implementation.
"""

from smart_farming.environment.equipment_state import EquipmentState


class FailureModel:
    """
    Applies failure probability calculations.
    """

    def apply(
        self,
        state: EquipmentState,
        probability: float,
    ) -> None:
        """
        Update failure probability.

        Parameters
        ----------
        state:
            Runtime equipment state.

        probability:
            Newly calculated probability.
        """

        state.failure_probability = probability