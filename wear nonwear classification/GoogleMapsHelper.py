from datetime import datetime
import json

class GoogleMapsHelper:
    def __init__(self):
        with open('../data/google_timeline_25_1.json', 'r') as file:
            self.data = [item for item in json.loads(file.read()) if 'activity' in item] # Include only activity objects

    def get_activity_for_timestamp(self, timestamp):
        for record in self.data:
            start_date = datetime.fromisoformat(record['startTime'])
            end_date = datetime.fromisoformat(record['endTime'])
            if start_date <= timestamp <= end_date:
                return record['activity']
