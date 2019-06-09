from trie.trie_node import TrieNode
from tempfile import NamedTemporaryFile
import shutil
import csv
import time
import shelve

class Trie():
    def __init__(self, wordlist_path):
        self._root = TrieNode("root")
        self._root._isroot = True
        self._level = 0
        self.num_words = 0
        self.word_in_progress = []
        self.build_trie(wordlist_path)
        self.best_candidate = ('', 0)
        self.word_buffer = {}

    def _word_increment(self, current_node, current_word, current_char, frequency):
        #if last char, then must be word
        if current_char == current_word[-1]:
            current_node.set_word(True)
            current_node.set_base_freq(frequency)
            self.num_words += 1

    def _get_wip(self):
        return ''.join(map(str, self.word_in_progress))

    def save_custom(self):
        print("Saving trie...")
        with shelve.open('data/personal_wordlist') as personal_wordlist:
            for k, v in self.word_buffer.items():
                personal_wordlist[str(k)] = v
        self.word_buffer = {}
        print("Saved")

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
                if not current.is_word():
                    current.set_word(True)
                    self.num_words += 1
                current.set_base_freq(freq_strip)                
        with shelve.open('data/personal_wordlist') as custom_wordlist:
            for k, v in custom_wordlist.items():
                word = str(k)
                freq = int(v)
                print('Adding: {word}, {freq}'.format(word=word, freq=freq))
                current = self._root
                for char in word:
                    if not current.node_exists(char):
                        current.add_child(char)
                    current = current.get_child_node(char)
                if not current.is_word():
                    current.set_word(True)
                    self.num_words += 1
                current.set_personal_freq(freq)
        children = self._root.get_children()
        for child_node in children.values():
            child_node.top_word = self.predict(child_node.get_value(), True)
            print(child_node.top_word[0])
        print("Trie build time: " + str(time.time() - build_time))
        print("Trie number of words: " + str(self.num_words))

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

    def enumerate_save(self, word_in_progress=None, parent_node=None, handle=None):
        if word_in_progress is None:
            word_in_progress = self.word_in_progress
        if parent_node is None:
            parent_node = self._root
        for k,v in parent_node._children.items():
            word_in_progress.append(k)
            #if its a complete word, we can print it
            if v.is_word() and v.get_personal_freq() > 0:
                handle.write("{custom},{freq}\n".format(custom=''.join(map(str, word_in_progress)), freq=str(v.get_personal_freq())))
            #if it has children we still need to move down the trie
            if v._children:
                self.enumerate_save(word_in_progress, v)
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
                print(''.join(map(str, word_in_progress)) + " " + str(v.get_frequency())) 
            #if it has children we still need to move down the trie
            if v._children:
                self.enumerate(word_in_progress, v)
            #no children, we can start removing chars
            word_in_progress.pop()

    def update_rank(self, text):
        if text is not '':
            node = self.find_subtree(text)
            if node is not None and node.is_word():
                node.increment_frequency()
                self.word_buffer[text] = node.get_personal_freq()
                print("{text}: {freq}".format(text=text, freq=node.get_frequency()))
                #update new L1 top child
                child = self._root.get_child_node(text[0])
                child.top_word = self.predict(child.get_value(), True)
                print("Current word buffer: ")
                for k in self.word_buffer.keys():
                    print(k)
            else:
                print("{text} is not in dictionary".format(text=text))
        else:
            print("Empty string invalid.")

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
                if v.is_word() and v.get_frequency() > self.best_candidate[1]:
                    self.best_candidate = (''.join(map(str,self.word_in_progress)), v.get_frequency())
                #if it has children we still need to move down subtree
                if v._children:
                    self.search_candidates(v)
                #no children, we can start removing chars
                self.word_in_progress.pop()
        
    def predict(self, text, init=False):
        #Reset/Initialize
        self.word_in_progress = []
        for char in text:
            self.word_in_progress.append(char)
        self.best_candidate = ('', 0)
        #if text is empty, no need to search
        if text is not '':
            search_start = time.time()
            #if only 1 char, retrieve presearched results
            if init is True:
                self.search_candidates(self.find_subtree(text))
            else:
                if len(text) == 1:
                    child = self._root.get_child_node(text)
                    self.best_candidate = child.top_word
                else:
                    self.search_candidates(self.find_subtree(text))
            print(text + " search time: " + str(time.time()-search_start))
        return self.best_candidate
