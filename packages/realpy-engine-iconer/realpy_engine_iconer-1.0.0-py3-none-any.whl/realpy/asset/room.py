from typing import Union, Optional

from ..preset import RsPreset
from ..scene import RsScene


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

    Number = len(RsPreset.RoomOrder)
    if 0 < Number:
        LastRoom = RsPreset.RsLastRoom
        if LastRoom and NewRoom:
            NewRoom.before = LastRoom
            LastRoom.next = NewRoom
    else:
        RsPreset.RsRoom = NewRoom
        RsPreset.RsLastRoom = NewRoom

    RsPreset.RoomOrder.append(NewRoom)
    RsPreset.RoomPot[Name] = NewRoom
    return NewRoom


def room_get(id: Union[int, str]):
    if type(id) is int:
        return RsPreset.RoomOrder[id]
    elif type(id) is str:
        return RsPreset.RoomPot[id]


def room_set(taget: RsScene):
    if RsPreset.RsRoom:
        RsPreset.RsRoom.onDestroy()
    RsPreset.RsRoom = taget
    RsPreset.RsRoom.onAwake()
    print("Go to " + str(RsPreset.RsRoom))


def room_goto(name: str):
    Temp = room_get(name)
    if not Temp:
        raise RuntimeError("The room " + name + " doesn't exist.")
    elif Temp is not RsPreset.RsRoom:
        room_set(Temp)


def room_goto_next():
    Next = RsPreset.RsRoom.next
    if Next:
        room_set(Next)
    else:
        raise RuntimeError("The next room doesn't exist.\n")
