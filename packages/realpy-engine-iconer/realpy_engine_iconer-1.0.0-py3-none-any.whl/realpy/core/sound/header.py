from typing import Optional, overload

from pygame import mixer as PyAudio
from pygame.mixer import music as PyMusic, Channel as PyChannel, Sound as PySound

from .sfx import RsSound

audio_set_channel_count = PyAudio.set_num_channels
audio_get_channel_count = PyAudio.get_num_channels


def audio_play(sound: RsSound, loop=False):
    return sound.play(-1) if loop else sound.play()


def audio_stop(sound: Optional[RsSound] = None):
    if sound:
        sound.stop()
    else:
        PyAudio.stop()


def audio_play_single(sound: RsSound, loop=False):
    sound.stop()
    audio_play(sound, loop)


def audio_pause(sound: Optional[RsSound] = None):
    if sound:
        if sound.is_playing():
            for Place in sound.fields:
                if Place.get_sound() is sound:
                    Place.pause()
    else:
        PyAudio.pause()


def audio_resume(sound: Optional[RsSound] = None):
    if sound:
        for Place in sound.fields:
            if Place.get_sound() is sound:
                Place.unpause()
    else:
        PyAudio.unpause()


@overload
def audio_is_playing(sound: Optional[PySound]) -> bool: ...


@overload
def audio_is_playing(sound: Optional[PyChannel]) -> bool: ...


def audio_is_playing(sound=None) -> bool:
    if sound is None:
        return PyAudio.get_busy()
    elif isinstance(sound, PySound):
        return 0 < sound.get_num_channels()
    elif isinstance(sound, PyChannel):
        return sound.get_busy()
    else:
        raise TypeError(f"{sound} is not sound element.")


@overload
def audio_fadeout(time: int, sound: Optional[PySound]): ...


@overload
def audio_fadeout(time: int, sound: Optional[PyChannel]): ...


def audio_fadeout(time: int, sound=None):
    if sound is None:
        PyAudio.fadeout(time)
    elif isinstance(sound, PySound):
        sound.fadeout(time)
    elif isinstance(sound, PyChannel):
        sound.fadeout(time)
    else:
        raise TypeError(f"{sound} is not sound element.")
