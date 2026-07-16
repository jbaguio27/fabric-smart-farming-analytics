"""
Runtime state manager for simulated crop batches.

This module owns the mutable runtime state for all simulated crop
batches. It is responsible for creating, storing, and evolving
CropState instances throughout the simulation lifecycle.

This initial implementation intentionally focuses only on state
ownership. Lifecycle progression, growth simulation, and event
generation will be introduced in subsequent roadmap steps.
"""

from smart_farming.models import CropState
from smart_farming.utils import RandomManager
from smart_farming.environment import CropRegistry

class CropStateManager:
    """
    Manages runtime state for simulated crop batches.

    The manager acts as the authoritative owner of CropState instances.
    Higher-level components interact with crop runtime data exclusively
    through this manager to ensure a single source of truth.

    No lifecycle progression logic is implemented during this step.
    """

    def __init__(
        self,
        crop_registry: CropRegistry,
        random_manager: RandomManager,
    ) -> None:
        """
        Initialize the crop runtime state manager.

        Args:
            random_manager:
                Shared random number provider used throughout the
                simulator.
        """

        self._crop_registry = crop_registry
        self._random_manager = random_manager

        self._states: dict[str, CropState] = {}

        self.initialize()

    def initialize(self) -> None:
        """
        Initialize runtime crop state.

        A runtime CropState is created for every crop batch registered
        in the CropRegistry. This establishes the mutable simulation
        state without introducing lifecycle progression.

        Runtime values are initialized directly from the immutable crop
        definitions. Future roadmap steps will evolve these values as
        the simulation advances.
        """

        self._states.clear()

        for crop in self._crop_registry._crop_batches.values():
            self._states[crop.crop_batch_id] = CropState(
                crop_batch_id=crop.crop_batch_id,
                field_id=crop.field_id,
                crop_type=crop.crop_type,
                lifecycle_stage="PLANTED",
                planting_timestamp=None,
                expected_harvest_timestamp=None,
                age_days=0,
                healt_score=100.0,
                is_active=True,
            )