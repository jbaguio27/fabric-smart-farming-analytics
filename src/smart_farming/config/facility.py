"""
Facility Domain Configuration.

This module contains hardcoded configuration data and regional profiles
for all 8 smart farming facilities in the Philippines (FAC-001 to FAC-008).
"""

from typing import Final
from smart_farming.schemas import FacilityProfile


# ========================================================================================
# Philippine Regional Facility Profiles Registry
# ========================================================================================

PHILIPPINE_FACILITY_PROFILES: Final[dict[str, FacilityProfile]] = {
    "FAC-001": FacilityProfile(
        facility_id="FAC-001",
        facility_name="Benguet High-Altitude Strawberries & Greens",
        location="La Trinidad, Benguet",
        region="Cordillera Administrative Region (CAR)",
        domain_focus="Highland Hydroponics & Strawberries",
        target_temperature_celsius=18.0,
        target_humidity_percent=75.0,
        target_ph=5.80,
        target_ec=1.80,
        primary_crops=("Butterhead Lettuce", "Strawberries", "Kale"),
        operating_hours="05:00 - 21:00 PHT",
        anomaly_trait="Mountain morning fog power drops and duplicate event bursts (~3%)",
    ),
    "FAC-002": FacilityProfile(
        facility_id="FAC-002",
        facility_name="Tagaytay Ridge Smart Greenhouse & Nursery",
        location="Tagaytay City, Cavite",
        region="CALABARZON (Region IV-A)",
        domain_focus="Culinary Herbs & Sub-Tropical Nursery",
        target_temperature_celsius=22.0,
        target_humidity_percent=70.0,
        target_ph=6.00,
        target_ec=1.70,
        primary_crops=("Batavia Lettuce", "Genovese Basil", "Arugula"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Ridge cloud condensation drift and empty string payloads ('')",
    ),
    "FAC-003": FacilityProfile(
        facility_id="FAC-003",
        facility_name="Davao Cacao & Vertical Agro-Plantation",
        location="Davao City, Davao del Sur",
        region="Davao Region (Region XI)",
        domain_focus="Premium Cacao & Vertical Asian Greens",
        target_temperature_celsius=25.0,
        target_humidity_percent=80.0,
        target_ph=6.50,
        target_ec=1.90,
        primary_crops=("Spinach", "Microgreens", "Asian Greens"),
        operating_hours="05:30 - 21:30 PHT",
        anomaly_trait="Afternoon HVAC thermal overload spikes (temperature = 9999.99)",
    ),
    "FAC-004": FacilityProfile(
        facility_id="FAC-004",
        facility_name="Bukidnon Cattle & High-Altitude Agro-Ranch",
        location="Manolo Fortich, Bukidnon",
        region="Northern Mindanao (Region X)",
        domain_focus="Livestock Environmental & Herbs",
        target_temperature_celsius=20.0,
        target_humidity_percent=72.0,
        target_ph=5.90,
        target_ec=1.75,
        primary_crops=("Parsley", "Cilantro", "High-Value Herbs"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Uncalibrated pH probe sub-zero corrupted values (-999.0)",
    ),
    "FAC-005": FacilityProfile(
        facility_id="FAC-005",
        facility_name="Laguna Technopark Smart Hydro-Facility",
        location="Calamba City, Laguna",
        region="CALABARZON (Region IV-A)",
        domain_focus="Commercial Romaine & Hydroponic Tomatoes",
        target_temperature_celsius=24.0,
        target_humidity_percent=68.0,
        target_ph=6.00,
        target_ec=1.80,
        primary_crops=("Romaine Lettuce", "Mint", "Cherry Tomatoes"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Omitted payload keys (null) and lowercase string casing (fac-005, online)",
    ),
    "FAC-006": FacilityProfile(
        facility_id="FAC-006",
        facility_name="Pampanga Lowland Poultry & Agri-Center",
        location="City of San Fernando, Pampanga",
        region="Central Luzon (Region III)",
        domain_focus="Poultry Climate & Lowland Veggies",
        target_temperature_celsius=27.0,
        target_humidity_percent=72.0,
        target_ph=6.20,
        target_ec=2.00,
        primary_crops=("Bell Peppers", "Cucumbers", "Watercress"),
        operating_hours="05:00 - 21:00 PHT",
        anomaly_trait="Rural gateway latency causing out-of-order late timestamps (15-120 min delay)",
    ),
    "FAC-007": FacilityProfile(
        facility_id="FAC-007",
        facility_name="Western Visayas Rice & Coastal Aquaculture Hub",
        location="Iloilo City, Iloilo",
        region="Western Visayas (Region VI)",
        domain_focus="Smart Rice Paddy Irrigation & Aquaponics",
        target_temperature_celsius=26.0,
        target_humidity_percent=75.0,
        target_ph=6.80,
        target_ec=1.85,
        primary_crops=("Butterhead Lettuce", "Bok Choy", "Microgreens"),
        operating_hours="05:30 - 21:30 PHT",
        anomaly_trait="Mixed timestamp formats (ISO 8601 strings mixed with Unix Epoch integers)",
    ),
    "FAC-008": FacilityProfile(
        facility_id="FAC-008",
        facility_name="Cagayan Valley Smart Agro-Research Station",
        location="Tuguegarao City, Cagayan",
        region="Cagayan Valley (Region II)",
        domain_focus="Hybrid Grain Seeds & Agro-Forestry",
        target_temperature_celsius=28.0,
        target_humidity_percent=65.0,
        target_ph=6.15,
        target_ec=1.95,
        primary_crops=("Spinach", "Genovese Basil", "Strawberries"),
        operating_hours="06:00 - 22:00 PHT",
        anomaly_trait="Serial buffer string typos (operating_status: 'ONLNE', sensor_status: 'WARNIN')",
    ),
}
