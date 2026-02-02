"""🏃‍♂️ Main application entry point for GarminChatApp."""

import json
import logging
import sys
from src.garmin.client import GarminClient
from src.llm.chat import ChatSession

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class GarminChatApp:
    """Core application logic coordinating data fetching and chat orchestration."""

    def __init__(self, data_file: str = "garmin_data.json"):
        self.data_file = data_file
        self.client = GarminClient()

    def fetch_workflow(self):
        """Execute the data fetch workflow."""
        logging.info("Starting Garmin data fetch workflow...")
        # 1. Fetch activities (includes login internally if needed)
        activities = self.client.fetch_running_activities(days=180)
        
        # 2. Save to file
        logging.info(f"Saving {len(activities)} activities to '{self.data_file}'...")
        self.client.save_to_file(activities, self.data_file)
        print(f"✅ Data successfully saved to {self.data_file}")

    def chat_workflow(self):
        """Execute the chat workflow."""
        logging.info("Starting Garmin chat workflow...")
        # 1. Load stored activity data
        activities = self.client.load_from_file(self.data_file)
        
        # 2. Convert to compact JSON string for LLM context
        context_payload = json.dumps(activities, separators=(',', ':'))
        
        # 3. Initialize and start the chat session
        chat = ChatSession(context_payload)
        chat.start()

    def run_all(self):
        """Run fetch followed by chat."""
        self.fetch_workflow()
        print("\n" + "="*40 + "\n")
        self.chat_workflow()