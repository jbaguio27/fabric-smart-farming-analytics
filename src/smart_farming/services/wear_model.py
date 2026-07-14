"""
Wear model for equipment simulation.
"""

from smart_farming.environment.equipment_state import (
    EquipmentState,
)


class WearModel:
    """
    Calculates equipment health degradation.
    """

    def calculate_health(
        self,
        state: EquipmentState,
        degradation: float,
        wear_multiplier: float = 1.0,
    ) -> float:
        """
        Calculate the next health value.

        Parameters
        ----------
        state:
            Runtime equipment state.

        degradation:
            Base degradation amount.

        wear_multiplier:
            Equipment-type wear multiplier.

        Returns
        -------
        float
            Updated health value.
        """

        effective_degradation = (
            degradation
            * wear_multiplier
        )

        return max(
            0.0,
            state.health - effective_degradation,
        )