"""🏃‍♂️ Unit tests for GarminClient logic."""

import unittest
from unittest.mock import MagicMock, patch
from src.garmin.client import GarminClient
from src.garmin.storage import save_activities, load_activities
from src.garmin.models import ActivitySummary, LapData
import json
import os

class TestGarminStorage(unittest.TestCase):
    """Test suite for Garmin data persistence."""

    def setUp(self):
        self.test_file = "test_data.json"
        self.sample_activities = [
            ActivitySummary(
                activityId=1,
                activityName="Run 1",
                activityType="running",
                startTimeLocal="2026-02-01 08:00:00",
                distance=5000.0,
                duration=1500.0,
                averageHR=150.0,
                maxHR=170.0,
                averageSpeed=3.33,
                laps=[
                    LapData(1, "08:00:00", 5000.0, 1500.0, 3.33, 150.0)
                ]
            )
        ]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_success(self):
        """Test that data is correctly serialized and deserialized."""
        save_activities(self.sample_activities, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        loaded = load_activities(self.test_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["activityId"], 1)
        self.assertEqual(loaded[0]["laps"][0]["lapNumber"], 1)

    @patch('sys.exit')
    def test_load_file_not_found(self, mock_exit):
        """Test that missing file triggers an exit."""
        load_activities("non_existent_file.json")
        mock_exit.assert_called_with(1)

    @patch('sys.exit')
    def test_load_corrupted_json(self, mock_exit):
        """Test that corrupted JSON triggers an exit."""
        with open(self.test_file, 'w') as f:
            f.write("{ invalid json")
        
        load_activities(self.test_file)
        mock_exit.assert_called_with(1)

class TestGarminClient(unittest.TestCase):
    """Test suite for Garmin data processing."""

    def setUp(self):
        # Patch environment variables
        self.env_patcher = patch.dict('os.environ', {
            'GARMIN_EMAIL': 'test@example.com',
            'GARMIN_PASSWORD': 'password123',
            'GOOGLE_API_KEY': 'ai_key'
        })
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @patch('src.garmin.client.Garmin')
    def test_fetch_running_activities_filtering(self, mock_garmin_class):
        """Test that only 'running' activities are filtered and mapped."""
        mock_api = MagicMock()
        mock_garmin_class.return_value = mock_api
        
        # Mocking get_activities to return one running and one cycling
        mock_api.get_activities.return_value = [
            {
                "activityId": 101,
                "activityName": "Morning Run",
                "activityType": {"typeKey": "running"},
                "startTimeLocal": "2026-02-01 08:00:00",
                "distance": 5000.0,
                "duration": 1500.0
            },
            {
                "activityId": 102,
                "activityName": "Bike Ride",
                "activityType": {"typeKey": "cycling"},
                "startTimeLocal": "2026-02-01 10:00:00",
                "distance": 20000.0,
                "duration": 3600.0
            }
        ]
        
        # Mocking laps
        mock_api.get_activity_laps.return_value = [
            {"lapIndex": 1, "distance": 5000.0, "duration": 1500.0}
        ]

        client = GarminClient(token_dir="/tmp/garmin_test")
        client.api = mock_api # Skip login for unit test
        
        results = client.fetch_running_activities(days=10)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].activityId, 101)
        self.assertEqual(results[0].activityType, "running")
        self.assertEqual(len(results[0].laps), 1)

if __name__ == '__main__':
    unittest.main()