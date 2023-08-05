from .constants import INPUT_STATES
from .preset import RsPreset


def keyboard_check(key: int) -> bool:
    Place = RsPreset.event_key.get(key)
    if Place and Place == INPUT_STATES.ING or Place == INPUT_STATES.PRESSED:
        return True
    else:
        return False


def keyboard_check_pressed(key: int) -> bool:
    Place = RsPreset.event_key.get(key)
    if Place and Place == INPUT_STATES.PRESSED:
        return True
    else:
        return False


def keyboard_check_released(key: int) -> bool:
    Place = RsPreset.event_key.get(key)
    if Place and Place == INPUT_STATES.RELEASED:
        return True
    else:
        return False


def mouse_check(button: int) -> bool:
    Place = RsPreset.event_mouse.get(button)
    if Place and Place == INPUT_STATES.ING or Place == INPUT_STATES.PRESSED:
        return True
    else:
        return False


def mouse_check_pressed(button: int) -> bool:
    Place = RsPreset.event_mouse.get(button)
    if Place and Place == INPUT_STATES.PRESSED:
        return True
    else:
        return False


def mouse_check_released(button: int) -> bool:
    Place = RsPreset.event_mouse.get(button)
    if Place and Place == INPUT_STATES.RELEASED:
        return True
    else:
        return False
