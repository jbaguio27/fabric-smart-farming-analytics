"""
Failure model for equipment simulation.

This service centralizes operating-status decisions and future
failure-state behavior.

The initial implementation reproduces the existing simulator
behavior without changing thresholds or probabilities.
"""

from smart_farming.environment.equipment_state import (
    EquipmentState,
)

from smart_farming.models.equipment import (
    EquipmentOperatingStatus,
)

from smart_farming.config.constants import (
    ONLINE_FAILURE_THRESHOLD,
    WARNING_FAILURE_THRESHOLD,
    MAX_FAILURE_PROBABILITY,
    MIN_FAILURE_PROBABILITY,
)


class FailureModel:
    """
    Determines equipment operating status.
    """

    def determine_operating_status(
        self,
        state: EquipmentState,
    ) -> EquipmentOperatingStatus:
        """
        Determine operating status from failure probability.

        Parameters
        ----------
        state:
            Runtime equipment state.

        Returns
        -------
        EquipmentOperatingStatus
            Calculated operating condition.
        """

        if (
            state.failure_probability
            < ONLINE_FAILURE_THRESHOLD
        ):
            return (
                EquipmentOperatingStatus.ONLINE
            )

        if (
            state.failure_probability
            < WARNING_FAILURE_THRESHOLD
        ):
            return (
                EquipmentOperatingStatus.WARNING
            )

        if (
            state.failure_probability
            < ERROR_FAILURE_THRESHOLD
        ):
            return (
                EquipmentOperatingStatus.ERROR
            )
    
    def calculate_probability(
    self,
    probability: float,
    ) -> float:
        """
        Normalize and constrain failure probability.
        """

        return round(
            max(
                MIN_FAILURE_PROBABILITY,
                min(
                    MAX_FAILURE_PROBABILITY,
                    probability,
                ),
            ),
            4,
        )

    def is_terminal_failure(
    self,
    state: EquipmentState,
    ) -> bool:
        """
        Determine whether equipment has entered a terminal
        failure condition.

        A terminal failure occurs when failure probability
        exceeds the ERROR threshold.

        Once an asset reaches ERROR state it remains in that
        state until a maintenance event restores operation.

        Parameters
        ----------
        state:
            Runtime equipment state.

        Returns
        -------
        bool
            True if terminal failure occurred.
        """

        return (
            state.failure_probability
            >= WARNING_FAILURE_THRESHOLD
        )