"""
Maintenance manager.

This class intentionally performs no work yet.

It exists as the extension point for scheduled maintenance,
repair events, and failure recovery.
"""

from smart_farming.environment.equipment_state import EquipmentState


class MaintenanceManager:
    """
    Handles maintenance operations.
    """

    def apply(
        self,
        state: EquipmentState,
    ) -> None:
        """
        Apply maintenance.

        During the structural refactor this method is
        intentionally a no-op.
        """

        return