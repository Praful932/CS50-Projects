#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int n=-1,flag=0;
    char filename[10];
    unsigned char *buffer=malloc(512*sizeof(char));
    FILE *img=NULL;
    if(argc!=2)
    {
        fprintf(stderr,"Usage ./recover image");
        return 1;
    }
    // open raw card file for reading
    FILE *mcardptr=fopen("card.raw","r");
    if(mcardptr==NULL)
    {
    fclose(mcardptr);
    fprintf(stderr,"Image could not be opened");
    return 2;
    }
    int r=fread(buffer,1,512,mcardptr);
    while(r==512)
    {
        //checks for start of new jpeg
        if(buffer[0]==0xff && buffer[1]==0xd8 && buffer[2]==0xff && (buffer[3] & 0xf0) == 0xe0)
        {

                flag=1;
                if(n>=0)
                fclose(img);
                n++;
                sprintf(filename,"%03i.jpg",n);
                img=fopen(filename,"w");
                fwrite(buffer,1,512,img);
        }
        //if already found keep writing
        else if(flag==1)
        fwrite(buffer,1,512,img);
        r=fread(buffer,1,512,mcardptr);
    }
    free(buffer);
    fclose(img);
    fclose(mcardptr);
}
