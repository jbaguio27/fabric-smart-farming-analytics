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
from smart_farming.models import CropGrowthProfile

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

        Growth profiles are indexed by their human-readable crop type to
        provide consistent lookup throughout the simulator.
        """

        self._profiles: dict[str, CropGrowthProfile] = {
            profile.crop_type: profile
            for profile in CROP_GROWTH_PROFILES.values()
        }

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

    def get_all_profiles(self) -> list[CropGrowthProfile]:
        """
        Return every registered crop growth profile.

        Returns:
            List containing all immutable crop growth profiles.
        """

        return list(self._profiles.values())

    @property
    def profiles(self) -> dict[str, CropGrowthProfile]:
        """
        Return all registered crop profiles.

        Returns:
            Mapping of crop type names to immutable biological
            profiles.
        """

        return self._profiles