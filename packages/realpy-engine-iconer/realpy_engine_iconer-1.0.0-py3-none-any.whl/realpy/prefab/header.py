from typing import Type, Optional, List

from ..sprite import RsSprite


class RsPrefab(object):
    """`RsPrefab`
        ---
        A template class of game object. Contains its own sprite and hierachies.

        Do not instantiate this primitive behavior.
    """
    sprite_index: Optional[RsSprite] = None

    def __new__(cls, *args, **kargs):
        cls.__parent: Optional[Type[RsPrefab]] = None
        cls.children: Optional[List[Type[RsPrefab]]] = []
        return super(RsPrefab, cls).__new__(cls, *args, **kargs)

    def __repr__(self) -> str:
        SpriteCheck = f" ({self.sprite_index})" if self.sprite_index else ""
        return f"Prefab" + SpriteCheck + f" of {type(self)}"

    @property
    @classmethod
    def parent(cls):
        return cls.__parent

    @parent.setter
    @classmethod
    def parent(cls, target):
        if not target:
            if cls.__parent:
                cls.__parent.children.remove(cls)
            cls.__parent = None
        else:
            Parent = cls.__parent
            if Parent:
                Parent.children.remove(cls)
            cls.__parent = target
            target.children.append(cls)

    @staticmethod
    def onAwake(itself) -> None:
        """`onAwake(instance)`
            ---
            This will run on its instance. You may override it.
        """
        pass

    @staticmethod
    def onDestroy(itself) -> None:
        """`onDestroy(instance)`
            ---
            This will run on its instance. You may override it.
        """
        pass

    @staticmethod
    def onUpdate(itself, time: float):
        """`onUpdate(instance, time)`
            ---
            This will run on its instance. You may override it.
        """
        pass

    @staticmethod
    def onUpdateLater(itself, time: float) -> None:
        """`onUpdateLater(instance, time)`
            ---
            This will run on its instance. You may override it.
        """
        pass

    @staticmethod
    def onDraw(itself, time: float) -> None:
        """`onAwake(instance, time)`
            ---
            This will run on its instance. You may override it.
        """
        from realpy import RsPreset

        if itself.sprite_index:
            itself.sprite_index.draw(RsPreset.application_surface, itself.image_index, itself.x, itself.y,
                                     itself.image_scale, itself.image_angle, itself.image_alpha)

    @classmethod
    def instantiate(cls, scene, layer, x: float = 0, y: float = 0):
        """`instantiate(Scene, Layer, x=0, y=0)`
            ---
            Creates a instance of game object.
        """
        from .instance import RsInstance

        Result = RsInstance(cls, scene, layer, x, y)
        return Result
