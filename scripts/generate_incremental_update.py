"""
HydroGrow Smart Farming Analytics Platform - Incremental Batch Update Generator
Script: scripts/generate_incremental_update.py

Generates an incremental batch of operational data containing:
1. Multiple SCD Type 2 dimension updates (Facilities, Equipment, Zones).
2. Brand-new equipment asset additions.
3. Fresh 24-hour telemetry across all 12 platform streams.

When uploaded to OneLake, this triggers the incremental Delta MERGE in Gold,
automatically closing out old records (is_current = False) and creating new active records (is_current = True).
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Ensure src/ directory is on Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from smart_farming.config import Settings, PHILIPPINE_FACILITY_PROFILES
from smart_farming.environment import (
    CropProfileRegistry,
    CropRegistry,
    CropStateManager,
    EnvironmentStateManager,
    EquipmentRegistry,
    EquipmentStateManager,
    FacilityStateManager,
    GrowingEnvironmentStateManager,
    IrrigationStateManager,
    LightingStateManager,
    MaintenanceStateManager,
    CropDefinition,
)
from smart_farming.generators import (
    CropLifecycleGenerator,
    CropTelemetryGenerator,
    EnvironmentalTelemetryGenerator,
    EquipmentTelemetryGenerator,
    FacilityGenerator,
    IrrigationTelemetryGenerator,
    LightingTelemetryGenerator,
    MaintenanceEventGenerator,
)
from smart_farming.services import (
    FacilityDemandModel,
    FailureModel,
    MaintenanceManager,
    WearModel,
)
from smart_farming.utils import RandomManager


def make_uuidv5(stream: str, seed: str) -> str:
    """Generate deterministic UUIDv5 identity based on stream and seed string."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"hydrogrow.{stream}.{seed}"))


