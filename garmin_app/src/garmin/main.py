from .client import GarminClient

def main():
    """Main entry point for Garmin data retrieval."""
    client = GarminClient()
    client.login()
    
    print("Fetching running activities from the last 180 days...")
    activities = client.fetch_running_activities(days=180)
    
    print(f"Found {len(activities)} running activities.")
    
    # Save activities to file
    data_file = "garmin_data.json"
    client.save_to_file(activities, data_file)
    
    # Load activities from file to verify
    loaded_activities = client.load_from_file(data_file)
    print(f"Successfully reloaded {len(loaded_activities)} activities from {data_file}.")

if __name__ == "__main__":
    main()