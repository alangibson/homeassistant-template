import time
from datetime import datetime


class DemoApiConnectException(Exception):
    """Demonstration connect exception"""


class DemoApiAuthenticationException(Exception):
    """Demonstration authentication exception"""


class DemoApi:
    def __init__(self, config_options):
        self._config_options = config_options

    def connect(self):
        if self._config_options.get("always_error_on_connect", False):
            raise DemoApiConnectException("Requested always_error_on_connect")

    def fetch_data(self) -> dict:
        """Creates fake data"""
        return {"timestamp": datetime.now(), "timestamp_ms": time.time_ns() / 1000000}
