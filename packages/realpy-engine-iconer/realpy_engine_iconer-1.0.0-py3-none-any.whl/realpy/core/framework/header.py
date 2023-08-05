import asyncio
import sys

import pygame
import pygame.constants as PyConstants
import pygame.display as PyDisplay
import pygame.fastevent as PyEvent
import pygame.mixer as PyAudio
from pygame.time import Clock

__all__ = ["rs_init", "rs_startup", "rs_quit"]

mouse_igniter = []
key_igniter = []
controller_igniter = []
mouse_proceed = []
key_proceed = []
controller_proceed = []
other_proceed = []


def proceed_ing(where, pack):
    from realpy.core import INPUT_STATES, debug_get

    while True:
        try:
            Upk = where.pop()
            if pack.get(Upk) == INPUT_STATES.RELEASED:
                pack[Upk] = INPUT_STATES.NONE
                continue
            pack[Upk] = INPUT_STATES.ING
            if debug_get():
                print("Start at later:", Upk)
        except IndexError:
            break
    where.clear()


def proceed_done(where, pack):
    from realpy.core import INPUT_STATES, debug_get

    while True:
        try:
            Upk = where.pop()
            pack[Upk] = INPUT_STATES.NONE
            if debug_get():
                print("Cleaned at later:", Upk)
        except IndexError:
            break
    where.clear()


async def update_hand():
    from realpy.core.constants import INPUT_STATES
    from realpy.core.preset import RsPreset

    RsPreset.event_others.clear()

    # Await
    Temp = PyEvent.get()
    Len = len(Temp)

    proceed_ing(mouse_igniter, RsPreset.event_mouse)
    proceed_ing(key_igniter, RsPreset.event_key)
    proceed_ing(controller_igniter, RsPreset.event_controller)
    proceed_done(mouse_proceed, RsPreset.event_mouse)
    proceed_done(key_proceed, RsPreset.event_key)
    proceed_done(controller_proceed, RsPreset.event_controller)
    # await asyncio.gather(proceed_ing(mouse_igniter, RsPreset.event_mouse), ...)

    if 0 < Len:
        for event in Temp:
            if event.type == PyConstants.QUIT:
                raise RsPreset.RsInteruptError

            elif event.type == PyConstants.KEYDOWN:
                Seed: int = event.key
                Place = RsPreset.event_key.get(Seed)

                if Place:  # Key can be able to be None
                    if Place == INPUT_STATES.NONE:  # Normal
                        RsPreset.event_key[Seed] = INPUT_STATES.PRESSED
                    elif Place == INPUT_STATES.RELEASED:  # Should not happen
                        RsPreset.event_key[Seed] = INPUT_STATES.NONE
                    else:  # It may not be runned
                        RsPreset.event_key[Seed] = INPUT_STATES.ING
                else:  # Add a new key
                    key_igniter.append(Seed)
                    RsPreset.event_key[Seed] = INPUT_STATES.PRESSED
                    if RsPreset.debug_get():
                        print("New Key:", Seed)

            elif event.type == PyConstants.KEYUP:
                Seed = event.key
                Place = RsPreset.event_key.get(Seed)

                if Place:
                    if Place == INPUT_STATES.RELEASED:  # Should not happen
                        RsPreset.event_key[Seed] = INPUT_STATES.NONE
                    elif Place != INPUT_STATES.NONE:
                        key_proceed.append(Seed)  # Clear later
                        RsPreset.event_key[Seed] = INPUT_STATES.RELEASED
                else:
                    RsPreset.event_key[Seed] = INPUT_STATES.NONE

            elif event.type == PyConstants.MOUSEBUTTONDOWN:
                Seed: int = event.button
                Place = RsPreset.event_mouse.get(Seed)
                RsPreset.mouse_x, RsPreset.mouse_y = event.pos

                if Place:
                    if Place == INPUT_STATES.NONE:
                        RsPreset.event_mouse[Seed] = INPUT_STATES.PRESSED
                    elif Place == INPUT_STATES.RELEASED:
                        RsPreset.event_mouse[Seed] = INPUT_STATES.NONE
                    else:
                        RsPreset.event_mouse[Seed] = INPUT_STATES.ING
                else:
                    mouse_igniter.append(Seed)
                    RsPreset.event_mouse[Seed] = INPUT_STATES.PRESSED
                    if RsPreset.debug_get():
                        print("New Click:", Seed)

            elif event.type == PyConstants.MOUSEBUTTONUP:
                Seed = event.button
                Place = RsPreset.event_mouse.get(Seed)
                RsPreset.mouse_x, RsPreset.mouse_y = event.pos

                if Place:
                    if Place == INPUT_STATES.RELEASED:
                        RsPreset.event_mouse[Seed] = INPUT_STATES.NONE
                    elif Place != INPUT_STATES.NONE:
                        mouse_proceed.append(Seed)  # Clear later
                        RsPreset.event_mouse[Seed] = INPUT_STATES.RELEASED
                else:
                    RsPreset.event_mouse[Seed] = INPUT_STATES.NONE

            elif event.type == PyConstants.MOUSEMOTION:
                RsPreset.mouse_x, RsPreset.mouse_y = event.pos
            else:
                RsPreset.event_others.append(event)


async def update_flow(room, time: float):
    room.onUpdate(time)
    room.onUpdateLater(time)


async def update_draw(room, time: float):
    from realpy.core.preset import RsPreset

    RsPreset.application_surface.fill("black")
    room.onDraw(time)
    PyDisplay.update()


async def update_all(room, time: float):
    await asyncio.gather(update_flow(room, time), update_draw(room, time))


def rs_init(title: str, view_port_width: int, view_port_height: int, *, audio_channels=12, audio_buffer=1024):
    from realpy.core.preset import RsPreset

    PyAudio.pre_init(channels=audio_channels, buffer=audio_buffer)
    pygame.init()
    PyDisplay.init()
    PyEvent.init()
    PyAudio.init()

    PyDisplay.set_caption(title)
    PyDisplay.set_allow_screensaver(False)

    RsPreset.dimension = (view_port_width, view_port_height)
    RsPreset.application_surface = PyDisplay.set_mode(RsPreset.dimension)


def rs_startup():
    from realpy.core.preset import RsPreset
    from realpy.core.scene import RsScene

    # Startup
    Rooms = RsPreset.room_order
    StartRoom = None
    try:
        StartRoom = Rooms[0]
        RsPreset.room = StartRoom
    except IndexError:
        raise RuntimeError("No scene found.")

    if not StartRoom:
        raise RuntimeError("Invalid scene.")

    RoomCurrent: RsScene = RsPreset.room
    AbsoluteTimer = Clock()
    TimeOccured: float = 0

    # Load rooms
    RsPreset.room.onAwake()
    while True:
        TimeOccured = 0 if RsPreset.room.paused else AbsoluteTimer.get_time() * 0.001  # Millisecond

        try:
            asyncio.run(update_hand())
            asyncio.run(update_all(RoomCurrent, TimeOccured))
        except RsPreset.RsInteruptError:
            rs_quit()

        AbsoluteTimer.tick(RsPreset.game_speed)
        RoomCurrent = RsPreset.room


def rs_quit():
    print("Program is ended.")
    PyAudio.quit()
    pygame.quit()
    sys.exit(0)
