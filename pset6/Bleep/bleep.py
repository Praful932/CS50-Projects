from cs50 import get_string
from sys import argv
import string


def main():
    banned = []
    if len(argv) != 2:
        exit("Usage: python bleep.py dictionary")
    else:
        #   open list of banned words in read mode
        dict = open(argv[1], "r")
        for x in dict:
            # since words will be one per line, skip last character of each readLine
            banned.append(x[:-1])
        print("What message would you like to censor?")
        msg = input()
        msg = msg.split()
        # iterate through list of banned words
        for word in msg:
            if word.lower() in banned:
                for x in word:
                    print("*", end='')
            else:
                print(word, end='')
            # for space after every word
            print(' ',end='')
        print()

if __name__=='__main__':
    main()
