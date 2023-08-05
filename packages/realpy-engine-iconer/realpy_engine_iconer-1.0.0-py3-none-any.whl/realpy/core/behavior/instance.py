from copy import copy
from typing import Any, List, Optional, Tuple, Type


class RsInstance(object):
    """`RsInstance(Prefab, Layer, x, y)`
        ---
    """

    def __init__(self, original: Type[Any], layer, x: float = 0, y: float = 0):
        from pygame.surface import Surface
        from realpy.core.layer import RsLayer
        from realpy.core.sprite import RsSprite

        self.enabled: bool = True
        self.layer: Optional[RsLayer] = layer
        self.department: List[List] = []
        self.visible: bool = True
        self.original = original
        self.x: float = x
        self.y: float = y
        self.__use_collision: bool = original.use_collision
        self.__sprite_index: Optional[RsSprite] = original.sprite_index
        self.__image: Optional[Surface] = None
        self.image_index: float = 0
        self.__image_angle: float = 0
        self.image_scale: float = 1
        self.image_alpha: float = 1
        self.__speed: float = 0
        self.__direction: float = 0
        self.__hspeed: float = 0
        self.__vspeed: float = 0
        self.friction: float = 0
        self.boundbox: Optional[List[Tuple[int, int]]]
        self.bound_vertexes: Optional[List[Tuple[int, int]]]
        if self.__sprite_index:
            self.boundbox = copy(self.__sprite_index.boundbox)
            self.bound_vertexes = copy(self.__sprite_index.boundbox)
        else:
            self.boundbox = None
            self.bound_vertexes = None

        MethodA = self.original.onAwake
        if MethodA:
            self.onAwake = lambda: MethodA(self)
        else:
            self.onAwake = None
        MethodD = self.original.onDestroy
        if MethodD:
            self.onDestroy = lambda: MethodD(self)
        else:
            self.onDestroy = None
        Method = self.original.onUpdate
        if Method:
            self.onUpdate = lambda time: Method(self, time)
        else:
            self.onUpdate = None

    def __del__(self):
        for Group in self.department:
            Group.remove(self)

    def attach(self, ogroup: List):
        ogroup.append(self)
        self.department.append(ogroup)

    def acceleration(self, velocity, direction):
        from realpy.core.arithmetic import lengthdir_x, lengthdir_y, point_distance, point_direction

        Vx = lengthdir_x(velocity, direction)
        Vy = lengthdir_y(velocity, direction)
        self.__hspeed += Vx
        self.__vspeed += Vy
        self.__speed = point_distance(0, 0, self.__hspeed, self.__vspeed)
        self.__direction = point_direction(0, 0, self.__hspeed, self.__vspeed)

    def draw_self(self) -> bool:
        from realpy import RsPreset

        Where = RsPreset.application_surface
        if Where and self.sprite_index:
            self.__image = self.sprite_index.draw(Where, self.image_index, self.x, self.y,
                                                  self.image_scale, self.image_angle, self.image_alpha).convert_alpha()

            if RsPreset.debug_get() and self.can_collide:
                from pygame import draw
                draw.line(Where, "red", self.bound_vertexes[0], self.bound_vertexes[1])
                draw.line(Where, "red", self.bound_vertexes[1], self.bound_vertexes[3])
                draw.line(Where, "red", self.bound_vertexes[3], self.bound_vertexes[2])
                draw.line(Where, "red", self.bound_vertexes[2], self.bound_vertexes[0])
                draw.circle(Where, "red", (self.x, self.y), 8)
            return True
        else:
            return False

    @property
    def can_collide(self) -> bool:
        return self.__use_collision

    @property
    def sprite_index(self):
        return self.__sprite_index

    @property
    def current_image(self):
        return self.__image

    @property
    def speed(self) -> float:
        return self.__speed

    @property
    def direction(self) -> float:
        return self.__direction

    @property
    def hspeed(self) -> float:
        return self.__hspeed

    @property
    def vspeed(self) -> float:
        return self.__vspeed

    @property
    def image_angle(self) -> float:
        return self.__image_angle

    @speed.setter
    def speed(self, value: float):
        from realpy.core.arithmetic import lengthdir_x, lengthdir_y

        self.__speed = value
        self.__hspeed = lengthdir_x(value, self.__direction)
        self.__vspeed = lengthdir_y(value, self.__direction)

    @direction.setter
    def direction(self, value: float):
        from realpy.core.arithmetic import lengthdir_x, lengthdir_y

        self.__direction = value
        if self.__speed != 0:
            self.__hspeed = lengthdir_x(self.__speed, self.__direction)
            self.__vspeed = lengthdir_y(self.__speed, self.__direction)

    @hspeed.setter
    def hspeed(self, value: float):
        from realpy.core.arithmetic import point_distance, point_direction

        self.__hspeed = value
        self.__speed = point_distance(0, 0, self.__hspeed, self.__vspeed)
        self.__direction = point_direction(0, 0, self.__hspeed, self.__vspeed)

    @vspeed.setter
    def vspeed(self, value: float):
        from realpy.core.arithmetic import point_distance, point_direction

        self.__vspeed = value
        self.__speed = point_distance(0, 0, self.__hspeed, self.__vspeed)
        self.__direction = point_direction(0, 0, self.__hspeed, self.__vspeed)

    @sprite_index.setter
    def sprite_index(self, index):
        # Update the original boundbox
        if not index:  # Free the memory
            self.__sprite_index = None
            del self.__image
            del self.boundbox
            del self.bound_vertexes
        elif not self.__sprite_index:  # Create boundbox
            self.__sprite_index = index
            if self.can_collide:  # Use only at it can collide with other
                self.boundbox = copy(index.boundbox)
                self.bound_vertexes = copy(index.boundbox)
        else:  # Don't update the currrent boundbox
            self.__sprite_index = index

    @image_angle.setter
    def image_angle(self, value: float):
        # Update the actual boundbox
        if self.__image_angle != value:
            self.__image_angle = value

    def onUpdateLater(self, time: float) -> None:
        """`onUpdateLater(time)`
            ---
            Do not override it.
        """
        from realpy import RsPreset
        from realpy.core.arithmetic import lengthdir_x, lengthdir_y

        Method = self.original.onUpdateLater
        if Method:
            Method(self, time)

        if self.speed != 0:
            Hspeed: float
            Vspeed: float
            if self.friction != 0:
                Fx = lengthdir_x(self.friction, self.direction)
                Fy = lengthdir_y(self.friction, self.direction)
                if 0 < self.speed:
                    Hspeed = self.__hspeed * time - 0.5 * time * time * Fx
                    Vspeed = self.__vspeed * time - 0.5 * time * time * Fy
                    self.speed = max(0, self.speed - self.friction * time)
                else:
                    Hspeed = self.__hspeed * time + 0.5 * time * time * Fx
                    Vspeed = self.__vspeed * time + 0.5 * time * time * Fy
                    self.speed = min(0, self.speed + self.friction * time)
            else:
                Hspeed = self.__hspeed * time
                Vspeed = self.__vspeed * time

            if Hspeed != 0:
                self.x += Hspeed

            if Vspeed != 0:
                self.y += Vspeed

        if self.can_collide and self.__sprite_index and RsPreset.debug_get():
            self._set_vertex_boundary(self.__image_angle)

    def onDraw(self, time: float) -> None:
        """`onDraw(time)`
            ---
            Do not override it.
        """
        if self.visible:
            Method = self.original.onDraw
            if Method:
                Method(self, time)
            else:
                self.draw_self()

    def __str__(self) -> str:
        return f"Realpy Instance of {self.original}"

    def __repr__(self) -> str:
        return f"Instance {id(self)} at '{self.layer}'"

    def _set_vertex_boundary(self, angle: float) -> None:
        from realpy.core.arithmetic import lengthdir_x, lengthdir_y

        Cos = lengthdir_x(self.image_scale, angle)
        Sin = lengthdir_y(self.image_scale, angle)

        for i in range(0, 4):
            TempPoint = self.boundbox[i]
            TempA = TempPoint[0]
            TempB = TempPoint[1]
            TempX = round(self.x + TempA * Cos - TempB * Sin)
            TempY = round(self.y + TempA * Sin + TempB * Cos)
            # print("Point(", i, ") - ", TempPoint, " -> (", TempX, ", ", TempY, ")")

            self.bound_vertexes[i] = (TempX, TempY)
