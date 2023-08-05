""" Image Resource
    ---
    ```
    from realpy import RsImage
    ```
"""
import os
from typing import Sequence, overload, AnyStr

import pygame.image as PyImage
import pygame.rect as PyRect

__all__ = ["RsImage"]


class RsImage(object):
    """`RsImage(image_path)`
        ---
        Raw image of a sprite that contains single or multiple images.
    """

    @overload
    def __init__(self, filepath: AnyStr):
        ...

    @overload
    def __init__(self, filepath: Sequence[AnyStr]):
        ...

    def __init__(self, filepath):
        self.number: int = -1
        self.raw_data = []
        self.boundbox = PyRect.Rect(0, 0, 0, 0)

        if isinstance(filepath, str):
            filepath = (filepath,)

        self.number = len(filepath)
        if self.number == 0:
            raise FileNotFoundError

        FileLoc: str
        for FileLoc in filepath:
            self.raw_data.append(PyImage.load(FileLoc).convert_alpha())

        FileLoc = filepath[0]
        self.filename = os.path.basename(FileLoc)
        self.boundbox = self.raw_data[0].get_rect()
