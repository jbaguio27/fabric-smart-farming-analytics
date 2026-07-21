"""
Equipment maintenance manager.

This module implements the domain service responsible for applying
maintenance operations to equipment runtime state.

The MaintenanceManager encapsulates all simulator maintenance policies
and keeps maintenance behavior separate from runtime orchestration.

Responsibilities
----------------
The MaintenanceManager is responsible only for:

- Evaluating whether maintenance is required
- Restoring equipment condition
- Recording maintenance execution

It intentionally does not perform:

- Equipment wear calculations
- Failure probability calculations
- Load simulation
- Telemetry generation

Those responsibilities belong to their respective domain services.
"""

from datetime import UTC, datetime

from smart_farming.config import (
    MAINTENANCE_HEALTH_THRESHOLD,
    MAINTENANCE_INTERVAL_HOURS,
    MAINTENANCE_RESTORE_HEALTH,
    MAINTENANCE_RESET_FAILURE_PROBABILITY,
)
from smart_farming.models import (
    EquipmentState,
    EquipmentOperatingStatus,
)


class MaintenanceManager:
    """
    Stateless domain service responsible for maintenance operations.

    The MaintenanceManager evaluates runtime equipment condition and
    applies maintenance whenever simulator policy requires it.

    Aside from its internal maintenance counter used for reporting, the
    service owns no persistent simulator state.
    """

    def __init__(self) -> None:
        """
        Initialize maintenance statistics.
        """

        self._maintenance_count = 0
        self._last_pm_runtime: dict[str, float] = {}

    def requires_maintenance(
        self,
        equipment_id: str,
        state: EquipmentState,
    ) -> bool:
        """
        Determine whether equipment requires maintenance.

        Maintenance is required when either:

            - Equipment health drops below the configured threshold.
            - Runtime hours accumulated since the last PM exceeds the preventive interval.

        Args:
            equipment_id: Injected identifier of the target equipment.
            state: Runtime equipment state.
        Returns:
            True if maintenance should be performed.
        """
        runtime_since_pm = state.runtime_hours - self._last_pm_runtime.get(equipment_id, 0.0)

        return (
            state.health <= MAINTENANCE_HEALTH_THRESHOLD
            or state.runtime_hours >= MAINTENANCE_INTERVAL_HOURS
        )

    def apply(
        self,
        equipment_id: str,
        state: EquipmentState,
    ) -> None:
        """
        Apply maintenance to an equipment runtime state.

        Maintenance restores equipment condition when simulator-defined
        maintenance thresholds have been exceeded.

        Parameters
        ----------
        equipment_id:
            Identifier of the equipment asset.
        state:
            Runtime state that may receive maintenance.
        """

        if not self.requires_maintenance(equipment_id, state):
            return

        state.health = MAINTENANCE_RESTORE_HEALTH

        state.failure_probability = (
            MAINTENANCE_RESET_FAILURE_PROBABILITY
        )

        state.operating_status = (
            EquipmentOperatingStatus.ONLINE
        )

        state.last_maintenance_at = datetime.now(UTC)
        self._maintenance_count += 1

    @property
    def maintenance_count(self) -> int:
        """
        Return the total number of maintenance operations performed.

        Returns
        -------
        int
            Cumulative maintenance operations executed during the current
            simulator lifetime.
        """

        return self._maintenance_count