"""Configuration par l'interface : l'utilisateur saisit son arrêt, sa ligne et son sens."""

import voluptuous as vol
from homeassistant import config_entries

from .const import (
    CONF_DIRECTION_ID,
    CONF_NAME,
    CONF_ROUTE_ID,
    CONF_STOP_ID,
    DOMAIN,
)


class MobiusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Flux de configuration Möbius."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Formulaire de saisie de l'arrêt."""
        errors = {}

        if user_input is not None:
            stop_id = user_input[CONF_STOP_ID].strip()
            route_id = user_input[CONF_ROUTE_ID].strip()
            direction_id = user_input[CONF_DIRECTION_ID]

            if not stop_id or not route_id:
                errors["base"] = "missing_fields"
            else:
                user_input[CONF_STOP_ID] = stop_id
                user_input[CONF_ROUTE_ID] = route_id
                await self.async_set_unique_id(
                    f"{stop_id}_{route_id}_{direction_id}"
                )
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Prochain bus"): str,
                vol.Required(CONF_STOP_ID): str,
                vol.Required(CONF_ROUTE_ID, default="174"): str,
                vol.Required(CONF_DIRECTION_ID, default=1): vol.In([0, 1]),
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )
