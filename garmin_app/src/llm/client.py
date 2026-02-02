"""🤖 LLM Client implementation for Google Gemini."""

import os
import sys
import logging
from typing import Optional
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class LLMClient:
    """Service to interface with Google Gemini."""

    def __init__(self, model_id: str = "gemini-3-flash-preview"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.error("CRITICAL: GOOGLE_API_KEY environment variable is not set.")
            sys.exit(1)
        
        try:
            self.client = genai.Client(api_key=self.api_key)
            self.model_id = model_id
        except Exception as e:
            logger.error(f"CRITICAL: Failed to initialize Google GenAI Client: {e}")
            sys.exit(1)

    def create_chat_session(self, context_data: str):
        """Creates a chat session with the Garmin data as context.
        
        Args:
            context_data: Stringified JSON of Garmin activities.
        """
        # Authoritative system instruction
        system_instruction = (
            "You are a specialized Garmin Running Analyst. "
            "The user HAS PROVIDED their Garmin activity data below in JSON format. "
            "You MUST use this provided data to answer all questions. "
            "DO NOT claim you do not have access to the user's data, as it is provided directly here. "
            "Answer questions specifically about the runs, laps, heart rate, and speed found in the data. "
            "If the information is not in the data (like shoe brands or gear), state that it's not provided."
        )

        # History preamble to ensure context persistence even if config is overridden
        history = [
            types.Content(
                role="user",
                parts=[types.Part(text=(
                    f"I am providing my Garmin running data for the last 180 days in JSON format. "
                    f"Please analyze this data and answer my questions based ONLY on it.\n\n"
                    f"--- DATA START ---\n{context_data}\n--- DATA END ---"
                ))]
            ),
            types.Content(
                role="model",
                parts=[types.Part(text=(
                    "I have received your Garmin running data. I am ready to analyze it and answer "
                    "specific questions about your runs, laps, heart rate, and speed based on the JSON provided."
                ))]
            )
        ]
        
        try:
            # Using the chat session feature of the google-genai SDK
            return self.client.chats.create(
                model=self.model_id,
                history=history,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2,
                )
            )
        except Exception as e:
            logger.error(f"CRITICAL: Failed to initiate LLM Chat Session: {e}")
            sys.exit(1)