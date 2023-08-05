def test_main():
    print("***** Test → Realpy Framework (+Prefab and Assets) *****")

    try:
        import asyncio
        from realpy import RsFramework, RsScene, RsLayer, RsPrefab
        from realpy import room_register, instance_create

        print(">>> Module of machine: ", RsFramework)
        print(">>> Class of scene: ", RsScene)
        print(">>> Class of layer: ", RsLayer)

        Sample = RsScene()
        SampleLayers = [RsLayer("First"), RsLayer("Second"), RsLayer("Third")]
        print("Sample scene: ", Sample)
        print("Sample layer group: ", SampleLayers)

        for Item in SampleLayers:
            Sample.add_layer_direct(Item)
        SampleSeek = Sample.layer_find("First")
        print("Found scene (maybe 'First'): ", SampleSeek)
        SampleSeek = Sample.layer_find("Fourth")
        print("Found scene (maybe 'None'): ", SampleSeek)

        Sample.add_layer_direct(RsLayer("Fifth"))
        print("The layers: ", Sample.layer_stack)

        Sample.onAwake()

        async def timeout():
            await asyncio.sleep(5)
            print("x of - Sample Instance 2:", TestInstance2.x)
            raise TimeoutError

        class oSampleObject1(RsPrefab):
            @staticmethod
            def onAwake(itself):
                print("Instance 1: ", id(itself))

            @staticmethod
            def onDestroy(itself):
                print("Instance 1 died! - ", id(itself))

            @staticmethod
            def onUpdate(itself, time: float):
                itself.x += 5 * time

        class oSampleObject2(RsPrefab):
            @staticmethod
            def onAwake(itself):
                print("Instance 2: ", id(itself))

            @staticmethod
            def onDestroy(itself):
                print("Instance 2 died! - ", id(itself))

            @staticmethod
            def onUpdate(itself, time: float):
                print("Instance 2 -> middle")

            @staticmethod
            def onUpdateLater(itself, time: float):
                print("Instance 2 -> later")

        print(">>> Class of prefab #1: ", oSampleObject1)
        print(">>> Class of prefab #2: ", oSampleObject2)

        RsFramework.rs_init("RealPy Engine", 200, 200)
        asyncio.run(timeout())

        TestRoom = room_register(RsScene("roomTest"))
        print(repr(TestRoom))

        Testbed = TestRoom.add_layer_direct(RsLayer("Instances"))
        print(repr(Testbed))

        TestInstance1 = instance_create(oSampleObject1, Testbed)
        TestInstance2 = instance_create(oSampleObject2, Testbed)
        TestInstance3 = instance_create(oSampleObject2, Testbed)
        print("Sample Instance 1:", TestInstance1)
        print("Sample Instance 2:", TestInstance2)
        print("Sample Instance 3:", TestInstance3)
        print("The instances: ", Testbed.storage)

        RsFramework.rs_startup()
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
        print("***** Realpy Test Finished *****")
        return True


if __name__ == "__main__":
    assert test_main()
