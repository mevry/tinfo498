from node import Node

class Bst:
    def __init__(self, data):
        if data is None:
            self._root = None
            self._count = 0
        else:
            self._root = Node(data, None)
            self._count = 1 
        
    def insert(self, data):
        if self._root is None:
            pass