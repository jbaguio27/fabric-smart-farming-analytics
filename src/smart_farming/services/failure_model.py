"""
Equipment failure model.

This module implements the domain service responsible for evaluating
equipment reliability during simulation.

The FailureModel is intentionally stateless. It receives immutable input
values or runtime state and returns derived results without mutating the
simulation.

Responsibilities
----------------
The FailureModel is responsible for:

- Normalizing failure probability values
- Determining operating status from runtime condition

It intentionally does not perform:

- Health degradation
- Load simulation
- Maintenance scheduling
- Telemetry generation

Those concerns belong to other domain services.
"""
from smart_farming.models import (
    EquipmentState,
    EquipmentOperatingStatus
)
from smart_farming.config import (
    MIN_FAILURE_PROBABILITY,
    MAX_FAILURE_PROBABILITY,
    ONLINE_FAILURE_THRESHOLD,
    WARNING_FAILURE_THRESHOLD,
    ERROR_FAILURE_THRESHOLD,
)


class FailureModel:
    """
    Stateless domain service responsible for equipment reliability.

    The FailureModel evaluates runtime equipment condition and produces
    normalized reliability metrics used throughout the simulator.

    The service contains no persistent state and performs no mutation of
    simulator objects.
    """

    def normalize_probability(
        self,
        probability: float,
    ) -> float:
        """
        Normalize a calculated failure probability.

        Failure probability is constrained to the simulator's configured
        minimum and maximum limits.

        Parameters
        ----------
        probability:
            Raw probability calculated by the simulation.

        Returns
        -------
        float
            Probability constrained to the configured limits.
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

    def determine_operating_status(
        self,
        state: EquipmentState,
    ) -> EquipmentOperatingStatus:
        """
        Determine the equipment operating status.

        Operating status is derived from the current runtime condition
        using configured warning and error thresholds.

        Parameters
        ----------
        state:
            Runtime equipment state.

        Returns
        -------
        EquipmentOperatingStatus
            Operating status representing the current equipment
            condition.
        """

        if (
            state.operating_status
            == EquipmentOperatingStatus.ERROR
        ):
            return EquipmentOperatingStatus.ERROR

        if (
            state.failure_probability
            >= ERROR_FAILURE_THRESHOLD
        ):
            return EquipmentOperatingStatus.ERROR

        if (
            state.failure_probability
            >= WARNING_FAILURE_THRESHOLD
        ):
            return EquipmentOperatingStatus.WARNING

        return EquipmentOperatingStatus.ONLINE

    def is_terminal_failure(
        self,
        state: EquipmentState,
    ) -> bool:
        """
        Determine whether the equipment has entered a
        non-recoverable runtime failure condition.

        Parameters
        ----------
        state:
            Runtime equipment state.

        Returns
        -------
        bool
            True if the equipment is in terminal failure.
        """

        return (
            state.failure_probability
            >= ERROR_FAILURE_THRESHOLD
        )