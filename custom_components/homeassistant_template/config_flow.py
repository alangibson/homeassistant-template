"""Config flow."""

from __future__ import annotations

import logging
from typing import Any

from habluetooth import BluetoothServiceInfoBleak
from homeassistant.components.dhcp import DhcpServiceInfo
from homeassistant.components.hassio.discovery import HassioServiceInfo

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .src.config import DEVICE_HAS_UNIQUE_ID
from .src.devices import HACSTemplateDevice
from .src.const import DEFAULT_NAME, DOMAIN
from .src.flows.config import validate
from .src.flows.config.schema import data_schema
from .src.flows.options.options import HACSTemplateOptionsFlow

logger = logging.getLogger(__name__)


class HACSTemplateConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow definition."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    MINOR_VERSION = 1

    async def validate(
        self, hass: HomeAssistant, user_input: dict = None
    ) -> dict[str, Any]:
        """Validate that the user input allows us to connect to the device.

        Data has the keys from DATA_SCHEMA with values provided by the user.
        """

        # Don't do anything if we don't have a configuration
        if not user_input:
            return None

        # Accumulate validation errors. Key is name of field from DATA_SCHEMA
        errors = await validate.validate_input(hass, user_input)

        if errors and len(errors.keys()) > 0:
            return errors

        # Do a test connection to your device here
        errors = await validate.validate_connection(hass, user_input)

        return errors

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Take user input, validate, and either create an entry or show form.

        Invoked when a user initiates a flow via the user interface
        or when discovered and the matching and discovery step are not defined.

        Result is either show config data entry form to the user,
        or create a config entry.
        """

        logger.debug("Entered HACSTemplateConfigFlow.async_step_user()")

        # Either show modal form, or create config entry then move on
        if not user_input:  # Just show the modal form and return if no user input
            return self.async_show_form(step_id="user", data_schema=data_schema({}))
        else:
            # We got user input, so do something with it

            errors = await validate.validate_input(self.hass, user_input)
            if errors and len(errors.keys()) > 0:
                return self.async_show_form(
                    step_id="user", data_schema=data_schema(user_input), errors=errors
                )

            # Validate inputs and do a test connection/scrape of the heater
            # Both info and errors are None when config flow is first invoked
            # errors = await self.validate(self.hass, user_input)

            device = HACSTemplateDevice(self.hass, user_input)

            errors = await validate.validate_connection(device)

            # Either display errors in form, or close form and create config entry
            if errors and len(errors.keys()) > 0:
                # If there is no user input or there were errors, show the form again,
                # including any errors that were found with the input.
                return self.async_show_form(
                    step_id="user", data_schema=data_schema(user_input), errors=errors
                )

            if DEVICE_HAS_UNIQUE_ID:
                # Get a unique id (that never changes!) for the device
                unique_device_id = await device.get_unique_id()

                await self.async_set_unique_id(unique_device_id)
                # TODO we can update CONF_* properties in the updates dict
                updates = {}
                self._abort_if_unique_id_configured(updates=updates)
            else:
                await self._async_handle_discovery_without_unique_id()

            logger.debug("Invoking self.async_create_entry with title=%s", DEFAULT_NAME)

            # Forward user input on to create a device.
            r = self.async_create_entry(title=DEFAULT_NAME, data=user_input)

            logger.debug("Exiting async_step_user")

            # Results in async_setup_entry() in the platform file being called.
            return r

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak = None
    ):
        """Integration has been discovered via Bluetooth.

        https://developers.home-assistant.io/docs/creating_integration_manifest#bluetooth
        """

    async def async_step_dhcp(self, discovery_info: DhcpServiceInfo = None):
        """Integration has been discovered via DHCP.

        https://developers.home-assistant.io/docs/creating_integration_manifest#dhcp
        """

    async def async_step_hassio(self, discovery_info: HassioServiceInfo = None):
        """Integration has been discovered via a Supervisor add-on."""

    async def async_step_homekit(self, discovery_info: Any = None):
        """Integration has been discovered via DHCP as specified using dhcp in the manifest.

        https://developers.home-assistant.io/docs/creating_integration_manifest#homekit
        """

    async def async_step_unignore(self, user_input: dict[str, Any] = None):
        """Discovered device should be unignored.

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
    return True  # or False on failure
