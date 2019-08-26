from sys import argv
import string
import crypt
from itertools import permutations

if len(argv)!=2:
    exit("Usage: python crack.py hash")
else:
    inputhash = argv[1]
    salt = inputhash[0:2]
    alphabets = string.ascii_letters
    # itertools will generate a tuple
    for n in range(5):
        for p in permutations(alphabets, n+5):
            #   to join the string genereate as ('a'), ('b'),...
            outputhash = crypt.crypt("".join(p),salt)
            if inputhash == outputhash:
                exit("".join(p))
