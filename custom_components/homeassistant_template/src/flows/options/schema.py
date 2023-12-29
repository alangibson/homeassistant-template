import voluptuous as vol

def options_schema(defaults: dict):
    return vol.Schema(
            {
                vol.Required(CONF_UNIQUE_ID, default=conf_unique_id): str,
                vol.Required(CONF_MODEL, default=conf_model): selector(
                    {
                        "select": {
                            "options": ["easyfire_1"],
                        }
                    }
                ),
                vol.Required(CONF_SENDER, default=conf_sender): selector(
                    {
                        "select": {
                            "options": ["comfort_3"],
                        }
                    }
                ),
                vol.Required(CONF_PROTOCOL, default=conf_protocol): selector(
                    {
                        "select": {
                            "options": ["tcp"],
                        }
                    }
                ),
                vol.Required(CONF_HOST, default=conf_host): str,
                vol.Required(CONF_PORT, default=conf_port): int,
                vol.Required(CONF_TIMEOUT, default=conf_timeout): int,
                # vol.Optional(CONF_BOILER_EFFICIENCY, default=conf_boiler_efficiency): float,
                # vol.Optional(CONF_BOILER_NOMINAL_POWER, default=conf_boiler_nominal_power): float,
                # vol.Optional(CONF_PELLET_NOMINAL_ENERGY, default=conf_pellet_nominal_energy): float,
                # vol.Optional(OPT_LAST_BOILER_RUN_TIME, default=last_boiler_run_time): float,
                # vol.Optional(OPT_LAST_ENERGY_OUTPUT, default=last_energy_output): float,
                # vol.Optional(OPT_LAST_PELLET_CONSUMPTION, default=last_pellet_consumption): float,
                # vol.Optional(OPT_LAST_TIMESTAMP, default=last_timestamp): float,
            }
        )