""" Image Resource
    ---
    ```
    from realpy import RsImage
    ```
"""
from .header import RsImage

__all__ = ["RsImage"]


def test():
    print("***** Test → Realpy Image *****")

    try:
        import os, pygame

        pygame.init()

        print(">>> Class of image: ", RsImage)

        Sample_location = os.path.dirname(__file__) + "\\test_image.png"
        print("Sample location: ", Sample_location)

        Sample_s = RsImage(Sample_location)
        print("Sample single image: ", Sample_s)
        print("Filename: ", Sample_s.filename)
        print("Frames: ", Sample_s.number)
        print("Dimension: ", Sample_s.boundbox)
        print("Raw: ", Sample_s.raw_data[0])

        Sample_m = RsImage([Sample_location] * 5)
        print("Sample multiple image: ", Sample_m)
        print("Filename: ", Sample_m.filename)
        print("Frames: ", Sample_m.number)
        print("Dimension: ", Sample_m.boundbox)
        print("Raw pile: ", Sample_m.raw_data)
        print("Raw: ", *Sample_m.raw_data)
    except SystemError as e:
        print("System Error: ", e)
        return False
    except FileNotFoundError as e:
        print("FileNotFound Error: ", e)
        return False
    except OSError as e:
        print("OS Error: ", e)
        return False
    except AttributeError as e:
        print("Attribute Error: ", e)
        return False
    except PermissionError as e:
        print("Permission Error: ", e)
        return False
    except RuntimeError as e:
        print("Runtime Error: ", e)
        return False
    except Exception as e:
        print("Error: ", e)
        return False
    return True
