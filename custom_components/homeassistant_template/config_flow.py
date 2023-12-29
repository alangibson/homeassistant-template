"""Config flow."""

from __future__ import annotations

import logging
import time
from typing import Any, Dict

from homeassistant.config_entries import (
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
)
from homeassistant.core import (
    HomeAssistant,
    callback
)

from .src.const import (
    DEFAULT_NAME,
    DOMAIN,
)
from .src.config import DEVICE_HAS_UNIQUE_ID
from .src.flow.config.schema import DATA_SCHEMA
from .src.flow.config import validate
from .src.flow.options.options import HACSTemplateOptionsFlow


logger = logging.getLogger(__name__)


class HACSTemplateConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow definition."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def validate_input(
        self, hass: HomeAssistant, user_input: dict = None
    ) -> dict[str, Any]:
        """Validate that the user input allows us to connect to the heater.
        Data has the keys from DATA_SCHEMA with values provided by the user.
        """

        # Don't do anything if we don't have a configuration
        if not user_input:
            return None

        # Accumulate validation errors. Key is name of field from DATA_SCHEMA
        errors = validate.validate_input(hass, user_input)

        if errors and len(errors.keys()) > 0:
            return errors

        # Do a test connection to your device here
        errors = validate.validate_connection(hass, user_input)

        return errors

    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface 
        or when discovered and the matching and discovery step are not defined.

        Either show config data entry form to the user, or create a config entry.
        """

        # Either show modal form, or create config entry then move on
        if not user_input:  # Just show the modal form and return if no user input
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
        else:
            # We got user input, so do something with it

            # Validate inputs and do a test connection/scrape of the heater
            # Both info and errors are None when config flow is first invoked
            errors = await self.validate_input(self.hass, user_input)

            # Either display errors in form, or close form and create config entry
            if len(errors.keys()) > 0:
                # If there is no user input or there were errors, show the form again,
                # including any errors that were found with the input.
                return self.async_show_form(
                    step_id="user", data_schema=DATA_SCHEMA, errors=errors
                )
            else:
                if DEVICE_HAS_UNIQUE_ID:
                    # TODO Figure out a unique id (that never changes!) for the device
                    # unique_device_id = user_input.get(CONF_UNIQUE_ID)
                    
                    unique_device_id = ...

                    await self.async_set_unique_id(unique_device_id)
                    # TODO we can update CONF_* properties in the updates dict
                    updates = {}
                    self._abort_if_unique_id_configured(updates=updates)
                else:
                    await self._async_handle_discovery_without_unique_id()

                # Forward user input on to create a device.
                # Results in async_setup_entry() in the platform file being called.
                return self.async_create_entry(title=DEFAULT_NAME, data=user_input)

    async def async_step_bluetooth(self, user_input=None):
        """Invoked if your integration has been discovered via Bluetooth as specified using bluetooth in the manifest.

        https://developers.home-assistant.io/docs/creating_integration_manifest#bluetooth
        """

    async def async_step_dhcp(self, user_input=None):
        """Invoked if your integration has been discovered via DHCP as specified using dhcp in the manifest.

        https://developers.home-assistant.io/docs/creating_integration_manifest#dhcp
        """

    async def async_step_hassio(self, user_input=None):
        """Invoked if your integration has been discovered via a Supervisor add-on."""

    async def async_step_homekit(self, user_input=None):
        """Invoked if your integration has been discovered via DHCP as specified using dhcp in the manifest.

        https://developers.home-assistant.io/docs/creating_integration_manifest#homekit
        """

    async def async_step_unignore(self, user_input = None):
        """Invoked when an discovered device should be unignored

        https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#unignoring
        """

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Create the options flow."""
        return HACSTemplateOptionsFlow(config_entry)


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Invoked when VERSION and/or MINOR_VERION numbers are changed
    
    https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#config-entry-migration
    """
    return True # or False on failure
