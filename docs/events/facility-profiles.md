# Comprehensive Hydroponics Vertical Farming Architecture & Package Integration

**Document Owner:** Hydroponics IoT, Systems Architecture & Data Engineering Team  
**Version:** 7.0 (Complete System Package Integration)  
**Status:** Approved  
**Last Updated:** 2026-07-21  

---

## Executive Summary

The Microsoft Fabric Smart Farming Analytics Platform focuses **exclusively on multi-facility Hydroponics Vertical Farming systems**.

This document maps all core Python packages (`schemas`, `services`, `validation`, `monitoring`, `producer`, `config`, `environment`, `generators`, `models`) to their role in driving the simulator loop, paired equipment-maintenance lifecycle, biological crop growth, and raw dirty data streaming for Microsoft Fabric Medallion data cleaning.

---

## Integrated Package Architecture Layout (`src/smart_farming`)

```text
src/smart_farming/
├── config/                               # Hydroponics Subsystem Configuration Constants
│   ├── crop.py                           # [CROP PROFILES] Biological growth profiles (CROP_GROWTH_PROFILES)
│   ├── facility.py                       # Hardcoded PHILIPPINE_FACILITY_PROFILES dictionary data
│   ├── nutrient_solution_domain.py       # pH (5.5-6.5), EC (1.2-2.4 mS/cm), Dissolved Oxygen, N-P-K dosing bounds
│   ├── hvac_climate_domain.py            # Air temp, relative humidity, CO2 enrichment (800-1200ppm), CFM airflow
│   ├── led_lighting_domain.py            # PPFD (200-600 µmol/m²/s), DLI (14-22 mol/m²/d), photoperiod hours
│   ├── water_recirculation_domain.py     # Reservoir levels, GPM flow rates, pump pressure, chiller water temp
│   ├── equipment_maintenance_domain.py   # Equipment wear rates, load profiles, failure curves
│   ├── constants.py                      # Global prefixes (FAC-, ZONE-, EQ-)
│   └── settings.py                       # Environment settings loader
│
├── schemas/                              # Structural Configuration Schemas
│   ├── facility_profiles.py              # FacilityProfile & ZoneMicroLocation dataclasses
│   ├── crop_growth_profile.py            # CropGrowthProfile dataclass
│   ├── equipment_load_profile.py          # EquipmentLoadProfile dataclass
│   └── equipment_sensor_profile.py        # EquipmentSensorProfile dataclass
│
├── services/                             # Physics, Mechanical & Wear Models
│   ├── wear_model.py                     # Calculates equipment health wear per cycle based on load & hours
│   ├── failure_model.py                  # Calculates failure probability curves based on accumulated wear
│   ├── maintenance_manager.py            # Drives work order triggers, technician assignment & repair resets
│   └── facility_demand_model.py          # Computes diurnal resource demand multipliers (power & water)
│
├── validation/                           # Pre-Dispatch Structural Sanity Validators
│   ├── telemetry_validator.py            # Validates structural fields of telemetry events without filtering dirty data
│   ├── crop_lifecycle_validator.py       # Structural validation for crop stage transitions
│   └── irrigation_telemetry_validator.py # Structural validation for irrigation & dosing events
│
├── monitoring/                           # Application Health & Logging
│   └── logger.py                         # Structured logging, execution cycle tracing & metrics logging
│
├── environment/                          # State Managers (Paired Equipment & Maintenance)
│   ├── facility_state_manager.py          # Tracks facility operational state & aggregated metrics
│   ├── equipment_registry.py              # Inventory lookup linking EQ-00001 to FACILITY_ID + ZONE_ID
│   ├── equipment_state_manager.py         # Tracks health degradation, load, runtime hours via services/
│   ├── maintenance_state_manager.py       # Tracks active work orders, technicians, repair cycles
│   ├── crop_state_manager.py              # Biological crop growth & stage progression (hooks to crop.py)
│   ├── growing_environment_state_manager.py # Zone climate state tracking
│   ├── irrigation_state_manager.py        # Water recirculation & dosing state
│   └── lighting_state_manager.py          # LED array intensity & DLI tracking
│
├── generators/                           # Telemetry Event Generators
│   ├── facility_generator.py             # Instantiates & emits vertical farm operational telemetry
│   ├── equipment_telemetry_generator.py   # Emits hardware health & wear telemetry
│   ├── maintenance_event_generator.py     # Emits work order & repair activity events
│   ├── crop_lifecycle_generator.py
│   ├── crop_telemetry_generator.py
│   ├── environmental_telemetry_generator.py
│   ├── irrigation_telemetry_generator.py
│   └── lighting_telemetry_generator.py
│
├── producer/                             # Event Orchestration & Raw Anomaly Injection
│   ├── simulator.py                      # Master simulation loop driving all state managers
│   ├── event_dispatcher.py               # Serializes payloads and posts HTTP batches to Eventstream
│   └── anomaly_injector.py               # Injects raw data quality defects (pH drift, nulls, typos, duplicates)
│
└── main.py                               # Application entry point & composition root
```

