"""
Equipment wear model.

This module provides the domain service responsible for calculating
equipment health degradation over time.

The WearModel is intentionally stateless. It receives the current
runtime state and degradation inputs from the EquipmentStateManager and
returns the updated health value without mutating simulator state.

Responsibilities
----------------
The WearModel is responsible only for:

- Applying health degradation
- Applying equipment-specific wear multipliers
- Enforcing health boundaries

It intentionally does not determine:

- Equipment load
- Failure probability
- Operating status
- Maintenance scheduling

Those responsibilities belong to their respective domain services.
"""

from smart_farming.config import (
    MAX_EQUIPMENT_HEALTH,
    MIN_EQUIPMENT_HEALTH,
)
from smart_farming.models import EquipmentState


class WearModel:
    """
    Stateless domain service for equipment wear calculations.
    """

    def calculate_health(
        self,
        state: EquipmentState,
        degradation: float,
        wear_multiplier: float,
    ) -> float:
        """
        Calculate the next equipment health value.

        Parameters
        ----------
        state:
            Current runtime state.

        degradation:
            Base degradation for the simulation cycle.

        wear_multiplier:
            Equipment-specific wear multiplier.

        Returns
        -------
        float
            Updated equipment health constrained to the configured
            health boundaries.
        """

        health = (
            state.health
            - (degradation * wear_multiplier)
        )

        return max(
            MIN_EQUIPMENT_HEALTH,
            min(
                MAX_EQUIPMENT_HEALTH,
                health,
            ),
        )