from typing import List


class RsActor(object):
    """`RsActor(Layer)`
        ---
    """

    def __init__(self, layer):
        self.enabled: bool = True
        self.layer = layer
        self.department: List[List] = []
        self.onAwake = None
        self.onDestroy = None
        self.onUpdate = None
        self.onUpdateLater = None
        self.onDraw = None

    def __del__(self):
        for Group in self.department:
            Group.remove(self)

    def attach(self, ogroup: List):
        ogroup.append(self)
        self.department.append(ogroup)
