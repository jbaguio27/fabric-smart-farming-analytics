"""
Facility Domain Configuration - Hydroponics Vertical Farming.

This module contains hardcoded configuration data and regional profiles
for all 8 hydroponics vertical farming facilities in the Philippines (FAC-001 to FAC-008).
"""

from typing import Final
from smart_farming.schemas import FacilityProfile, ZoneMicroLocation


# ========================================================================================
# Philippine Regional Hydroponics Vertical Farming Profiles Registry
# ========================================================================================

PHILIPPINE_FACILITY_PROFILES: Final[dict[str, FacilityProfile]] = {
    "FAC-001": FacilityProfile(
        facility_id="FAC-001",
        facility_name="Benguet Highland Strawberries Vertical Farm",
        location="La Trinidad, Benguet",
        region="Cordillera Administrative Region (CAR)",
        domain_focus="6-Tier Vertical Racks (Strawberries & Kale)",
        target_temperature_celsius=18.0,
        target_humidity_percent=75.0,
        target_ph=5.80,
        target_ec=1.80,
        primary_crops=("Alpine Strawberries", "Butterhead Lettuce", "Kale"),
        operating_hours="05:00 - 21:00 PHT",
        anomaly_trait="Mountain power dips, water level duplicate bursts (~3%)",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "Top-Tier Highland LED Canopy", "strawberry"),
            ZoneMicroLocation("ZONE-002", "Mid-Tier NFT Rack Alpha", "butterhead_lettuce"),
            ZoneMicroLocation("ZONE-003", "Lower-Tier High-Humidity Bed", "kale"),
        ),
    ),
    "FAC-002": FacilityProfile(
        facility_id="FAC-002",
        facility_name="Tagaytay Ridge Hydroponics Nursery",
        location="Tagaytay City, Cavite",
        region="CALABARZON (Region IV-A)",
        domain_focus="4-Tier Ridge Modules (Basil & Arugula)",
        target_temperature_celsius=22.0,
        target_humidity_percent=70.0,
        target_ph=6.00,
        target_ec=1.70,
        primary_crops=("Genovese Basil", "Batavia Lettuce", "Arugula"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Condensation humidity drift, empty payload strings ('')",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "Ridge Micro-Climate Nursery Chamber", "basil"),
            ZoneMicroLocation("ZONE-002", "Vertical NFT Rack Beta", "batavia_lettuce"),
            ZoneMicroLocation("ZONE-003", "Controlled Herb Tier", "arugula"),
        ),
    ),
    "FAC-003": FacilityProfile(
        facility_id="FAC-003",
        facility_name="Metro Manila Rooftop Vertical Hydro-Farm",
        location="Bonifacio Global City (BGC), Taguig City",
        region="National Capital Region (NCR)",
        domain_focus="8-Tier Plant Factory (Romaine & Microgreens)",
        target_temperature_celsius=23.0,
        target_humidity_percent=65.0,
        target_ph=6.00,
        target_ec=1.85,
        primary_crops=("Romaine Lettuce", "Microgreens", "Wheatgrass"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Urban HVAC thermal overload spikes (temperature = 9999.99)",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "Top-Tier High PPFD Canopy", "butterhead_lettuce"),
            ZoneMicroLocation("ZONE-002", "BGC Urban Microgreen Chamber", "microgreens"),
            ZoneMicroLocation("ZONE-003", "NFT High-Density Rack", "spinach"),
        ),
    ),
    "FAC-004": FacilityProfile(
        facility_id="FAC-004",
        facility_name="Davao City Indoor Greens Vertical Facility",
        location="Davao City, Davao del Sur",
        region="Davao Region (Region XI)",
        domain_focus="10-Tier Hydro Towers (Pak Choy & Spinach)",
        target_temperature_celsius=25.0,
        target_humidity_percent=75.0,
        target_ph=6.10,
        target_ec=1.90,
        primary_crops=("Pak Choy", "Spinach", "Asian Baby Greens"),
        operating_hours="05:30 - 21:30 PHT",
        anomaly_trait="pH sensor probe calibration sub-zero reading (-999.0)",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "High-Tower Aeroponic Array A", "spinach"),
            ZoneMicroLocation("ZONE-002", "Sub-Tropical Vertical Chamber", "kale"),
            ZoneMicroLocation("ZONE-003", "DWC Nutrient Tank 1", "arugula"),
        ),
    ),
    "FAC-005": FacilityProfile(
        facility_id="FAC-005",
        facility_name="Laguna Technopark Hydroponic Plant Factory",
        location="Calamba City, Laguna",
        region="CALABARZON (Region IV-A)",
        domain_focus="Industrial NFT/DWC Lines (Tomatoes & Herbs)",
        target_temperature_celsius=24.0,
        target_humidity_percent=68.0,
        target_ph=6.00,
        target_ec=1.80,
        primary_crops=("Cherry Tomatoes", "Sweet Basil", "Oakleaf Lettuce"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Omitted payload keys (null), lowercase casing (fac-005, online)",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "Industrial DWC Vine System", "basil"),
            ZoneMicroLocation("ZONE-002", "NFT Commercial Rack Line 1", "butterhead_lettuce"),
            ZoneMicroLocation("ZONE-003", "High-Output Herb Tier", "parsley"),
        ),
    ),
    "FAC-006": FacilityProfile(
        facility_id="FAC-006",
        facility_name="Cebu Urban Vertical Greens Hub",
        location="Cebu IT Park, Cebu City",
        region="Central Visayas (Region VII)",
        domain_focus="6-Tier Smart City Hydro (Lollo Rossa & Watercress)",
        target_temperature_celsius=24.5,
        target_humidity_percent=70.0,
        target_ph=6.05,
        target_ec=1.80,
        primary_crops=("Lollo Rossa Lettuce", "Cilantro", "Watercress"),
        operating_hours="05:00 - 21:00 PHT",
        anomaly_trait="Gateway network latency out-of-order timestamps (15-120 min delay)",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "IT Park Smart LED Canopy", "batavia_lettuce"),
            ZoneMicroLocation("ZONE-002", "Urban Vertical NFT Rack 2", "cilantro"),
            ZoneMicroLocation("ZONE-003", "Aeroponic Herb Chamber", "arugula"),
        ),
    ),
    "FAC-007": FacilityProfile(
        facility_id="FAC-007",
        facility_name="Clark Freeport Urban Hydroponic Complex",
        location="Clark Freeport Zone, Angeles City, Pampanga",
        region="Central Luzon (Region III)",
        domain_focus="12-Tier Aeroponic Towers (Peppers & Mint)",
        target_temperature_celsius=25.0,
        target_humidity_percent=68.0,
        target_ph=6.15,
        target_ec=1.95,
        primary_crops=("Bell Peppers", "Mint", "Red Coral Lettuce"),
        operating_hours="05:00 - 21:00 PHT",
        anomaly_trait="Dual-clock microcontrollers emitting mixed timestamp formats (ISO vs. Epoch)",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "High-Capacity Aeroponic Tower A", "spinach"),
            ZoneMicroLocation("ZONE-002", "Controlled Photoperiod Module", "parsley"),
            ZoneMicroLocation("ZONE-003", "NFT Leafy Greens Tier", "butterhead_lettuce"),
        ),
    ),
    "FAC-008": FacilityProfile(
        facility_id="FAC-008",
        facility_name="Iloilo City Microgreens Vertical Agro-Lab",
        location="Mandurriao, Iloilo City",
        region="Western Visayas (Region VI)",
        domain_focus="5-Tier Precision LED Modules (Radish & Pea Shoots)",
        target_temperature_celsius=23.5,
        target_humidity_percent=72.0,
        target_ph=5.95,
        target_ec=1.75,
        primary_crops=("Radish Microgreens", "Sunflower Shoots", "Pea Shoots"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Serial buffer string typos (operating_status: 'ONLNE', sensor_status: 'WARNIN')",
        micro_locations=(
            ZoneMicroLocation("ZONE-001", "Precision Microgreen Tray Module A", "microgreens"),
            ZoneMicroLocation("ZONE-002", "LED Agro-Research Chamber", "basil"),
            ZoneMicroLocation("ZONE-003", "High-Density Sprout Rack", "strawberry"),
        ),
    ),
}

# ========================================================================================
# Facility Operational Calculation Constants
# ========================================================================================

EVENT_TYPE_FACILITY: Final[str] = "FacilityEvent"
HEALTHY_FACILITY_THRESHOLD: Final[float] = 70.0
ZONE_POWER_CONSUMPTION_KW: Final[float] = 45.5
ZONE_WATER_RECIRCULATION_LPH: Final[float] = 250.0
