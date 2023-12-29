from typing import Any, Dict

import voluptuous as vol

from homeassistant.helpers.selector import selector
from homeassistant.config_entries import (
    OptionsFlow,
    ConfigEntry,
    FlowResult
)
from homeassistant.const import (
    CONF_HOST,
    CONF_MODEL,
    CONF_PORT,
    CONF_PROTOCOL,
    CONF_SENDER,
    CONF_TIMEOUT,
    CONF_UNIQUE_ID,
)

from .schema import options_schema

class HACSTemplateOptionsFlow(OptionsFlow):
    
    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage the options."""

          # TODO Load up existing options/config values
        conf_unique_id = self.config_entry.data.get(CONF_UNIQUE_ID)
  
        schema = options_schema(user_input)

        if user_input is not None:
            # We got user input, so save it

            errors: Dict[str, str] = {}

            if not errors:
                return self.async_create_entry(title=DEFAULT_NAME, data=user_input)
            else:
                # We got errors, so show error form
                # TODO clone and set default= in data schema
                return self.async_show_form(
                    step_id="init",
                    data_schema=schema,
                    errors=errors
                )
        else:
            # We haven't gotten user input yet, so display form

            # TODO clone and set default= in data schema
            return self.async_show_form(
                step_id="init",
                data_schema=schema
            )
