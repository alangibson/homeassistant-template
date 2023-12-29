import voluptuous as vol

from homeassistant.helpers.selector import selector
from homeassistant.const import (
    CONF_HOST,
    CONF_MODEL,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_SENDER,
    CONF_TIMEOUT,
    CONF_UNIQUE_ID,
)

# This is the schema that used to display the UI to the user.
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_UNIQUE_ID, default="KWB"): str,
        vol.Required(CONF_MODEL, default="easyfire_1"): selector(
            {
                "select": {
                    "options": ["easyfire_1"],
                }
            }
        ),
        vol.Required(CONF_SENDER, default="comfort_3"): selector(
            {
                "select": {
                    "options": ["comfort_3"],
                }
            }
        ),
        vol.Required(CONF_PROTOCOL, default="tcp"): selector(
            {
                "select": {
                    "options": ["tcp"],
                }
            }
        ),
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=8899): int,
        vol.Required(CONF_TIMEOUT, default=2): int,
        # vol.Optional(CONF_BOILER_EFFICIENCY): float,
        # vol.Optional(CONF_BOILER_NOMINAL_POWER): float,
        # vol.Optional(CONF_PELLET_NOMINAL_ENERGY): float,
    }
)