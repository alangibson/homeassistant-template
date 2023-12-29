import time
from datetime import datetime

class DemoApi:

    def fetch_data(self) -> dict:
        """Creates fake data"""
        return {
            'timestamp': datetime.now(),
            'timestamp_ms': time.time_ns() / 1000000
        }
    