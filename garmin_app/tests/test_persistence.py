import unittest
import os
import json
from src.garmin.client import GarminClient
from src.garmin.models import ActivitySummary, LapData

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_garmin_data.json"
        os.environ['GARMIN_EMAIL'] = "test@example.com"
        os.environ['GARMIN_PASSWORD'] = "test_pass"
        self.client = GarminClient()
        
        # Create dummy data
        lap = LapData(1, "2024-01-01T10:00:00", 1000.0, 300.0, 3.33, 150.0)
        self.activities = [
            ActivitySummary(
                "123", "Morning Run", "running", "2024-01-01T10:00:00",
                5000.0, 1800.0, 160.0, 180.0, 2.77, [lap]
            )
        ]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        # Test Save
        self.client.save_to_file(self.activities, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Test Load
        loaded_data = self.client.load_from_file(self.test_file)
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]['activityId'], "123")
        self.assertEqual(len(loaded_data[0]['laps']), 1)
        self.assertEqual(loaded_data[0]['laps'][0]['distance'], 1000.0)

    def test_load_non_existent_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.client.load_from_file("non_existent.json")
        self.assertEqual(cm.exception.code, 1)

    def test_load_corrupted_file(self):
        with open(self.test_file, 'w') as f:
            f.write("{ invalid json }")
        
        with self.assertRaises(SystemExit) as cm:
            self.client.load_from_file(self.test_file)
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()