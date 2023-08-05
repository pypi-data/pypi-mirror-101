from typing import Optional, overload

from .preset import RsPreset
from .scene import RsScene


def room_register(info: RsScene, caption: Optional[str] = None):
    NewRoom: RsScene = info
    Name: str
    if caption:
        if caption == "":
            raise RuntimeError(f"Please enter name of the scene {id(info)}")
        NewRoom.name = caption
        Name = caption
    else:
        Name = info.name

    Number = len(RsPreset.room_order)
    if 0 < Number:
        LastRoom = RsPreset.room_last
        if LastRoom and NewRoom:
            NewRoom.before = LastRoom
            LastRoom.next = NewRoom
    else:
        RsPreset.room = NewRoom
    RsPreset.room_last = NewRoom

    RsPreset.room_order.append(NewRoom)
    RsPreset.room_all[Name] = NewRoom
    return NewRoom


@overload
def room_lookup(id: int) -> Optional[RsScene]: ...


@overload
def room_lookup(id: str) -> Optional[RsScene]: ...


def room_lookup(id):
    if isinstance(id, int):
        return RsPreset.room_order[id]
    elif isinstance(id, str):
        return RsPreset.room_all[id]


def _room_set(taget: RsScene):
    if RsPreset.room:
        RsPreset.room.onDestroy()
    RsPreset.room = taget
    RsPreset.room.onAwake()

    if RsPreset.debug_get():
        print("Go to " + str(RsPreset.room))


def room_goto(name: str):
    Temp = room_lookup(name)
    if not Temp:
        raise RuntimeError("The room " + name + " doesn't exist.")
    elif Temp is not RsPreset.room:
        _room_set(Temp)


def room_goto_next():
    Next = RsPreset.room.next
    if Next:
        _room_set(Next)
    else:
        raise RuntimeError("The next room doesn't exist.\n")
