from cs50 import get_int
while True:
    n=get_int("Height: ")
    if n>8 or n<=0:
        continue
    else:
        for i in range(n):
            for w in range(n-i-1):
                print(" ",end='')
            for h in range(i+1):
                print("#",end='')
            print()
        break

