"""Entity definitions."""

import logging

from homeassistant.config_entries import ConfigEntry

from ...coordinator import HACSTemplateCoordinator
from ...devices import HACSTemplateDevice
from .entity_coordinators import HACSTemplateSensorCoordinatorEntity
from .entity_descriptions import HACSTemplateSensorDescription

logger = logging.getLogger(__name__)


async def generate_entities(
    coordinator: HACSTemplateCoordinator,
    device: HACSTemplateDevice,
    config_entry: ConfigEntry,
) -> list(HACSTemplateSensorCoordinatorEntity):
    """Generate sensor entities for HomeAssistant based on config entry.

    yield entries as they are created.
    """

    yield HACSTemplateSensorCoordinatorEntity(
        coordinator,
        HACSTemplateSensorDescription(
            device_id=device.get_unique_id(),
            key="boiler_on",
            translation_key="boiler_on",
            name="Boiler On",
            device_class=device_class,
            state_class=state_class,
            device_model=model,
        ),
    )
