import sys
from ..garmin.client import GarminClient

def run_data_fetch_workflow():
    """
    Executes the data fetch workflow:
    1. Initializes GarminClient
    2. Logins to Garmin Connect
    3. Fetches running activities and laps (with progress updates)
    4. Saves data to disk
    """
    print("--- Garmin Data Fetch Workflow Started ---")
    
    try:
        # 1. Initialize
        client = GarminClient()
        
        # 2. Login
        print("Authenticating with Garmin Connect...")
        client.login()
        print("Authentication successful.")
        
        # 3. Fetch Data
        days = 180
        print(f"Fetching running activities from the last {days} days...")
        # Note: Progress updates are handled inside fetch_running_activities
        activities = client.fetch_running_activities(days=days)
        
        if not activities:
            print("No running activities found in the specified period.")
            return

        print(f"Successfully retrieved {len(activities)} activities.")
        
        # 4. Save to disk
        data_file = "garmin_data.json"
        print(f"Saving data to {data_file}...")
        client.save_to_file(activities, data_file)
        
        print("--- Workflow Completed Successfully ---")
        
    except SystemExit as e:
        raise e
    except Exception as e:
        print(f"Critical error during workflow execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_data_fetch_workflow()