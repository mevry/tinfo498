import random
import os.path
from pathlib import Path


def gen_rand_freq(max_rand_val, in_file, out_path=Path.cwd()):
    print("out_path: " + str(out_path))
    with open(in_file, 'r') as raw_dictionary, open(out_path, 'a+') as out_dictionary:
        for word in raw_dictionary:
            out_dictionary.write('{word},{random}\n'.format(word=word.rstrip(), random=random.randint(0, max_rand_val)))

#foreach word, generate k,v w/random val 
infile = Path.cwd() / 'data/wordlist.10000.txt'
outfile = Path.cwd() / 'data/wordlist.10000.rank.txt'
gen_rand_freq(1, infile, outfile)
