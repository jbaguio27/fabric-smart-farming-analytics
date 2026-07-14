"""
Maintenance service.

This service manages maintenance eligibility
and maintenance execution for equipment assets.
"""
from datetime import datetime
from smart_farming.environment.equipment_state import EquipmentState
from smart_farming.config import (
    MAINTENANCE_INTERVAL_HOURS,
    MAINTENANCE_HEALTH_THRESHOLD,
    MAINTENANCE_RESTORE_HEALTH,
    MAINTENANCE_RESET_FAILURE_PROBABILITY,
)


class MaintenanceManager:
    """
    Executes preventive maintenance logic.
    """

    def __init__(self) -> None:
        """
        Initialize maintenance statistics.
        """

        self._maintenance_count = 0

    def requires_maintenance(
        self,
        state: EquipmentState,
    ) -> bool:
        """
        Determine whether maintenance should
        be scheduled for an asset.

        Parameters
        ----------
        state:
            Runtime equipment state.

        Returns
        -------
        bool
            True when maintenance criteria
            are met.
        """

        if (
            state.health
            <= MAINTENANCE_HEALTH_THRESHOLD
        ):
            return True

        if (
            state.runtime_hours
            >= MAINTENANCE_INTERVAL_HOURS
        ):
            return True

        return False

    def apply(
        self,
        state: EquipmentState,
    ) -> None:
        """
        Apply maintenance to an asset when
        maintenance criteria are satisfied.
        """

        if not self.requires_maintenance(
            state,
        ):
            return

        self._maintenance_count += 1

        state.health = (
            MAINTENANCE_RESTORE_HEALTH
        )

        state.failure_probability = (
            MAINTENANCE_RESET_FAILURE_PROBABILITY
        )

        state.last_maintenance_at = (
            datetime.utcnow()
        )

        state.runtime_hours = 0.0

    def maintenance_count(
        self,
    ) -> int:
        """
        Return the number of maintenance
        executions performed.

        Returns
        -------
        int
            Total maintenance executions.
        """

        return self._maintenance_count