---

## Equipment & Maintenance Pairing Model (`services/`)

Equipment tracking and maintenance scheduling are tightly coupled throughout the simulation lifecycle using `services/`:

```text
+-----------------------------------------------------------------------------------+
|                        1. Equipment Inventory & Asset Registry                    |
|  (Each asset assigned to FACILITY_ID + ZONE_ID: e.g. EQ-00001 Water Pump FAC-001) |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|               2. Wear & Failure Models (wear_model.py & failure_model.py)          |
|  (EquipmentStateManager calculates runtime_hours, health degradation, load,       |
|   and failure_probability using WearModel & FailureModel)                          |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|             3. Predictive Maintenance Manager (services/maintenance_manager.py)    |
|  (When Health < 85% or Failure Prob > 10%, MaintenanceStateManager generates a    |
|   WorkOrder: WORK-00042 assigned to Technician, setting state to PENDING/ACTIVE)  |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|                   4. Maintenance Completion & Equipment Reset                     |
|  (Once remaining_duration_minutes reaches 0, Equipment Health resets to 100%,      |
|   operating_status resets to ONLINE, and WorkOrder is marked COMPLETED)           |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
|              5. Raw Dirty Telemetry & Maintenance Anomaly Injection                |
|  (DataAnomalyInjector introduces typos in work_status, duplicate work orders,     |
|   delayed repair timestamps, null technician notes, and mismatched equipment IDs)  |
+-----------------------------------------------------------------------------------+
```

---

## Philippine Hydroponics Vertical Farm Directory & Crop Allocation

Each Philippine facility maps internal micro-locations (zones/racks/chambers) to dominant crops in `CROP_GROWTH_PROFILES` (`crop.py`) and installed equipment sets:

