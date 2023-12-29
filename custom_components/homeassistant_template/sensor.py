"""Support for KWB Easyfire."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .src.const import DOMAIN
from .src.config import UPDATE_BEFORE_ADD
from .src.platforms.sensors.schema import PLATFORM_SCHEMA
from .src.coordinator import HACSTemplateCoordinator
from .src.platforms.sensors import init 
from .src.platforms.sensors.sensor import HACSTemplateSensorCoordinatorEntity

logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
):
    """Creates one or more SensorEntity based on a ConfigEntry.

    For a platform to support config entries, it will need to add a setup entry method.
    https://developers.home-assistant.io/docs/config_entries_index/#for-platforms
    """

    # Retrieve the data update coordinator
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: HACSTemplateCoordinator = data['coordinator']

    entities: list[HACSTemplateSensorCoordinatorEntity] = init.generate_entities(config_entry=config_entry, coordinator=coordinator)

    # Create entities and hand them off to HomeAssistant
    async_add_entities(entities, update_before_add=UPDATE_BEFORE_ADD)
