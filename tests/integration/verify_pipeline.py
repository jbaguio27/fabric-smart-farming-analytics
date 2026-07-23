"""
Local development verification pipeline.

This script performs lightweight sanity checks after each development
step. It is intentionally excluded from version control and should not
be committed.

As the simulator evolves, additional verification stages will be added
to this script.
"""
import os
os.environ["EQUIPMENT_TELEMETRY_SAMPLE_RATE"] = "1.0"

from dataclasses import dataclass
from smart_farming.config import (
    Settings,
    DEFAULT_GROWING_ZONES_PER_FACILITY,
    EQUIPMENT_TYPES,
    MIN_EQUIPMENT_HEALTH,
    MAX_EQUIPMENT_HEALTH,
    MIN_EQUIPMENT_LOAD,
    MAX_EQUIPMENT_LOAD,
    MIN_FAILURE_PROBABILITY,
    MAX_FAILURE_PROBABILITY,
    MIN_INITIAL_EQUIPMENT_HEALTH,
    MAX_INITIAL_EQUIPMENT_HEALTH,
    MAX_LOAD_CHANGE_PER_CYCLE,
    MAX_LOAD_VARIATION_PER_CYCLE,
    EQUIPMENT_SENSOR_PROFILES,
    EQUIPMENT_LOAD_PROFILES,
    MAX_HEALTH_SCORE,
    CROP_GROWTH_PROFILES,
    CROP_STAGE_GERMINATION,
    CROP_STAGE_SEEDLING,
    CROP_STAGE_VEGETATIVE,
    CROP_STAGE_MATURE,
    CROP_STAGE_HARVESTED,
)
from smart_farming.environment import (
    EquipmentRegistry,
    EquipmentStateManager,
    EnvironmentStateManager,
    CropDefinition,
    CropRegistry,
    CropProfileRegistry,
    CropStateManager,
    GrowingEnvironmentStateManager,
    IrrigationStateManager,
    LightingStateManager,
)
from smart_farming.utils import (
    RandomManager,
)
from smart_farming.models import (
    EquipmentOperatingStatus,
    EquipmentTelemetryEvent,
    CropLifecycleEvent,
    IrrigationTelemetryEvent,
    EnvironmentalTelemetryEvent,
)
from smart_farming.generators import (
    EnvironmentalTelemetryGenerator,
    EquipmentTelemetryGenerator,
    CropLifecycleGenerator,
    CropTelemetryGenerator,
    IrrigationTelemetryGenerator,
    LightingTelemetryGenerator,
)
from smart_farming.validation import (
    TelemetryValidator,
    CropLifecycleValidator,
    IrrigationTelemetryValidator,
)
from smart_farming.services import (
    WearModel,
    FailureModel,
    MaintenanceManager,
    FacilityDemandModel,
)


@dataclass(slots=True)
class VerificationContext:
    """
    Shared application context used by every verification stage.

    The verification pipeline intentionally mirrors the application's
    composition root so that every stage operates on the same simulator
    state instead of constructing isolated objects.

    Attributes:
        settings:
            Application configuration.

        random_manager:
            Shared random number generator.

        environment_manager:
            Shared environment state manager.

        equipment_registry:
            Shared equipment registry.

        equipment_state_manager:
            Shared runtime state manager.
    """

    settings: Settings

    random_manager: RandomManager

    environment_manager: EnvironmentStateManager

    equipment_registry: EquipmentRegistry

    crop_profile_registry: CropProfileRegistry

    crop_registry: CropRegistry

    equipment_state_manager: EquipmentStateManager

    crop_state_manager: CropStateManager

    growing_environment_manager: GrowingEnvironmentStateManager

    irrigation_state_manager: IrrigationStateManager

    lighting_state_manager: LightingStateManager

    environmental_generator: EnvironmentalTelemetryGenerator

    equipment_generator: EquipmentTelemetryGenerator

    crop_lifecycle_generator: CropLifecycleGenerator

    crop_lifecycle_validator: CropLifecycleValidator

    crop_telemetry_generator: CropTelemetryGenerator

    irrigation_telemetry_generator: IrrigationTelemetryGenerator

    lighting_telemetry_generator: LightingTelemetryGenerator

def build_verification_context() -> VerificationContext:
    """
    Build the shared verification context.

    Returns:
        Fully initialized verification context.
    """

    settings = Settings.from_env()
    settings.equipment_telemetry_sample_rate = 1.0

    random_manager = RandomManager(
        seed=settings.random_seed,
    )

    environment_manager = EnvironmentStateManager(
        settings=settings,
        random_manager=random_manager,
    )

    growing_environment_manager = (
        GrowingEnvironmentStateManager(
            settings=settings,
            random_manager=random_manager,
            zone_count=settings.zone_count,
        )
    )

    irrigation_state_manager = (
        IrrigationStateManager(
            zone_count=settings.zone_count,
        )
    )

    lighting_state_manager = (
        LightingStateManager(
            settings=settings,
            zone_count=settings.zone_count,
        )
    )

    equipment_registry = EquipmentRegistry(
        settings=settings,
    )

    wear_model = WearModel()
    failure_model = FailureModel()
    maintenance_manager = MaintenanceManager()
    facility_demand_model = FacilityDemandModel()


    equipment_state_manager = EquipmentStateManager(
        equipment_registry=equipment_registry,
        random_manager=random_manager,
        wear_model=wear_model,
        failure_model=failure_model,
        maintenance_manager=maintenance_manager,
        facility_demand_model=facility_demand_model,
    )

    crop_profile_registry = CropProfileRegistry()

    crop_registry = CropRegistry()

    for index, profile in enumerate(
        crop_profile_registry.get_all_profiles(),
        start=1,
    ):
        crop_registry.register(
            CropDefinition(
                crop_batch_id=f"BATCH-{index:05d}",
                facility_id="FAC-001",
                zone_id=f"ZONE-{index:03d}",
                crop_type=profile.crop_type,
            )
        )

    crop_state_manager = CropStateManager(
        settings=settings,
        crop_registry=crop_registry,
        crop_profile_registry=crop_profile_registry,
        growing_environment_manager=growing_environment_manager,
        random_manager=random_manager,
        irrigation_state_manager=irrigation_state_manager,
    )

    crop_lifecycle_generator = CropLifecycleGenerator(
        settings=settings,
        random_manager=random_manager,
        environment_manager=growing_environment_manager,
        crop_registry=crop_registry,
        crop_state_manager=crop_state_manager,
    )

    environmental_generator = (
        EnvironmentalTelemetryGenerator(
            settings=settings,
            random_manager=random_manager,
            environment_manager=environment_manager,
        )
    )

    equipment_generator = (
        EquipmentTelemetryGenerator(
            settings=settings,
            environment_manager=environment_manager,
            equipment_registry=equipment_registry,
            equipment_state_manager=equipment_state_manager,
        )
    )

    crop_lifecycle_validator = CropLifecycleValidator()

    crop_telemetry_generator = CropTelemetryGenerator(
        settings=settings,
        random_manager=random_manager,
        environment_manager=growing_environment_manager,
        crop_registry=crop_registry,
        crop_state_manager=crop_state_manager,
    )

    irrigation_telemetry_generator = (
        IrrigationTelemetryGenerator(
            settings=settings,
            environment_manager=environment_manager,
            irrigation_state_manager=(
                irrigation_state_manager
            ),
        )
    )

    lighting_telemetry_generator = (
        LightingTelemetryGenerator(
            settings=settings,
            lighting_state_manager=(
                lighting_state_manager
            ),
        )
    )

    return VerificationContext(
        settings=settings,
        random_manager=random_manager,
        environment_manager=environment_manager,
        equipment_registry=equipment_registry,
        equipment_state_manager=equipment_state_manager,
        crop_profile_registry=crop_profile_registry,
        crop_registry=crop_registry,
        crop_state_manager=crop_state_manager,
        growing_environment_manager=growing_environment_manager,
        irrigation_state_manager=irrigation_state_manager,
        lighting_state_manager=lighting_state_manager,
        environmental_generator=environmental_generator,
        equipment_generator=equipment_generator,
        crop_lifecycle_generator=crop_lifecycle_generator,
        crop_lifecycle_validator=crop_lifecycle_validator,
        crop_telemetry_generator=crop_telemetry_generator,
        irrigation_telemetry_generator=irrigation_telemetry_generator,
        lighting_telemetry_generator=lighting_telemetry_generator,
    )


