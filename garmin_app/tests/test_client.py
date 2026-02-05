import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.garmin.client import GarminClient

class TestGarminClient(unittest.TestCase):
    def setUp(self):
        # Patch environment variables
        self.env_patcher = patch.dict('os.environ', {
            'GARMIN_EMAIL': 'test@example.com',
            'GARMIN_PASSWORD': 'password123'
        })
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('src.garmin.client.Garmin')
    def test_login_failure(self, mock_garmin, mock_makedirs, mock_exists):
        from garminconnect import GarminConnectAuthenticationError
        instance = mock_garmin.return_value
        instance.login.side_effect = GarminConnectAuthenticationError("Auth failed")
        mock_exists.return_value = False
        
        client = GarminClient()
        with self.assertRaises(SystemExit) as cm:
            client.login()
        self.assertEqual(cm.exception.code, 1)

    @patch('src.garmin.client.Garmin')
    def test_fetch_running_activities_filtering(self, mock_garmin):
        instance = mock_garmin.return_value
        activities_data = [
            {"activityId": 1, "activityType": {"typeKey": "running"}, "distance": 5000},
            {"activityId": 2, "activityType": {"typeKey": "cycling"}, "distance": 20000},
            {"activityId": 3, "activityType": {"typeKey": "trail_running"}, "distance": 10000}
        ]
        instance.get_activities_by_date.return_value = activities_data
        
        # Mock get_activity to return the item being requested
        def get_activity_mock(activity_id):
            for a in activities_data:
                if str(a["activityId"]) == str(activity_id):
                    return a
            return {}
            
        instance.get_activity.side_effect = get_activity_mock
        instance.get_activity_splits.return_value = {"lapDTOs": []}
        
        client = GarminClient()
        activities = client.fetch_running_activities()
        
        # Should find 'running' and 'trail_running'
        self.assertEqual(len(activities), 2)
        self.assertEqual(activities[0].activityId, "1")
        self.assertEqual(activities[1].activityId, "3")

if __name__ == '__main__':
    unittest.main()