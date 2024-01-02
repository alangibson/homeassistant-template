"""Support for KWB Easyfire."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .src.config import UPDATE_BEFORE_ADD
from .src.devices import HACSTemplateDevice
from .src.const import DOMAIN
from .src.coordinator import HACSTemplateCoordinator
from .src.platforms.sensors.entities import generate_entities
from .src.platforms.sensors.entity_coordinators import (
    HACSTemplateSensorCoordinatorEntity,
)
from .src.platforms.sensors.schema import PLATFORM_SCHEMA

logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Create one or more SensorEntity based on a ConfigEntry.

    For a platform to support config entries, it will need to add a setup entry method.
    https://developers.home-assistant.io/docs/config_entries_index/#for-platforms
    """

    logger.debug("Entering sensor async_setup_entry()")

    # Retrieve the data update coordinator
    data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator: HACSTemplateCoordinator = data["coordinator"]
    device: HACSTemplateDevice = data["device"]

    entity_list: list[HACSTemplateSensorCoordinatorEntity] = generate_entities(
        coordinator=coordinator, device=device, config_entry=config_entry
    )

    logger.debug("Invoking async_add_entities()")

    # Create entities and hand them off to HomeAssistant
    async_add_entities(entity_list, update_before_add=UPDATE_BEFORE_ADD)
