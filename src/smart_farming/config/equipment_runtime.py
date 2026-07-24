from typing import Final, Mapping
from smart_farming.schemas import (
    EquipmentLoadProfile,
    EquipmentSensorProfile,
)

# =====================================================================
# Runtime Limits
# =====================================================================

MIN_EQUIPMENT_LOAD = 0.0
MAX_EQUIPMENT_LOAD = 100.0

MIN_FAILURE_PROBABILITY = 0.0
MAX_FAILURE_PROBABILITY = 1.0

MAX_EQUIPMENT_HEALTH = 100.0
MIN_EQUIPMENT_HEALTH = 0.0

MIN_INITIAL_EQUIPMENT_HEALTH = 48.0
MAX_INITIAL_EQUIPMENT_HEALTH = 100.0

MAX_EQUIPMENT_RUNTIME_HOURS = 50000.0

MIN_SIMULATION_CYCLE_HOURS = 0.25

# =====================================================================
# Wear Model
# =====================================================================

HEALTH_DEGRADATION_PER_RUNTIME_HOUR = 0.025

HEALTHY_EQUIPMENT_THRESHOLD = 85.0

# =====================================================================
# Failure Thresholds
# =====================================================================

ONLINE_FAILURE_THRESHOLD = 0.20
WARNING_FAILURE_THRESHOLD = 0.50
ERROR_FAILURE_THRESHOLD = 0.80

MAX_LOAD_FAILURE_ADJUSTMENT = 0.20

# =====================================================================
# Load Simulation
# =====================================================================

NORMAL_OPERATING_LOAD_THRESHOLD = 70.0

MAX_LOAD_CHANGE_PER_CYCLE = 4.0

MAX_LOAD_VARIATION_PER_CYCLE = 2.0

# =====================================================================
# Facility Demand
# =====================================================================

DAYTIME_DEMAND_MULTIPLIER = 1.00

NIGHTTIME_DEMAND_MULTIPLIER = 0.65

HOURS_PER_DAY = 24

# =====================================================================
# Sensor Stress Model
# =====================================================================

SENSOR_POWER_HEALTH_STRESS_MULTIPLIER = 0.08

SENSOR_TEMPERATURE_HEALTH_STRESS_CELSIUS = 6.0
SENSOR_TEMPERATURE_FAILURE_STRESS_CELSIUS = 12.0
SENSOR_TEMPERATURE_VARIATION_CELSIUS = 0.40

SENSOR_VIBRATION_HEALTH_STRESS_MM_S = 1.50
SENSOR_VIBRATION_FAILURE_STRESS_MM_S = 2.50
SENSOR_VIBRATION_VARIATION_MM_S = 0.10

# =====================================================================
# Equipment Load Profiles
# =====================================================================

EQUIPMENT_LOAD_PROFILES: Final[
    Mapping[str, EquipmentLoadProfile]
] = {
    "water_pump": EquipmentLoadProfile(
        minimum=60.0,
        maximum=95.0,
        target=80.0,
        wear_multiplier=1.35,
        failure_multiplier=1.30,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.35,
        critical_factor_max=1.00,
    ),
    "nutrient_pump": EquipmentLoadProfile(
        minimum=45.0,
        maximum=85.0,
        target=65.0,
        wear_multiplier=1.15,
        failure_multiplier=1.15,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.35,
        critical_factor_max=1.00,
    ),
    "hvac": EquipmentLoadProfile(
        minimum=35.0,
        maximum=90.0,
        target=60.0,
        wear_multiplier=1.00,
        failure_multiplier=1.00,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.35,
        critical_factor_max=1.00,
    ),
    "ventilation_fan": EquipmentLoadProfile(
        minimum=25.0,
        maximum=75.0,
        target=45.0,
        wear_multiplier=0.80,
        failure_multiplier=0.80,
        normal_threshold=75.0,
        warning_threshold=95.0,
        moderate_factor_max=0.25,
        critical_factor_max=0.80,
    ),
    "led_panel": EquipmentLoadProfile(
        minimum=80.0,
        maximum=100.0,
        target=90.0,
        wear_multiplier=0.45,
        failure_multiplier=0.60,
        normal_threshold=80.0,
        warning_threshold=95.0,
        moderate_factor_max=0.20,
        critical_factor_max=0.60,
    ),
    "co2_injector": EquipmentLoadProfile(
        minimum=15.0,
        target=35.0,
        maximum=60.0,
        normal_threshold=45.0,
        warning_threshold=55.0,
        wear_multiplier=0.70,
        failure_multiplier=0.80,
        moderate_factor_max=0.20,
        critical_factor_max=0.35,
    ),
    "ro_system": EquipmentLoadProfile(
        minimum=50.0,
        maximum=90.0,
        target=75.0,
        wear_multiplier=0.90,
        failure_multiplier=0.90,
        normal_threshold=70.0,
        warning_threshold=90.0,
        moderate_factor_max=0.30,
        critical_factor_max=0.85,
    ),
    "plc_controller": EquipmentLoadProfile(
        minimum=95.0,
        maximum=100.0,
        target=98.0,
        wear_multiplier=0.20,
        failure_multiplier=0.15,
        normal_threshold=99.0,
        warning_threshold=99.9,
        moderate_factor_max=0.10,
        critical_factor_max=0.30,
    ),
    "ups_system": EquipmentLoadProfile(
        minimum=20.0,
        maximum=100.0,
        target=90.0,
        wear_multiplier=0.50,
        failure_multiplier=0.50,
        normal_threshold=85.0,
        warning_threshold=95.0,
        moderate_factor_max=0.15,
        critical_factor_max=0.50,
    ),
    "edge_gateway": EquipmentLoadProfile(
        minimum=90.0,
        maximum=100.0,
        target=95.0,
        wear_multiplier=0.30,
        failure_multiplier=0.25,
        normal_threshold=98.0,
        warning_threshold=99.5,
        moderate_factor_max=0.10,
        critical_factor_max=0.40,
    ),
}

