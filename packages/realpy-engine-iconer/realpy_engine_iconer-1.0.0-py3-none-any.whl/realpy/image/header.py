import os
from typing import List

import pygame.rect as PyRect
import pygame.image as PyImage


class RsImage(object):
    """`RsImage(image_path)`
        ---
        Raw image of a sprite that contains single or multiple images.
    """

    def __init__(self, filepath):
        self.number: int = -1
        self.raw_data = []
        self.boundbox = PyRect.Rect(0, 0, 0, 0)

        if type(filepath) is str:
            self.number = 0

            Temp = PyImage.load(filepath).convert_alpha()
            self.raw_data.append(Temp)
            self.filename = os.path.basename(filepath)
            self.boundbox = Temp.get_rect()
        else:
            self.number = len(filepath)

            for file in filepath:
                self.raw_data.append(PyImage.load(file).convert_alpha())
            self.filename = os.path.basename(filepath[0])
            self.boundbox = self.raw_data[0].get_rect()
