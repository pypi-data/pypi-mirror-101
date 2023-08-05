from typing import Optional
from numpy import matrixlib

from pygame.surface import Surface
from pygame import transform

__all__ = ["RsSprite"]


class RsSprite(object):
    """`RsSprite(image, mask_type, x_offset, y_offset)`
        ---
        Advance asset of image.
    """

    def __init__(self, image, mask_type: int = 0, xo: int = 0, yo: int = 0):
        self.image = image
        self.mask_type: int = mask_type
        self.width: int = image.boundbox.width
        self.height: int = image.boundbox.height
        self.radius: int = max(xo, yo)
        self.xoffset: int = xo
        self.yoffset: int = yo

    def draw(self, where: Surface, index: int, x: int, y: int, scale: float = 1, orientation: float = 0,
             alpha: float = 1):
        if 0 == scale or alpha <= 0:
            return
        if self.image:
            if self.image.number == 0:
                Image: Surface = self.image.raw_data[0]

                Trx: Surface = transform.rotozoom(Image, orientation, scale)
                Position = Trx.get_rect()
                Position.center = (x, y)
                where.blit(Trx, Position)
            elif 0 < self.image.number:
                Image: Surface = self.image.raw_data[index]
                Position = Image.get_rect()
                Position.center = (x, y)
                where.blit(Image, Position)


"""
def sprite_json_loads():
    try:
        with open("Data\\sprite.json") as sprfile:
            parsed = json.load(sprfile)

            for content in parsed:
                sprite_load(content["path"], content["name"], content["xoffset"], content["yoffset"], content["number"])

    except FileNotFoundError:
        pass
"""
