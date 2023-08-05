""" Layer
    ---
    ```
    from realpy import RsLayer
    ```
"""
from .header import RsLayer

__all__ = ["RsLayer"]


def test():
    print("***** Test → Realpy Layer *****")

    class PseudoInstance1:
        def __init__(self) -> None:
            self.x = 0

        def onAwake(self):
            print("Instance 1: ", id(self))

        def onDestroy(self):
            print("Instance 1 died! - ", id(self))

        def onUpdate(self, time: float):
            self.x += 5 * time

    class PseudoInstance2:
        def onAwake(self):
            print("Instance 2: ", id(self))

        def onDestroy(self):
            print("Instance 2 died! - ", id(self))

        def onUpdate(self, time: float):
            print("Instance 2 -> middle")

        def onUpdateLater(self, time: float):
            print("Instance 2 -> later")

    try:
        print(">>> Class of scene: ", RsLayer)
        print(">>> Class of simulated instance #1: ", PseudoInstance1)
        print(">>> Class of simulated instance #2: ", PseudoInstance2)

        Sample = RsLayer("Sample Layer")
        print("Sample layer: ", Sample)

        Instance1 = Sample.add_instance(PseudoInstance2())
        Instance2 = Sample.add_instance(PseudoInstance1())
        Instance3 = Sample.add_instance(PseudoInstance2())
        print("Sample Instance 1: ", Instance1)
        print("Sample Instance 2: ", Instance2)
        print("Sample Instance 3: ", Instance3)
        print("The instances: ", Sample.storage)

        Sample.onAwake()
        for i in range(10):
            Sample.onUpdate(1)
        Sample.onDestroy()

        print("Resulf - Sample Instance 2: ", Instance2.x)
    except TypeError as e:
        print("Type Error: ", e)
        return False
    except AttributeError as e:
        print("Attribute Error: ", e)
        return False
    except Exception as e:
        print("Error: ", e)
        return False
    return True
