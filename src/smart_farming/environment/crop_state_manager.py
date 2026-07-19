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
from .crop_registry import CropRegistry
from .crop_profile_registry import (
    CropProfileRegistry,
)
from .growing_environment_state_manager import (
    GrowingEnvironmentStateManager,
)
from smart_farming.config import (
    Settings,
    CROP_STAGE_GERMINATION,
    CROP_STAGE_SEEDLING,
    CROP_STAGE_VEGETATIVE,
    CROP_STAGE_MATURE,
    CROP_STAGE_HARVESTED,
    MAX_HEALTH_SCORE,
    IDEAL_GROWTH_TEMPERATURE_C,
    IDEAL_GROWTH_HUMIDITY_PERCENT,
    TEMPERATURE_GROWTH_TOLERANCE_C,
    HUMIDITY_GROWTH_TOLERANCE_PERCENT,
    BIOMASS_GROWTH_MULTIPLIER,
    WATER_UPTAKE_PER_GRAM_BIOMASS,
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
        growing_environment_manager: GrowingEnvironmentStateManager,
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

            growing_environment_manager:
                Manager supplying the current environmental conditions for each
                growing zone.

            random_manager:
                Shared random number provider used throughout the simulator.
        """

        self._settings = settings
        self._crop_registry = crop_registry
        self._crop_profile_registry = crop_profile_registry
        self._growing_environment_manager = growing_environment_manager
        self._random_manager = random_manager

        self._states: dict[str, CropState] = {}

        self._simulation_cycle = 0

        self.initialize()

    @property
    def simulation_cycle(self) -> int:
        """
        Current biological simulation cycle.

        Returns:
            int:
                Number of completed lifecycle updates.
        """

        return self._simulation_cycle

    def initialize(self) -> None:
        """
        Create runtime state for every registered crop batch.

        This method is executed once during simulator startup. One mutable
        CropState instance is created for every immutable CropDefinition
        stored in the CropRegistry.

        Runtime state is initialized to represent newly planted crops.
        Lifecycle progression is intentionally not performed during
        initialization.

        Repeated calls completely rebuild the runtime state from the
        registered crop definitions.
        """

        self._states.clear()

        for definition in self._crop_registry.get_all():

            profile = self._crop_profile_registry.get_profile(
                definition.crop_type,
            )

            self._states[definition.crop_batch_id] = CropState(
                crop_batch_id=definition.crop_batch_id,
                zone_id=definition.zone_id,
                crop_type=definition.crop_type,
                lifecycle_stage=CROP_STAGE_GERMINATION,
                planting_timestamp=None,
                expected_harvest_timestamp=None,
                age_days=0.0,
                health_score=profile.optimal_health,
                growth_rate=0.0,
                biomass_grams=0.0,
                water_uptake_liters=0.0,
                nutrient_uptake_grams=0.0,
                stress_index=0.0,
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

            self._update_growth_rate(state)

            self._advance_crop_age(state)

            self._update_biomass(state)

            self._update_water_uptake(state)

            self._update_nutrient_uptake(state)

            self._update_stress_index(state)

            self.evaluate_lifecycle_transition(state)
            
            if state.lifecycle_stage == CROP_STAGE_HARVESTED:
                state.is_active = False
        
        self._simulation_cycle += 1


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
        Update the runtime crop health score.

        Crop health represents the overall biological condition of the crop
        on a normalized scale from zero to one hundred.

        During this implementation phase health degradation is influenced by
        the current stress index, creating a deterministic relationship
        between crop stress and biological performance.

        Future milestones will incorporate environmental conditions,
        irrigation performance, nutrient availability, equipment failures,
        and crop-specific physiological responses.

        Args:
            state:
                Mutable runtime crop state.
        """

        profile = self._crop_profile_registry.get_profile(
            state.crop_type
        )

        environment = (
            self._growing_environment_manager
            .get_zone_state(
                state.zone_id,
            )
        )

        # Individual Environmental deviations

        temperature_error = abs(
            environment.air_temperature_celsius
            - profile.optimal_temperature_celsius
        )

        humidity_error = abs(
            environment.humidity_percent
            - profile.optimal_humidity_percent
        )

        ph_error = abs(
            environment.water_ph
            - profile.optimal_ph
        )

        ec_error = abs(
            environment.electrical_conductivity
            - profile.optimal_ec
        )

        # Convert deviations into a normalized environmental stress score. 
        # Smaller values indicate healthier growing conditions.

        stress = (
            temperature_error * 0.20
            + humidity_error * 0.05
            + ph_error * 4.00
            + ec_error * 1.50
        )

        # Gradual health adjustment.

        if stress <= 1.0:
            health_delta = +0.05

        elif stress <= 3.0:
            health_delta = -0.01
        
        elif stress <= 6.0:
            health_delta = -0.05

        else:
            health_delta = -0.10

        state.health_score = max(
            0.0,
            min(
                MAX_HEALTH_SCORE,
                state.health_score + health_delta,
            )
        )

    def _update_growth_rate(
        self,
        state: CropState,
    ) -> None:
        """
        Update the simulated crop growth rate.

        Growth rate represents the relative biological growth achieved during
        the current simulation cycle.

        During this implementation phase the estimate combines crop health
        with the current growing environment. The calculation remains fully
        deterministic while establishing the foundation for richer
        physiological models.

        Future milestones may incorporate crop-specific coefficients,
        lighting intensity, carbon dioxide concentration, irrigation,
        nutrient availability, and equipment performance.

        Args:
            state:
                Mutable runtime crop state.
        """

        environment = self._growing_environment_manager.get_zone_state(
            state.zone_id,
        )

        temperature_factor = max(
            0.0,
            1.0 - (
                abs(
                    environment.air_temperature_celsius - IDEAL_GROWTH_TEMPERATURE_C
                )
                / TEMPERATURE_GROWTH_TOLERANCE_C
            ),
        )

        humidity_factor = max(
            0.0,
            1.0 - (
                abs(
                    environment.humidity_percent - IDEAL_GROWTH_HUMIDITY_PERCENT
                )
                / HUMIDITY_GROWTH_TOLERANCE_PERCENT
            ),
        )

        health_factor = max(
            0.0,
            min(
                state.health_score / MAX_HEALTH_SCORE,
                1.0,
            ),
        )

        state.growth_rate = (
            health_factor
            * temperature_factor
            * humidity_factor
        )

    def _update_biomass(
        self,
        state: CropState,
    ) -> None:
        """
        Update the estimated crop biomass.

        Biomass represents the cumulative above-ground plant mass
        produced by the simulated crop.

        During this implementation phase biomass is intentionally
        estimated using accumulated crop age and current growth
        rate only.

        Future milestones will incorporate environmental conditions,
        lighting, irrigation, nutrient availability, and crop-specific
        physiological models.

        Args
        ----
        state:
            Mutable runtime crop state.
        """

        state.biomass_grams = (
            state.age_days
            * state.growth_rate
            * BIOMASS_GROWTH_MULTIPLIER
        )

    def _update_water_uptake(
        self,
        state: CropState,
    ) -> None:
        """
        Update the estimated crop water uptake.

        Water uptake represents the cumulative volume of irrigation
        solution absorbed by the crop.

        During this implementation phase the value is estimated from
        accumulated biomass.

        Future milestones will incorporate environmental conditions,
        vapor pressure deficit, lighting intensity, irrigation
        scheduling, and crop-specific physiology.

        Args
        ----
        state:
            Mutable runtime crop state.
        """

        state.water_uptake_liters = (
            state.biomass_grams
            * WATER_UPTAKE_PER_GRAM_BIOMASS
        )

    def _update_nutrient_uptake(
        self,
        state: CropState,
    ) -> None:
        """
        Update the estimated nutrient uptake.

        Nutrient uptake represents the cumulative mass of dissolved nutrients
        absorbed by the crop from the hydroponic solution.

        During this implementation phase the estimate is derived directly from
        cumulative water uptake using a fixed proportional relationship.

        Future milestones will incorporate nutrient solution electrical
        conductivity, crop growth stage, crop species, irrigation strategy,
        and environmental conditions.

        Args
        ----
        state:
            Mutable runtime crop state.
        """

        state.nutrient_uptake_grams = (
            state.water_uptake_liters
            * 45.0
        )

    def _update_stress_index(
        self,
        state: CropState,
    ) -> None:
        """
        Update the crop stress index.

        The stress index provides a normalized estimate of overall crop
        stress.

        A value of zero represents an ideal growing condition, while a
        value of one hundred represents severe biological stress.

        During this implementation phase the index is derived solely from
        crop health.

        Future milestones will incorporate environmental conditions,
        irrigation performance, nutrient availability, equipment health,
        and crop-specific physiological responses.

        Args:
            state:
                Mutable runtime crop state.
        """

        state.stress_index = (
            100.0
            - state.health_score
        )

    def _determine_next_stage(
        self,
        state: CropState,
    ) -> str | None:
        """
        Determine whether a crop batch should advance to its next lifecycle
        stage.

        Lifecycle progression during this phase is deterministic and depends
        solely on accumulated crop age compared with the configured growth
        profile.

        Environmental conditions, equipment health, irrigation, disease,
        stress, and harvest scheduling are intentionally excluded from this
        implementation to minimize regression risk. Those influences will be
        introduced in later roadmap phases.

        Args:
            state:
                Runtime crop state.

        Returns:
            The next lifecycle stage if the crop has reached the required
            biological age; otherwise None.
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
            and age >= (
                profile.germination_days
                + profile.seedling_days
                + profile.vegetative_days
                + profile.maturity_days
            )
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