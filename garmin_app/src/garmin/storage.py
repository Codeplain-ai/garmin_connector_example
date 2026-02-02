"""🏃‍♂️ Storage utilities for saving and loading Garmin activity data."""

import json
import logging
import sys
from pathlib import Path
from typing import List, Any
from dataclasses import asdict
from src.garmin.models import ActivitySummary

logger = logging.getLogger(__name__)

def save_activities(activities: List[ActivitySummary], filename: str = "garmin_data.json") -> None:
    """Serialize ActivitySummary list to JSON and write to file, overwriting existing data.
    
    Args:
        activities: List of ActivitySummary objects to save.
        filename: Target JSON file path.
    """
    try:
        # Convert dataclasses to dictionary format recursively
        serialized_data = [asdict(activity) for activity in activities]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serialized_data, f, indent=4, ensure_ascii=False)
            
        logger.info("Successfully saved %d activities to '%s'.", len(activities), filename)
    except Exception as e:
        logger.error("CRITICAL: Failed to save activity data to '%s'. Error: %s", filename, str(e))
        sys.exit(1)

def load_activities(filename: str = "garmin_data.json") -> List[dict]:
    """Load activity data from a JSON file for use by the LLM.
    
    Args:
        filename: Path to the JSON data file.
        
    Returns:
        List of dictionaries representing the activity data.
    """
    file_path = Path(filename)
    
    if not file_path.exists():
        logger.error("CRITICAL: Data file '%s' not found. Please run the fetch process first.", filename)
        sys.exit(1)
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            logger.error("CRITICAL: Data file '%s' format is invalid. Expected a list of activities.", filename)
            sys.exit(1)
            
        return data
    except json.JSONDecodeError as e:
        logger.error("CRITICAL: Data file '%s' is corrupted or contains invalid JSON. Error: %s", filename, str(e))
        sys.exit(1)
    except Exception as e:
        logger.error("CRITICAL: Unexpected error while loading data from '%s'. Error: %s", filename, str(e))
        sys.exit(1)