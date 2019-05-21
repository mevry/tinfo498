from trie.trie_node import TrieNode

class Trie():
    
    def __init__(self, wordlist_path):
        self._root = TrieNode("root")
        self._root._isroot = True
        self.num_words = 0
        self.word_in_progress = []
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

    def _build_word(self, word_in_progress, parent_node):
        for k,v in parent_node._children.items():
            word_in_progress.append(k)
            #if its a complete word, we can print it
            if v._word:
                print(''.join(map(str,word_in_progress)))
                

            #if it has children we still need to move down the trie
            if v._children:
                self._build_word(word_in_progress, v)
            #no children, we can start removing chars
            word_in_progress.pop()


    def enumerate(self, word_in_progress=None, parent_node=None):
        if word_in_progress is None:
            word_in_progress = self.word_in_progress
        if parent_node is None:
            parent_node = self._root
        for k,v in parent_node._children.items():
            word_in_progress.append(k)
            #if its a complete word, we can print it
            if v._word:
                yield ''.join(map(str,word_in_progress))
                
            #if it has children we still need to move down the trie
            if v._children:
                self.enumerate(word_in_progress, v)
            #no children, we can start removing chars
            word_in_progress.pop()
            
    def find_subtree(self, text, parent_node=None):
        #Search for text
        if parent_node is None:
            parent_node = self._root
        if text[0] is not None and text[0] in parent_node._children.keys():
            self.predict(text[1:], parent_node)
        return parent_node

        #Return subtree of text

        #Sort subtree by ranking (priority queue)

    def insert_child(self, child_node):
        pass

        
    def remove_child(self, child_node):
        pass

        
    def find(self, character):
        pass
