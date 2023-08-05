""" Sprite
    ---
    ```
    from realpy import RsSprite
    ```
"""
from .header import RsSprite

__all__ = ["RsSprite"]


def test():
    print("***** Test → Realpy Sprite *****")

    class PseudoRect:
        def __init__(self, w: int, h: int) -> None:
            self.width: int = w
            self.height: int = h

    class PseudoImage:
        def __init__(self) -> None:
            self.raw_data = []
            self.boundbox = PseudoRect(32, 32)

    try:
        print(">>> Class of sprite: ", RsSprite)
        print(">>> Class of simulated rectangle: ", PseudoRect)
        print(">>> Class of simulated image: ", PseudoImage)

        SampleImage = PseudoImage()
        Sample = RsSprite(SampleImage, 0, 16, 16)

        print("Sample image: ", SampleImage)
        print("Sample sprite: ", Sample)
    except Exception as e:
        print("Error: ", e)
        return False
    return True
