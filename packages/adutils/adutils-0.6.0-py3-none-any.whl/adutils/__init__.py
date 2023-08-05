"""adutils - helper functions for AppDaemon apps

  @benleb / https://github.com/benleb/adutils
"""

# from datetime import datetime, timedelta, timezone
from importlib.metadata import version
from sys import version_info
from typing import Any, Dict, Optional, Union, Set

from appdaemon.appdaemon import AppDaemon
from statistics import fmean


__version__ = version(__name__)

# version checks
py3_or_higher = version_info.major >= 3
py37_or_higher = py3_or_higher and version_info.minor >= 7
py38_or_higher = py3_or_higher and version_info.minor >= 8
py39_or_higher = py3_or_higher and version_info.minor >= 9

# timing
SECONDS_PER_MIN: int = 60


def hl(text: Union[int, float, str]) -> str:
    return f"\033[1m{text}\033[0m"


def hl_entity(entity: str) -> str:
    domain, entity = entity.split(".")
    return f"{domain}.{hl(entity)}"


def natural_time(duration: Union[int, float]) -> str:

    duration_min, duration_sec = divmod(duration, float(SECONDS_PER_MIN))

    # append suitable unit
    if duration >= SECONDS_PER_MIN:
        if duration_sec < 10 or duration_sec > 50:
            natural = f"{hl(int(duration_min))}min"
        else:
            natural = f"{hl(int(duration_min))}min {hl(int(duration_sec))}sec"
    else:
        natural = f"{hl(int(duration_sec))}sec"

    return natural


class Room:
    """Class for keeping track of a room."""

    def __init__(
        self,
        name: str,
        door_window: Set[str],
        temperature: Set[str],
        push_data: Optional[Dict[str, Union[str, int]]] = None,
        appdaemon: AppDaemon = None
    ) -> None:

        self.name: str = name
        # door/window sensors of a room
        self.door_window: Set[str] = door_window
        # temperature sensors of a room
        self.temperature: Set[str] = temperature
        # reminder notification callback handles
        self.handles: Dict[str, str] = {}
        # ios push settings
        self.push_data: Dict[str, Union[str, int]] = push_data

        # callback handles to switch off the lights
        self.handles_automoli: Set[str] = set()
        # callback handles for notifreeze notifications
        self.handles_notifreeze: Set[str] = set()

        # appdaemon instance
        self._ad = appdaemon

    async def indoor(self, nf: Any) -> Optional[float]:
        indoor_temperatures = set()
        invalid_sensors = {}

        for sensor in self.temperature:
            try:
                indoor_temperatures.add(float(await nf.get_state(sensor)))
            except ValueError:
                invalid_sensors[sensor] = await nf.get_state(sensor)
                continue

        if indoor_temperatures:
            return fmean(indoor_temperatures)

        nf.lg(f"{self.name}: No valid values ¯\\_(ツ)_/¯ {invalid_sensors = }")

        return None