| Facility ID | Facility Name & Region | Zone ID | Zone Micro-Location Name | Dominant Crop Key | Dominant Crop Name | Equipment Set Installed |
|-------------|------------------------|---------|-------------------------------|-------------------|--------------------|-------------------------|
| **FAC-001** | Benguet Highland Strawberries Vertical Farm (La Trinidad, Benguet) | `ZONE-001` | Top-Tier Highland LED Canopy | `strawberry` | Strawberry | LED Array, Water Pump, HVAC Blower |
| | | `ZONE-002` | Mid-Tier NFT Rack Alpha | `butterhead_lettuce` | Butterhead Lettuce | Dosing Valve, Chiller |
| | | `ZONE-003` | Lower-Tier High-Humidity Bed | `kale` | Kale | CO2 Injector, Water Pump |
| **FAC-002** | Tagaytay Ridge Hydroponics Nursery (Tagaytay City, Cavite) | `ZONE-001` | Ridge Micro-Climate Nursery Chamber | `basil` | Genovese Basil | LED Array, Dosing Valve |
| | | `ZONE-002` | Vertical NFT Rack Beta | `batavia_lettuce` | Batavia Lettuce | Water Pump, HVAC Blower |
| | | `ZONE-003` | Controlled Herb Tier | `arugula` | Arugula | Chiller, CO2 Injector |
| **FAC-003** | Metro Manila Rooftop Vertical Hydro-Farm (BGC, Taguig City, NCR) | `ZONE-001` | Top-Tier High PPFD Canopy | `butterhead_lettuce` | Butterhead Lettuce | LED Array, HVAC Blower |
| | | `ZONE-002` | BGC Urban Microgreen Chamber | `microgreens` | Microgreens | Water Pump, Dosing Valve |
| | | `ZONE-003` | NFT High-Density Rack | `spinach` | Spinach | Chiller, CO2 Injector |
| **FAC-004** | Davao City Indoor Greens Vertical Facility (Davao City, Davao del Sur) | `ZONE-001` | High-Tower Aeroponic Array A | `spinach` | Spinach | Aeroponic Pump, HVAC Blower |
| | | `ZONE-002` | Sub-Tropical Vertical Chamber | `kale` | Kale | LED Array, Dosing Valve |
| | | `ZONE-003` | DWC Nutrient Tank 1 | `arugula` | Arugula | Chiller, CO2 Injector |
| **FAC-005** | Laguna Technopark Hydroponic Plant Factory (Calamba City, Laguna) | `ZONE-001` | Industrial DWC Vine System | `basil` | Genovese Basil | Industrial DWC Pump, Chiller |
| | | `ZONE-002` | NFT Commercial Rack Line 1 | `butterhead_lettuce` | Butterhead Lettuce | LED Array, Dosing Valve |
| | | `ZONE-003` | High-Output Herb Tier | `parsley` | Parsley | HVAC Blower, CO2 Injector |
| **FAC-006** | Cebu Urban Vertical Greens Hub (Cebu IT Park, Cebu City) | `ZONE-001` | IT Park Smart LED Canopy | `batavia_lettuce` | Batavia Lettuce | LED Array, HVAC Blower |
| | | `ZONE-002` | Urban Vertical NFT Rack 2 | `cilantro` | Cilantro | Water Pump, Dosing Valve |
| | | `ZONE-003` | Aeroponic Herb Chamber | `arugula` | Arugula | Aeroponic Pump, Chiller |
| **FAC-007** | Clark Freeport Urban Hydroponic Complex (Clark Freeport, Pampanga) | `ZONE-001` | High-Capacity Aeroponic Tower A | `spinach` | Spinach | Aeroponic Tower Pump |
| | | `ZONE-002` | Controlled Photoperiod Module | `parsley` | Parsley | LED Array, CO2 Injector |
| | | `ZONE-003` | NFT Leafy Greens Tier | `butterhead_lettuce` | Butterhead Lettuce | Water Pump, Chiller |
| **FAC-008** | Iloilo City Microgreens Vertical Agro-Lab (Mandurriao, Iloilo City) | `ZONE-001` | Precision Microgreen Tray Module A | `microgreens` | Microgreens | Precision LED Module |
| | | `ZONE-002` | LED Agro-Research Chamber | `basil` | Genovese Basil | Dosing Valve, HVAC Blower |
| | | `ZONE-003` | High-Density Sprout Rack | `strawberry` | Strawberry | Water Pump, Chiller |

---

## Role of Pre-Dispatch Validation (`validation/`) vs Raw Anomaly Injection (`producer/`)

1. **`validation/` Package**:
   - `telemetry_validator.py`, `crop_lifecycle_validator.py`, `irrigation_telemetry_validator.py` perform structural checks (ensuring required schema keys exist, field types are compatible, payloads are non-empty).
   - *Crucial Rule*: Validation checks ensure structural sanity before payload dispatching without cleaning or stripping out raw telemetry defects (spikes, nulls, typos, out-of-order timestamps).

2. **`producer/anomaly_injector.py` Package**:
   - Intentionally injects real-world raw data quality defects into the JSON payload stream prior to Eventstream transmission.
   - Ensures that **Microsoft Fabric (Bronze to Silver Lakehouse)** receives realistic dirty data for testing PySpark deduplication, null imputation, timestamp standardization, and outlier handling.
