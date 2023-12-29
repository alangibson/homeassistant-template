""""""

from typing import Any

class HACSTemplateConnection:
    """All connection management logic should go in this class"""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry):
        self._hass = hass
        self._config_entry = config_entry

    async def connect(self) -> tuple[bool, KWBHeater | Exception]:

        try:
            signal_maps = load_signal_maps()
            heater = KWBHeater(config_heater, signal_maps)
            is_success = heater.scrape()
        except Exception as e:
            logger.error("Error connecting to heater: %s" % e)
            return False, e

        return is_success, heater

    async def poll(self) -> dict[str, Any]:
        """Poll for new data"""
        return {}

    async def disconnect(self):
        """Disconnect from device"""
        pass