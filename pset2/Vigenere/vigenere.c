#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c)
    {
        if(islower(c))
            return c-97;
        else if(isupper(c))
            return c-65;
    return 0;
    }   

int main(int argc, string argv[])
{
    int key,flag=1,j=0;
    string pt;
    char keyword[100];        
    if(argc!=2)
    {
        printf("Usage: ./vigenere keyword");
        return 1;
    }
    strcpy(keyword,argv[1]);
    int lenkey=strlen(keyword);
    for(int i=0;i<lenkey;i++)
    {
        if(!isalpha(keyword[i]))
            flag=0;
    }
    if(flag==0)
    {
        printf("Usage: ./vigenere keyword");
        return 1;
    }
        pt=get_string("plaintext: ");
        for(int i=0;i<strlen(pt);i++)
        {
            if(j>lenkey-1)
                j=0;
            if(isalpha(pt[i]))
            {
                key=shift(keyword[j]);
                if(islower(pt[i]))
                   pt[i]=97 +((pt[i]-97+key)%26);
                if(isupper(pt[i]))
                    pt[i]=65 +((pt[i]-65+key)%26);
                j++;
            }
        }
        printf("ciphertext: %s\n",pt);
    return 0; 
}
