""" Global Game Settings
    ---
    ```
    from realpy import RsPreset
    ```
"""
from . import header as RsPreset

__all__ = ["RsPreset"]


# TODO: #22 Make a test from preset.
def test():
    print("***** Test → Realpy Settings *****")

    try:
        print(">>> Module of setting: ", RsPreset)
    except Exception as e:
        print("Error: ", e)
        return False
    return True
