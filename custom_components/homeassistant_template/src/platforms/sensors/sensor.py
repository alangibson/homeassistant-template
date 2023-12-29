"""
"""

from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorEntity,
    RestoreSensor
)
from homeassistant.const import (
    STATE_UNAVAILABLE
)

from ...config import RESTORE_SENSOR
from ....coordinator import HACSTemplateCoordinator

class HACSTemplateSensorDescription(SensorEntityDescription):
    # Add any custom attributes here
    pass
# TODO
# https://developers.home-assistant.io/docs/core/entity#example
# @dataclass(kw_only=True)
# class ExampleSensorEntityDescription(SensorEntityDescription):
#     """Describes Example sensor entity."""
#     exists_fn: Callable[[ExampleDevice], bool] = lambda _: True
#     value_fn: Callable[[ExampleDevice], StateType]

class HACSTemplateSensorEntity(RestoreSensor if RESTORE_SENSOR else SensorEntity):
    """Representation of a sensor.
    
    This sensor will automatically restore its previous state after restart
    when RESTORE_SENSOR == True in config.py.

    https://developers.home-assistant.io/docs/core/entity/sensor
    """

    # async def async_added_to_hass(self) -> None:
    #     """Called when this entity is added to HomeAssistant."""
    #     # Restore sensor state
    #     last_state = await self.async_get_last_state()
    #     last_sensor_state = await self.async_get_last_sensor_data()
    #     if (
    #         not last_state
    #         or not last_sensor_state
    #         or last_state.state == STATE_UNAVAILABLE
    #     ):
    #         # There is no last state, so do nothing
    #         return
    #     self._attr_native_value = last_sensor_state.native_value
    #     self._attr_native_unit_of_measurement = (
    #         last_sensor_state.native_unit_of_measurement
    #     )
    #     # Register a method to be run on removal from HomeAssistant
    #     self.async_on_remove(...)

    # def async_update(self) -> None:
    #     """Fetch new state data for the sensor.
    #     This is the only method that should fetch new data for Home Assistant.
    #     If you can map exactly one device endpoint to a single entity, you can fetch 
    #     the data for this entity inside the update()/async_update() methods. 
    #     Make sure polling is set to True and Home Assistant will call this method regularly.
    #     """
    #     pass


class HACSTemplateSensorCoordinatorEntity(CoordinatorEntity[HACSTemplateCoordinator], HACSTemplateSensorEntity):
    """Turns our entity into something the data update coordinator can talk to"""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""

        # TODO any special handling of data fetched by the data update coordinator
        # from the connection should go here. 
        # Limit what you do here to setting attributes of this entity.

        self.async_write_ha_state()