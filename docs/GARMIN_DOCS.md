# Garmin Connect Activities API Documentation

This document provides comprehensive documentation for all activity-related functions in the `python-garminconnect` library, including retrieving activities, activity details, laps/splits, heart rate data, pace, power, and more.

garminconnect version 0.2.38

## Table of Contents
- [Setup](#setup)
- [Retrieving Activities](#retrieving-activities)
- [Activity Details & Metrics](#activity-details--metrics)
- [Activity Splits & Laps](#activity-splits--laps)
- [Activity Heart Rate Data](#activity-heart-rate-data)
- [Activity Power Data](#activity-power-data)
- [Activity Types](#activity-types)
- [Complete Examples](#complete-examples)

---

## Setup

```python
import os
from garminconnect import Garmin

# Initialize with environment variables
client = Garmin(
    email=os.getenv("GARMIN_EMAIL"),
    password=os.getenv("GARMIN_PASSWORD")
)

# Login
client.login()
```

---

## Retrieving Activities

### `count_activities()`

Retrieves the total count of all activities in your account.

**Returns:**
- `int`: Total number of activities

**Example:**
```python
count = client.count_activities()
print(f"Total activities: {count}")
```

---

### `get_activities(start, limit)`

Retrieves a list of activities with pagination.

**Parameters:**
- `start` (int): Starting index (0-based)
- `limit` (int): Maximum number of activities to retrieve (max 1000)

**Returns:**
- `list[dict]`: List of activity summaries

**Activity Summary Fields:**
- `activityId`: Unique activity identifier
- `activityName`: Activity name/title
- `activityType`: Dict with `typeId`, `typeKey`, `parentTypeId`
- `startTimeLocal`: Activity start time in local timezone
- `startTimeGMT`: Activity start time in GMT
- `distance`: Distance in meters
- `duration`: Duration in seconds
- `elapsedDuration`: Elapsed duration including pauses (seconds)
- `movingDuration`: Moving time excluding pauses (seconds)
- `averageSpeed`: Average speed in meters/second
- `maxSpeed`: Maximum speed in meters/second
- `calories`: Calories burned
- `averageHeartRateInBeatsPerMinute`: Average heart rate (bpm)
- `maxHeartRateInBeatsPerMinute`: Maximum heart rate (bpm)
- `averageRunningCadenceInStepsPerMinute`: Average cadence (running)
- `maxRunningCadenceInStepsPerMinute`: Maximum cadence (running)
- `steps`: Total step count
- `elevationGain`: Elevation gain in meters
- `elevationLoss`: Elevation loss in meters
- `minElevation`: Minimum elevation in meters
- `maxElevation`: Maximum elevation in meters

**Example:**
```python
# Get the 20 most recent activities
activities = client.get_activities(0, 20)

for activity in activities:
    print(f"\nActivity: {activity['activityName']}")
    print(f"  ID: {activity['activityId']}")
    print(f"  Type: {activity['activityType']['typeKey']}")
    print(f"  Date: {activity['startTimeLocal']}")
    print(f"  Distance: {activity.get('distance', 0) / 1000:.2f} km")
    print(f"  Duration: {activity.get('duration', 0) / 60:.1f} minutes")
    print(f"  Avg Pace: {1000 / (activity.get('averageSpeed', 1) * 60):.2f} min/km")
    print(f"  Calories: {activity.get('calories', 0)}")
    print(f"  Avg HR: {activity.get('averageHeartRateInBeatsPerMinute', 'N/A')} bpm")
    print(f"  Max HR: {activity.get('maxHeartRateInBeatsPerMinute', 'N/A')} bpm")
    print(f"  Elevation Gain: {activity.get('elevationGain', 0):.0f} m")

# Pagination example - get activities 20-40
next_batch = client.get_activities(20, 20)
```

---

### `get_last_activity()`

Retrieves the most recent activity.

**Returns:**
- `dict | None`: Most recent activity data, or None if no activities exist

**Example:**
```python
activity = client.get_last_activity()

if activity:
    print(f"Last activity: {activity['activityName']}")
    print(f"Date: {activity['startTimeLocal']}")
    print(f"Type: {activity['activityType']['typeKey']}")
else:
    print("No activities found")
```

---

### `get_activities_by_date(startdate, enddate, activitytype=None, start=None, limit=None)`

Retrieves activities within a specific date range, with optional filtering by activity type.

**Parameters:**
- `startdate` (str): Start date in format 'YYYY-MM-DD'
- `enddate` (str): End date in format 'YYYY-MM-DD'
- `activitytype` (str, optional): Filter by activity type (e.g., "running", "cycling", "swimming")
- `start` (int, optional): Starting index for pagination
- `limit` (int, optional): Maximum number of activities to retrieve

**Returns:**
- `list[dict]`: List of activities in the date range

**Example:**
```python
# Get all activities in January 2024
activities = client.get_activities_by_date("2024-01-01", "2024-01-31")
print(f"Found {len(activities)} activities in January")

# Get only running activities
running = client.get_activities_by_date(
    "2024-01-01",
    "2024-01-31",
    activitytype="running"
)
print(f"Found {len(running)} running activities")

# Get cycling activities with pagination
cycling = client.get_activities_by_date(
    "2024-01-01",
    "2024-01-31",
    activitytype="cycling",
    start=0,
    limit=10
)

# Common activity types:
# - running
# - cycling
# - swimming
# - walking
# - hiking
# - strength_training
# - yoga
```

---

### `get_activities_fordate(fordate)`

Retrieves activities for a specific date.

**Parameters:**
- `fordate` (str): Date in format 'YYYY-MM-DD'

**Returns:**
- `dict`: Activities for the specified date

**Example:**
```python
from datetime import date

today = date.today().isoformat()
activities = client.get_activities_fordate(today)

for activity in activities:
    print(f"Activity: {activity['activityName']}")
```

---

## Activity Details & Metrics

### `get_activity(activity_id)`

Retrieves detailed activity information without time-series data.

**Parameters:**
- `activity_id` (str): Activity ID

**Returns:**
- `dict`: Detailed activity information

**Key Fields:**
- All fields from activity summary, plus:
- `locationName`: Location/city
- `ownerDisplayName`: Owner name
- `description`: Activity description
- `avgPower`: Average power (watts) for cycling
- `maxPower`: Maximum power (watts)
- `normPower`: Normalized power
- `avgVerticalOscillation`: Average vertical oscillation (running)
- `avgGroundContactTime`: Average ground contact time (running)
- `trainingEffect`: Aerobic training effect
- `anaerobicTrainingEffect`: Anaerobic training effect
- `avgStrideLength`: Average stride length
- `vO2MaxValue`: VO2 Max value

**Example:**
```python
activity = client.get_activity("123456789")

print(f"Activity: {activity['activityName']}")
print(f"Location: {activity.get('locationName', 'Unknown')}")
print(f"Description: {activity.get('description', 'No description')}")
print(f"\nPerformance Metrics:")
print(f"  Avg HR: {activity.get('averageHeartRateInBeatsPerMinute', 'N/A')} bpm")
print(f"  Max HR: {activity.get('maxHeartRateInBeatsPerMinute', 'N/A')} bpm")
print(f"  Avg Pace: {1000 / (activity.get('averageSpeed', 1) * 60):.2f} min/km")
print(f"  Max Pace: {1000 / (activity.get('maxSpeed', 1) * 60):.2f} min/km")
print(f"  Aerobic TE: {activity.get('trainingEffect', 'N/A')}")
print(f"  Anaerobic TE: {activity.get('anaerobicTrainingEffect', 'N/A')}")

# Cycling-specific metrics
if 'avgPower' in activity:
    print(f"\nPower Metrics:")
    print(f"  Avg Power: {activity['avgPower']} watts")
    print(f"  Max Power: {activity.get('maxPower', 'N/A')} watts")
    print(f"  Normalized Power: {activity.get('normPower', 'N/A')} watts")

# Running-specific metrics
if 'avgVerticalOscillation' in activity:
    print(f"\nRunning Dynamics:")
    print(f"  Avg Vertical Oscillation: {activity['avgVerticalOscillation']} cm")
    print(f"  Avg Ground Contact Time: {activity['avgGroundContactTime']} ms")
    print(f"  Avg Stride Length: {activity.get('avgStrideLength', 'N/A')} m")
```

---

### `get_activity_details(activity_id, maxchartsize=2000, maxpolylinesize=4000)`

Retrieves comprehensive activity data including time-series metrics (pace, heart rate, cadence, power) and GPS track.

**Parameters:**
- `activity_id` (str): Activity ID
- `maxchartsize` (int, default=2000): Maximum number of chart data points
- `maxpolylinesize` (int, default=4000): Maximum GPS polyline size

**Returns:**
- `dict`: Detailed activity with time-series data

**Key Fields:**
- `metricDescriptors`: List of available metrics (HR, pace, cadence, etc.)
- `activityDetailMetrics`: Time-series data for each metric
- `geoPolylineDTO`: GPS track data
- `sampledActivityMetrics`: Sampled metric data points

**Metric Types Available:**
- Heart rate (bpm)
- Pace (min/km or min/mile)
- Speed (m/s)
- Cadence (steps/min or rpm)
- Power (watts)
- Elevation (meters)
- Distance (meters)
- Time (seconds)

**Example:**
```python
details = client.get_activity_details("123456789")

print(f"Activity: {details['activityName']}")
print(f"\nAvailable Metrics:")
for metric in details.get('metricDescriptors', []):
    print(f"  - {metric['metricsIndex']}: {metric['key']}")

# Extract heart rate data
for metric in details.get('activityDetailMetrics', []):
    if metric['metrics']:
        metric_key = metric.get('metricKey', 'unknown')
        values = metric['metrics']

        if metric_key == 'directHeartRate':
            print(f"\nHeart Rate Data ({len(values)} samples):")
            print(f"  First sample: {values[0]} bpm")
            print(f"  Last sample: {values[-1]} bpm")

        elif metric_key == 'directSpeed':
            print(f"\nSpeed Data ({len(values)} samples):")
            # Convert m/s to min/km
            paces = [1000 / (v * 60) if v > 0 else 0 for v in values]
            avg_pace = sum(paces) / len(paces) if paces else 0
            print(f"  Average pace: {avg_pace:.2f} min/km")

        elif metric_key == 'directRunCadence':
            print(f"\nCadence Data ({len(values)} samples):")
            avg_cadence = sum(values) / len(values) if values else 0
            print(f"  Average cadence: {avg_cadence:.0f} spm")

# GPS track data
if 'geoPolylineDTO' in details and details['geoPolylineDTO']:
    polyline = details['geoPolylineDTO'].get('polyline', [])
    print(f"\nGPS Track: {len(polyline)} points")
```

---

### `get_progress_summary_between_dates(startdate, enddate, metric_id, aggregation)`

Retrieves progress summary for a specific metric over a date range.

**Parameters:**
- `startdate` (str): Start date in format 'YYYY-MM-DD'
- `enddate` (str): End date in format 'YYYY-MM-DD'
- `metric_id` (int): Metric ID to track
- `aggregation` (str): Aggregation type ("sum", "avg", "max", "min")

**Returns:**
- `dict`: Progress summary for the metric

**Example:**
```python
# Get total distance for running activities in January
progress = client.get_progress_summary_between_dates(
    "2024-01-01",
    "2024-01-31",
    metric_id=1,  # Distance metric
    aggregation="sum"
)
```

---

## Activity Splits & Laps

### `get_activity_splits(activity_id)`

Retrieves activity splits/laps with per-lap metrics.

**Parameters:**
- `activity_id` (str): Activity ID

**Returns:**
- `dict`: Split/lap information

**Lap Fields:**
- `lapIndex`: Lap number (0-based)
- `startTimeGMT`: Lap start time
- `distance`: Lap distance (meters)
- `duration`: Lap duration (seconds)
- `movingDuration`: Moving time (seconds)
- `averageSpeed`: Average speed (m/s)
- `maxSpeed`: Maximum speed (m/s)
- `averageHeartRate`: Average heart rate (bpm)
- `maxHeartRate`: Maximum heart rate (bpm)
- `calories`: Calories burned in lap
- `averageRunningCadence`: Average cadence
- `maxRunningCadence`: Maximum cadence
- `elevationGain`: Elevation gain (meters)
- `elevationLoss`: Elevation loss (meters)

**Example:**
```python
splits = client.get_activity_splits("123456789")

print("Activity Splits/Laps:")
print("-" * 80)

for lap in splits.get('lapDTOs', []):
    lap_num = lap['lapIndex'] + 1
    distance_km = lap.get('distance', 0) / 1000
    duration_sec = lap.get('duration', 0)
    duration_min = duration_sec / 60

    # Calculate pace (min/km)
    if lap.get('averageSpeed', 0) > 0:
        pace = 1000 / (lap['averageSpeed'] * 60)
    else:
        pace = 0

    print(f"\nLap {lap_num}:")
    print(f"  Distance: {distance_km:.2f} km")
    print(f"  Duration: {duration_min:.2f} minutes ({duration_sec:.0f} seconds)")
    print(f"  Avg Pace: {pace:.2f} min/km")
    print(f"  Max Speed: {lap.get('maxSpeed', 0) * 3.6:.2f} km/h")
    print(f"  Avg HR: {lap.get('averageHeartRate', 'N/A')} bpm")
    print(f"  Max HR: {lap.get('maxHeartRate', 'N/A')} bpm")
    print(f"  Avg Cadence: {lap.get('averageRunningCadence', 'N/A')} spm")
    print(f"  Calories: {lap.get('calories', 0)}")
    print(f"  Elevation Gain: {lap.get('elevationGain', 0):.0f} m")
    print(f"  Elevation Loss: {lap.get('elevationLoss', 0):.0f} m")

# Calculate summary statistics
total_distance = sum(lap.get('distance', 0) for lap in splits.get('lapDTOs', []))
total_duration = sum(lap.get('duration', 0) for lap in splits.get('lapDTOs', []))
avg_pace_overall = 1000 / ((total_distance / total_duration) * 60) if total_duration > 0 else 0

print(f"\nSummary:")
print(f"  Total Laps: {len(splits.get('lapDTOs', []))}")
print(f"  Total Distance: {total_distance / 1000:.2f} km")
print(f"  Total Duration: {total_duration / 60:.2f} minutes")
print(f"  Overall Avg Pace: {avg_pace_overall:.2f} min/km")
```

---

### `get_activity_split_summaries(activity_id)`

Retrieves split summary statistics.

**Parameters:**
- `activity_id` (str): Activity ID

**Returns:**
- `dict`: Split summary statistics

**Example:**
```python
split_summaries = client.get_activity_split_summaries("123456789")

print("Split Summaries:")
for summary in split_summaries.get('splitSummaries', []):
    print(f"  Type: {summary.get('splitType')}")
    print(f"  Distance: {summary.get('distance', 0) / 1000:.2f} km")
    print(f"  Duration: {summary.get('duration', 0) / 60:.2f} min")
```

---

### `get_activity_typed_splits(activity_id)`

Retrieves typed splits (e.g., kilometer splits, mile splits).

**Parameters:**
- `activity_id` (str): Activity ID

**Returns:**
- `dict`: Typed split information

**Example:**
```python
typed_splits = client.get_activity_typed_splits("123456789")

# Usually returns kilometer or mile splits depending on settings
for split_type, splits in typed_splits.items():
    print(f"\n{split_type} Splits:")
    for i, split in enumerate(splits, 1):
        print(f"  Split {i}: {split.get('duration', 0):.1f} seconds")
```

---

## Activity Heart Rate Data

### `get_activity_hr_in_timezones(activity_id)`

Retrieves time spent in each heart rate zone during the activity.

**Parameters:**
- `activity_id` (str): Activity ID

**Returns:**
- `dict`: Heart rate zone distribution

**Heart Rate Zones:**
- Zone 1: Warm-up (50-60% max HR)
- Zone 2: Easy (60-70% max HR)
- Zone 3: Aerobic (70-80% max HR)
- Zone 4: Threshold (80-90% max HR)
- Zone 5: Maximum (90-100% max HR)

**Example:**
```python
hr_zones = client.get_activity_hr_in_timezones("123456789")

print("Heart Rate Zone Distribution:")
print("-" * 60)

total_time = 0
for zone in hr_zones.get('heartRateZones', []):
    zone_num = zone.get('zoneNumber', 0)
    seconds = zone.get('secsInZone', 0)
    minutes = seconds / 60
    total_time += seconds

    print(f"Zone {zone_num}: {minutes:.1f} minutes ({seconds} seconds)")
    print(f"  Range: {zone.get('zoneLowBoundary', 'N/A')} - {zone.get('zoneHighBoundary', 'N/A')} bpm")

# Calculate percentage in each zone
print(f"\nPercentage Distribution:")
for zone in hr_zones.get('heartRateZones', []):
    zone_num = zone.get('zoneNumber', 0)
    seconds = zone.get('secsInZone', 0)
    percentage = (seconds / total_time * 100) if total_time > 0 else 0
    print(f"Zone {zone_num}: {percentage:.1f}%")
```

---

## Activity Power Data

### `get_activity_power_in_timezones(activity_id)`

Retrieves time spent in each power zone during cycling activities.

**Parameters:**
- `activity_id` (str): Activity ID

**Returns:**
- `dict`: Power zone distribution

**Power Zones (typical):**
- Zone 1: Active Recovery (<55% FTP)
- Zone 2: Endurance (55-75% FTP)
- Zone 3: Tempo (75-90% FTP)
- Zone 4: Threshold (90-105% FTP)
- Zone 5: VO2 Max (105-120% FTP)
- Zone 6: Anaerobic (>120% FTP)

**Example:**
```python
power_zones = client.get_activity_power_in_timezones("123456789")

print("Power Zone Distribution:")
print("-" * 60)

for zone in power_zones.get('powerZones', []):
    zone_num = zone.get('zoneNumber', 0)
    seconds = zone.get('secsInZone', 0)
    minutes = seconds / 60

    print(f"Zone {zone_num}: {minutes:.1f} minutes")
    print(f"  Range: {zone.get('zoneLowBoundary', 'N/A')} - {zone.get('zoneHighBoundary', 'N/A')} watts")
```

---

### `get_cycling_ftp(cdate=None)`

Retrieves Functional Threshold Power (FTP) for cycling.

**Parameters:**
- `cdate` (str, optional): Date in format 'YYYY-MM-DD'

**Returns:**
- `dict`: FTP data

**Example:**
```python
from datetime import date

ftp = client.get_cycling_ftp(date.today().isoformat())
print(f"Current FTP: {ftp.get('ftp', 'N/A')} watts")
```

---

## Activity Types

### `get_activity_types()`

Retrieves all available activity types and their IDs.

**Returns:**
- `dict`: Activity types with IDs and metadata

**Example:**
```python
types = client.get_activity_types()

print("Available Activity Types:")
for activity_type in types:
    type_key = activity_type.get('typeKey', 'unknown')
    type_id = activity_type.get('typeId', 'N/A')
    parent_id = activity_type.get('parentTypeId', 'N/A')

    print(f"  {type_key}")
    print(f"    ID: {type_id}")
    print(f"    Parent ID: {parent_id}")

# Common activity types you'll see:
# - running (typeId: 1)
# - cycling (typeId: 2)
# - swimming (typeId: 5)
# - trail_running
# - mountain_biking
# - strength_training
# - walking
# - hiking
# - yoga
```

---

## Complete Examples

### Example 1: Analyze Your Last 10 Runs

```python
import os
from datetime import date
from garminconnect import Garmin

# Initialize
client = Garmin(
    email=os.getenv("GARMIN_EMAIL"),
    password=os.getenv("GARMIN_PASSWORD")
)
client.login()

# Get running activities from the last month
start = (date.today().replace(day=1)).isoformat()
end = date.today().isoformat()

activities = client.get_activities_by_date(start, end, activitytype="running")
activities = activities[:10]  # Last 10 runs

print(f"Analyzing your last {len(activities)} runs:\n")
print("=" * 80)

total_distance = 0
total_duration = 0

for i, activity in enumerate(activities, 1):
    activity_id = activity['activityId']

    # Get detailed info
    details = client.get_activity(activity_id)

    # Get splits
    splits = client.get_activity_splits(activity_id)

    # Get HR zones
    hr_zones = client.get_activity_hr_in_timezones(activity_id)

    # Get weather
    try:
        weather = client.get_activity_weather(activity_id)
    except:
        weather = {}

    # Calculate metrics
    distance = activity.get('distance', 0) / 1000
    duration = activity.get('duration', 0) / 60
    avg_pace = 1000 / (activity.get('averageSpeed', 1) * 60) if activity.get('averageSpeed') else 0
    avg_hr = activity.get('averageHeartRateInBeatsPerMinute', 'N/A')

    total_distance += distance
    total_duration += duration

    print(f"\n{i}. {activity['activityName']}")
    print(f"   Date: {activity['startTimeLocal'][:10]}")
    print(f"   Distance: {distance:.2f} km")
    print(f"   Duration: {duration:.1f} minutes")
    print(f"   Avg Pace: {avg_pace:.2f} min/km")
    print(f"   Avg HR: {avg_hr} bpm")
    print(f"   Calories: {activity.get('calories', 0)}")
    print(f"   Elevation Gain: {activity.get('elevationGain', 0):.0f} m")

    if weather.get('temp'):
        print(f"   Weather: {weather['temp']}°C, {weather.get('weatherTypeKey', 'Unknown')}")

    # Show splits
    num_laps = len(splits.get('lapDTOs', []))
    if num_laps > 0:
        print(f"   Splits: {num_laps} laps")
        fastest_lap = min(splits['lapDTOs'],
                         key=lambda x: x.get('averageSpeed', 0),
                         default={})
        if fastest_lap and fastest_lap.get('averageSpeed'):
            fastest_pace = 1000 / (fastest_lap['averageSpeed'] * 60)
            print(f"   Fastest lap pace: {fastest_pace:.2f} min/km")

    # Show HR zone distribution
    if hr_zones.get('heartRateZones'):
        zone_4_5_time = sum(z.get('secsInZone', 0)
                           for z in hr_zones['heartRateZones']
                           if z.get('zoneNumber', 0) >= 4)
        if zone_4_5_time > 0:
            print(f"   High intensity time (Zone 4+5): {zone_4_5_time / 60:.1f} min")

print("\n" + "=" * 80)
print(f"\nSummary:")
print(f"  Total Distance: {total_distance:.2f} km")
print(f"  Total Duration: {total_duration:.1f} minutes ({total_duration / 60:.1f} hours)")
print(f"  Average per run: {total_distance / len(activities):.2f} km")
print(f"  Average pace: {(total_duration / total_distance):.2f} min/km")
```

---

### Example 2: Find Your Fastest 5K

```python
import os
from garminconnect import Garmin

# Initialize
client = Garmin(
    email=os.getenv("GARMIN_EMAIL"),
    password=os.getenv("GARMIN_PASSWORD")
)
client.login()

# Get all running activities
activities = client.get_activities_by_date("2020-01-01", "2024-12-31", activitytype="running")

# Filter for 5K activities (4.5 - 5.5 km range)
five_k_runs = []
for activity in activities:
    distance = activity.get('distance', 0) / 1000
    if 4.5 <= distance <= 5.5:
        duration = activity.get('duration', 0)
        pace = duration / distance / 60  # min/km
        five_k_runs.append({
            'id': activity['activityId'],
            'name': activity['activityName'],
            'date': activity['startTimeLocal'][:10],
            'distance': distance,
            'duration': duration,
            'pace': pace
        })

# Sort by duration (fastest first)
five_k_runs.sort(key=lambda x: x['duration'])

print(f"Found {len(five_k_runs)} 5K runs")
print("\nYour Top 10 Fastest 5K Times:")
print("=" * 80)

for i, run in enumerate(five_k_runs[:10], 1):
    minutes = int(run['duration'] / 60)
    seconds = int(run['duration'] % 60)

    print(f"\n{i}. {run['name']}")
    print(f"   Date: {run['date']}")
    print(f"   Time: {minutes}:{seconds:02d}")
    print(f"   Distance: {run['distance']:.2f} km")
    print(f"   Pace: {run['pace']:.2f} min/km")

    # Get splits for the fastest
    if i == 1:
        splits = client.get_activity_splits(run['id'])
        print(f"   Splits:")
        for lap in splits.get('lapDTOs', []):
            lap_pace = 1000 / (lap.get('averageSpeed', 1) * 60)
            print(f"     Lap {lap['lapIndex'] + 1}: {lap_pace:.2f} min/km")
```

---

### Example 3: Weekly Activity Summary

```python
import os
from datetime import date, timedelta
from garminconnect import Garmin

# Initialize
client = Garmin(
    email=os.getenv("GARMIN_EMAIL"),
    password=os.getenv("GARMIN_PASSWORD")
)
client.login()

# Get last 7 days
end = date.today()
start = end - timedelta(days=7)

activities = client.get_activities_by_date(start.isoformat(), end.isoformat())

# Group by activity type
by_type = {}
for activity in activities:
    activity_type = activity['activityType']['typeKey']

    if activity_type not in by_type:
        by_type[activity_type] = {
            'count': 0,
            'distance': 0,
            'duration': 0,
            'calories': 0
        }

    by_type[activity_type]['count'] += 1
    by_type[activity_type]['distance'] += activity.get('distance', 0) / 1000
    by_type[activity_type]['duration'] += activity.get('duration', 0) / 60
    by_type[activity_type]['calories'] += activity.get('calories', 0)

print(f"Weekly Activity Summary ({start} to {end})")
print("=" * 80)
print(f"\nTotal Activities: {len(activities)}")

for activity_type, stats in sorted(by_type.items()):
    print(f"\n{activity_type.upper()}:")
    print(f"  Count: {stats['count']}")
    print(f"  Total Distance: {stats['distance']:.2f} km")
    print(f"  Total Duration: {stats['duration']:.0f} minutes ({stats['duration'] / 60:.1f} hours)")
    print(f"  Total Calories: {stats['calories']:.0f}")

    if stats['distance'] > 0:
        avg_pace = stats['duration'] / stats['distance']
        print(f"  Average Pace: {avg_pace:.2f} min/km")

# Total stats
total_distance = sum(s['distance'] for s in by_type.values())
total_duration = sum(s['duration'] for s in by_type.values())
total_calories = sum(s['calories'] for s in by_type.values())

print("\n" + "=" * 80)
print("\nOVERALL TOTALS:")
print(f"  Distance: {total_distance:.2f} km")
print(f"  Duration: {total_duration:.0f} minutes ({total_duration / 60:.1f} hours)")
print(f"  Calories: {total_calories:.0f}")
```

---

## Tips & Best Practices

### 1. Rate Limiting

Add delays when making many API requests:

```python
import time

for activity_id in activity_ids:
    activity = client.get_activity(activity_id)
    time.sleep(1)  # 1 second delay
```

### 2. Error Handling

Always wrap API calls in try-except blocks:

```python
from garminconnect import GarminConnectConnectionError

try:
    activity = client.get_activity("123456789")
except GarminConnectConnectionError as e:
    print(f"Failed to retrieve activity: {e}")
```

### 3. Pace Calculations

Convert speed (m/s) to pace (min/km):

```python
# From activity data
speed_ms = activity.get('averageSpeed', 0)
if speed_ms > 0:
    pace_min_km = 1000 / (speed_ms * 60)
    print(f"Pace: {pace_min_km:.2f} min/km")
```

### 4. Distance Conversions

```python
# Meters to kilometers
distance_km = distance_meters / 1000

# Meters to miles
distance_miles = distance_meters / 1609.34
```

### 5. Duration Formatting

```python
# Seconds to minutes:seconds
duration_sec = 1845
minutes = duration_sec // 60
seconds = duration_sec % 60
print(f"Duration: {minutes}:{seconds:02d}")
```

---

## Common Activity Type Keys

- `running`
- `street_running`
- `trail_running`
- `track_running`
- `virtual_run`
- `treadmill_running`
- `cycling`
- `road_biking`
- `mountain_biking`
- `gravel_cycling`
- `indoor_cycling`
- `virtual_ride`
- `swimming`
- `lap_swimming`
- `open_water_swimming`
- `walking`
- `casual_walking`
- `speed_walking`
- `hiking`
- `strength_training`
- `cardio_training`
- `elliptical`
- `yoga`
- `pilates`
- `rowing`
- `indoor_rowing`

---
