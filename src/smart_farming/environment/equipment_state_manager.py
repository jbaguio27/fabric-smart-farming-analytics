"""
Equipment runtime state manager.

This module manages mutable runtime state for registered equipment assets.

The manager owns all state transitions, initialization, and runtime
updates. It intentionally separates business logic from the Equipment
and EquipmentState models.
"""

from smart_farming.environment import (
    EquipmentRegistry,
    EquipmentState
)
from smart_farming.config import (
    HEALTH_DEGRADATION_PER_RUNTIME_HOUR,
    MAX_EQUIPMENT_HEALTH,
    MIN_EQUIPMENT_HEALTH,
    MAX_EQUIPMENT_LOAD,
    MIN_EQUIPMENT_LOAD,
    MIN_FAILURE_PROBABILITY,
    MAX_FAILURE_PROBABILITY,
    ERROR_FAILURE_THRESHOLD,
    MAX_LOAD_FAILURE_ADJUSTMENT,
    HEALTHY_EQUIPMENT_THRESHOLD,
    MIN_INITIAL_EQUIPMENT_HEALTH,
    MAX_INITIAL_EQUIPMENT_HEALTH,
    MAX_EQUIPMENT_RUNTIME_HOURS,
    NORMAL_OPERATING_LOAD_THRESHOLD,
    MAX_LOAD_CHANGE_PER_CYCLE,
    EQUIPMENT_LOAD_PROFILES,
    MAX_LOAD_VARIATION_PER_CYCLE,
)
from smart_farming.models import (
    EquipmentOperatingStatus,
)
from smart_farming.utils import (
    SimulationError,
    RandomManager,
)
from smart_farming.services import (
    FailureModel,
    MaintenanceManager,
    WearModel,
    FacilityDemandModel,
)


