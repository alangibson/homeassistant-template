from homeassistant.core import HomeAssistant


def validate_input(hass: HomeAssistant, user_input: dict) -> dict[str, str]:
    # TODO put your user_input validation here
    return {}

def validate_connection(hass: HomeAssistant, user_input: dict) -> dict[str, str]:
    # TODO validate connection to device
    # TODO and set an error if it fails
    # errors["base"] = "cannot_connect"
    return {}
