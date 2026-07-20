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

    def requires_maintenance(
        self,
        state: EquipmentState,
    ) -> bool:
        """
        Determine whether equipment requires maintenance.

        Maintenance is required when either:

        - Equipment health drops below the configured threshold.
        - Runtime exceeds the configured preventive interval.

        Args:
            state:
                Runtime equipment state.

        Returns:
            True if maintenance should be performed.
        """

        return (
            state.health <= MAINTENANCE_HEALTH_THRESHOLD
            or state.runtime_hours >= MAINTENANCE_INTERVAL_HOURS
        )

    def apply(
        self,
        state: EquipmentState,
    ) -> None:
        """
        Apply maintenance to an equipment runtime state.

        Maintenance restores equipment condition when simulator-defined
        maintenance thresholds have been exceeded.

        Parameters
        ----------
        state:
            Runtime state that may receive maintenance.

        Notes
        -----
        The maintenance policy itself is intentionally implemented within
        this service so that EquipmentStateManager remains responsible
        only for orchestration.
        """

        if not self.requires_maintenance(state):
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