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
        random_manager: RandomManager,
    ) -> None:
        """
        Initialize the crop runtime state manager.

        Args:
            random_manager:
                Shared random number provider used throughout the
                simulator.
        """

        self._random_manager = random_manager

        self._states: dict[str, CropState] = {}

        self.initialize()

    def initialize(self) -> None:
        """
        Initialize runtime crop state.

        This method currently prepares the manager for future crop
        registration. Runtime crop batches will be created during a
        subsequent implementation step.

        The method exists to establish a consistent lifecycle pattern
        with the other simulator state managers.
        """

        self._states.clear()