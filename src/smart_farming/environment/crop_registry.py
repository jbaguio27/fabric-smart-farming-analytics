"""
Crop registry for the HydroGrow Smart Farming Simulator.

This module defines the immutable crop batch registry used throughout the
simulation.

The registry owns CropDefinition objects describing each simulated crop
batch. These definitions remain constant during the simulation while
mutable runtime state is maintained separately by CropStateManager.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CropDefinition:
    """
    Immutable definition of a simulated crop batch.

    Attributes:
        crop_batch_id:
            Unique identifier assigned to the crop batch.

        zone_id:
            Identifier of the growing zone containing the crop.

        crop_type:
            Human-readable crop variety.
    """

    crop_batch_id: str
    zone_id: str
    crop_type: str


class CropRegistry:
    """
    Registry containing immutable crop batch definitions.

    Runtime managers reference this registry whenever immutable crop
    metadata is required. Biological state such as age, health, and
    lifecycle progression is intentionally excluded.
    """

    def __init__(self) -> None:
        """
        Initialize an empty crop registry.
        """

        self._crop_batches: dict[str, CropDefinition] = {}

    def register(
        self,
        definition: CropDefinition,
    ) -> None:
        """
        Register a crop batch.

        Args:
            definition:
                Immutable crop batch definition.
        """

        self._crop_batches[definition.crop_batch_id] = definition

    def get(
        self,
        crop_batch_id: str,
    ) -> CropDefinition:
        """
        Retrieve a crop batch definition.

        Args:
            crop_batch_id:
                Crop batch identifier.

        Returns:
            The corresponding CropDefinition.
        """

        return self._crop_batches[crop_batch_id]

    def get_all(self) -> list[CropDefinition]:
        """
        Return every registered crop batch.

        Returns:
            List of immutable crop batch definitions.
        """

        return list(self._crop_batches.values())

    def get_all_batches(self) -> list[CropDefinition]:
        """
        Return every registered crop batch.

        Returns:
            List of immutable crop batch definitions.
        """

        return list(self._crop_batches.values())

    @property
    def crop_batches(self) -> dict[str, CropDefinition]:
        """
        Return all registered crop batches.

        Returns:
            Dictionary mapping crop batch identifiers to immutable crop
            definitions.
        """

        return self._crop_batches