"""🏃‍♂️ Data models for Garmin activity and lap data."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LapData:
    """Structure representing a single lap within an activity."""
    lapNumber: int
    startTime: str
    distance: float
    duration: float
    averageSpeed: float
    averageHR: float


@dataclass
class ActivitySummary:
    """Structure representing a Garmin activity summary."""
    activityId: int
    activityName: str
    activityType: str
    startTimeLocal: str
    distance: float
    duration: float
    averageHR: float
    maxHR: float
    averageSpeed: float
    laps: List[LapData]