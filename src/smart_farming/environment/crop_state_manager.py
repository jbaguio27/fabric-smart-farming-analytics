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
from smart_farming.config import Settings

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
        settings: Settings,
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

        self._settings = settings
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
    
    def get_state(
        self,
        crop_batch_id: str,
    ) -> CropState:
        """
        Return the runtime state for a registered crop batch.

        Args:
            crop_batch_id:
                Unique identifier of the crop batch.

        Returns:
            The mutable runtime state associated with the crop batch.

        Raises:
            KeyError:
                If the crop batch is not managed by this state manager.
        """

        return self._states[crop_batch_id]

    @property
    def states(self) -> dict[str, CropState]:
        """
        Return all runtime crop states.

        Returns:
            Dictionary mapping crop batch identifiers to runtime state
            objects.

        Notes:
            The returned mapping is intended for iteration and reporting.
            Individual runtime state updates should continue to occur
            through the manager.
        """

        return self._states

    @property
    def crop_registry(self) -> CropRegistry:
        """
        Return the crop registry managed by this state manager.

        Returns:
            Registry containing all configured crop batches.
        """

        return self._crop_registry

    def evaluate_lifecycle_transition(
        self,
        state: CropState,
    ) -> None:
        """
        Evaluate whether a crop batch should transition to a new
        lifecycle stage.

        This method acts as the single orchestration point for all future
        lifecycle transition logic. During this implementation phase, no
        biological transitions are performed in order to preserve existing
        simulator behavior.

        Future phases will extend this method to evaluate:

        - crop age
        - environmental suitability
        - equipment availability
        - harvest readiness
        - biological progression

        Args:
            state:
                Runtime state of the crop batch to evaluate.
        """

        next_stage = self._determine_next_stage(state)

        if next_stage is None:
            return

        state.lifecycle_stage = next_stage

    def advance_cycle(self) -> None:
        """
        Advance the runtime state of every managed crop batch by one
        simulation cycle.

        This phase of the Crop Lifecycle Generator is intentionally limited
        to deterministic time progression. Biological lifecycle transitions,
        environmental effects, equipment effects, and health calculations
        are introduced in subsequent implementation phases.

        Each simulation cycle increases the accumulated crop age based on
        the configured simulation time step.
        """

        for state in self._states.values():
            self._advance_crop_age(state)

    def _advance_crop_age(
        self,
        state: CropState,
    ) -> None:
        """
        Advance the age of a crop batch by one simulation cycle.

        Args:
            state:
                Runtime crop state to update.

        Notes:
            Crop age is stored in days. The configured simulation time step
            is converted into a fractional day to support deterministic
            progression regardless of simulator cadence.
        """

        minutes_per_day = 24 * 60

        stage.age_days += (
            self._settings.simulation_time_step_minutes
            / minutes_per_day
        )

    def _determine_next_stage(
        self,
        state: CropState,
    ) -> str | None:
        """
        Determine the next lifecycle stage for a crop batch.

        During the current implementation phase, lifecycle transitions are
        intentionally disabled. The method exists to establish the future
        extension point for biological progression.

        Args:
            state:
                Runtime crop state.

        Returns:
            None, indicating that no lifecycle transition should occur.
        """

        return None
# ------------------------------------------------------------------
# Lifecycle simulation methods will be introduced in the next phase.
#
# Upcoming responsibilities include:
#
#   • Lifecycle stage transitions
#   • Crop aging
#   • Environmental influence
#   • Equipment influence
#   • Harvest readiness evaluation
#
# This phase intentionally introduces no simulation behavior to
# minimize regression risk.
# ------------------------------------------------------------------