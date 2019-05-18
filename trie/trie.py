from trie_node import TrieNode

class Trie():
    
    def __init__(self, wordlist_path):
        self._root = TrieNode("root")
        self._root._isroot = True
        self.num_words = 0
        self.build_trie(wordlist_path)
        
    def _word_increment(self, current_node, current_word, current_char):
        if current_char == current_word[-1]:
            current_node._word = True
            self.num_words += 1

    def build_trie(self, wordlist_path):
        #open wordlist file
        with open(wordlist_path, 'r') as wordlist:
            for word in wordlist:
                #strip \n off end
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
                        self._word_increment(current, word_strip, char)
                    #if yes, update pointer
                    else:
                        current = current.get_child_node(char)
                        self._word_increment(current, word_strip, char)

    def _build_word(self,word_in_progress, parent_node):
        for k,v in parent_node._children.items():
            word_in_progress.append(k)
            #if its a complete word, we can print it
            if v._word:
                yield ''.join(map(str,word_in_progress))

            #if it has children we still need to move down the trie
            if v._children:
                self._build_word(word_in_progress, v)
            #no children, we can start removing chars
            word_in_progress.pop()


    def enumerate(self):
        word = []
        self._build_word(word, self._root)
        print("Number of words: ", self.num_words)

            
    def search_word(self, word):
        pass

    def insert_child(self, child_node):
        pass

        
    def remove_child(self, child_node):
        pass

        
    def find(self, character):
        pass
