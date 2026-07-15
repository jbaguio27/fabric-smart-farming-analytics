"""
Facility demand model.

This service provides facility-wide demand adjustments that influence
equipment utilization patterns across the simulator.

The initial implementation introduces a simple day/night operating
cycle that affects all facilities uniformly.

Future enhancements may introduce:

- Seasonal demand variation
- Harvest-period demand spikes
- Facility-specific operating schedules
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
    Simulates facility-wide demand conditions.
    """

    DAY_MULTIPLIER: Final[float] = DAYTIME_DEMAND_MULTIPLIER
    NIGHT_MULTIPLIER: Final[float] = NIGHTTIME_DEMAND_MULTIPLIER
    HOURS_PER_DAY: Final[float] = HOURS_PER_DAY

    def get_multiplier(
        self,
        runtime_hours: float,
    ) -> float:
        """
        Return the current facility demand multiplier.

        Runtime is mapped into a repeating 24-hour operating cycle.

        Hours 06:00-18:00 are considered daytime.

        Parameters
        ----------
        runtime_hours:
            Total elapsed simulation runtime.

        Returns
        -------
        float
            Current demand multiplier.
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