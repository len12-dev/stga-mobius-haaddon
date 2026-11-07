"""Coordinateur qui récupère le flux temps réel Möbius et calcule les prochains passages."""

import logging
import time
from datetime import timedelta

from google.transit import gtfs_realtime_pb2
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, RT_URL, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class MobiusCoordinator(DataUpdateCoordinator):
    """Renvoie la liste triée des timestamps de passage à venir."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        stop_id: str,
        route_id: str,
        direction_id: int,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{DOMAIN}_{stop_id}_{route_id}_{direction_id}",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self._session = async_get_clientsession(hass)
        self._stop_id = stop_id
        self._route_id = route_id
        self._direction_id = direction_id

    async def _async_update_data(self) -> list[int]:
        try:
            async with self._session.get(RT_URL, timeout=20) as resp:
                resp.raise_for_status()
                raw = await resp.read()
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Flux Möbius injoignable : {err}") from err

        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            feed.ParseFromString(raw)
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Flux Möbius illisible : {err}") from err

        now = time.time()
        passages: list[int] = []
        for entity in feed.entity:
            if not entity.HasField("trip_update"):
                continue
            trip_update = entity.trip_update
            if trip_update.trip.route_id != self._route_id:
                continue
            if trip_update.trip.direction_id != self._direction_id:
                continue
            for stop_update in trip_update.stop_time_update:
                if stop_update.stop_id != self._stop_id:
                    continue
                ts = stop_update.arrival.time or stop_update.departure.time
                if ts and ts > now:
                    passages.append(ts)

        return sorted(passages)
