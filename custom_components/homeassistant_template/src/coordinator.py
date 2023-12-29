"""Example integration using DataUpdateCoordinator."""

import logging
from typing import Any

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .connection import HACSTemplateConnection

_LOGGER = logging.getLogger(__name__)


class HACSTemplateCoordinator(DataUpdateCoordinator):
    """My custom coordinator.
    
    https://developers.home-assistant.io/docs/integration_fetching_data/#coordinated-single-api-poll-for-data-for-all-entities
    """

    def __init__(self, *args, connection: HACSTemplateConnection, **kwargs):
        super().__init__(*args, **kwargs)
        self._connection = connection

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
       
        try:
            # TODO First fetch the data from your device using the connection
            data: dict[str, Any] = self._connection.poll()
            # TODO then validate it
            ...
        except Exception as e:
            raise UpdateFailed(e) from e

        # TODO If needed, pre-process the data to lookup tables
        # so entities can quickly look up their data.

        # If everything is good, return the data so it can be sent to the entities
        return data
