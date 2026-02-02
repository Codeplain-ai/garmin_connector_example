"""💬 Interactive Chat Session for Garmin Data Analysis."""

import sys
import logging
from src.llm.client import LLMClient

# ANSI Color Codes
CLR_USER = "\033[94m"    # Blue
CLR_LLM = "\033[92m"     # Green
CLR_RESET = "\033[0m"
CLR_ERROR = "\033[91m"   # Red
CLR_INFO = "\033[93m"    # Yellow

logger = logging.getLogger(__name__)

class ChatSession:
    """Orchestrates the interactive conversation state."""

    def __init__(self, context_json: str):
        self.llm_client = LLMClient()
        self.session = self.llm_client.create_chat_session(context_json)

    def start(self):
        """Starts the interactive CLI loop."""
        print(f"{CLR_INFO}--- Garmin Running Analyst Connected ---{CLR_RESET}")
        print("Type 'exit' or 'quit' to end the session.\n")

        while True:
            try:
                user_input = input(f"{CLR_USER}You: {CLR_RESET}").strip()
                
                if user_input.lower() in ["exit", "quit"]:
                    print(f"{CLR_INFO}Goodbye!{CLR_RESET}")
                    break
                
                if not user_input:
                    continue

                print(f"{CLR_LLM}Gemini: ", end="", flush=True)
                
                for chunk in self.session.send_message_stream(user_input):
                    if chunk.text:
                        print(chunk.text, end="", flush=True)
                print(f"{CLR_RESET}\n")

            except KeyboardInterrupt:
                print(f"\n{CLR_INFO}Session ended by user.{CLR_RESET}")
                break
            except Exception as e:
                print(f"\n{CLR_ERROR}Error during LLM interaction: {e}{CLR_RESET}")
                logger.error(f"LLM Call failed: {e}", exc_info=True)
                sys.exit(1)