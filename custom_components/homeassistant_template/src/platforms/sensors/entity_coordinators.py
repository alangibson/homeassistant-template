from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ...coordinator import HACSTemplateCoordinator
from .entity import HACSTemplateSensorEntity


class HACSTemplateSensorCoordinatorEntity(
    CoordinatorEntity[HACSTemplateCoordinator], HACSTemplateSensorEntity
):
    """Turns our entity into something the data update coordinator can talk to"""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        # TODO any special handling of data fetched by the data update coordinator
        # from the connection should go here.
        # Limit what you do here to setting attributes of this entity.
