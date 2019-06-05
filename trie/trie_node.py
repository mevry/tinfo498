

class TrieNode():
    def __init__(self, value):
        self._value = value
        self._children = {}
        self._word = False
        self._frequency = 0

    #add node for character
    def add_child(self, child_character):
        self._children[child_character] = TrieNode(child_character)


    def get_value(self):
        return self._value

    def get_children(self):
        return self._children

    #retrieve node for character
    def get_child_node(self, child_character):
        return self._children[child_character]

    #check if node exists for character
    def node_exists(self, child_character):
        if child_character not in self._children:
            return False
        else:
            return True
    
    def increment_frequency(self):
        self._frequency += 1