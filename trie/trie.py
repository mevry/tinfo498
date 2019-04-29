from trie_node import TrieNode

class Trie():
    
    def __init__(self, wordlist_path):
        self._root = TrieNode("root")
        self._root._isroot = True
        self.num_words = 0
        self.build_dictionary(wordlist_path)
        
    
    def build_dictionary(self, wordlist_path):
        #open wordlist file
        with open(wordlist_path, 'r') as wordlist:
            for word in wordlist:
                word_strip = word.rstrip()
                current = self._root
                for char in word_strip:
                    #check if char exists
                    #if no, add and update pointer
                    if not current.node_exists(char):
                        current.add_child(char)
                        #move down tree
                        current = current.get_child_node(char)
                        #if last char in word, mark as complete word
                        if char == word_strip[-1]:
                            current._word = True
                            self.num_words += 1
                        
                    #if yes, update pointer
                    else:
                        current = current.get_child_node(char)




    def search_word(self, word):
        pass

    def insert_child(self, child_node):
        pass

        
    def remove_child(self, child_node):
        pass

        
    def find(self, character):
        pass

'''
a
an
cat
and
'''