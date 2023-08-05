""" Prefab
    ---
    ```
    from realpy import RsPrefab, RsActor, RsInstance
    ```
"""
from .actor import RsActor
from .instance import RsInstance

__all__ = ["RsPrefab", "RsActor", "RsInstance"]


class RsPrefab(object):
    """`RsPrefab`
        ---
        Predefined behavior object.

        Do not instantiate it.

        ### List of flow methods
        - `onAwake()`
        - `onDestroy()`
        - `onUpdate(delta_time)`
        - `onUpdateLater(delta_time)`
        - `onDraw(delta_time)`

        ### Specification
        ```
        @staticmethod
        def onDraw(itself, time: float) -> None:
            pass
        ```
    """

    name: str = ""
    sprite_index = None
    use_collision: bool = True
    trait_instance = RsInstance

    onAwake = None
    onDestroy = None
    onUpdate = None
    onUpdateLater = None
    onDraw = None

    @staticmethod
    def onTest(itself, time: float) -> None:
        """`onTest(instance, time)`
            ---
            This will run on its instance. You may override it.
        """
        pass
