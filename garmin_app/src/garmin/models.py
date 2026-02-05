from dataclasses import dataclass, asdict
from typing import List, Optional, Any, Dict

@dataclass
class LapData:
    """Structure representing a single lap within an activity."""
    lapNumber: int
    startTime: str
    distance: float
    duration: float
    averageSpeed: float
    averageHR: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert LapData to a dictionary."""
        return asdict(self)

@dataclass
class ActivitySummary:
    """Structure representing a Garmin activity summary."""
    activityId: str
    activityName: str
    activityType: str
    startTimeLocal: str
    distance: float
    duration: float
    averageHR: Optional[float]
    maxHR: Optional[float]
    averageSpeed: float
    laps: List[LapData]

    def to_dict(self) -> Dict[str, Any]:
        """Convert ActivitySummary and nested laps to a dictionary."""
        return asdict(self)