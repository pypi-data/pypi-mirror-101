from typing import Optional, List, Dict

from pygame.mixer import Sound as PyAudio
from pygame.surface import Surface as PySurface

from ..scene import RsScene

__all__ = [
    "game_speed", "mouse_x", "mouse_y",
    "dimension", "application_surface",
    "room", "room_last", "room_order", "room_all",
    "event_mouse", "event_key", "event_controller", "event_others", "RsInteruptError",
    "debug_set", "debug_get"
]

# General
game_speed: int = 30
mouse_x: int = 0
mouse_y: int = 0

_realpy_debug: bool = False


def debug_set(flag: bool):
    global _realpy_debug
    _realpy_debug = flag


def debug_get() -> bool:
    global _realpy_debug
    return _realpy_debug


# Display
dimension = (640, 480)

# Application surface
application_surface: Optional[PySurface] = None

# Rooms
room: Optional[RsScene] = None
room_last: Optional[RsScene] = None
room_order: List[RsScene] = []
room_all: Dict[str, RsScene] = {}

# Events
event_mouse: Dict[int, int] = {}
event_key: Dict[int, int] = {}
event_controller: Dict[int, int] = {}
event_others = []

# Others
AudioPot: Dict[str, PyAudio] = {}


class RsInteruptError(Exception):
    pass
