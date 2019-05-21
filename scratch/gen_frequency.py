import random
import os.path
from pathlib import Path


def gen_rand_freq(max_rand_val, in_file, out_path=Path.cwd().parent):
    print("out_path: " + str(out_path))
    out_file = out_path / "new_dictionary.txt"
    with open(in_file, 'r') as raw_dictionary, open(out_file, 'a+') as out_dictionary:
        for word in raw_dictionary:
            out_dictionary.write('{word},{random}\n'.format(word=word.rstrip(), random=random.randint(0, max_rand_val)))
        
#open text file

#foreach word, generate k,v w/random val 
infile = Path.cwd().parent / 'data/wordlist.txt'

gen_rand_freq(50, infile)
