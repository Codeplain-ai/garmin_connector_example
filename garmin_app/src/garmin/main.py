"""🏃‍♂️ Entry point to execute the Functional Requirement."""

import sys
import logging
from src.garmin.client import GarminClient
from src.garmin.storage import load_activities

def main():
    """Execute the Garmin running data retrieval and persistence."""
    # Configure logging to display progress updates to the user
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    client = GarminClient()
    
    # 1. Fetch activities
    activities = client.fetch_running_activities(days=180)
    print(f"\n✅ Successfully retrieved {len(activities)} running activities.")
    
    # 2. Save to file via GarminClient
    data_file = "garmin_data.json"
    client.save_to_file(activities, data_file)
    
    # 3. Load from file (verifying the functional requirement)
    loaded_data = load_activities(data_file)
    print(f"📂 Loaded {len(loaded_data)} activities from {data_file}.")
    
    for activity in loaded_data:
        print(f"- {activity['startTimeLocal']}: {activity['activityName']} ({len(activity['laps'])} laps)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)