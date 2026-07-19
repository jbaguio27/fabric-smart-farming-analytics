"""
Crop simulation configuration.

This module defines the immutable crop profiles used by the HydroGrow
Smart Farming Simulator.

The values in this module represent business configuration rather than
runtime state. They describe the biological characteristics of each crop
supported by the simulator and are consumed by the CropProfileRegistry.

Simulation logic must never be implemented here.
"""

from typing import Final
from smart_farming.models import CropGrowthProfile

# ============================================================================
# Lifecycle
# ============================================================================

EVENT_TYPE_CROP_LIFECYCLE: Final[str] = "CropLifecycleEvent"
CROP_GROWTH_PROFILES: Final[dict[str, CropGrowthProfile]] = {
    "butterhead_lettuce": CropGrowthProfile(
        crop_type="Butterhead Lettuce",
        germination_days=4,
        seedling_days=7,
        vegetative_days=24,
        maturity_days=35,
        optimal_temperature_celsius=22.0,
        optimal_humidity_percent=65.0,
        optimal_ph=6.0,
        optimal_ec=1.8,
    ),
    "batavia_lettuce": CropGrowthProfile(
        crop_type="Batavia Lettuce",
        germination_days=4,
        seedling_days=7,
        vegetative_days=26,
        maturity_days=38,
        optimal_temperature_celsius=21.5,
        optimal_humidity_percent=65.0,
        optimal_ph=6.0,
        optimal_ec=1.9,
    ),
    "kale": CropGrowthProfile(
        crop_type="Kale",
        germination_days=5,
        seedling_days=8,
        vegetative_days=32,
        maturity_days=45,
        optimal_temperature_celsius=20.0,
        optimal_humidity_percent=60.0,
        optimal_ph=6.2,
        optimal_ec=2.2,
    ),
    "spinach": CropGrowthProfile(
        crop_type="Spinach",
        germination_days=5,
        seedling_days=7,
        vegetative_days=23,
        maturity_days=35,
        optimal_temperature_celsius=19.0,
        optimal_humidity_percent=65.0,
        optimal_ph=6.3,
        optimal_ec=1.8,
    ),
    "arugula": CropGrowthProfile(
        crop_type="Arugula",
        germination_days=4,
        seedling_days=6,
        vegetative_days=20,
        maturity_days=30,
        optimal_temperature_celsius=20.0,
        optimal_humidity_percent=60.0,
        optimal_ph=6.1,
        optimal_ec=1.7,
    ),
    "basil": CropGrowthProfile(
        crop_type="Genovese Basil",
        germination_days=5,
        seedling_days=8,
        vegetative_days=27,
        maturity_days=40,
        optimal_temperature_celsius=24.0,
        optimal_humidity_percent=65.0,
        optimal_ph=6.0,
        optimal_ec=2.0,
    ),
    "cilantro": CropGrowthProfile(
        crop_type="Cilantro",
        germination_days=7,
        seedling_days=8,
        vegetative_days=25,
        maturity_days=40,
        optimal_temperature_celsius=20.0,
        optimal_humidity_percent=60.0,
        optimal_ph=6.3,
        optimal_ec=1.8,
    ),
    "parsley": CropGrowthProfile(
        crop_type="Parsley",
        germination_days=10,
        seedling_days=10,
        vegetative_days=35,
        maturity_days=55,
        optimal_temperature_celsius=20.0,
        optimal_humidity_percent=65.0,
        optimal_ph=6.2,
        optimal_ec=1.9,
    ),
    "microgreens": CropGrowthProfile(
        crop_type="Microgreens",
        germination_days=2,
        seedling_days=3,
        vegetative_days=5,
        maturity_days=10,
        optimal_temperature_celsius=22.0,
        optimal_humidity_percent=60.0,
        optimal_ph=6.0,
        optimal_ec=1.2,
    ),
    "strawberry": CropGrowthProfile(
        crop_type="Strawberry",
        germination_days=8,
        seedling_days=14,
        vegetative_days=45,
        maturity_days=90,
        optimal_temperature_celsius=19.0,
        optimal_humidity_percent=70.0,
        optimal_ph=5.8,
        optimal_ec=2.2,
    ),
}

# ============================================================================
# Health
# ============================================================================

MAX_HEALTH_SCORE = 100.0

# ============================================================================
# Growth Model
# ============================================================================

IDEAL_GROWTH_TEMPERATURE_C = 22.0
IDEAL_GROWTH_HUMIDITY_PERCENT = 65.0

TEMPERATURE_GROWTH_TOLERANCE_C = 10.0
HUMIDITY_GROWTH_TOLERANCE_PERCENT = 25.0

# ============================================================================
# Biomass Model
# ============================================================================

BIOMASS_GROWTH_MULTIPLIER = 10.0

# ============================================================================
# Water Uptake Model
# ============================================================================

WATER_UPTAKE_PER_GRAM_BIOMASS = 0.002

# ============================================================================
# Crop Lifecycle Stages
# ============================================================================

CROP_STAGE_GERMINATION: Final[str] = "GERMINATION"

CROP_STAGE_SEEDLING: Final[str] = "SEEDLING"

CROP_STAGE_VEGETATIVE: Final[str] = "VEGETATIVE"

CROP_STAGE_MATURE: Final[str] = "MATURE"

CROP_STAGE_HARVESTED: Final[str] = "HARVESTED"


CROP_LIFECYCLE_STAGES: Final[tuple[str, ...]] = (
    CROP_STAGE_GERMINATION,
    CROP_STAGE_SEEDLING,
    CROP_STAGE_VEGETATIVE,
    CROP_STAGE_MATURE,
    CROP_STAGE_HARVESTED,
)


# ============================================================================
# Lifecycle Progression
# ============================================================================

NEXT_CROP_STAGE: Final[dict[str, str | None]] = {
    CROP_STAGE_GERMINATION: CROP_STAGE_SEEDLING,
    CROP_STAGE_SEEDLING: CROP_STAGE_VEGETATIVE,
    CROP_STAGE_VEGETATIVE: CROP_STAGE_MATURE,
    CROP_STAGE_MATURE: CROP_STAGE_HARVESTED,
    CROP_STAGE_HARVESTED: None,
}

# ============================================================================
# Air Environment
# ============================================================================

DEFAULT_AIR_TEMPERATURE_C = 22.0
DEFAULT_RELATIVE_HUMIDITY_PERCENT = 65.0

# ============================================================================
# Hydroponic Solution
# ============================================================================

DEFAULT_WATER_PH = 6.0
DEFAULT_ELECTRICAL_CONDUCTIVITY = 1.8

# ============================================================================
# Environmental Variation
# ============================================================================

AIR_TEMPERATURE_VARIATION_C = 0.20

HUMIDITY_VARIATION_PERCENT = 0.75

WATER_PH_VARIATION = 0.03

EC_VARIATION = 0.02
