"""
Facility demand model.

This module provides the domain service responsible for estimating the
overall facility demand multiplier used during equipment load
simulation.

The FacilityDemandModel is intentionally stateless. It converts
simulation runtime into a demand multiplier that represents changing
facility utilization throughout a typical operating day.

Responsibilities
----------------
The FacilityDemandModel is responsible only for:

- Calculating facility demand multipliers
- Representing predictable utilization cycles

It intentionally does not perform:

- Equipment load simulation
- Equipment wear calculations
- Failure analysis
- Maintenance scheduling
- Telemetry generation

Those responsibilities belong to other simulator components.
"""

from typing import Final
from smart_farming.config import (
    DAYTIME_DEMAND_MULTIPLIER,
    NIGHTTIME_DEMAND_MULTIPLIER,
    DAY_START_HOUR,
    NIGHT_START_HOUR,
    HOURS_PER_DAY,
)

class FacilityDemandModel:
    """
    Stateless domain service for facility utilization.

    The FacilityDemandModel converts simulator runtime into a facility
    demand multiplier used by EquipmentStateManager when calculating
    equipment operating load.

    The service contains no mutable state and performs no modification
    of simulator objects.
    """

    DAY_MULTIPLIER: Final[float] = DAYTIME_DEMAND_MULTIPLIER
    NIGHT_MULTIPLIER: Final[float] = NIGHTTIME_DEMAND_MULTIPLIER
    HOURS_PER_DAY: Final[float] = HOURS_PER_DAY

    def get_multiplier(
        self,
        runtime_hours: float,
    ) -> float:
        """
        Calculate the facility demand multiplier.

        The multiplier represents predictable changes in overall
        facility utilization throughout the simulated operating day.

        Parameters
        ----------
        runtime_hours:
            Total accumulated simulator runtime.

        Returns
        -------
        float
            Facility demand multiplier applied during equipment load
            simulation.
        """

        hour_of_day = int(
            runtime_hours
        ) % self.HOURS_PER_DAY

        if(
            DAY_START_HOUR
            <= hour_of_day
            < NIGHT_START_HOUR
        ):
            return self.DAY_MULTIPLIER

        return self.NIGHT_MULTIPLIER