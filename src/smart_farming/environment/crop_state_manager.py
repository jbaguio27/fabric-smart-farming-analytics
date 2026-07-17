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
from smart_farming.environment import (
    CropRegistry,
    CropProfileRegistry,
    EnvironmentStateManager,
)
from smart_farming.config import (
    Settings,
    CROP_STAGE_GERMINATION,
    CROP_STAGE_SEEDLING,
    CROP_STAGE_VEGETATIVE,
    CROP_STAGE_MATURE,
    CROP_STAGE_HARVESTED
)

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
        crop_profile_registry: CropProfileRegistry,
        environment_manager: EnvironmentStateManager,
        random_manager: RandomManager,
    ) -> None:
        """
        Initialize the crop runtime state manager.

        Args:
            settings:
                Runtime simulator configuration.

            crop_registry:
                Registry containing all simulated crop batches.

            crop_profile_registry:
                Registry providing immutable biological growth profiles.

            environment_manager:
                Manager supplying the current environmental conditions for each
                growing zone.

            random_manager:
                Shared random number provider used throughout the simulator.
        """

        self._settings = settings
        self._crop_registry = crop_registry
        self._crop_profile_registry = crop_profile_registry
        self._environment_manager = environment_manager
        self._random_manager = random_manager

        self._states: dict[str, CropState] = {}

        self.initialize()

    def initialize(self) -> None:
        """
        Create runtime state for every registered crop batch.

        This method is executed once during simulator startup. It 
        creates one runtime CropState instance for each
        registered crop batch.

        The initialized runtime state represents newly planted crop batches.
        Lifecycle progression is intentionally not performed here and will be
        implemented in a later roadmap step.

        Repeated calls reset the internal runtime state.
        """

        self._states.clear()

        for index, profile in enumerate(
            self._crop_registry.get_all_profiles(),
            start=1,
        ):
            crop_batch_id = f"BATCH-{index:05d}"

            self._states[crop_batch_id] = CropState(
                crop_batch_id=crop_batch_id,
                zone_id=f"ZONE-{index}",
                crop_type=profile.crop_type,
                lifecycle_stage=CROP_STAGE_GERMINATION,
                planting_timestamp=None,
                expected_harvest_timestamp=None,
                age_days=0,
                health_score=100.0,
                is_active=True,
            )
    
    def get_all_states(self) -> list[CropState]:
        """
        Return every managed crop runtime state.

        Returns:
            A list containing the mutable runtime state for every active
            crop batch.
        """

        return list(self._states.values())

    def get_state(
        self,
        crop_batch_id: str,
    ) -> CropState:
        """
        Retrieve the runtime state for a crop batch.

        Args:
            crop_batch_id:
                Unique crop batch identifier.

        Returns:
            The mutable CropState associated with the supplied batch.
        """

        return self._states[crop_batch_id]

    @property
    def crop_profile_registry(self) -> CropProfileRegistry:
        """
        Return the registry supplying immutable crop definitions.

        Returns:
            The injected CropProfileRegistry instance.
        """

        return self._crop_profile_registry

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

            if not state.is_active:
                continue

            self._update_health(state)

            self._advance_crop_age(state)

            self.evaluate_lifecycle_transition(state)

            if state.lifecycle_stage == CROP_STAGE_HARVESTED:
                state.is_active = False

    def _advance_crop_age(
        self,
        state: CropState,
    ) -> None:
        """
        Advance the biological age of a crop batch.

        Crop development is influenced by its current biological health.
        Healthy crops progress at the normal simulation rate, while crops
        experiencing environmental stress develop more slowly. Extremely
        unhealthy crops cease development entirely.

        This implementation introduces biological realism without altering
        lifecycle transition rules. Stage progression continues to be
        determined solely by accumulated biological age.

        Args:
            state:
                Runtime crop state to update.

        Notes:
        Biological age is expressed in days. The configured simulation
        time step is converted into fractional days and then scaled by
        the crop's current health. This allows environmental stress to
        naturally delay development without changing lifecycle
        thresholds.
        """

        minutes_per_day = 24 * 60

        age_increment = (
            self._settings.simulation_time_step_minutes
            / minutes_per_day
        )

        health = state.health_score

        if health >= 90.0:
            growth_factor = 1.0

        elif health >= 75.0:
            growth_factor = 0.90
        
        elif health >= 60.0:
            growth_factor = 0.75
        
        elif health >= 40.0:
            growth_factor = 0.50

        elif health >= 20.0:
            growth_factor = 0.25

        else:
            growth_factor = 0.00
        
        state.age_days += age_increment * growth_factor

    def _update_health(
        self,
        state: CropState
    ) -> None:
        """
        Update the biological health of a crop batch.

        Health is evaluated by comparing the current environmental
        conditions with the optimal growing conditions defined by the crop's
        immutable growth profile.

        During this implementation phase, the health model is intentionally
        deterministic and applies only small adjustments each simulation
        cycle. Equipment influence, disease simulation, and nutrient
        depletion will be introduced in later roadmap phases.

        Args:
            state:
                Runtime crop state to evaluate.
        """

        profile = self._crop_profile_registry.get_profile(
            state.crop_type
        )

        environment = self._environment_manager.get_zone_state(
            state.zone_id,
        )

        health_delta = 0.0

        health_delta -= (
            abs(
                environment.air_temperature_celcius
                - profile.optimal_temperature_celsius
            )
            * 0.15
        )

        health_delta -= (
            abs(
                environment.humidity_percent
                - profile.optimal_humidity_percent
            )
            * 0.05
        )

        health_delta -= (
            abs(
                environment.water_ph
                - profile.optimal_ph
            )
            * 8.0
        )

        health_delta -= (
            abs(
                environment.electrical_conductivity
                - profile.optimal_ec
            )
            * 3.0
        )

        state.health_score = max(
            0.0,
            min(
                100.0,
                state.health_score + health_delta,
            ),
        )

    def _determine_next_stage(
        self,
        state: CropState,
    ) -> str | None:
        """
        Determine the next biological lifecycle stage for a crop batch.

        Stage progression is based entirely on the elapsed biological age
        defined by the crop's immutable growth profile. No environmental
        influence, equipment influence, or health adjustments are considered
        during this implementation phase.

        Args:
            state:
                Runtime crop state.

        Returns:
            The next lifecycle stage if a transition should occur;
            otherwise None.
        """

        profile = self._crop_profile_registry.get_profile(
            state.crop_type
        )

        age = state.age_days

        if (
            state.lifecycle_stage == CROP_STAGE_GERMINATION
            and age >= profile.germination_days
        ):
            return CROP_STAGE_SEEDLING

        if (
            state.lifecycle_stage == CROP_STAGE_SEEDLING
            and age >= (
                profile.germination_days
                + profile.seedling_days
            )
        ):
            return CROP_STAGE_VEGETATIVE

        if (
            state.lifecycle_stage == CROP_STAGE_VEGETATIVE
            and age >= (
                profile.germination_days
                + profile.seedling_days
                + profile.vegetative_days
            )
        ):
            return CROP_STAGE_MATURE
        
        if (
            state.lifecycle_stage == CROP_STAGE_MATURE
            and age >= profile.maturity_days
        ):
            return CROP_STAGE_HARVESTED

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