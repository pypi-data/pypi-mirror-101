from typing import List, Optional

from pygame import mixer as PyAudio
from pygame.mixer import Channel as PyChannel, Sound as PySound


class RsSound(PySound):
    def __init__(self, info):
        super().__init__(info)
        self.fields: List[PyChannel] = []

    def play(self, loops: Optional[int] = 0, maxtime: Optional[int] = 0, fade_ms: Optional[int] = 0) -> Optional[
        PyChannel]:
        Place: Optional[PyChannel] = PyAudio.find_channel(False)
        if not Place:
            return None
        else:
            self.fields.append(Place)
            Place.play(self, loops, maxtime, fade_ms)
            return Place

    def stop(self) -> None:
        self.fields.clear()
        super().stop()

    def is_playing(self) -> bool:
        return 0 < self.get_num_channels()
