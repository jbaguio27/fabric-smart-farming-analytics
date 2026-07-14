"""
Maintenance service.

This service centralizes maintenance-related
decision logic for equipment assets.

The initial implementation introduces only
maintenance eligibility evaluation.

No simulator behavior changes occur during
this phase.
"""

from smart_farming.environment.equipment_state import EquipmentState
from smart_farming.config import (
    MAINTENANCE_INTERVAL_HOURS,
    MAINTENANCE_HEALTH_THRESHOLD,
)


class MaintenanceManager:
    """
    Evaluates maintenance requirements.
    """

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
        Placeholder maintenance hook.

        Future maintenance behavior will be
        implemented here.

        Current implementation intentionally
        performs no state changes.
        """

        _ = state