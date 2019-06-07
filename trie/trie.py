from trie.trie_node import TrieNode
import csv
import time


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

    def _get_wip(self):
        return ''.join(map(str,self.word_in_progress))

    def build_trie(self, wordlist_path):
        print("Building trie...")
        build_time = time.time()
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
        print("Trie build time: " + str(time.time() - build_time))

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

    def update_rank(self, text):
        node = self.find_subtree(text)
        if node is not None and node.is_word():
            node.increment_frequency()
            print("{text}: {freq}".format(text=text,freq=node.get_frequency()))
        else:
            print("{text} is not in dictionary".format(text=text))

    def find_subtree(self, text, current_node=None):
        #Start at root
        if current_node is None:
            current_node = self._root
        #print("Current Node: " + current_node._value)
        #if no matching child, then there is no possible match
        if str(text[0]) not in current_node._children.keys():
            current_node = None
        else:
            current_node = current_node.get_child_node(text[0])
            #If there are more chars in text, recurse
            if text[1:]:
                current_node = self.find_subtree(text[1:], current_node)
        return current_node

    def search_candidates(self, current_node):
        if current_node is None:
            print("No parent node.")
            return
        if current_node._children.items() is not None:
            for k,v in current_node._children.items():
                self.word_in_progress.append(k)
                #if its a complete word, check candidacy
                if v._word and v._frequency > self.best_candidate[1]:
                    self.best_candidate = (''.join(map(str,self.word_in_progress)), v._frequency)
                #if it has children we still need to move down subtree
                if v._children:
                    self.search_candidates(v)
                #no children, we can start removing chars
                self.word_in_progress.pop()
        
    def predict(self, text):
        #Reset/Initialize
        self.word_in_progress = []
        for char in text:
            self.word_in_progress.append(char)
        self.best_candidate = ('', 0)
        #if text is empty, no need to search
        if text is not '':
            search_start = time.time()
            self.search_candidates(self.find_subtree(text))
            print(text + " search time: " + str(time.time()-search_start))
        return self.best_candidate[0]

    def remove_child(self, child_node):
        pass
        