# =====================================================================
# Equipment Sensor Profiles
# =====================================================================

EQUIPMENT_SENSOR_PROFILES: Final[
    Mapping[str, EquipmentSensorProfile]
] = {
    "water_pump": EquipmentSensorProfile(
        idle_power_kw=1.20,
        max_power_kw=4.80,
        base_temperature_celsius=32.0,
        max_temperature_celsius=72.0,
        base_vibration_mm_s=1.20,
        max_vibration_mm_s=5.80,
    ),
    "nutrient_pump": EquipmentSensorProfile(
        idle_power_kw=0.80,
        max_power_kw=3.20,
        base_temperature_celsius=30.0,
        max_temperature_celsius=66.0,
        base_vibration_mm_s=0.90,
        max_vibration_mm_s=4.80,
    ),
    "hvac": EquipmentSensorProfile(
        idle_power_kw=3.50,
        max_power_kw=18.0,
        base_temperature_celsius=36.0,
        max_temperature_celsius=82.0,
        base_vibration_mm_s=1.50,
        max_vibration_mm_s=6.50,
    ),
    "ventilation_fan": EquipmentSensorProfile(
        idle_power_kw=0.40,
        max_power_kw=2.20,
        base_temperature_celsius=28.0,
        max_temperature_celsius=58.0,
        base_vibration_mm_s=0.70,
        max_vibration_mm_s=4.20,
    ),
    "led_panel": EquipmentSensorProfile(
        idle_power_kw=0.60,
        max_power_kw=2.80,
        base_temperature_celsius=34.0,
        max_temperature_celsius=76.0,
        base_vibration_mm_s=0.05,
        max_vibration_mm_s=0.35,
    ),
    "co2_injector": EquipmentSensorProfile(
        idle_power_kw=0.30,
        max_power_kw=1.80,
        base_temperature_celsius=22.0,
        max_temperature_celsius=45.0,
        base_vibration_mm_s=0.10,
        max_vibration_mm_s=1.20,
    ),
    "ro_system": EquipmentSensorProfile(
        idle_power_kw=1.50,
        max_power_kw=5.50,
        base_temperature_celsius=25.0,
        max_temperature_celsius=55.0,
        base_vibration_mm_s=0.80,
        max_vibration_mm_s=3.50,
    ),
    "plc_controller": EquipmentSensorProfile(
        idle_power_kw=0.15,
        max_power_kw=0.25,
        base_temperature_celsius=24.0,
        max_temperature_celsius=42.0,
        base_vibration_mm_s=0.01,
        max_vibration_mm_s=0.05,
    ),
    "ups_system": EquipmentSensorProfile(
        idle_power_kw=0.20,
        max_power_kw=1.20,
        base_temperature_celsius=26.0,
        max_temperature_celsius=48.0,
        base_vibration_mm_s=0.02,
        max_vibration_mm_s=0.10,
    ),
    "edge_gateway": EquipmentSensorProfile(
        idle_power_kw=0.10,
        max_power_kw=0.20,
        base_temperature_celsius=28.0,
        max_temperature_celsius=46.0,
        base_vibration_mm_s=0.01,
        max_vibration_mm_s=0.05,
    ),
}
