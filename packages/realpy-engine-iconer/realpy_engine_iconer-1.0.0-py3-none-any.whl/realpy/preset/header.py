from typing import Type, Optional, List, Dict

from pygame.event import Event
from pygame.surface import Surface as PySurface

from ..scene import RsScene
from ..prefab import RsPrefab
from ..sprite import RsSprite

__all__ = [
    "game_speed", "dimension", "application_surface", "RsRoom", "RsLastRoom",
    "RoomOrder", "RoomPot", "Events", "Atlas", "PrefabsPot", "PrefabsPot", "AudioPot",
    "MASKS", "phy_mess", "phy_velocity"
]

# General
game_speed: int = 60

# Display
dimension = (640, 480)

# Application surface
application_surface: PySurface

# Rooms
RsRoom: Optional[RsScene] = None
RsLastRoom: Optional[RsScene] = None
RoomOrder: List[RsScene] = []
RoomPot: Dict[str, RsScene] = {}

# Events
Events: Dict[str, Event] = {}

# Sprite texture group
Atlas: Dict[str, RsSprite] = {}

# All game objects
PrefabsPot: List[Type[RsPrefab]] = []

# All sounds
AudioPot: Dict[str, object] = {}

# 10 px == 1 metre
phy_mess: float = 10.0 / 1
phy_velocity: float = (((1000.0 / 60.0) / 60.0) * phy_mess)


class MASKS:
    RECTANGLE: int = 0
    CIRCLE: int = 2
