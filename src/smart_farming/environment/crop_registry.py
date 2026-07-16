"""
Crop registry for the HydroGrow Smart Farming Simulator.

Maintains the collection of simulated crop batches that participate in
the simulation. The registry owns immutable crop metadata while mutable
runtime state is managed separately by CropStateManager.
"""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CropDefinition:
    """
    Immutable definition of a simulated crop batch.

    This model represents static information describing a crop batch.
    Runtime attributes such as lifecycle progression and health are
    intentionally excluded and belong in CropState.
    """

    crop_batch_id: str
    field_id: str
    crop_type: str

class CropRegistry:
    """
    Registry containing all simulated crop batches.

    The registry serves as the authoritative source of immutable crop
    metadata. Runtime managers should reference this registry when
    creating or accessing CropState instances.
    """

    def __init__(self) -> None:
        """
        Initialize an empty crop registry.
        """

        self._crop_batches: dict[str, CropDefinition] = {}

    @property
    def _crop_batches(self) -> dict[str, CropDefinition]:
        """
        Return the registered crop batches.

        Returns:
            Dictionary keyed by crop batch identifier.
        """

        return self._crop_batches