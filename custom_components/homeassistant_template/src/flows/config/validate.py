import logging

from ...devices import HACSTemplateDevice
from homeassistant.core import HomeAssistant

logger = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, user_input: dict) -> dict[str, str]:
    # TODO put your user_input validation here
    return {}


# async def validate_connection(hass: HomeAssistant, user_input: dict) -> dict[str, str]:
async def validate_connection(connection: HACSTemplateDevice) -> dict[str, str]:
    errors = {}
    # TODO validate connection to device
    # TODO and set an error if it fails
    # errors["base"] = "cannot_connect"

    try:
        # connection = HACSTemplateDevice(hass=hass, config=user_input)
        success = await connection.test()
        if not success:
            errors["base"] = "cannot_connect"
    except Exception as e:
        logger.warning(e)
        errors["base"] = "cannot_connect"

    return errors
