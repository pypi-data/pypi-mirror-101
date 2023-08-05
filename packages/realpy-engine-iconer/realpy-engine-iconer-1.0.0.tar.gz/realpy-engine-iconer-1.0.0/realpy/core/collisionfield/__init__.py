# TODO: #38 Collision field: New tile based collider
from typing import List, overload


class RsCollsionField(object):
    def __init__(self, x: int, y: int, width: int, height: int, grid_width: int, grid_height: int):
        self.enabled = True
        self.X = x
        self.Y = y
        self.WIDTH = width
        self.HEIGHT = height
        self.GRID_W: int = grid_width
        self.GRID_H: int = grid_height

        count_w = int(width / grid_width)
        count_h = int(height / grid_height)
        self.cells: List[int] = [0] * count_h * count_w

    @overload
    def set(self, x: int, y: int, value: int):
        self.cells[x + y * self.WIDTH] = value

    @overload
    def set(self, x: int, y: int, container: List[int]):
        for nth, value in enumerate(container):
            self.cells[x + y * self.WIDTH + nth] = value

    def get(self, x: int, y: int) -> int:
        return self.cells[x + y * self.WIDTH]
