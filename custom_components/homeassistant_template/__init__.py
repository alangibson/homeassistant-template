"""hacs-template integration"""

import logging

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigEntryAuthFailed,
    ConfigEntryNotReady,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry

from .src.config import FIRST_REFRESH_RETRY_ON_FAILURE, PLATFORMS, UPDATE_INTERVAL
from .src.devices import HACSTemplateDevice
from .src.const import DOMAIN
from .src.coordinator import HACSTemplateCoordinator

logger = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Entry point to set up integration.

    This function allows us to set up more than one platform with a single ConfigEntry.
    It is called after the user finishes the configuration flow in the UI.
    """

    logger.debug("Entered async_step_user()")

    # try:
    # TODO maybe see if config_flow put a connection in hass.data?

    #
    # Test connection to device
    #

    logger.debug("Connecting to device")

    # Connect to your device via 3rd party library here
    try:
        config = {**config_entry.data, **config_entry.options}

        device = HACSTemplateDevice(hass=hass, config=config)
        await device.connect()
    # TODO
    #   If authentication fails, you need to `raise ConfigEntryAuthFailed(e)`
    #   https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#reauthentication`
    #   raise ConfigEntryAuthFailed from e
    except Exception as e:
        logger.error(e)
        # Otherwise raise the ConfigEntryNotReady exception and Home Assistant will
        # automatically take care of retrying set up later.
        raise ConfigEntryNotReady from e

    logger.debug("Successfully connected to device")

    #
    # Register device with HomeAssistant
    #

    # Register our inverter device
    device_registry.async_get(hass).async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, device.get_unique_id())},
        # TODO
        # manufacturer="KWB",
        # name=f"KWB {config_entry.data.get(CONF_MODEL)}",
        # model=config_entry.data.get(CONF_MODEL),
    )

    #
    # Create data update coordinator and load data from device
    #

    logger.debug("Creating template coordinator")

    # Create a data update coordinator that will pull data and
    # update our platforms for us
    coordinator = HACSTemplateCoordinator(
        hass=hass,
        logger=logger,
        name=DOMAIN,
        update_interval=UPDATE_INTERVAL,
        connection=device,
    )

    # Fetch initial data so we have data when entities subscribe
    if FIRST_REFRESH_RETRY_ON_FAILURE:
        # If the refresh fails, async_config_entry_first_refresh will
        # raise ConfigEntryNotReady and setup will try again later
        await coordinator.async_config_entry_first_refresh()
    else:
        # If you do not want to retry setup on failure, use async_refresh()
        await coordinator.async_refresh()

    logger.debug("Created template coordinator and refreshed data")

    #
    # Configure platforms
    #

    # Save reference to data update coordinator so we can access it in platform setup
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        "connection": device,
        "coordinator": coordinator,
    }

    logger.debug("Forward config entry to platforms for setup")

    # Forward the ConfigEntry to the sensor platform(s)
    # hass.async_create_task(
    #     hass.config_entries.async_forward_entry_setup(config_entry, PLATFORMS)
    # )
    # TODO or can we just do this?
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    #
    # Register listeners
    #

    config_entry.async_on_unload(config_entry.add_update_listener(async_update_options))

    return True


async def async_update_config(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""

    logger.debug("Entered async_update_config()")

    # Reload our entities if the ConfigEntry changes
    await hass.config_entries.async_reload(entry.entry_id)


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""

    logger.debug("Entered async_update_options()")

    await hass.config_entries.async_reload(entry.entry_id)


# TODO Unload gracefully
# https://github.com/home-assistant/core/blob/dev/homeassistant/components/fronius/__init__.py
async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    logger.debug("Entered async_unload_entry()")

    # Clean up any connections you have open, etc.
    connection: HACSTemplateDevice = hass.data[DOMAIN][config_entry.entry_id].get(
        "connection"
    )
    if connection:
        connection.disconnect()

    # and return True if everything went OK
    return True
