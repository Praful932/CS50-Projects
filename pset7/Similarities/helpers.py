from nltk.tokenize import sent_tokenize
def lines(a, b):
    """Return lines in both a and b"""
    # splitlines breaks the string wherever newline is encountered
    a=a.splitlines()
    b=b.splitlines()
    # converts list into set to use set function intersection
    result=list((set(a)).intersection(set(b)))
    return result


def sentences(a, b):
    """Return sentences in both a and b"""
    # sent_tokenize returns a list of sentences
    a=sent_tokenize(a)
    b=sent_tokenize(b)
    result=list((set(a)).intersection(set(b)))
    return result

def subs(s,n):
    sub=[]
    for i in range((len(s)-n+1)):
        # append the len string to sub
            sub.append(s[i:(i+n)])
    return sub

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # pass to subs function to obtain list of substrings
    a=subs(a,n)
    b=subs(b,n)
    return list((set(a)).intersection(set(b)))
