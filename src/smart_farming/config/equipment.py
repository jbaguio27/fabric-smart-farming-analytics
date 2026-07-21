"""
Equipment configuration.

This module contains all immutable configuration required by the
equipment subsystem.

It serves as the single source of truth for:

- Equipment asset catalog
- Runtime operating limits
- Failure thresholds
- Load simulation configuration
- Facility demand configuration
- Sensor simulation configuration
- Equipment load profiles
- Equipment sensor profiles

Simulation logic must never be implemented here.
"""

# =====================================================================
# Equipment Asset Catalog
# =====================================================================

EQUIPMENT_ID_PREFIX = "EQ"

DEFAULT_GROWING_ZONES_PER_FACILITY = 10


EQUIPMENT_TYPES = (
    "water_pump",
    "hvac",
    "led_panel",
    "nutrient_pump",
    "ventilation_fan",
    "co2_injector",
)

FACILITY_EQUIPMENT_TYPES = (
    "ro_system",
    "plc_controller",
    "ups_system",
    "edge_gateway",
)

EQUIPMENT_MANUFACTURERS = {
    "water_pump": "Grundfos",
    "hvac": "Daikin",
    "led_panel": "Philips",
    "nutrient_pump": "Netafim",
    "ventilation_fan": "ebm-papst",
    "co2_injector": "Atlas Copco",
    "ro_system": "Suez",
    "plc_controller": "Siemens",
    "ups_system": "APC",
    "edge_gateway": "Advantech",
}

EQUIPMENT_MODELS = {
    "water_pump": "CRN10",
    "hvac": "VRV X",
    "led_panel": "GreenPower LED",
    "nutrient_pump": "NMC Pro",
    "ventilation_fan": "AxiBlade",
    "co2_injector": "GA11",
    "ro_system": "PRO-RO",
    "plc_controller": "S7-1500",
    "ups_system": "Smart-UPS",
    "edge_gateway": "UNO-2484G",
}
