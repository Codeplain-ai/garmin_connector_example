import sys
from src.app_flow.garmin_flow import run_data_fetch_workflow
from src.app_flow.chat_flow import run_chat_workflow

def main():
    """
    Main entry point for the Garmin Chat application.
    Sequences the data retrieval and the interactive AI chat.
    """
    try:
        # Step 1: Fetch and Save Data
        run_data_fetch_workflow()
        
        # Step 2: Start Chat Session
        run_chat_workflow()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except SystemExit as e:
        # Ensure we exit with the code provided, handling both int and None
        sys.exit(e.code if e.code is not None else 1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()