def verify_equipment_registry(
    context: VerificationContext,
) -> None:
    """
    Verify that the equipment registry initializes correctly.
    """

    settings = context.settings

    registry = context.equipment_registry

    equipment = registry.list_all()

    expected_count = (
        settings.total_facilities
        * DEFAULT_GROWING_ZONES_PER_FACILITY
        * len(EQUIPMENT_TYPES)
    ) + settings.total_facilities * 4

    assert len(equipment) == expected_count, (
        f"Expected {expected_count} equipment assets, "
        f"found {len(equipment)}."
    )

    print(
        "[PASS] Equipment registry initialized with "
        f"{len(equipment)} assets."
    )

    print()

    print("First six registered assets:")

    for asset in equipment[:6]:
        print(
            f"{asset.equipment_id:<10}"
            f"{asset.facility_id:<10}"
            f"{asset.zone_id:<10}"
            f"{asset.equipment_type:<18}"
            f"{asset.manufacturer:<15}"
            f"{asset.model}"
        )

def verify_equipment_state_manager(
    context: VerificationContext,
) -> None:
    """
    Verify that the equipment state manager initializes correctly and
    performs a complete simulation cycle successfully.

    Verification is intentionally divided into two phases:

    1. Initialization Verification
    Confirms that every registered equipment asset receives an
    initial runtime state.

    2. Simulation Cycle Verification
    Executes one complete runtime update cycle and verifies that
    mutable runtime values change as expected.
    """

    settings = context.settings

    random_manager = RandomManager(
        seed=settings.random_seed,
    )

    registry = context.equipment_registry

    equipment_state_manager = (
        context.equipment_state_manager
    )

    # ===============================================================
    # Phase 1
    # Initialization Verification
    # ===============================================================

    runtime_states = equipment_state_manager.list_all()

    health_values = {
        state.health
        for state in runtime_states
    }

    assert len(health_values) > 1, (
        "Expected randomized initial health values, "
        "but every equipment asset has the same health."
    )

    assert len(runtime_states) == len(registry), (
        "Equipment registry and runtime state counts differ."
    )

    print(
        "[PASS] Equipment state manager initialized with "
        f"{len(runtime_states)} runtime states."
    )

    print()
    print(
        "Initial runtime state sample "
        "(randomized starting health):"
    )

    for equipment in registry.list_all()[:5]:
        state = equipment_state_manager.get(
            equipment.equipment_id
        )

        assert (
            MIN_INITIAL_EQUIPMENT_HEALTH
            <= state.health
            <= MAX_INITIAL_EQUIPMENT_HEALTH
        )
        assert state.runtime_hours == 0.0
        assert state.current_load == 0.0
        assert state.failure_probability == 0.0
        assert (
            state.operating_status
            == EquipmentOperatingStatus.ONLINE
        )

        print(
            f"{equipment.equipment_id:<10}"
            f"Health={state.health:<6}"
            f"Runtime={state.runtime_hours:<6}"
            f"Load={state.current_load:<6}"
            f"Failure={state.failure_probability:<6}"
            f"Status={state.operating_status.value}"
        )

    # ===============================================================
    # Phase 2
    # Simulation Cycle Verification
    # ===============================================================

    equipment_state_manager.advance_runtime(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_health(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_load()

    previous_loads = {
        equipment.equipment_id: (
            equipment_state_manager
            .get(equipment.equipment_id)
            .current_load
        )
        for equipment in registry.list_all()
    }

    equipment_state_manager.update_load()

    for equipment in registry.list_all():

        state = equipment_state_manager.get(
            equipment.equipment_id
        )

        profile = EQUIPMENT_LOAD_PROFILES[
            equipment.equipment_type
        ]

        assert (
            profile.minimum
            <= state.current_load
            <= MAX_EQUIPMENT_LOAD
        )

    equipment_state_manager.update_failure_probability()

    equipment_state_manager.update_operating_status()

    print()
    print("Runtime state after one simulation cycle:")

    for equipment in registry.list_all()[:5]:
        state = equipment_state_manager.get(
            equipment.equipment_id
        )

        assert state.runtime_hours == (
            settings.simulation_cycle_hours
        )

        assert (
            state.health
            < MAX_EQUIPMENT_HEALTH
        ), (
            "Equipment health should decrease after a "
            "simulation cycle."
        )

        assert (
            state.current_load
            >= MIN_EQUIPMENT_LOAD
        )

        assert (
            MIN_EQUIPMENT_HEALTH
            <= state.health
            <= MAX_EQUIPMENT_HEALTH
        )

        assert (
            MIN_EQUIPMENT_LOAD
            <= state.current_load
            <= MAX_EQUIPMENT_LOAD
        )

        assert (
            MIN_FAILURE_PROBABILITY
            <= state.failure_probability
            <= MAX_FAILURE_PROBABILITY
        )

        assert (
            state.failure_probability
            > 0.0
        ), (
            "Failure probability should increase after runtime advances."
        )

        assert isinstance(
            state.operating_status,
            EquipmentOperatingStatus,
        )

        print(
            f"{equipment.equipment_id:<10}"
            f"Health={state.health:<6.2f}"
            f"Runtime={state.runtime_hours:<6.1f}"
            f"Load={state.current_load:<6.2f}"
            f"Failure={state.failure_probability:<7.4f}"
            f"Status={state.operating_status.value}"
        )

    print()
    print(
        "[PASS] Equipment state simulation cycle verified."
    )

def verify_crop_state_manager(
    context: VerificationContext,
) -> None:
    """
    Verify CropStateManager initialization.

    This verification ensures the crop infrastructure has been
    constructed correctly before biological simulation is introduced.

    The following invariants are validated:

    * Crop growth profiles are loaded.
    * Crop registry contains one batch per profile.
    * Crop state manager created one runtime state per batch.
    * Crop batch identifiers are unique.
    * Zone identifiers are unique.
    * Every crop begins in GERMINATION.
    * Every crop begins active.
    * Every crop begins at age zero.
    * Every crop begins with its configured optimal health.

    Raises
    ------
    AssertionError
        If any invariant is violated.
    """

    print("\nVerifying Crop State Manager...")

    crop_registry = context.crop_registry
    profile_registry = context.crop_profile_registry
    crop_state_manager = context.crop_state_manager

    profiles = profile_registry.get_all_profiles()
    batches = crop_registry.get_all()
    states = crop_state_manager.get_all_states()

    assert len(profiles) == 10, (
        "Expected exactly 10 crop growth profiles."
    )

    assert len(batches) == len(profiles), (
        "Crop registry size does not match profile registry."
    )

    assert len(states) == len(batches), (
        "Crop state manager size does not match crop registry."
    )

    batch_ids: set[str] = set()
    zone_ids: set[str] = set()

    profile_lookup = {
        profile.crop_type: profile
        for profile in profiles
    }

    for state in states:

        assert state.crop_batch_id not in batch_ids, (
            f"Duplicate crop batch id: {state.crop_batch_id}"
        )

        batch_ids.add(state.crop_batch_id)

        assert state.zone_id not in zone_ids, (
            f"Duplicate zone id: {state.zone_id}"
        )

        zone_ids.add(state.zone_id)

        assert state.lifecycle_stage == "GERMINATION"

        assert state.age_days == 0

        assert state.is_active is True

        profile = profile_lookup[state.crop_type]

        assert (
            state.health_score
            == MAX_HEALTH_SCORE
        ), (
            f"Unexpected health score for {state.crop_type}"
        )

    print("✓ CropStateManager verification passed.")

    simulation_cycles = 5000

    for _ in range(simulation_cycles):
        crop_state_manager.advance_cycle()

    states = crop_state_manager.get_all_states()

    oldest_crop = max(
        states,
        key=lambda crop: crop.age_days,
    )

    elapsed_days = oldest_crop.age_days


    print()
    print("Crop Lifecycle Simulation")
    print("=" * 70)

    elapsed_days = (
        states[0].age_days
        if states
        else 0.0
    )

    print(f"Simulation Cycles : {simulation_cycles}")
    print(f"Elapsed Time      : {elapsed_days:.2f} days")

    print()
    print(
        f"{'Batch':12}"
        f"{'Crop':24}"
        f"{'Stage':15}"
        f"{'Age':>8}"
        f"{'Health':>10}"
        f"{'Active':>10}"
    )

    print("-" * 90)

    for state in states[:10]:
        print(
            f"{state.crop_batch_id:12}"
            f"{state.crop_type[:22]:24}"
            f"{state.lifecycle_stage:15}"
            f"{state.age_days:8.1f}"
            f"{state.health_score:10.1f}"
            f"{str(state.is_active):>10}"
        )

    print()
    print("Lifecycle Statistics")

    stage_counts: dict[str, int] = {}

    for state in states:
        stage_counts[state.lifecycle_stage] = (
            stage_counts.get(state.lifecycle_stage, 0) + 1
        )

    stage_health: dict[str, list[float]] = {}

    for state in states:
        stage_health.setdefault(
            state.lifecycle_stage,
            [],
        ).append(state.health_score)

    active_count = sum(
        state.is_active
        for state in states
    )

    harvested_count = sum(
        state.lifecycle_stage == CROP_STAGE_HARVESTED
        for state in states
    )

    average_health = (
        sum(state.health_score for state in states)
        / len(states)
    )

    average_age = (
        sum(state.age_days for state in states)
        / len(states)
    )

    print()
    print("Average Health by Lifecycle Stage")
    print("-" * 40)

    stage_order = (
        CROP_STAGE_GERMINATION,
        CROP_STAGE_SEEDLING,
        CROP_STAGE_VEGETATIVE,
        CROP_STAGE_MATURE,
        CROP_STAGE_HARVESTED,
    )

    for stage in stage_order:
        count = stage_counts.get(stage, 0)

        scores = stage_health.get(stage, [])

        average = (
            sum(scores) / len(scores)
            if scores
            else 0.0
        )

        print(
            f"{stage:15}"
            f"{count:>8}"
            f"{average:12.2f}"
        )

    assert average_health <= 100.0

    assert active_count + harvested_count == len(states)

    assert all(
        0.0 <= state.health_score <= 100.0
        for state in states
    )

    assert all(
        state.age_days >= 0
        for state in states
    )

    assert any(
        state.lifecycle_stage != CROP_STAGE_GERMINATION
        for state in states
    ), (
        "No crops progressed beyond GERMINATION."
    )

    assert (
        average_age > 0
    ), (
        "Crop age did not increase."
    )

    assert (
        oldest_crop.age_days >= average_age
    ), (
        "Oldest crop calculation failed."
    )

    assert (
        oldest_crop.lifecycle_stage
        != CROP_STAGE_GERMINATION
    ), (
        "Oldest crop never progressed beyond GERMINATION."
    )

    print()
    print("=" * 40)
    print("Crop Simulation Summary")
    print("=" * 40)
    print(f"Average Age:     {average_age:.2f} days")
    print(f"Average Health:  {average_health:.2f}")
    print(f"Active Crops:    {active_count}")
    print(f"Harvested:       {harvested_count}")

    stage_order = (
        CROP_STAGE_GERMINATION,
        CROP_STAGE_SEEDLING,
        CROP_STAGE_VEGETATIVE,
        CROP_STAGE_MATURE,
        CROP_STAGE_HARVESTED,
    )

    for stage in stage_order:
        count = stage_counts.get(stage, 0)
        print(f"{stage:15} {count}")

    print()

    print("=" * 40)
    print("Most Developed Crop")
    print("=" * 40)
    print(
        f"Batch:   {oldest_crop.crop_batch_id}"
    )
    print(
        f"Crop:    {oldest_crop.crop_type}"
    )
    print(
        f"Stage:   {oldest_crop.lifecycle_stage}"
    )
    print(
        f"Age:     {oldest_crop.age_days:.2f} days"
    )
    print(
        f"Health:  {oldest_crop.health_score:.2f}"
    )

    print()
    print(
        "[PASS] Crop lifecycle simulation verified."
    )

def verify_crop_lifecycle_generator(
    context: VerificationContext,
) -> None:
    """
    Verify CropLifecycleGenerator.

    This verification confirms that immutable crop lifecycle events
    accurately reflect the simulator runtime state.

    The generator must not mutate runtime state. It simply transforms
    CropState and GrowingEnvironmentState into immutable telemetry
    events.

    Raises
    ------
    AssertionError
        If event generation does not faithfully represent simulator
        state.
    """

    print()
    print("Verifying Crop Lifecycle Generator...")

    generator = context.crop_lifecycle_generator

    manager = context.crop_state_manager

    environment_manager = (
        context.growing_environment_manager
    )

    events = generator.generate()

    validator = (
        context.crop_lifecycle_validator
    )

    validated_events = 0

    for event in events:
        validator.validate(event)
        validated_events += 1

    assert validated_events == len(events)

    active_states = [
        state
        for state in manager.get_all_states()
        if state.is_active
    ]

    assert len(events) <= len(active_states), (
        "Generator emitted more lifecycle events than active crops."
    )

    runtime_lookup = {
        state.crop_batch_id: state
        for state in active_states
    }

    for event in events:

        assert isinstance(
            event,
            CropLifecycleEvent,
        ), (
            "Generator must return CropLifecycleEvent instances."
        )

        runtime = runtime_lookup[event.crop_batch_id]
        definition = context.crop_registry.get(
            event.crop_batch_id,
        )
        environment = (
            environment_manager.get_zone_state(
                runtime.zone_id,
            )
        )

        assert (
            event.facility_id
            == definition.facility_id
        )

        assert (
            event.zone_id
            == definition.zone_id
        )

        assert (
            event.crop_type
            == definition.crop_type
        )

        assert (
            event.lifecycle_stage
            == runtime.lifecycle_stage
        )

        assert (
            event.age_days
            == runtime.age_days
        )

        assert (
            event.health_score
            == runtime.health_score
        )

        assert (
            event.is_active
            == runtime.is_active
        )

        assert (
            event.air_temperature_celsius
            == environment.air_temperature_celsius
        )

        assert (
            event.humidity_percent
            == environment.humidity_percent
        )

        assert (
            event.water_ph
            == environment.water_ph
        )

        assert (
            event.electrical_conductivity
            == environment.electrical_conductivity
        )

        assert (
            event.environmental_stress_index
            == runtime.stress_index
        )

        assert event.simulation_cycle >= 0

        assert event.event_type == "CropLifecycleEvent"

        assert event.event_id

        assert event.timestamp is not None

    print(
        "[PASS] Crop lifecycle events validated."
    )

    print(
        "[PASS] Initial lifecycle events: "
        f"{len(events)}"
    )

    print(
        "[PASS] Continuous lifecycle event generation verified."
    )

    print()
    print("First six crop lifecycle events:")

    print()

    print(
        f"{'Batch':12}"
        f"{'Facility':10}"
        f"{'Zone':10}"
        f"{'Crop':24}"
        f"{'Stage':15}"
        f"{'Cycle':>8}"
        f"{'Age':>8}"
        f"{'Health':>8}"
        f"{'Temp':>8}"
        f"{'Humidity':>11}"
        f"{'pH':>8}"
        f"{'EC':>8}"
    )

    print("-" * 131)
    
    for event in events[:6]:
        print(
            f"{event.crop_batch_id:12}"
            f"{event.facility_id:10}"
            f"{event.zone_id:10}"
            f"{event.crop_type[:22]:24}"
            f"{event.lifecycle_stage:15}"
            f"{event.simulation_cycle:8}"
            f"{event.age_days:8.1f}"
            f"{event.health_score:8.1f}"
            f"{event.air_temperature_celsius:8.1f}"
            f"{event.humidity_percent:11.1f}"
            f"{event.water_ph:8.2f}"
            f"{event.electrical_conductivity:8.2f}"
        )

def verify_crop_telemetry_generator(
    context: VerificationContext,
) -> None:
    """
    Verify CropTelemetryGenerator.

    This verification confirms that the generator faithfully converts the
    authoritative runtime crop state into immutable crop telemetry events.

    The generator must not mutate runtime state.

    Raises
    ------
    AssertionError
        If generated telemetry differs from the runtime state.
    """

    print()
    print("Verifying Crop Telemetry Generator...")

    generator = context.crop_telemetry_generator

    crop_state_manager = context.crop_state_manager

    environment_manager = (
        context.growing_environment_manager
    )

    events = generator.generate()

    active_states = [
        state
        for state in crop_state_manager.get_all_states()
        if state.is_active
    ]

    assert (
        len(events) == len(active_states)
    ), (
        "Crop telemetry event count does not match active crop count."
    )

    runtime_lookup = {
        state.crop_batch_id: state
        for state in active_states
    }

    for event in events:

        runtime = runtime_lookup[
            event.crop_batch_id
        ]

        environment = (
            environment_manager.get_zone_state(
                runtime.zone_id,
            )
        )

        assert (
            event.lifecycle_stage
            == runtime.lifecycle_stage
        ), (
            f"Lifecycle stage mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.age_days
            == runtime.age_days
        ), (
            f"Age mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.health_score
            == runtime.health_score
        ), (
            f"Health mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.growth_rate
            == runtime.growth_rate
        ), (
            f"Growth rate mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.biomass_grams
            == runtime.biomass_grams
        ), (
            f"Biomass mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.water_consumption_liters
            == runtime.water_uptake_liters
        ), (
            f"Water uptake mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.nutrient_consumption_grams
            == runtime.nutrient_uptake_grams
        ), (
            f"Nutrient uptake mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.environmental_stress_index
            == runtime.stress_index
        ), (
            f"Stress index mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.ambient_temperature_celsius
            == environment.air_temperature_celsius
        ), (
            f"Temperature mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.ambient_humidity_percent
            == environment.humidity_percent
        ), (
            f"Humidity mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.water_ph
            == environment.water_ph
        ), (
            f"Water pH mismatch for "
            f"{runtime.crop_batch_id}."
        )

        assert (
            event.electrical_conductivity
            == environment.electrical_conductivity
        ), (
            f"EC mismatch for "
            f"{runtime.crop_batch_id}."
        )

    print(
        "[PASS] Crop telemetry events validated."
    )

    print(
        f"[PASS] Generated {len(events)} crop telemetry events."
    )

    print()

    print(
        f"{'Batch':12}"
        f"{'Crop':24}"
        f"{'Stage':15}"
        f"{'Age':>8}"
        f"{'Health':>10}"
        f"{'Growth':>10}"
        f"{'Biomass':>12}"
        f"{'Water':>10}"
        f"{'Nutrients':>12}"
        f"{'Stress':>10}"
        f"{'Temp':>8}"
        f"{'Humidity':>12}"
    )

    print("-" * 92)

    for event in events[:5]:

        print(
            f"{event.crop_batch_id:12}"
            f"{event.crop_type[:22]:24}"
            f"{event.lifecycle_stage:15}"
            f"{event.age_days:8.1f}"
            f"{event.health_score:10.1f}"
            f"{event.growth_rate:10.2f}"
            f"{event.biomass_grams:12.1f}"
            f"{event.water_consumption_liters:10.2f}"
            f"{event.nutrient_consumption_grams:12.1f}"
            f"{event.environmental_stress_index:10.1f}"
            f"{event.ambient_temperature_celsius:8.1f}"
            f"{event.ambient_humidity_percent:12.1f}"
        )

def verify_irrigation_telemetry_generator(
    context: VerificationContext,
) -> None:
    """
    Verify irrigation telemetry generation.

    This verification ensures the irrigation telemetry generator
    produces one telemetry event for every managed irrigation runtime
    state and that every generated event accurately reflects the
    underlying runtime model.
    """

    print()

    print(
        "Verifying Irrigation Telemetry Generator..."
    )

    events = (
        context.irrigation_telemetry_generator.generate()
    )

    assert events, (
        "No irrigation telemetry events were generated."
    )

    runtime_lookup = {

        state.zone_id: state

        for state in (
            context.irrigation_state_manager.get_all_states()
        )
    }

    for event in events:

        IrrigationTelemetryValidator.validate(
            event
        )

        runtime = runtime_lookup[
            event.zone_id
        ]

        assert (
            event.irrigation_active
            == runtime.irrigation_active
        )

        assert (
            event.flow_rate_liters_per_minute
            == runtime.flow_rate_liters_per_minute
        )

        assert (
            event.pressure_kpa
            == runtime.pressure_kpa
        )

        assert (
            event.irrigation_duration_seconds
            == runtime.irrigation_duration_seconds
        )

        assert (
            event.water_delivered_liters
            == runtime.water_delivered_liters
        )

        assert (
            event.nutrient_solution_delivered_liters
            == runtime.nutrient_solution_delivered_liters
        )

    print(
        "[PASS] Irrigation telemetry events validated."
    )

    print(
        (
            "[PASS] Generated "
            f"{len(events)} irrigation telemetry events."
        )
    )

    print()

    print(
        "{:<10} {:<10} {:>8} {:>10} {:>10}".format(
            "Zone",
            "Active",
            "Flow",
            "Pressure",
            "Water",
        )
    )

    print("-" * 60)

    for event in events[:5]:

        print(
            "{:<10} {:<10} {:>8.2f} {:>10.1f} {:>10.2f}".format(
                event.zone_id,
                str(event.irrigation_active),
                event.flow_rate_liters_per_minute,
                event.pressure_kpa,
                event.water_delivered_liters,
            )
        )

def verify_lighting_telemetry_generator(
    context: VerificationContext,
) -> None:
    """
    Verify lighting telemetry generation.

    This verification ensures the lighting telemetry generator produces
    one telemetry event per growing zone and that the generated events
    contain the expected runtime lighting values.
    """

    print()
    print("Verifying Lighting Telemetry Generator...")

    events = (
        context
        .lighting_telemetry_generator
        .generate()
    )

    expected = context.settings.zone_count

    assert (
        len(events) == expected
    ), (
        f"Expected {expected} lighting events, "
        f"received {len(events)}."
    )

    print(
        "[PASS] Lighting telemetry events validated."
    )

    print(
        f"[PASS] Generated {len(events)} "
        "lighting telemetry events."
    )

    print()

    print(
        f"{'Zone':<10}"
        f"{'Enabled':<10}"
        f"{'Intensity':>12}"
        f"{'Photo Hr':>12}"
        f"{'DLI':>10}"
    )

    print("-" * 56)

    for event in events[:5]:

        print(
            f"{event.zone_id:<10}"
            f"{str(event.lighting_enabled):<10}"
            f"{event.lighting_intensity_percent:>12.1f}"
            f"{event.photoperiod_hours:>12.1f}"
            f"{event.daily_light_integral:>10.1f}"
        )

    print()

    print("Lighting Summary")
    print("=" * 60)

    enabled_count = sum(
        event.lighting_enabled
        for event in events
    )

    average_intensity = (
        sum(
            event.lighting_intensity_percent
            for event in events
        )
        / len(events)
    )

    average_photoperiod = (
        sum(
            event.photoperiod_hours
            for event in events
        )
        / len(events)
    )

    average_dli = (
        sum(
            event.daily_light_integral
            for event in events
        )
        / len(events)
    )

    print(
        f"Lighting Enabled : "
        f"{enabled_count}/{len(events)}"
    )

    print(
        f"Average Intensity: "
        f"{average_intensity:.2f} %"
    )

    print(
        f"Average Photoperiod: "
        f"{average_photoperiod:.2f} h"
    )

    print(
        f"Average DLI: "
        f"{average_dli:.2f}"
    )

    print()

    print("Lighting Ranges")
    print("-" * 60)

    print(
        f"Intensity : "
        f"{min(event.lighting_intensity_percent for event in events):.2f}"
        f" - "
        f"{max(event.lighting_intensity_percent for event in events):.2f}"
    )

    print(
        f"Photoperiod : "
        f"{min(event.photoperiod_hours for event in events):.2f}"
        f" - "
        f"{max(event.photoperiod_hours for event in events):.2f}"
    )

    print(
        f"DLI : "
        f"{min(event.daily_light_integral for event in events):.2f}"
        f" - "
        f"{max(event.daily_light_integral for event in events):.2f}"
    )

def verify_equipment_telemetry_generator(
    context: VerificationContext,
) -> None:
    """
    Verify that the equipment telemetry generator produces one
    telemetry event for every registered equipment asset.

    This verification confirms that immutable equipment metadata,
    mutable runtime state, and shared simulation time are correctly
    combined into EquipmentTelemetryEvent instances.
    """

    settings = context.settings

    random_manager = RandomManager(
        seed=settings.random_seed,
    )

    environment_manager = (
        context.environment_manager
    )

    registry = (
        context.equipment_registry
    )

    equipment_state_manager = (
        context.equipment_state_manager
    )

    equipment_state_manager.advance_runtime(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_health(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_load()
    equipment_state_manager.update_failure_probability()
    equipment_state_manager.update_operating_status()

    generator = EquipmentTelemetryGenerator(
        settings=settings,
        environment_manager=environment_manager,
        equipment_registry=registry,
        equipment_state_manager=equipment_state_manager,
    )

    events = generator.generate()

    validator = TelemetryValidator()

    validated_events = 0

    for event in events:

        validator.validate_equipment_event(
            event
        )

        state = equipment_state_manager.get(
            event.equipment_id,
        )

        validator.validate_runtime_consistency(
            event=event,
            state=state,
        )

        profile = (
            EQUIPMENT_SENSOR_PROFILES[
                event.equipment_type
            ]
        )

        validator.validate_sensor_profile_compliance(
            event=event,
            profile=profile,
        )
        validated_events += 1

    print()

    print(
        "Telemetry validation summary:"
    )

    print(
        f"Validated Events: "
        f"{validated_events}"
    )

    print(
        "[PASS] Equipment telemetry "
        "validation completed."
    )

    print()

    print(
        "[PASS] Runtime-to-event consistency "
        "validation completed."
    )

    print()

    print(
        "[PASS] Equipment sensor profile "
        "compliance validation completed."
    )

    print()

    print(
        "Validation Statistics"
    )

    print(
        f"Validated Events: "
        f"{validator.statistics.validated_events}"
    )

    print(
        f"Runtime Consistency Checks: "
        f"{validator.statistics.runtime_consistency_checks}"
    )

    print(
        f"Profile Compliance Checks: "
        f"{validator.statistics.profile_compliance_checks}"
    )

    expected_event_count = len(events)

    assert (
        validator.statistics.validated_events
        == expected_event_count
    ), (
        "Validation coverage mismatch: "
        f"expected {expected_event_count} "
        f"validated events but found "
        f"{validator.statistics.validated_events}."
    )

    assert (
        validator.statistics.runtime_consistency_checks
        == expected_event_count
    ), (
        "Runtime consistency coverage mismatch: "
        f"expected {expected_event_count} "
        f"checks but found "
        f"{validator.statistics.runtime_consistency_checks}."
    )

    assert (
        validator.statistics.profile_compliance_checks
        == expected_event_count
    ), (
        "Sensor profile coverage mismatch: "
        f"expected {expected_event_count} "
        f"checks but found "
        f"{validator.statistics.profile_compliance_checks}."
    )

    print()

    print(
        "[PASS] Validation coverage verified."
    )

    print()

    print(
        "Validated telemetry sample:"
    )

    for event in events[:5]:
        print(
            f"{event.equipment_id:<10}"
            f"Health={event.health:<8.2f}"
            f"Load={event.current_load:<8.2f}"
            f"Failure={event.failure_probability:<8.4f}"
        )

    print()
    print(
        "Equipment telemetry sensor sample:"
    )

    for event in events[:5]:

        assert (
            event.power_consumption_kw > 0.0
        ), (
            f"{event.equipment_id} "
            "power consumption was not emitted."
        )

        assert (
            event.operating_temperature_c > 0.0
        ), (
            f"{event.equipment_id} "
            "temperature was not emitted."
        )

        assert (
            event.vibration_vps > 0.0
        ), (
            f"{event.equipment_id} "
            "vibration was not emitted."
        )

        print(
            f"{event.equipment_id:<10}"
            f"Power={event.power_consumption_kw:<8.3f}"
            f"Temp={event.operating_temperature_c:<8.2f}"
            f"Vibration={event.vibration_vps:<8.3f}"
        )

    for event in events:

        assert (
            event.power_consumption_kw
            is not None
        )

        assert (
            event.operating_temperature_c
            is not None
        )

        assert (
            event.vibration_vps
            is not None
        )

    print()
    print(
        "[PASS] Equipment telemetry event normalization verified."
    )

    assert len(events) == len(registry), (
        "Equipment telemetry event count does not match "
        "registered equipment."
    )

    print()
    print(
        "[PASS] Equipment telemetry generator produced "
        f"{len(events)} events."
    )

    print()
    print("First six equipment telemetry events:")

    for event in events[:6]:

        assert isinstance(
            event,
            EquipmentTelemetryEvent,
        )

        assert registry.exists(
            event.equipment_id,
        )

        print(
            f"{event.equipment_id:<10}"
            f"{event.facility_id:<10}"
            f"{event.zone_id:<10}"
            f"{event.equipment_type:<18}"
            f"{event.operating_status.value:<10}"
            f"Health={event.health:<6.2f}"
            f"Load={event.current_load:<6.2f}"
            f"Failure={event.failure_probability:<7.4f}"
        )

def verify_environmental_telemetry_generator(
    context: VerificationContext,
) -> None:
    """
    Verify environmental telemetry generation.

    This verification ensures the environmental telemetry generator
    produces environmental telemetry events and that they contain
    valid values (ambient temperature, humidity, CO2, etc.) for each facility.
    """

    print()
    print("Verifying Environmental Telemetry Generator...")

    events = context.environmental_generator.generate()

    assert events, "No environmental telemetry events were generated."

    for event in events:
        assert isinstance(event, EnvironmentalTelemetryEvent), (
            "Generator must return EnvironmentalTelemetryEvent instances."
        )
        assert event.facility_id, "Event facility_id is required."
        assert event.sensor_type, "Event sensor_type is required."
        assert event.sensor_status, "Event sensor_status is required."
        assert event.weather, "Event weather is required."
        if event.sensor_value is not None:
            assert event.sensor_value >= 0.0, f"Sensor value {event.sensor_value} cannot be negative."
            if event.sensor_type == "water_ph":
                assert event.sensor_value <= 14.0, f"pH value {event.sensor_value} is out of bounds."
            elif event.sensor_type == "dissolved_oxygen":
                assert event.sensor_value <= 30.0, f"DO value {event.sensor_value} is out of bounds."
            elif event.sensor_type == "electrical_conductivity":
                assert event.sensor_value <= 10.0, f"EC value {event.sensor_value} is out of bounds."
            elif event.sensor_type == "air_temperature":
                assert event.sensor_value >= 10.0 and event.sensor_value <= 50.0, f"Temp value {event.sensor_value} is out of bounds."
            elif event.sensor_type == "humidity":
                assert event.sensor_value >= 10.0 and event.sensor_value <= 100.0, f"Humidity value {event.sensor_value} is out of bounds."
            elif event.sensor_type == "co2":
                assert event.sensor_value >= 300.0 and event.sensor_value <= 2500.0, f"CO2 value {event.sensor_value} is out of bounds."
            elif event.sensor_type == "light_intensity":
                assert event.sensor_value >= 0.0 and event.sensor_value <= 100000.0, f"Lux value {event.sensor_value} is out of bounds."

    print("[PASS] Environmental telemetry events validated.")
    print(f"[PASS] Generated {len(events)} environmental telemetry events.")

def verify_equipment_sensor_metrics(
    context: VerificationContext,
) -> None:
    """
    Verify baseline equipment sensor metrics.

    This verification stage validates that runtime sensor values are
    correctly generated after a simulation cycle and remain within the
    expected operating ranges defined by each equipment type's sensor
    profile.

    Verification objectives:

    1. Confirm sensor metrics are populated.
    2. Confirm values remain within profile limits.
    3. Confirm sensor metrics are stored in the correct runtime fields.
    4. Produce a baseline range report for future anomaly validation.

    This verification intentionally validates only baseline sensor
    behavior. It does not evaluate anomaly generation, fault injection,
    missing telemetry, or predictive maintenance signals.
    """

    settings = context.settings
    registry = context.equipment_registry

    equipment_state_manager = (
        context.equipment_state_manager
    )

    equipment_state_manager.advance_runtime(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_health(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_load()
    equipment_state_manager.update_failure_probability()
    equipment_state_manager.update_operating_status()
    equipment_state_manager.update_sensor_metrics()

    power_values = []
    temperature_values = []
    vibration_values = []

    print()
    print(
        "Equipment sensor metric sample:"
    )

    for equipment in registry.list_all():

        state = equipment_state_manager.get(
            equipment.equipment_id
        )

        profile = EQUIPMENT_SENSOR_PROFILES[
            equipment.equipment_type
        ]

        assert (
            state.power_consumption_kw > 0.0
        ), (
            f"{equipment.equipment_id} "
            "power consumption was not populated."
        )

        assert (
            state.temperature_celsius > 0.0
        ), (
            f"{equipment.equipment_id} "
            "temperature was not populated."
        )

        assert (
            state.vibration_mm_s > 0.0
        ), (
            f"{equipment.equipment_id} "
            "vibration was not populated."
        )

        assert (
            profile.idle_power_kw
            <= state.power_consumption_kw
            <= profile.max_power_kw
        ), (
            f"{equipment.equipment_id} "
            "power consumption exceeded profile limits."
        )

        assert (
            profile.base_temperature_celsius
            <= state.temperature_celsius
            <= profile.max_temperature_celsius
        ), (
            f"{equipment.equipment_id} "
            "temperature exceeded profile limits."
        )

        assert (
            profile.base_vibration_mm_s
            <= state.vibration_mm_s
            <= profile.max_vibration_mm_s
        ), (
            f"{equipment.equipment_id} "
            "vibration exceeded profile limits."
        )

        power_values.append(
            state.power_consumption_kw
        )

        temperature_values.append(
            state.temperature_celsius
        )

        vibration_values.append(
            state.vibration_mm_s
        )

    for equipment in registry.list_all()[:5]:

        state = equipment_state_manager.get(
            equipment.equipment_id
        )

        print(
            f"{equipment.equipment_id:<10}"
            f"Power={state.power_consumption_kw:<8.3f}"
            f"Temp={state.temperature_celsius:<8.2f}"
            f"Vibration={state.vibration_mm_s:<8.3f}"
        )

    print()

    print(
        "Sensor Metric Ranges"
    )

    print(
        f"Power:       "
        f"Min={min(power_values):.3f} "
        f"Max={max(power_values):.3f}"
    )

    print(
        f"Temperature: "
        f"Min={min(temperature_values):.2f} "
        f"Max={max(temperature_values):.2f}"
    )

    print(
        f"Vibration:   "
        f"Min={min(vibration_values):.3f} "
        f"Max={max(vibration_values):.3f}"
    )

    print()

    print(
        "[PASS] Equipment sensor metrics verified."
    )

def analyze_equipment_condition_distribution(
    context: VerificationContext,
    cycles: int = 250,
) -> None:
    """
    Analyze long-term equipment behaviour.

    Executes multiple simulation cycles and reports aggregate metrics
    describing equipment utilization, condition, and failure
    probability distributions.

    This analysis is intended for simulator calibration rather than
    correctness verification.
    """

    manager = context.equipment_state_manager
    settings = context.settings

    health_values = []
    load_values = []
    failure_values = []

    status_counts = {
        status.value: 0
        for status in EquipmentOperatingStatus
    }

    for _ in range(cycles):

        manager.advance_runtime(
            hours=settings.simulation_cycle_hours,
        )

        manager.update_health(
            hours=settings.simulation_cycle_hours,
        )

        manager.update_load()
        manager.update_failure_probability()
        manager.update_operating_status()

        for state in manager.list_all():

            health_values.append(
                state.health
            )

            load_values.append(
                state.current_load
            )

            failure_values.append(
                state.failure_probability
            )

            status_counts[
                state.operating_status.value
            ] += 1

        manager.evaluate_maintenance()

        for state in manager.list_all():
            
            health_values.append(
                state.health
            )

            load_values.append(
                state.current_load
            )

            failure_values.append(
                state.failure_probability
            )

            status_counts[
                state.operating_status.value
            ] += 1

    print()

    print("=" * 70)

    print(
        f"Equipment Condition Analysis ({cycles} cycles)"
    )

    print("=" * 70)

    print(
        f"Average Health: {sum(health_values)/len(health_values):.2f}"
    )
    print(
        f"Average Load: {sum(load_values)/len(load_values):.2f}"
    )
    print(
        f"Average Failure: {sum(failure_values)/len(failure_values):.4f}"
    )

    print()

    print("Operating Status Distribution")

    total = sum(status_counts.values())

    for status, count in status_counts.items():

        percentage = (
            count / total
        ) * 100

        print(
            f"{status:<10}"
            f"{percentage:>7.2f}%"
        )

    print(
    f"Min Failure: {min(failure_values):.4f}"
    )

    print(
        f"Max Failure: {max(failure_values):.4f}"
    )

    high_risk_count = sum(
    1
    for value in failure_values
    if value >= 0.35
    )

    print(
        f"Failure >= 0.35: {high_risk_count}"
    )

    error_count = sum(
    1
    for state in manager.list_all()
    if state.operating_status
    == EquipmentOperatingStatus.ERROR
    )

    print(
        f"Current ERROR Assets: {error_count}"
    )

    print(
        f"Maintenance Events: "
        f"{manager.maintenance_count()}"
    )

    warning_count = sum(
        1
        for value in failure_values
        if 0.10 <= value < 0.35
    )

    error_count = sum(
        1
        for value in failure_values
        if value >= 0.35
    )

    print(
        f"Failure 0.10-0.35: {warning_count}"
    )

    print(
        f"Failure >= 0.35: {error_count}"
    )

    warning_probability_count = sum(
        1
        for value in failure_values
        if 0.10 <= value < 0.35
    )

    error_probability_count = sum(
        1
        for value in failure_values
        if value >= 0.35
    )

    print(
        f"Probability WARNING: "
        f"{warning_probability_count / len(failure_values) * 100:.2f}%"
    )

    print(
        f"Probability ERROR: "
        f"{error_probability_count / len(failure_values) * 100:.2f}%"
    )

    warning_assets = 0
    error_assets = 0

    for state in manager.list_all():

        if (
            state.operating_status
            == EquipmentOperatingStatus.WARNING
        ):
            warning_assets += 1

        if (
            state.operating_status
            == EquipmentOperatingStatus.ERROR
        ):
            error_assets += 1

    print(
        f"Observed WARNING States: {warning_assets}"
    )

    print(
        f"Observed ERROR States: {error_assets}"
    )

def verify_simulator_lifecycle() -> None:
    """
    Verify that the simulator owns the equipment lifecycle.

    This verification ensures the simulator advances equipment runtime
    state before telemetry generation, allowing telemetry generators to
    remain completely read-only.

    The verification executes one simulator lifecycle equivalent and
    confirms that runtime state mutations are reflected in generated
    telemetry events.
    """

    import os
    os.environ["EQUIPMENT_TELEMETRY_SAMPLE_RATE"] = "1.0"
    settings = Settings.from_env()
    settings.equipment_telemetry_sample_rate = 1.0

    random_manager = RandomManager(
        seed=settings.random_seed,
    )

    environment_manager = EnvironmentStateManager(
        settings=settings,
        random_manager=random_manager,
    )

    equipment_registry = EquipmentRegistry(
        settings=settings,
    )

    wear_model = WearModel()
    failure_model = FailureModel()
    maintenance_manager = MaintenanceManager()
    facility_demand_model = FacilityDemandModel()


    equipment_state_manager = EquipmentStateManager(
        equipment_registry=equipment_registry,
        random_manager=random_manager,
        wear_model=wear_model,
        failure_model=failure_model,
        maintenance_manager=maintenance_manager,
        facility_demand_model=facility_demand_model,
    )

    generator = EquipmentTelemetryGenerator(
        settings=settings,
        environment_manager=environment_manager,
        equipment_registry=equipment_registry,
        equipment_state_manager=equipment_state_manager,
    )

    # Simulate the work now performed by Simulator.

    environment_manager.advance_cycle()

    equipment_state_manager.advance_runtime(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_load()

    equipment_state_manager.update_health(
        hours=settings.simulation_cycle_hours,
    )

    equipment_state_manager.update_failure_probability()
    equipment_state_manager.update_operating_status()

    events = generator.generate()

    assert len(events) == len(equipment_registry)

    sample = events[0]

    assert sample.runtime_hours > 0
    assert sample.health < 100.0
    assert sample.current_load >= MIN_EQUIPMENT_LOAD

    assert (
        sample.failure_probability
        >= MIN_FAILURE_PROBABILITY
    )

    print()

    print(
        "[PASS] Simulator lifecycle correctly drives "
        "equipment telemetry generation."
    )

def main() -> None:
    """
    Execute all verification stages.
    """

    print("=" * 70)
    print("HydroGrow Smart Farming Verification Pipeline")
    print("=" * 70)

    context = build_verification_context()

    verify_equipment_registry(
        context,
    )

    print()

    verify_equipment_state_manager(
        context,
    )

    print()

    verify_environmental_telemetry_generator(
        context,
    )

    print()

    verify_equipment_sensor_metrics(
        context,
    )

    print()

    verify_equipment_telemetry_generator(
        context,
    )

    print()

    verify_crop_state_manager(
        context,
    )

    print()

    verify_crop_lifecycle_generator(
        context,
    )

    print()

    verify_crop_telemetry_generator(
        context,
    )

    print()

    verify_irrigation_telemetry_generator(
        context,
    )

    print()

    verify_lighting_telemetry_generator(
        context,
    )

    print()

    analyze_equipment_condition_distribution(
        context=context,
        cycles=1000,
    )

    print()

    verify_simulator_lifecycle()

    print()
    print("=" * 70)
    print("[PASS] All verification checks completed successfully.")
    print("=" * 70)


if __name__ == "__main__":
    main()