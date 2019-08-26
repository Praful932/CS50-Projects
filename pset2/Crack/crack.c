#define _XOPEN_SOURCE
#include <unistd.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int findkey(char salt[],char hashi[],int length,char start)
{
    char key[6],hasho[20];key[5]=0;
    int n;
    int it=pow(26,length);                //iterations
    for(int i=5;i>=length;i--)
    {
        key[i]='\0';
    }
    for(int i=0;i<it;i++)
    {  
        n=i;
        for(int k=length-1;k>=0;k--)                //assign letter from end
        {
            key[k]=start + (n%26);
            n/=26;
        }
        if(strcmp(crypt(key,salt),hashi)==0)
        {
            printf("%s",key);
            return 1;
        }
    }
    return 0;
}
int main(int argc, string argv[])
{
    int found=0;
    char salt[3],hashi[20],one[100],start='a';
    strncpy(salt,argv[1],2);
    if(argc!=2)
    {
        printf("Usage: ./crack hash");
    }
    strcpy(hashi,argv[1]);
    for(int length=1;length<=5 && found==0;length++)
    {
    found =findkey(salt,hashi,length,start);
    start='A';
    if(found==0)
    found =findkey(salt,hashi,length,start);
    start='a';
    }
   
    return 0;    
}
         
          
