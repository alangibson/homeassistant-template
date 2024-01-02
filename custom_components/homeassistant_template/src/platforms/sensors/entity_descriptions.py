"""Entity descriptor."""

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntityDescription


@dataclass(kw_only=True)
class HACSTemplateSensorDescription(SensorEntityDescription):
    """Custom attributes should be added to this class.

    https://developers.home-assistant.io/docs/core/entity#example
    """
