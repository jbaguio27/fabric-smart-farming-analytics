"""
Maintenance service.

This service manages maintenance eligibility
and maintenance execution for equipment assets.
"""
from datetime import (
    datetime,
    UTC,
)
from smart_farming.environment.equipment_state import EquipmentState
from smart_farming.config import (
    MAINTENANCE_INTERVAL_HOURS,
    MAINTENANCE_HEALTH_THRESHOLD,
    MAINTENANCE_RESTORE_HEALTH,
    MAINTENANCE_RESET_FAILURE_PROBABILITY,
    MAX_EQUIPMENT_HEALTH,
    MIN_EQUIPMENT_HEALTH,
)
from smart_farming.models import (
    EquipmentOperatingStatus,
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
        Execute maintenance when equipment health falls below
        the maintenance threshold.

        Maintenance restores equipment condition and clears
        persistent failure states.
        """

        if (
            state.health
            > MAINTENANCE_HEALTH_THRESHOLD
        ):
            return

        state.health = MAX_EQUIPMENT_HEALTH

        state.failure_probability = MIN_EQUIPMENT_HEALTH

        state.operating_status = (
            EquipmentOperatingStatus.ONLINE
        )

        state.last_maintenance_at = (
            datetime.now(UTC)
        )

        self._maintenance_count += 1

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