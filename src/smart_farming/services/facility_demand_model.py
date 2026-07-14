"""
Facility demand model.

This service centralizes facility-wide utilization behavior.

The initial implementation intentionally introduces no behavioral
changes. Every simulation cycle returns a neutral demand multiplier
of 1.0.

Future enhancements will introduce:

- Day and night operating cycles
- Seasonal demand shifts
- Harvest-period utilization spikes
- Facility-specific operating patterns
"""

from typing import Final


class FacilityDemandModel:
    """
    Provides facility-wide demand adjustments.
    """

    DEFAULT_DEMAND_MULTIPLIER: Final[float] = 1.0

    def get_multiplier(self) -> float:
        """
        Return the current facility demand multiplier.

        Returns
        -------
        float
            Facility-wide utilization multiplier.
        """

        return self.DEFAULT_DEMAND_MULTIPLIER