"""API for managing a connection to a device.

This file is provided by HomeAssistant Template.
You shold modify the method definitions to connect HomeAssistant
to your 3rd party communciation library.
"""

import logging
import time
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.const import CONF_UNIQUE_ID

from .demo.api import DemoApi, DemoApiAuthenticationException
from .flows.config.schema import CONF_FORCE_CONNECTION_ERROR

logger = logging.getLogger(__name__)


class HACSTemplateDevice:
    """All connection management logic should go in this class."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        self._hass = hass
        self._config = config

        logger.debug(
            "force connection error: %s",
            config.get(CONF_FORCE_CONNECTION_ERROR),
        )

        # TODO Create a reference to your 3rd party library here
        self._api = DemoApi(
            {"always_error_on_connect": config.get(CONF_FORCE_CONNECTION_ERROR)}
        )

    async def connect(self) -> bool:
        """Connect to device.

        Return True if connection succeeded, otherwixe raise an exception"""
        # TODO connect to your device here
        self._api.connect()
        return True

    async def poll(self) -> dict[str, Any]:
        """Poll for new data."""
        # TODO poll for current state here
        return {}

    async def disconnect(self):
        """Disconnect from device."""
        # TODO disconnect from your device here

    async def test(self) -> bool:
        """Test connection and guarantee disconnect is called"""

        logger.debug("Entering test()")

        error = None
        success = None
        try:
            success = await self.connect()
        except Exception as e:
            error = e
        finally:
            await self.disconnect()

        logger.debug("Exiting test() error=%s success=%s", error, success)

        if error:
            raise error
        else:
            return success

    async def get_unique_id(self) -> str:
        """Return a unique, unchanging id for this device.

        This id should never change and the user should not be
        able to change it.

        https://developers.home-assistant.io/docs/entity_registry_index/#unique-id
        https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#unique-id-requirements
        """
        # TODO return a unique id
        return self._config.get(CONF_UNIQUE_ID)