class EquipmentStateManager:
    """
    Manages routine state for registered equipment assets.
    """

    def __init__(
        self,
        equipment_registry: EquipmentRegistry,
        random_manager: RandomManager,
    ) -> None:
        """
        Initialize the equipment runtime state manager.

        Runtime state is automatically created for every registered
        equipment asset during construction. This guarantees that all
        registered equipment has mutable runtime state available before
        telemetry generation begins.

        Args:
            equipment_registry:
                Registry containing all persistent equipment assets.
        """
        self._equipment_registry = equipment_registry
        self._random_manager = random_manager
        self._wear_model = WearModel()
        self._failure_model = FailureModel()
        self._maintenance_manager = MaintenanceManager()
        self._facility_demand_model = FacilityDemandModel()
        self._states: dict[str, EquipmentState] = {}
        
        self.initialize()

    def initialize(self) -> None:
        """
        Create runtime state for every registered equipment asset.

        Existing runtime state is cleared before rebuilding to ensure the
        manager remains synchronized with the equipment registry.

        Each equipment asset receives an independent runtime state with a
        slightly randomized starting health. This avoids identical aging
        patterns across the simulator while remaining within realistic
        operating limits.
        """

        self._states.clear()

        for equipment in self._equipment_registry.list_all():
            
            state = EquipmentState()

            state.health = round(
                self._random_manager.uniform(
                    MIN_INITIAL_EQUIPMENT_HEALTH,
                    MAX_INITIAL_EQUIPMENT_HEALTH,
                ),
                2,
            )

            self._states[
                equipment.equipment_id
            ] = state

    def advance_runtime(
        self,
        hours: float,
    ) -> None:
        """
        Advance runtime for every registered equipment asset.

        Each simulation cycle contributes operating time to every
        equipment asset. Runtime accumulation is performed before any
        health degradation or operating status evaluation.

        Args:
            hours:
                Number of operating hours represented by the current
                simulation cycle.
        """

        for state in self._states.values():
            state.runtime_hours = round(
                state.runtime_hours + hours,
                2,
            )

    def update_health(
        self,
        hours: float,
    ) -> None:
        """
        Update equipment health based on accumulated runtime and the
        operating load from the previous simulation cycle.

        Equipment operating under heavier utilization experiences faster
        degradation than lightly loaded equipment. This produces more
        realistic long-term wear patterns and naturally diversifies
        equipment condition across the simulator.

        The degradation factor is calculated as:

            effective_degradation =
                base_degradation × (0.5 + load / 100)

        A minimum multiplier of 0.5 ensures that idle equipment continues
        to experience slow aging while highly utilized equipment degrades
        more rapidly.

        Args:
            hours:
                Number of operating hours represented by the current
                simulation cycle.
        """
        for equipment in self._equipment_registry.list_all():

            state = self._states[
                equipment.equipment_id
            ]

            profile = EQUIPMENT_LOAD_PROFILES[
                equipment.equipment_type
            ]


            load_multiplier = (
                0.5
                + (
                    state.current_load
                    / MAX_EQUIPMENT_LOAD
                )
            )

            degradation = (
                HEALTH_DEGRADATION_PER_RUNTIME_HOUR
                * hours
                * load_multiplier
            )

            state.health = round(
                self._wear_model.calculate_health(
                    state=state,
                    degradation=degradation,
                    wear_multiplier=profile.wear_multiplier,
                ),
                2,
            )

    def update_load(self) -> None:
        """
        Update the operating load for every registered equipment asset.

        Equipment load evolves gradually around a preferred operating target
        specific to each equipment type. This produces smoother utilization
        trends while preserving realistic operating behavior for pumps,
        HVAC systems, lighting, and ventilation equipment.

        Newly initialized equipment begins within its expected operating
        range. Subsequent simulation cycles apply bounded adjustments toward
        the preferred target load while allowing natural variation.
        """

        for equipment in self._equipment_registry.list_all():

            state = self._states[equipment.equipment_id]

            profile = EQUIPMENT_LOAD_PROFILES[
                equipment.equipment_type
            ]

            demand_multiplier = (
                self._facility_demand_model
                .get_multiplier(
                    runtime_hours=state.runtime_hours,
                )
            )

            minimum = profile.minimum

            maximum = min(
                MAX_EQUIPMENT_LOAD,
                profile.maximum
                * demand_multiplier,
            )

            target = min(
                MAX_EQUIPMENT_LOAD,
                profile.target
                * demand_multiplier,
            )

            if state.current_load == 0.0:

                state.current_load = round(
                    self._random_manager.uniform(
                        minimum,
                        maximum,
                    ),
                    2,
                )

                continue

            if state.current_load < target:
                drift = self._random_manager.uniform(
                    0.0,
                    MAX_LOAD_CHANGE_PER_CYCLE,
                )

            else:
                drift = self._random_manager.uniform(
                    -MAX_LOAD_CHANGE_PER_CYCLE,
                    0.0,
                )

            variation = self._random_manager.uniform(
                -MAX_LOAD_VARIATION_PER_CYCLE,
                MAX_LOAD_VARIATION_PER_CYCLE,
            )

            new_load = (
                state.current_load
                + drift
                + variation
            )

            state.current_load = round(
                max(
                    minimum,
                    min(
                        maximum,
                        new_load,
                    ),
                ),
                2,
            )

    def update_failure_probability(self) -> None:
        """
        Update the failure probability for every registered equipment asset.

        Failure probability is derived from three weighted contributors.

        1. Equipment health (65%)
        2. Current operating load (30%)
        3. Accumulated runtime (5%)

        Equipment health is the primary indicator because it already reflects
        long-term wear accumulated over the asset's lifetime. Current load
        captures short-term operational stress, while runtime provides a small
        baseline adjustment so that older equipment naturally becomes more
        failure-prone than newly commissioned equipment operating under the
        same conditions.
        """

        for equipment in self._equipment_registry.list_all():

            state = self._states[
                equipment.equipment_id
            ]

            health_factor = (
                MAX_EQUIPMENT_HEALTH
                - state.health
            ) / MAX_EQUIPMENT_HEALTH

            profile = EQUIPMENT_LOAD_PROFILES[
                equipment.equipment_type
            ]

            load = state.current_load

            if load <= profile.normal_threshold:

                load_factor = (
                    load
                    / profile.normal_threshold
                ) * 0.05

            elif load <= profile.warning_threshold:

                load_factor = (
                    0.05
                    + (
                        (
                            load
                            - profile.normal_threshold
                        )
                        /
                        (
                            profile.warning_threshold
                            - profile.normal_threshold
                        )
                    )
                    * profile.moderate_factor_max
                )

            else:

                critical_progress = (
                    load
                    - profile.warning_threshold
                ) / (
                    MAX_EQUIPMENT_LOAD
                    - profile.warning_threshold
                )

                load_factor = (
                    0.05
                    + profile.moderate_factor_max
                    + (
                        critical_progress ** 2
                    )
                    * (
                        profile.critical_factor_max
                        - profile.moderate_factor_max
                    )
                )

            runtime_factor = min(
                state.runtime_hours
                / MAX_EQUIPMENT_RUNTIME_HOURS,
                profile.critical_factor_max,
            )

            probability = (
                (health_factor * 0.65)
                + (load_factor * 0.30)
                + (runtime_factor * 0.05)
            )

            probability *= profile.failure_multiplier

            state.failure_probability = (
                self._failure_model.calculate_probability(
                    probability=probability,
                )
            )

    def update_operating_status(self) -> None:
        """
        Update operating status for every registered equipment asset.

        Equipment entering ERROR state remains in ERROR until
        maintenance intervention occurs.

        WARNING and ONLINE states continue to be recalculated
        each simulation cycle.
        """

        for state in self._states.values():

            if (
                state.operating_status
                == EquipmentOperatingStatus.ERROR
            ):
                continue

            if (
                self._failure_model
                .is_terminal_failure(
                    state,
                )
            ):

                state.operating_status = (
                    self._failure_model
                    .determine_operating_status(
                        state,
                    )
                )

                continue

            state.operating_status = (
                self._failure_model
                .determine_operating_status(
                    state,
                )
            )

    def evaluate_maintenance(
        self,
    ) -> None:
        """
        Evaluate maintenance eligibility for all
        registered equipment assets.

        This method currently performs only
        eligibility checks and establishes the
        maintenance execution point for future
        simulator enhancements.

        No runtime state is modified.
        """

        for state in self._states.values():

            self._maintenance_manager.apply(
                state,
            )

    def get(
        self,
        equipment_id: str,
    ) -> EquipmentState:
        """
        Retrieve runtime state for an equipment asset.

        Raises:
            SimulationError:
                If runtime state has not been initialized.
        """

        try:
            return self._states[equipment_id]
        except KeyError as exc:
            raise SimulationError(
                f"No runtime state exists for equipment '{equipment_id}'."
            ) from exc
    
    def exists(
        self,
        equipment_id: str,
    ) -> bool:
        """
        Return whether runtime state exists.
        """
        return equipment_id in self._states

    def list_all(self) -> list[EquipmentState]:
        """
        Return all runtime equipment states.

        Returns:
            Collection of runtime equipment states.
        """
        return list(self._states.values())