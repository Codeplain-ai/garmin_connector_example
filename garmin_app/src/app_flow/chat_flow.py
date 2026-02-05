import sys
import os
from src.garmin.client import GarminClient
from src.llm.client import LLMClient

def run_chat_workflow():
    """
    Executes the chat workflow:
    1. Loads stored activity data via GarminClient
    2. Initializes LLMClient with the loaded data
    3. Starts an interactive loop for user input
    """
    print("--- Garmin AI Coach Chat Workflow Started ---")
    
    garmin_client = GarminClient()
    data_file = "garmin_data.json"
    
    # 1. Load stored activity data
    if not os.path.exists(data_file):
        print(f"Error: Data file '{data_file}' not found.")
        print("Please run the data fetch workflow first: python -m src.app_flow.garmin_flow")
        sys.exit(1)
        
    try:
        print(f"Loading activity data from {data_file}...")
        activities = garmin_client.load_from_file(data_file)
        print(f"Loaded {len(activities)} activities.")

        # 2. Initialize LLMClient
        print("Initializing AI Coach with your Garmin context...")
        llm_client = LLMClient()
        chat_session = llm_client.create_chat_session(activities)
    except SystemExit as e:
        raise e
    except Exception as e:
        print(f"Critical error during chat workflow initialization: {e}", file=sys.stderr)
        sys.exit(1)
    
    print("\n--- Session Ready ---")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    # 3. Interactive Loop
    while True:
        try:
            user_message = llm_client.get_user_input()
            
            if user_message.lower() in ['exit', 'quit']:
                print("Closing chat. Keep up the training!")
                break
                
            if not user_message.strip():
                continue

            response_stream = chat_session.send_message_stream(message=user_message)
            llm_client.print_llm_response(response_stream)
            
        except KeyboardInterrupt:
            print("\nChat interrupted by user.")
            break
        except SystemExit as e:
            raise e
        except Exception as e:
            print(f"\033[91mError during chat interaction: {e}\033[0m", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    run_chat_workflow()