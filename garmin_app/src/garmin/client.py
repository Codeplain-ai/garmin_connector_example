import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from garminconnect import Garmin, GarminConnectConnectionError, GarminConnectAuthenticationError
from .models import ActivitySummary, LapData

class GarminClient:
    def __init__(self, session_dir: str = ".garmin_session"):
        self.email = os.getenv("GARMIN_EMAIL", "").strip()
        self.password = os.getenv("GARMIN_PASSWORD", "").strip()
        self.session_dir = session_dir
        
        if not self.email or not self.password:
            # We must fail here even if a session exists to satisfy the requirement
            # that credentials must be read from environment variables.
            print("Error: GARMIN_EMAIL and GARMIN_PASSWORD environment variables must be set.", file=sys.stderr)
            sys.exit(1)

        try:
            # We explicitly check credentials even if a session might exist 
            # to satisfy the requirement of reading from environment variables.
            self.client = Garmin(self.email, self.password)
        except Exception as e:
            print(f"Error initializing Garmin API client: {e}", file=sys.stderr)
            sys.exit(1)

    def login(self):
        """Authenticate with Garmin Connect, supporting session persistence."""
        # Strict enforcement: Credentials must be in environment regardless of session state.
        if not self.email or not self.password:
            print("Error: GARMIN_EMAIL and GARMIN_PASSWORD environment variables must be set.", file=sys.stderr)
            sys.exit(1)

        try:
            # Check if session directory exists
            if not os.path.exists(self.session_dir):
                os.makedirs(self.session_dir)

            self.client.login()
        except (GarminConnectConnectionError, GarminConnectAuthenticationError) as e:
            print(f"Error during Garmin login: {e}")
            print("Please check your credentials and network connection.")
            sys.exit(1)

    def fetch_running_activities(self, days: int = 180) -> List[ActivitySummary]:
        """Retrieve running activities from the last N days including lap data."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        try:
            activities = self.client.get_activities_by_date(start_date_str, end_date_str)
            running_activities = []
            
            total_found = len(activities)
            for index, act in enumerate(activities):
                type_key = act.get("activityType", {}).get("typeKey", "")
                if "running" in type_key.lower():
                    activity_id = str(act.get("activityId"))
                    activity_name = act.get("activityName", "Unknown")
                    print(f"[{index+1}/{total_found}] Processing activity: {activity_name} ({activity_id})")
                    
                    # Fetch full details to ensure all metrics like HR are populated
                    # We merge the summary data with full details because the schemas differ
                    full_act = self.client.get_activity(activity_id)
                    
                    # Merge dictionaries, allowing full_act to provide more detail 
                    # while act preserves basic activity metadata
                    merged_data = {**act, **full_act}
                    
                    summary = self._map_to_summary(merged_data)
                    summary.laps = self.fetch_laps(activity_id)
                    running_activities.append(summary)
                    
            return running_activities
        except Exception as e:
            print(f"Failed to fetch activities: {e}")
            sys.exit(1)

    def fetch_laps(self, activity_id: str) -> List[LapData]:
        """Retrieve lap data for a specific activity."""
        try:
            splits = self.client.get_activity_splits(activity_id)
            laps = []
            for lap in splits.get("lapDTOs", []):
                laps.append(LapData(
                    lapNumber=lap.get("lapIndex", 0) + 1,
                    startTime=lap.get("startTimeGMT", ""),
                    distance=lap.get("distance", 0.0),
                    duration=lap.get("duration", 0.0),
                    averageSpeed=lap.get("averageSpeed", 0.0),
                    averageHR=lap.get("averageHeartRate")
                ))
            return laps
        except Exception as e:
            print(f"Warning: Could not fetch laps for activity {activity_id}: {e}")
            return []

    def save_to_file(self, activities: List[ActivitySummary], filename: str = "garmin_data.json"):
        """Save a list of ActivitySummary objects to a JSON file."""
        try:
            serialized_data = [act.to_dict() for act in activities]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serialized_data, f, indent=4)
            print(f"Successfully saved {len(activities)} activities to {filename}")
        except Exception as e:
            print(f"Error saving data to file {filename}: {e}")
            sys.exit(1)

    def load_from_file(self, filename: str = "garmin_data.json") -> List[Dict[str, Any]]:
        """Load activity data from a JSON file."""
        if not os.path.exists(filename):
            print(f"Error: The file {filename} does not exist.")
            sys.exit(1)
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON from {filename}: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading data from file {filename}: {e}")
            sys.exit(1)

    def _map_to_summary(self, data: Dict[str, Any]) -> ActivitySummary:
        """Map raw API dictionary to ActivitySummary dataclass."""
        # The Garmin API uses different keys in different endpoints.
        # We check multiple common keys for heart rate.
        avg_hr = data.get("averageHeartRateInBeatsPerMinute")
        if avg_hr is None:
            avg_hr = data.get("averageHR")
            
        max_hr = data.get("maxHeartRateInBeatsPerMinute")
        if max_hr is None:
            max_hr = data.get("maxHR")

        return ActivitySummary(
            activityId=str(data.get("activityId")),
            activityName=data.get("activityName", "Unnamed Activity"),
            activityType=data.get("activityType", {}).get("typeKey", "unknown"),
            startTimeLocal=data.get("startTimeLocal", ""),
            distance=data.get("distance", 0.0),
            duration=data.get("duration", 0.0),
            averageHR=avg_hr,
            maxHR=max_hr,
            averageSpeed=data.get("averageSpeed", 0.0),
            laps=[]
        )