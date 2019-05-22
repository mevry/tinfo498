from trie.trie_node import TrieNode
import csv

class Trie():
    
    def __init__(self, wordlist_path):
        self._root = TrieNode("root")
        self._root._isroot = True
        self.num_words = 0
        self.word_in_progress = []
        self.build_trie(wordlist_path)
        self.best_candidate = ('', 0)

    def _word_increment(self, current_node, current_word, current_char, frequency):
        if current_char == current_word[-1]:
            current_node._word = True
            current_node._frequency = frequency
            self.num_words += 1

    def build_trie(self, wordlist_path):
        #open wordlist file
        with open(wordlist_path, 'r') as wordlist:
            fieldnames = ("word", "frequency")
            csv_reader = csv.DictReader(wordlist, fieldnames=fieldnames)
            for row in csv_reader:
                word_strip = row["word"]
                freq_strip = int(row["frequency"])
                current = self._root
                for char in word_strip:
                    #check if char exists
                    #if no, add and update pointer
                    if not current.node_exists(char):
                        current.add_child(char)
                        #move down tree
                        current = current.get_child_node(char)
                        #if last char in word, mark as complete word
                        self._word_increment(current, word_strip, char, freq_strip)
                    #if yes, update pointer
                    else:
                        current = current.get_child_node(char)
                        self._word_increment(current, word_strip, char, freq_strip)

    def _build_word(self, word_in_progress, parent_node):
        for k,v in parent_node._children.items():
            word_in_progress.append(k)
            #if its a complete word, we can print it
            if v._word:
                print(''.join(map(str, word_in_progress)))
                

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
                print(''.join(map(str, word_in_progress)) + " " + str(v._frequency))
                
            #if it has children we still need to move down the trie
            if v._children:
                self.enumerate(word_in_progress, v)
            #no children, we can start removing chars
            word_in_progress.pop()
            
    def find_subtree(self, text, parent_node=None):
        #Search for text
        if parent_node is None:
            parent_node = self._root
        
        #skip if empty string or 1st char has no children
        if text is not '' and str(text[0]) in parent_node._children.keys():
            parent_node = parent_node.get_child_node(text[0])
            self.find_subtree(text[1:], parent_node)
        if parent_node is self._root:
            parent_node = None
        return parent_node


    def search_candidates(self, word_in_progress, parent_node):

        if parent_node is None:
            return
        if parent_node._children.items() is not None:
            for k,v in parent_node._children.items():
                self.word_in_progress.append(k)
                print("Word in progress: " + ''.join(map(str,self.word_in_progress)))
                print(str(k) + " Frequency: " + str(v._frequency))
                print("Current Best Candidate: " + str(self.best_candidate[0]))
                #if its a complete word, check candidacy
                if v._word and v._frequency > self.best_candidate[1]:
                    self.best_candidate = (''.join(map(str,self.word_in_progress)), v._frequency)
                    print("BC Tuple")
                    print("--------")
                    print(self.best_candidate)
                #if it has children we still need to move down subtree
                if v._children:
                    self.search_candidates(self.word_in_progress, v)
                #no children, we can start removing chars
                if len(self.word_in_progress) > 0:
                    self.word_in_progress.pop()

    def predict(self, text):
        print("Passed In: " + text)
        self.word_in_progress = []
        for char in text:
            self.word_in_progress.append(char)
        self.best_candidate = ('', 0)
        self.search_candidates(self.word_in_progress, self.find_subtree(text))
        return self.best_candidate[0]


        #Return subtree of text

        #Sort subtree by ranking (priority queue)

    def insert_child(self, child_node):
        pass

        
    def remove_child(self, child_node):
        pass

        
    def find(self, character):
        pass