def run_incremental_generator(hours: int = 24, output_dir: str = "Files_Incremental") -> None:
    """
    Generates an incremental batch of telemetry with multiple SCD Type 2 dimension updates.
    """
    now_dt = datetime.now(timezone.utc).replace(microsecond=0)
    start_dt = now_dt - timedelta(hours=hours)

    print(f"[+] Starting HydroGrow Incremental Batch Generator...")
    print(f" [info] Incremental Time Window: [{start_dt.isoformat()}] to [{now_dt.isoformat()}] ({hours} Hours)")

    settings = Settings.from_env()
    random_manager = RandomManager(seed=101)

    # 1. Initialize Composition Root
    environment_manager = EnvironmentStateManager(settings=settings, random_manager=random_manager)
    equipment_registry = EquipmentRegistry(settings=settings)
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

    batch_counter = 100
    for facility_id, fac_profile in PHILIPPINE_FACILITY_PROFILES.items():
        for micro in fac_profile.micro_locations:
            crop_registry.register(
                CropDefinition(
                    crop_batch_id=f"BATCH-{batch_counter:05d}",
                    facility_id=facility_id,
                    zone_id=micro.zone_id,
                    crop_type=micro.dominant_crop_key,
                )
            )
            batch_counter += 1

    growing_environment_manager = GrowingEnvironmentStateManager(
        settings=settings, random_manager=random_manager, zone_count=settings.zone_count
    )
    irrigation_state_manager = IrrigationStateManager(
        zone_count=settings.zone_count, random_manager=random_manager
    )
    lighting_state_manager = LightingStateManager(settings=settings, zone_count=settings.zone_count)
    crop_state_manager = CropStateManager(
        settings=settings,
        crop_registry=crop_registry,
        crop_profile_registry=crop_profile_registry,
        growing_environment_manager=growing_environment_manager,
        random_manager=random_manager,
        irrigation_state_manager=irrigation_state_manager,
    )
    maintenance_state_manager = MaintenanceStateManager()
    facility_state_manager = FacilityStateManager(
        equipment_state_manager=equipment_state_manager, equipment_registry=equipment_registry
    )

    # Generators
    environmental_generator = EnvironmentalTelemetryGenerator(
        settings=settings, random_manager=random_manager, environment_manager=environment_manager
    )
    equipment_generator = EquipmentTelemetryGenerator(
        settings=settings,
        environment_manager=environment_manager,
        equipment_registry=equipment_registry,
        equipment_state_manager=equipment_state_manager,
    )
    crop_generator = CropTelemetryGenerator(
        settings=settings,
        random_manager=random_manager,
        environment_manager=growing_environment_manager,
        crop_registry=crop_registry,
        crop_state_manager=crop_state_manager,
    )
    crop_lifecycle_generator = CropLifecycleGenerator(
        settings=settings,
        random_manager=random_manager,
        environment_manager=growing_environment_manager,
        crop_registry=crop_registry,
        crop_state_manager=crop_state_manager,
    )
    irrigation_generator = IrrigationTelemetryGenerator(
        settings=settings, environment_manager=environment_manager, irrigation_state_manager=irrigation_state_manager
    )
    lighting_generator = LightingTelemetryGenerator(
        settings=settings, lighting_state_manager=lighting_state_manager
    )
    facility_generator = FacilityGenerator(facility_state_manager=facility_state_manager)
    maintenance_generator = MaintenanceEventGenerator(
        settings=settings, maintenance_state_manager=maintenance_state_manager
    )

    # Accumulators
    env_rows = []
    eq_rows = []
    crop_rows = []
    irr_rows = []
    light_rows = []
    maint_rows = []
    fac_rows = []
    crop_lc_rows = []
    dl_rows = []

    # 2. Multiple SCD Type 2 Equipment Updates Definition
    equipment_updates = {
        "EQ-00001": {"manufacturer": "HydroPump Pro Global", "model_number": "HP-4000X-TITANIUM", "equipment_type": "WATER_PUMP"},
        "EQ-00002": {"manufacturer": "HydroPump Corp", "model_number": "HP-3500X-PRO", "equipment_type": "WATER_PUMP"},
        "EQ-00005": {"manufacturer": "CoolMaster Systems", "model_number": "HVAC-COOL-MAX-v3", "equipment_type": "HVAC_UNIT"},
        "EQ-00008": {"manufacturer": "Lumatec Precision", "model_number": "LED-QUANTUM-SPECTRUM-PRO", "equipment_type": "LIGHTING_ARRAY"},
        "EQ-00010": {"manufacturer": "AeroVent Technologies", "model_number": "VENT-SUPER-TURBO-v2", "equipment_type": "VENTILATION_FAN"},
        "EQ-00012": {"manufacturer": "SunPower Industrial", "model_number": "SOLAR-GEN-v4", "equipment_type": "SOLAR_GENERATOR"},
        "EQ-00015": {"manufacturer": "DoseTech Controls", "model_number": "NUTRI-DOSE-SMART-v2", "equipment_type": "NUTRIENT_PUMP"},
        "EQ-00020": {"manufacturer": "AquaPure Industrial", "model_number": "RO-PURIFIER-IND-v2", "equipment_type": "RO_SYSTEM"},
    }

    # 3. Multiple SCD Type 2 Facility Updates Definition
    facility_updates = {
        "FAC-001": {
            "facility_name": "Highland Benguet Smart Hydro-Farm Phase 3 Tech Hub",
            "max_zone_capacity": 36,
            "operator_contact": "director.ops@smartfarm.ph",
            "power_grid_redundancy": "DUAL_GRID_PLUS_SOLAR_PLUS_STORAGE",
        },
        "FAC-002": {
            "facility_name": "Lowland Laguna Precision Hydro-Center - Upgraded",
            "max_zone_capacity": 28,
            "operator_contact": "laguna.lead@smartfarm.ph",
            "power_grid_redundancy": "TRIPLE_GRID_SOLAR_HYDRO",
        },
        "FAC-003": {
            "facility_name": "Cebu Central Vertical Farm - Automated Hub",
            "max_zone_capacity": 30,
            "water_source": "DESALINATED_DEEP_WELL",
            "operator_contact": "cebu.tech@smartfarm.ph",
        },
    }

    # 4. Generate Telemetry Over Recent Hours (Hourly Intervals)
    for hour in range(hours):
        step_dt = start_dt + timedelta(hours=hour)
        ts_str = step_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Environmental Telemetry
        for ev in environmental_generator.generate():
            seed = f"{ev.facility_id}_{ev.zone_id}_{ev.sensor_type}_{ts_str}"
            ev_dict = ev.to_dict()
            ev_dict["event_id"] = make_uuidv5("EnvironmentalTelemetry", seed)
            ev_dict["timestamp"] = ts_str
            env_rows.append(ev_dict)

        # Equipment Telemetry (With Multiple Updated Attributes)
        for ev in equipment_generator.generate():
            seed = f"{ev.facility_id}_{ev.zone_id}_{ev.equipment_id}_{ts_str}"
            ev_dict = ev.to_dict()
            ev_dict["event_id"] = make_uuidv5("EquipmentTelemetry", seed)
            ev_dict["timestamp"] = ts_str

            # Apply SCD Type 2 Attribute Changes
            if ev.equipment_id in equipment_updates:
                upd = equipment_updates[ev.equipment_id]
                ev_dict["manufacturer"] = upd["manufacturer"]
                ev_dict["model_number"] = upd["model_number"]
                ev_dict["equipment_type"] = upd["equipment_type"]

            eq_rows.append(ev_dict)

        # Brand New Equipment Additions (SCD Type 2 New Inserts)
        for new_id, fac_id, zn_id, eq_type, mfr, model in [
            ("EQ-00060", "FAC-001", "ZONE-001", "UV_STERILIZER", "AquaRay Industrial", "UV-STERILIZE-PRO"),
            ("EQ-00061", "FAC-002", "ZONE-002", "OZONE_GENERATOR", "PureAir Systems", "O3-GEN-MAX"),
            ("EQ-00062", "FAC-003", "ZONE-003", "SPECTROMETER", "CropOptics Global", "SPEC-CAM-v2"),
        ]:
            seed = f"{fac_id}_{zn_id}_{new_id}_{ts_str}"
            eq_rows.append({
                "event_id": make_uuidv5("EquipmentTelemetry", seed),
                "event_type": "EquipmentTelemetry",
                "facility_id": fac_id,
                "zone_id": zn_id,
                "equipment_id": new_id,
                "equipment_type": eq_type,
                "manufacturer": mfr,
                "model_number": model,
                "runtime_hours": 12.5 + hour,
                "health": 99.5,
                "operating_status": "NORMAL",
                "vibration_level": 0.02,
                "temperature_celsius": 32.5,
                "power_draw_kw": 8.5,
                "operator_contact": "tech.support@smartfarm.ph",
                "operator_phone": "+639178452190",
                "timestamp": ts_str,
            })

        # Crop Telemetry & Lifecycle
        if hour % 4 == 0:
            for ev in crop_generator.generate():
                seed = f"{ev.crop_batch_id}_{ts_str}"
                ev_dict = ev.to_dict()
                ev_dict["event_id"] = make_uuidv5("CropTelemetry", seed)
                ev_dict["timestamp"] = ts_str
                crop_rows.append(ev_dict)

                crop_lc_rows.append({
                    "event_id": make_uuidv5("CropLifecycle", f"{ev.crop_batch_id}_LC_{ts_str}"),
                    "event_type": "CropLifecycle",
                    "facility_id": getattr(ev, "facility_id", "FAC-001"),
                    "zone_id": getattr(ev, "zone_id", "ZONE-001"),
                    "crop_batch_id": ev.crop_batch_id,
                    "crop_type": ev.crop_type,
                    "lifecycle_stage": "HARVESTED" if hour >= 16 else "MATURING",
                    "age_days": ev.age_days + 1,
                    "health_score": ev.health_score,
                    "environmental_stress_index": 0.02,
                    "harvest_cycle_days": 35,
                    "target_biomass_g": 165.0,
                    "operator_contact": "agronomy.lead@smartfarm.ph",
                    "operator_phone": "+639178452190",
                    "timestamp": ts_str,
                })

        # Irrigation & Lighting
        if hour % 2 == 0:
            for ev in irrigation_generator.generate():
                seed = f"{ev.facility_id}_{ev.zone_id}_{ts_str}"
                ev_dict = ev.to_dict()
                ev_dict["event_id"] = make_uuidv5("IrrigationTelemetry", seed)
                ev_dict["timestamp"] = ts_str
                irr_rows.append(ev_dict)

            for ev in lighting_generator.generate():
                seed = f"{ev.facility_id}_{ev.zone_id}_{ts_str}"
                ev_dict = ev.to_dict()
                ev_dict["event_id"] = make_uuidv5("LightingTelemetry", seed)
                ev_dict["timestamp"] = ts_str
                light_rows.append(ev_dict)

        # Maintenance Activity
        if hour % 4 == 0:
            for ev in maintenance_generator.generate():
                seed_maint = f"{ev.work_order_id}_{ts_str}"
                ev_dict = ev.to_dict() if hasattr(ev, "to_dict") else {}
                if ev_dict:
                    ev_dict["event_id"] = make_uuidv5("MaintenanceActivity", seed_maint)
                    ev_dict["timestamp"] = ts_str
                    maint_rows.append(ev_dict)

        # Facility Operations (With Updated Facility Attributes)
        if hour % 6 == 0:
            for fac_id, fac_prof in PHILIPPINE_FACILITY_PROFILES.items():
                seed_fac = f"{fac_id}_{ts_str}"
                fac_name = fac_prof.facility_name
                fac_cap = fac_prof.max_zone_capacity
                fac_contact = "facility.mgr@smartfarm.ph"
                fac_redundancy = fac_prof.power_grid_redundancy
                fac_water = fac_prof.water_source

                if fac_id in facility_updates:
                    upd = facility_updates[fac_id]
                    fac_name = upd.get("facility_name", fac_name)
                    fac_cap = upd.get("max_zone_capacity", fac_cap)
                    fac_contact = upd.get("operator_contact", fac_contact)
                    fac_redundancy = upd.get("power_grid_redundancy", fac_redundancy)
                    fac_water = upd.get("water_source", fac_water)

                fac_rows.append({
                    "event_id": make_uuidv5("FacilityOperations", seed_fac),
                    "event_type": "FacilityOperations",
                    "facility_id": fac_id,
                    "facility_name": fac_name,
                    "region": fac_prof.region,
                    "city": fac_prof.location,
                    "latitude": fac_prof.latitude,
                    "longitude": fac_prof.longitude,
                    "elevation_m": fac_prof.elevation_m,
                    "climate_zone": getattr(fac_prof, "climate_zone", "HUMID_SUBTROPICAL"),
                    "water_source": fac_water,
                    "power_grid_redundancy": fac_redundancy,
                    "max_zone_capacity": fac_cap,
                    "active_zones_count": len(fac_prof.micro_locations),
                    "total_equipment_count": 14 if fac_id in facility_updates else 12,
                    "overall_health": 98.5,
                    "power_draw_kw": 155.0,
                    "water_circulation_lph": 5200.0,
                    "active_critical_alerts": 0,
                    "operator_contact": fac_contact,
                    "operator_phone": "+639178452190",
                    "timestamp": ts_str,
                })

    # 5. Dead-Letter Samples
    for i, (strm, exc) in enumerate([
        ("EnvironmentalTelemetry", "MISSING_PRIMARY_KEY: null facility_id"),
        ("EquipmentTelemetry", "OUT_OF_BOUNDS_SENSOR_VALUE: temperature > 65C"),
        ("CropTelemetry", "DEPRECATED_SCHEMA_VERSION: v1.0 payload"),
        ("IrrigationTelemetry", "SERDES_PARSE_FAILURE: malformed JSON payload"),
    ]):
        seed_dl = f"DL-INC-{i:03d}"
        dl_rows.append({
            "event_id": make_uuidv5("DeadLetterTelemetry", seed_dl),
            "event_type": "DeadLetterTelemetry",
            "target_stream": strm,
            "exception_reason": exc,
            "raw_payload": '{"event_id": "DL-INC-FAIL", "facility_id": null}',
            "ingestion_timestamp": now_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        })

    # Write Output Files
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    stream_map = {
        "EnvironmentalTelemetry": env_rows,
        "EquipmentTelemetry": eq_rows,
        "CropTelemetry": crop_rows,
        "IrrigationTelemetry": irr_rows,
        "LightingTelemetry": light_rows,
        "MaintenanceActivity": maint_rows,
        "FacilityOperations": fac_rows,
        "CropLifecycle": crop_lc_rows,
        "DeadLetterTelemetry": dl_rows,
    }

    print("\n📦 Generated Incremental Batch Files:")
    total_records = 0
    for name, rows in stream_map.items():
        if rows:
            with open(out_path / f"{name}.json", "w", encoding="utf-8") as f:
                json.dump(rows, f, indent=2)
            print(f" ├── Saved {out_path}/{name}.json ({len(rows)} records)")
            total_records += len(rows)

    print(f"\n[+] Incremental Update Batch Finished Successfully! ({total_records:,} Total Records)")
    print(f" [info] SCD Type 2 Updates Generated:")
    print(f"   • Facilities Modified: {len(facility_updates)} ({', '.join(facility_updates.keys())})")
    print(f"   • Equipment Modified:  {len(equipment_updates)} ({', '.join(equipment_updates.keys())})")
    print(f"   • New Equipment Added: 3 (EQ-00060, EQ-00061, EQ-00062)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HydroGrow Incremental Batch Generator")
    parser.add_argument("--hours", type=int, default=24, help="Number of hours of incremental telemetry (default: 24)")
    parser.add_argument("--output-dir", type=str, default="Files_Incremental", help="Output directory (default: Files_Incremental)")
    args = parser.parse_args()

    run_incremental_generator(hours=args.hours, output_dir=args.output_dir)
