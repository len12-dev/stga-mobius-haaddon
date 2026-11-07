"""Capteur « minutes avant le prochain bus »."""

import time

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DIRECTION_ID, CONF_ROUTE_ID, CONF_STOP_ID
from .coordinator import MobiusCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Crée le capteur pour une entrée de configuration."""
    coordinator = MobiusCoordinator(
        hass,
        entry,
        entry.data[CONF_STOP_ID],
        entry.data[CONF_ROUTE_ID],
        entry.data[CONF_DIRECTION_ID],
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([MobiusNextBusSensor(coordinator, entry)])


class MobiusNextBusSensor(CoordinatorEntity, SensorEntity):
    """Minutes avant le prochain passage, avec les 5 suivants en attribut."""

    _attr_native_unit_of_measurement = "min"
    _attr_icon = "mdi:bus"

    def __init__(self, coordinator: MobiusCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_name = entry.title
        self._attr_unique_id = entry.entry_id

    @property
    def native_value(self) -> int | None:
        passages = self.coordinator.data or []
        if not passages:
            return None
        return max(0, round((passages[0] - time.time()) / 60))

    @property
    def extra_state_attributes(self) -> dict:
        passages = (self.coordinator.data or [])[:5]
        return {
            "prochains_passages": [
                time.strftime("%H:%M", time.localtime(ts)) for ts in passages
            ]
        }
