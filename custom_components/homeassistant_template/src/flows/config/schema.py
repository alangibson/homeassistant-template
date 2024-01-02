import voluptuous as vol

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_HOST, CONF_UNIQUE_ID
from homeassistant.helpers.selector import selector
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

# TODO move these somewhere
CONF_FORCE_CONNECTION_ERROR = "force_connection_error"
# CONF_FORCE_AUTHENTICATION_ERROR = "force_authentication_error"
OPT_FORCE_ERROR_ON = "force_error_on"
OPT_FORCE_ERROR_OFF = "force_error_off"
DEFAULT_FORCE_CONNECTION_ERROR = False


# This is the schema that used to display the UI to the user.
data_schema = lambda user_input={}: vol.Schema(
    {
        vol.Required(CONF_UNIQUE_ID, default=user_input.get(CONF_UNIQUE_ID)): str,
        vol.Required(CONF_HOST, default=user_input.get(CONF_HOST)): str,
        vol.Required(CONF_USERNAME, default=user_input.get(CONF_USERNAME)): str,
        vol.Required(CONF_PASSWORD, default=user_input.get(CONF_PASSWORD)): str,
        vol.Required(
            CONF_FORCE_CONNECTION_ERROR,
            default=user_input.get(
                CONF_FORCE_CONNECTION_ERROR, DEFAULT_FORCE_CONNECTION_ERROR
            ),
        ): bool,
        # vol.Required(CONF_PORT, default=8899): int,
        # vol.Optional(CONF_BOILER_EFFICIENCY): float,
        # vol.Required(
        #     CONF_FORCE_CONNECTION_ERROR,
        #     default=user_input.get(CONF_FORCE_CONNECTION_ERROR, OPT_FORCE_ERROR_OFF),
        # ): SelectSelector(
        #     SelectSelectorConfig(
        #         options=[OPT_FORCE_ERROR_ON, OPT_FORCE_ERROR_OFF],
        #         translation_key=CONF_FORCE_CONNECTION_ERROR,
        #     )
        # ),
    }
)
