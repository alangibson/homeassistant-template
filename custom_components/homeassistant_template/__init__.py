"""hacs-template integration"""

import logging

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigEntryNotReady,
    ConfigEntryAuthFailed,
)
from homeassistant.core import HomeAssistant

from .src.coordinator import HACSTemplateCoordinator
from .src.const import DOMAIN
from .src.config import PLATFORMS, UPDATE_INTERVAL, FIRST_REFRESH_RETRY_ON_FAILURE
from .src.connection import HACSTemplateConnection


logger = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Entry point to set up integration.

    This function allows us to set up more than one platform with a single ConfigEntry.
    It is called after the user finishes the configuration flow in the UI.
    """
    try:
        # TODO maybe see if config_flow put a connection in hass.data?

        # Connect to your device via 3rd party library here
        connection = HACSTemplateConnection(hass=hass, config_entry=config_entry)
        connection.connect()
    except ... as e:
        # If authentication fails, you need to `raise ConfigEntryAuthFailed(e)`
        # https://developers.home-assistant.io/docs/config_entries_config_flow_handler/#reauthentication`
        raise ConfigEntryAuthFailed(e)
    except Exception as e:
        # Otherwise raise the ConfigEntryNotReady exception and Home Assistant will
        # automatically take care of retrying set up later.
        raise ConfigEntryNotReady(e) from e

    # Create a data update coordinator that will pull data and update our platforms for us
    coordinator = HACSTemplateCoordinator(
        hass=hass, logger=logger, name=DOMAIN, update_interval=UPDATE_INTERVAL,
        connection=connection
    )

    # Fetch initial data so we have data when entities subscribe
    if FIRST_REFRESH_RETRY_ON_FAILURE:
        # If the refresh fails, async_config_entry_first_refresh will
        # raise ConfigEntryNotReady and setup will try again later
        await coordinator.async_config_entry_first_refresh()
    else:
        # If you do not want to retry setup on failure, use async_refresh()
        await coordinator.async_refresh()

    # Save reference to data update coordinator so we can access it in platform setup
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = {
        'connection': connection,
        "coordinator": coordinator
    }

    # Forward the ConfigEntry to the sensor platform(s)
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, PLATFORMS)
    )
    # TODO or can we just do this?
    # await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    # Register options update listener
    config_entry.async_on_unload(config_entry.add_update_listener(async_update_options))

    return True


async def async_update_config(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    # Reload our entities if the ConfigEntry changes
    await hass.config_entries.async_reload(entry.entry_id)


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options."""
    await hass.config_entries.async_reload(entry.entry_id)


# TODO Unload gracefully
# https://github.com/home-assistant/core/blob/dev/homeassistant/components/fronius/__init__.py
async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    
    # Clean up any connections you have open, etc.
    connection: HACSTemplateConnection = hass.data[DOMAIN][config_entry.entry_id].get('connection')
    if connection:
        connection.disconnect()

    # and return True if everything went OK
    return True
