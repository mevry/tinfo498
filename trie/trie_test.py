import unittest
import os.path
from pathlib import Path
from trie import Trie


class Test_TrieEnumerate(unittest.TestCase):
    test_path = Path.cwd() / 'data/wordlist.txt'


    trie = Trie(test_path)
    word = []
    word.append(trie.enumerate(word))
    print(word)
    print("omg")

