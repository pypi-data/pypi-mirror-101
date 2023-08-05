import asyncio, sys
from asyncio.exceptions import CancelledError
from typing import Union

import pygame
import pygame.constants as PyConstants
import pygame.display as PyDisplay
import pygame.fastevent as PyEvent
from pygame.time import Clock as Clock

from ..preset import RsPreset
from ..scene import RsScene

__all__ = ("rs_init", "rs_startup", "rs_quit")


class RsInteruptError(Exception):
    pass


async def hand_update():
    RsPreset.Events.clear()

    # Await
    Temp = PyEvent.get()

    for event in Temp:
        if event.type == PyConstants.QUIT:
            raise RsInteruptError
        elif event.type == PyConstants.KEYDOWN and event.key == PyConstants.K_ESCAPE:
            raise RsInteruptError
        elif event.type == PyConstants.MOUSEBUTTONDOWN:
            pass  # room_goto_next()
        elif event.type == PyConstants.MOUSEBUTTONUP:
            pass

    RsPreset.Events = Temp
    return len(RsPreset.Events)


async def scene_update(room: RsScene, time: float):
    room.onUpdate(time)
    room.onUpdateLater(time)


async def graphics_update(room: RsScene, time: float):
    RsPreset.application_surface.fill("black")
    room.onDraw(time)
    PyDisplay.update()


async def update_all(room: RsScene, time: float):
    await asyncio.gather(hand_update(), scene_update(room, time), graphics_update(room, time))


def rs_init(title: str, view_port_width: int, view_port_height: int):
    pygame.init()
    PyDisplay.init()
    PyEvent.init()

    PyDisplay.set_caption(title)
    PyDisplay.set_allow_screensaver(False)

    RsPreset.dimension = (view_port_width, view_port_height)
    RsPreset.application_surface = PyDisplay.set_mode(RsPreset.dimension)


def rs_startup():
    # Startup
    Rooms = RsPreset.RoomOrder
    StartRoom = None
    try:
        StartRoom = Rooms[0]
        RsPreset.RsRoom = StartRoom
    except IndexError:
        raise RuntimeError("No scene found.")

    if not StartRoom:
        raise RuntimeError("Invalid scene.")

    RoomCurrent: RsScene = RsPreset.RsRoom
    AbsoluteTimer = Clock()
    TimeOccured: float = 0

    # Load rooms
    print(RsPreset.RsRoom)
    RsPreset.RsRoom.onAwake()
    while True:
        TimeOccured = 0 if RsPreset.RsRoom.paused else AbsoluteTimer.get_time() * 0.001  # Millisecond
        print(TimeOccured)

        try:
            asyncio.run(update_all(RoomCurrent, TimeOccured))
        except CancelledError:
            rs_quit()
        except RsInteruptError:
            rs_quit()

        AbsoluteTimer.tick(RsPreset.game_speed)
        RoomCurrent = RsPreset.RsRoom


def rs_quit():
    print("Program is ended.")
    pygame.quit()
    sys.exit()
