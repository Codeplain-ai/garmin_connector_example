"""🏃‍♂️ Garmin Client implementation with session persistence and data retrieval."""

import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Any, Tuple

from garth.exc import GarthException, GarthHTTPError
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from src.garmin.models import ActivitySummary, LapData
from src.garmin.storage import save_activities, load_activities

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GarminClient:
    """Interface for Garmin Connect API."""

    def __init__(self, token_dir: str = "~/.garminconnect"):
        self.email = os.getenv("GARMIN_EMAIL")
        self.password = os.getenv("GARMIN_PASSWORD")
        self.token_dir = Path(token_dir).expanduser()
        self.api: Optional[Garmin] = None

        if not self.email or not self.password:
            logger.error("Missing GARMIN_EMAIL or GARMIN_PASSWORD environment variables.")
            sys.exit(1)

    def login(self):
        """Authenticate with Garmin Connect and handle session persistence."""
        try:
            # Attempt to use existing tokens
            self.api = Garmin()
            if self.token_dir.exists() and list(self.token_dir.glob("*.json")):
                logger.info("Attempting login with stored tokens...")
                self.api.login(str(self.token_dir))
            else:
                # Fresh login
                logger.info("No valid tokens found. Performing fresh login.")
                self.api = Garmin(self.email, self.password, is_cn=False, return_on_mfa=True)
                result1, result2 = self.api.login()

                if result1 == "needs_mfa":
                    mfa_code = input("Please enter your Garmin MFA code: ")
                    self.api.resume_login(result2, mfa_code)
                
                # Save tokens
                self.token_dir.mkdir(parents=True, exist_ok=True)
                self.api.garth.dump(str(self.token_dir))
                
            logger.info("Successfully authenticated.")

        except (GarminConnectAuthenticationError, GarthHTTPError) as e:
            logger.error(f"Authentication failed: {e}. Check your credentials.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            sys.exit(1)

    def _safe_call(self, func, *args, **kwargs) -> Any:
        """Execute API call with defensive error handling."""
        try:
            return func(*args, **kwargs)
        except GarminConnectTooManyRequestsError:
            logger.error("Rate limit exceeded. Please wait before trying again.")
            sys.exit(1)
        except GarminConnectConnectionError as e:
            logger.error(f"Connection error to Garmin: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"API call failed: {e}")
            sys.exit(1)

    def save_to_file(self, activities: List[ActivitySummary], filename: str = "garmin_data.json") -> None:
        """Pass the retrieved data to the storage utility for saving to disk."""
        save_activities(activities, filename)

    def load_from_file(self, filename: str = "garmin_data.json") -> List[dict]:
        """Load activity data from storage."""
        return load_activities(filename)

    def fetch_running_activities(self, days: int = 180) -> List[ActivitySummary]:
        """Fetch running activities from the last N days with lap data."""
        if not self.api:
            self.login()

        start_date = datetime.now() - timedelta(days=days)
        activities_data: List[ActivitySummary] = []
        
        start = 0
        limit = 20
        keep_fetching = True

        logger.info(f"Fetching activities since {start_date.date()}...")

        while keep_fetching:
            batch = self._safe_call(self.api.get_activities, start, limit)
            if not batch:
                break

            for act in batch:
                # Check date
                start_time_str = act.get("startTimeLocal")
                if not start_time_str:
                    continue
                
                act_date = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
                if act_date < start_date:
                    keep_fetching = False
                    break

                # Filter for running
                activity_type_key = act.get("activityType", {}).get("typeKey", "").lower()
                if "running" in activity_type_key:
                    activity_id = act["activityId"]
                    logger.info(f"Processing activity {activity_id}: {act.get('activityName')}")
                    
                    # Fetch Splits/Laps
                    splits = self._safe_call(self.api.get_activity_splits, activity_id)
                    laps_raw = splits.get("lapSplits", []) if isinstance(splits, dict) else []
                    laps = [
                        LapData(
                            lapNumber=l.get("lapIndex", 0),
                            startTime=l.get("startTimeGMT", ""),
                            distance=l.get("distance", 0.0),
                            duration=l.get("duration", 0.0),
                            averageSpeed=l.get("averageSpeed", 0.0),
                            averageHR=l.get("averageHeartRate", 0.0)
                        )
                        for l in laps_raw
                    ]

                    # Fallback to activity details if no laps found (common for some running types like Treadmill)
                    if not laps:
                        details = self._safe_call(self.api.get_activity_details, activity_id)
                        laps_raw = details.get("lapDTOs", []) if isinstance(details, dict) else []
                        laps = [
                            LapData(
                                lapNumber=l.get("lapIndex", 0),
                                startTime=l.get("startTimeGMT", ""),
                                distance=l.get("distance", 0.0),
                                duration=l.get("duration", 0.0),
                                averageSpeed=l.get("averageSpeed", 0.0),
                                averageHR=l.get("averageHeartRate", 0.0)
                            )
                            for l in laps_raw
                        ]

                    # Final fallback: Create a synthetic lap from activity summary if no laps were found
                    if not laps:
                        logger.info(f"No lap data found for activity {activity_id}, creating synthetic lap.")
                        laps = [
                            LapData(
                                lapNumber=1,
                                startTime=act.get("startTimeGMT", start_time_str),
                                distance=act.get("distance", 0.0),
                                duration=act.get("duration", 0.0),
                                averageSpeed=act.get("averageSpeed", 0.0),
                                averageHR=act.get("averageHR", 0.0)
                            )
                        ]

                    activities_data.append(
                        ActivitySummary(
                            activityId=activity_id,
                            activityName=act.get("activityName", "Unnamed"),
                            activityType=activity_type_key,
                            startTimeLocal=start_time_str,
                            distance=act.get("distance", 0.0),
                            duration=act.get("duration", 0.0),
                            averageHR=act.get("averageHR", 0.0),
                            maxHR=act.get("maxHR", 0.0),
                            averageSpeed=act.get("averageSpeed", 0.0),
                            laps=laps
                        )
                    )

            start += limit

        return activities_data