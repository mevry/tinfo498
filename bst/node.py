

class Node:
    def __init__(self, value, parent):
        self._value = value
        self._parent = parent
        self._leftNode = None
        self._rightNode = None
    
    def get_parent(self):
        return self._parent

    def set_left(self, leftNode):
        self._leftNode = leftNode

    def set_right(self, rightNode):
        self._rightNode = rightNode

    def get_value(self):
        return self._value