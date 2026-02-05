import os
import sys
import json
from google import genai
from typing import List, Dict, Any

class LLMClient:
    """Service to interface with Google Gemini for Garmin data analysis."""
    
    def __init__(self, model_id: str = "gemini-2.0-flash"):
        api_key = os.getenv("GOOGLE_API_KEY", "").strip()
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable is not set.", file=sys.stderr)
            sys.exit(1)
        
        try:
            self.client = genai.Client(api_key=api_key)
            self.model_id = model_id
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            sys.exit(1)

    def create_chat_session(self, activity_data: List[Dict[str, Any]]):
        """
        Initializes a chat session with the Garmin activity data provided as context.
        """
        # Convert activity data to a compact JSON string for the prompt
        context_json = json.dumps(activity_data, indent=2)
        
        system_instructions = (
            "You are a personal running coach and data analyst. "
            "The following is a JSON representation of the user's Garmin running activities "
            "from the last 180 days, including lap-by-lap details.\n\n"
            f"DATA:\n{context_json}\n\n"
            "INSTRUCTIONS:\n"
            "1. Answer questions specifically based on the provided runs, laps, heart rate, and speed data.\n"
            "2. If the user asks about trends, analyze the data to provide insights.\n"
            "3. If information is not available in the data, state that clearly.\n"
            "4. Be concise but encouraging."
        )

        try:
            # Start a chat session using the new SDK pattern
            chat = self.client.chats.create(
                model=self.model_id,
                config={'system_instruction': system_instructions}
            )
            return chat
        except Exception as e:
            print(f"Failed to initialize ChatSession: {e}")
            sys.exit(1)

    @staticmethod
    def get_user_input() -> str:
        """Get input from user with specific color."""
        # Blue for User input prompt
        return input("\033[94mUser: \033[0m")

    @staticmethod
    def print_llm_response(response_stream):
        """Print LLM response from a stream with specific color."""
        # Green for LLM response prefix
        print("\033[92mCoach: ", end="", flush=True)
        try:
            for chunk in response_stream:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
        except Exception as e:
            print(f"\n[Error during streaming: {e}]", end="")
        
        # Reset color and add final newline
        print("\033[0m\n")