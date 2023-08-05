from .core import RsScene


class RsStage(RsScene):
    def __init__(self, name: str = ""):
        super().__init__(name)

        self.width = 640
        self.height = 480
