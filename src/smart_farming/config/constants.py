"""
Application-wide constancts for the HydroGrow Smart Farming Simulator.

These values are considered static and should not be modified at runtime.
Runtime configuration belongs in settings.py
"""

from zoneinfo import ZoneInfo

print('#' + '=' * 70)
# Application
print('#' + '=' * 70)

APPLICATION_NAME = 'HydroGrow Smart Farming Simulator'
APPLICATION_VERSION = '1.0.0'

DEFAULT_TIMEZONE = ZoneInfo('UTC')
SCHEMA_VERSION = '1.0'

print('#' + '=' * 70)
# Event Types
print('#' + '=' * 70)

EVENT_TYPE_ENVIRONMENTAL = 'environmental'
EVENT_TYPE_EQUIPMENT = 'equipment'
EVENT_TYPE_CROP = 'crop'
EVENT_TYPE_MAINTENANCE = 'maintenance'
EVENT_TYPE_FACILITY = 'facility'

EVENT_TYPES = (
    EVENT_TYPE_ENVIRONMENTAL,
    EVENT_TYPE_EQUIPMENT,
    EVENT_TYPE_CROP,
    EVENT_TYPE_MAINTENANCE,
    EVENT_TYPE_FACILITY
)

print('#' + '=' * 70)
# Sensor Types
print('#' + '=' * 70)

SENSOR_TYPES = (
    'water_ph',
    'dissolved_oxygen',
    'electrical_conductivity',
    'air_temperature',
    'humidity',
    'co2',
    'light_intensity'
)

print('#' + '=' * 70)
# Equipment Types
print('#' + '=' * 70)

STATUS_ONLINE = 'ONLINE'
STATUS_OFFLINE = 'OFFLINE'
STATUS_WARNING = 'WARNING'
STATUS_ERROR = 'ERROR'

EQUIPMENT_STATUS = (
    STATUS_ONLINE,
    STATUS_OFFLINE,
    STATUS_WARNING,
    STATUS_ERROR
)

print('#' + '=' * 70)
# Sensor Health
print('#' + '=' * 70)

SENSOR_STATUS_HEALTHY = 'HEALTHY'
SENSOR_STATUS_WARNING = 'WARNING'
SENSOR_STATUS_FAILED = 'FAILED'

SENSOR_STATUSES = (
    SENSOR_STATUS_HEALTHY,
    SENSOR_STATUS_WARNING,
    SENSOR_STATUS_FAILED
)

print('#' + '=' * 70)
# Crop Status
print('#' + '=' * 70)

CROP_STAGE_SEEDLING = 'SEEDLING'
CROP_STAGE_GROWING = 'GROWING'
CROP_STAGE_READY = 'READY_FOR_HARVEST'
CROP_STAGE_HARVESTED = 'HARVESTED'

CROP_STAGES = (
    CROP_STAGE_SEEDLING,
    CROP_STAGE_GROWING,
    CROP_STAGE_READY,
    CROP_STAGE_HARVESTED
)

print('#' + '=' * 70)
# Timestamp
print('#' + '=' * 70)

IS0_8601_FORMAT = '%Y-%m-%dT%H:%M:%SZ'