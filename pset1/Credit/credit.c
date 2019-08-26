#include<stdio.h>
#include<cs50.h>
int main(void)
{
    int digit,notaltsum,m1,sum1,pos,check,counter,firsttwodigits;
    sum1=0;notaltsum=0;pos=0;counter=0;
    long int n;    // input number
    n=get_long_long("Number: ");
    do
    {
        digit=n%10;
        if(pos%2!=0)
        {
        m1=digit*2;
        if(m1/10!=0)
        sum1=sum1+(m1%10)+(m1/10);
        else
        sum1=sum1+m1;
        }
        else
        notaltsum=notaltsum+digit;
        n=n/10;
        pos++;
        if(pos==16&& digit==4)
        counter=1;
        if(n/10!=0)
        firsttwodigits=n;
    }while(n!=0);
    check=sum1+notaltsum;
    if(check%10==0 && pos>=13)
    {
        if(firsttwodigits==34 || firsttwodigits==37)
        printf("AMEX\n");
        else if(firsttwodigits>50 && firsttwodigits<56)
        printf("MASTERCARD\n");
        else if(firsttwodigits/10==4)
        printf("VISA\n");
        else
        printf("INVALID\n");
    }
    else
    printf("INVALID\n");
}
