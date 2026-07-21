# Philippine Facility Infrastructure & Regional Configurations

**Document Owner:** Data Engineering & IoT Architecture Team  
**Version:** 3.0  
**Status:** Approved  
**Last Updated:** 2026-07-21  

---

## Executive Summary

The Microsoft Fabric Smart Farming Analytics Platform simulates an enterprise network of **8 smart farming facilities** distributed across key agricultural regions in the Philippines.

This document details the facility infrastructure components, domain configuration layout, and regional facility profile specifications.

---

## Facility Infrastructure Architecture

To dynamically instantiate and manage facilities, the codebase incorporates the following architectural components:

```text
src/smart_farming/
├── config/                      # Domain-split configuration constants
│   ├── facility.py              # Facility operational defaults & capacity constants
│   ├── weather.py               # Regional weather & ambient baseline configs
│   ├── soil.py                  # Soil substrate, moisture & pH baselines
│   ├── livestock.py             # Livestock & poultry climate parameters
│   ├── crop.py                  # Crop growth & biomass constants
│   ├── environment.py           # Climate control bounds
│   ├── equipment.py             # Equipment asset definitions
│   ├── equipment_runtime.py     # Wear & failure probability constants
│   ├── irrigation.py            # Water & nutrient dosing thresholds
│   ├── maintenance.py          # Work order & technician rosters
│   └── settings.py              # Environment settings loader
│
├── schemas/                     # Schema profiles & registries
│   ├── facility_profiles.py     # [STRICT LOCATION] Facility profiles & registry
│   ├── crop_growth_profile.py
│   ├── equipment_load_profile.py
│   └── equipment_sensor_profile.py
│
├── environment/                 # State managers
│   ├── facility_state_manager.py # [FACILITY STATE] Tracks facility operational state
│   ├── crop_state_manager.py
│   ├── equipment_state_manager.py
│   └── growing_environment_state_manager.py
│
├── generators/                  # Telemetry event generators
│   ├── facility_generator.py    # [FACILITY GENERATOR] Emits facility telemetry events
│   ├── crop_lifecycle_generator.py
│   ├── crop_telemetry_generator.py
│   ├── environmental_telemetry_generator.py
│   ├── equipment_telemetry_generator.py
│   ├── irrigation_telemetry_generator.py
│   ├── lighting_telemetry_generator.py
│   └── maintenance_event_generator.py
│
└── models/                      # Telemetry event dataclasses
    ├── facility_event.py        # [FACILITY MODEL] Facility telemetry event dataclass
    ├── base_event.py
    └── ...
```

---

## Philippine Facility Directory

| Facility ID | Facility Name | Location / Region | Domain Focus | Target Temp (°C) | Target Humidity (%) | Target Soil/pH | Raw Ingestion Anomaly Profile (Bronze Layer) |
|-------------|---------------|-------------------|--------------|------------------|---------------------|----------------|----------------------------------------------|
| **FAC-001** | Benguet High-Altitude Strawberries & Greens | La Trinidad, Benguet (CAR) | Highland Crops & Strawberries | 18.0°C | 75% | pH 5.80 | Mountain morning fog power dips, duplicate events (~3%). |
| **FAC-002** | Tagaytay Ridge Smart Greenhouse & Nursery | Tagaytay City, Cavite (Region IV-A) | Culinary Herbs & Sub-Tropical Nursery | 22.0°C | 70% | pH 6.00 | Ridge cloud condensation drift, empty string payloads (`""`). |
| **FAC-003** | Davao Cacao & Vertical Agro-Plantation | Davao City, Davao del Sur (Region XI) | Premium Cacao & Vertical Asian Greens | 25.0°C | 80% | pH 6.50 | Afternoon HVAC thermal spikes (`temperature = 9999.99`). |
| **FAC-004** | Bukidnon Cattle & High-Altitude Agro-Ranch | Manolo Fortich, Bukidnon (Region X) | Livestock Environmental & Herbs | 20.0°C | 72% | pH 5.90 | Uncalibrated pH probe sub-zero corrupted values (`-999.0`). |
| **FAC-005** | Laguna Technopark Smart Hydro-Facility | Calamba City, Laguna (Region IV-A) | Commercial Romaine & Tomatoes | 24.0°C | 68% | pH 6.00 | Omitted payload keys (`null`), lowercase string casing (`fac-005`). |
| **FAC-006** | Pampanga Lowland Poultry & Agri-Center | San Fernando, Pampanga (Region III) | Poultry Climate & Lowland Veggies | 27.0°C | 72% | pH 6.20 | Gateway latency out-of-order timestamps (15–120 min delay). |
| **FAC-007** | Western Visayas Rice & Coastal Aquaculture Hub | Iloilo City, Iloilo (Region VI) | Rice Paddy Irrigation & Aquaponics | 26.0°C | 75% | pH 6.80 | Mixed timestamp formats (ISO 8601 vs. Unix Epoch integers). |
| **FAC-008** | Cagayan Valley Smart Agro-Research Station | Tuguegarao City, Cagayan (Region II) | Hybrid Grain Seeds & Agro-Forestry | 28.0°C | 65% | pH 6.15 | Serial buffer string typos (`operating_status: "ONLNE"`), duplicate bursts. |

---

## Dynamic Facility Generator Specification (`facility_generator.py`)

The `FacilityGenerator` reads registered profiles from `schemas/facility_profiles.py` and current operational states from `FacilityStateManager` to emit `facility.telemetry` events containing:

1. **Facility Metadata**: `facility_id`, `facility_name`, `location`, `region`, `domain_focus`.
2. **Environmental & Soil Metrics**: Aggregated ambient temperature, humidity, regional weather condition, soil moisture, and substrate pH.
3. **Operational Metrics**: Total power draw (kW), total water delivered (Liters), active zone counts, and online/warning/error equipment breakdown.
4. **Data Quality Anomalies**: Intentional raw noise (nulls, typos, epoch timestamps, corrupted bounds) injected per facility anomaly profile prior to Fabric Eventstream ingestion.
