"""🧪 Unit tests for LLM functionality."""

import unittest
from unittest.mock import patch, MagicMock
import os
from src.llm.client import LLMClient

class TestLLMClient(unittest.TestCase):
    """Tests for the LLMClient initialization and session creation."""

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"})
    @patch("google.genai.Client")
    def test_client_initialization(self, mock_genai):
        """Test that the client initializes with the correct API key."""
        client = LLMClient()
        mock_genai.assert_called_once_with(api_key="test_key")
        self.assertEqual(client.model_id, "gemini-3-flash-preview")

    @patch.dict(os.environ, {"GOOGLE_API_KEY": "test_key"})
    @patch("google.genai.Client")
    def test_create_chat_session(self, mock_genai):
        """Test the structure of session creation."""
        mock_client_instance = MagicMock()
        mock_genai.return_value = mock_client_instance
        
        client = LLMClient()
        context = '[{"activityName": "Morning Run"}]'
        client.create_chat_session(context)
        
        mock_client_instance.chats.create.assert_called_once()
        args, kwargs = mock_client_instance.chats.create.call_args
        self.assertEqual(kwargs['model'], "gemini-3-flash-preview")
        self.assertIn("Garmin Running Analyst", kwargs['config'].system_instruction)

if __name__ == "__main__":
    unittest.main()