""" Sprite
    ---
    ```
    from realpy import RsSprite
    ```
"""
from typing import Optional

from pygame.surface import Surface

__all__ = ["RsSprite"]


class RsSprite(object):
    """`RsSprite(image, mask_type, x_offset, y_offset)`
        ---
        Advance asset of image.
    """

    __slots__ = [
        "image", "mask_type", "width", "height", "radius", "xoffset", "yoffset", "boundbox", "center_distance",
        "center_angle", "using_custom_offset"
    ]

    from realpy.core.image import RsImage

    def __init__(self, image: RsImage, mask_type: int = 0, xo: int = 0, yo: int = 0):
        from realpy.core.image import RsImage
        from realpy.core.arithmetic import point_distance, point_direction

        assert image
        self.image: RsImage = image
        self.mask_type: int = mask_type
        self.width: int = image.boundbox.width
        self.height: int = image.boundbox.height
        self.radius: int = max(self.width, self.height)
        self.xoffset: int = xo
        self.yoffset: int = yo
        self.using_custom_offset: bool = False

        HalfX, HalfY = int(self.width * 0.5), int(self.height * 0.5)

        if self.xoffset == HalfX and self.yoffset == HalfY:
            self.center_distance = 0
            self.center_angle = 0
        else:
            self.center_distance = point_distance(xo, yo, HalfX, HalfY)
            self.center_angle = point_direction(xo, yo, HalfX, HalfY)
            self.using_custom_offset = True

        bx, bex = -xo, self.width - xo
        by, bey = -yo, self.height - yo
        self.boundbox = [(bx, by), (bex, by), (bx, bey), (bex, bey)]

    def draw(self, where: Surface, index, x, y, scale: float = 1, orientation: float = 0,
             alpha: float = 1, *, xflip: bool = False, yflip: bool = False) -> Optional[Surface]:
        from pygame import transform
        from pygame.surface import Surface
        from realpy.core.arithmetic import lengthdir_x, lengthdir_y

        if scale <= 0 or alpha <= 0:
            return None
        elif self.image:
            if 0 < self.image.number:
                index = index % self.image.number
                Frame: Surface = self.image.raw_data[index]

                Sizes = (int(scale * Frame.get_width()), int(scale * Frame.get_height()))
                Trx: Surface
                Trx = transform.scale(Frame, Sizes)
                if xflip or yflip:
                    Trx = transform.flip(Trx, xflip, yflip)

                if orientation != 0:
                    Trx = transform.rotate(Trx, orientation)
                # Trx = transform.rotozoom(Frame, orientation, scale)

                Position = Trx.get_rect()
                if self.using_custom_offset:
                    Lx = -lengthdir_x(self.center_distance, self.center_angle + orientation) * scale
                    if xflip:
                        Lx *= -1
                    Ly = -lengthdir_y(self.center_distance, self.center_angle + orientation) * scale
                    if yflip:
                        Ly *= -1
                    Position.center = (x + Lx, y + Ly)
                else:
                    Position.center = (x, y)

                where.blit(Trx, Position)
                return Trx
        return None


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
