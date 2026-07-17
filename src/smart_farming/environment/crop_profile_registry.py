"""
Registry of biological growth profiles for supported indoor crops.

This module centralizes immutable biological characteristics used by the
Crop Lifecycle Generator. Keeping growth profiles separate from runtime
state allows lifecycle simulation to remain deterministic, extensible,
and aligned with the project's single-responsibility architecture.

The registry owns profile storage and retrieval only. Biological
simulation remains the responsibility of CropStateManager.
"""

from smart_farming.config import (
    CROP_GROWTH_PROFILES
)

class CropProfileRegistry:
    """
    Registry containing supported crop growth profiles.

    Each profile describes the expected biological lifecycle of a crop
    variety grown within the HydroGrow indoor vertical farming
    simulator.

    The registry exposes immutable profile definitions while remaining
    independent of runtime crop state.
    """

    def __init__(self) -> None:
        """
        Initialize the registry.

        A single immutable profile is registered initially. Additional
        crop varieties can be introduced in future iterations without
        modifying lifecycle simulation code.
        """

        self._profiles = CROP_GROWTH_PROFILES

    def get_profile(
        self,
        crop_type: str,
    ) -> CropGrowthProfile:
        """
        Retrieve the growth profile for a crop type.

        Args:
            crop_type:
                Crop variety name.

        Returns:
            Immutable biological profile.

        Raises:
            KeyError:
                Raised if the requested crop type has not been
                registered.
        """

        return self._profiles[crop_type]

    @property
    def profiles(self) -> dict[str, CropGrowthProfile]:
        """
        Return all registered crop profiles.

        Returns:
            Mapping of crop type names to immutable biological
            profiles.
        """

        return self._profiles