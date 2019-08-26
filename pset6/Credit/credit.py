from cs50 import get_int
sum1,notaltsum,pos,counter=0,0,0,0
n=get_int("Number: ")
while n!=0:
    digit=n%10
    if pos%2!=0:
        m1=digit*2
        if m1/10!=0:
            # for x*2 if 2 digit product
            sum1=sum1+(m1%10)+(m1//10)
        else:
            sum1=sum1+m1
    else:
        notaltsum=notaltsum+digit
    if n//10!=0:
        firsttwodigits=n
    n=n//10
    pos=pos+1
    if pos==16 and digit==4:
        counter=1


check=sum1+notaltsum

if check%10==0 and pos>=13:
    if firsttwodigits==34 or firsttwodigits==37:
        print("AMEX")
    elif firsttwodigits>50 and firsttwodigits<56:
        print("MASTERCARD")
    elif firsttwodigits//10==4:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
