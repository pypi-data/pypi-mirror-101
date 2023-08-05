class RsLayer(object):
    """`RsLayer(name)`
        ---
        Belongs to a scene and executes game instances.
    """

    def __init__(self, name: str = ""):
        self.name: str = name
        self.storage = []

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Realpy Layer {self.name} ({len(self.storage)})"

    def add_instance(self, instance):
        self.storage.append(instance)
        return instance

    def onAwake(self) -> None:
        for Instance in self.storage:
            Instance.onAwake()

    def onDestroy(self) -> None:
        for Instance in self.storage:
            Instance.onDestroy()

    def onUpdate(self, time: float) -> None:
        for Instance in self.storage:
            Instance.onUpdate(time)

    def onUpdateLater(self, time: float) -> None:
        for Instance in self.storage:
            Instance.onUpdateLater(time)

    def onDraw(self, time: float) -> None:
        for Instance in self.storage:
            Instance.onDraw(time)
