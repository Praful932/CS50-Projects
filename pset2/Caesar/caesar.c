#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
int main(int argc, string argv[])
{
    int key;
    string pt;
    if(argc!=2)
    {
        printf("Usage: ./caesar key");
        return 1;
    }
    else
    {
        key=atoi(argv[1]);
        pt=get_string("plaintext: ");
        for(int i=0;i<strlen(pt);i++)
        {
            if(isalpha(pt[i]))
            {
                if(islower(pt[i]))
                {
                    pt[i]=96 +((pt[i]-96+key)%26);
                    //pt[i]=pt[i]>122?pt[i]-26:pt[i];
                }
                if(isupper(pt[i]))
                {
                    pt[i]=64 +((pt[i]-64+key)%26);
                    //pt[i]=pt[i]>90?pt[i]-26:pt[i];
                }
            }
        }
        printf("ciphertext: %s\n",pt);
    return 0;
    } 
        
}
