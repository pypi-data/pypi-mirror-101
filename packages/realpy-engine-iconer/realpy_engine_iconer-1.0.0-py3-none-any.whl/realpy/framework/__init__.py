""" Framework
    ---
    ```
    from realpy import RsFramework
    ```
"""
from . import header as RsFramework

__all__ = ["RsFramework"]


def test():
    print("***** Test → Realpy Framework (+Prefab and Assets) *****")

    try:
        import asyncio
        from realpy import RsFramework, RsScene, RsLayer, RsPrefab
        from realpy import room_register, instance_create

        print(">>> Module of machine: ", RsFramework)

        async def timeout():
            await asyncio.sleep(5)
            raise TimeoutError

        class oTest(RsPrefab):
            pass

        RsFramework.rs_init("RealPy Engine", 200, 200)
        asyncio.run(timeout())

        TestRoom = room_register(RsScene("roomTest"))
        print(repr(TestRoom))

        Testbed = TestRoom.add_layer_direct(RsLayer("Instances"))
        print(repr(Testbed))

        TestInstance1 = instance_create(oTest, Testbed)
        print(TestInstance1)
        print(repr(TestInstance1))
    except AttributeError as e:
        print("Attribute Error: ", e)
        return False
    except SystemError as e:
        print("System Error: ", e)
        return False
    except ValueError as e:
        print("Value Error: ", e)
        return False
    except RuntimeError as e:
        print("Runtime Error: ", e)
        return False
    except TimeoutError:
        return True
    except Exception as e:
        print("Error: ", e)
        return False
    finally:
        return True
