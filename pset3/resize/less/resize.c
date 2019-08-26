#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include "bmp.h"

int main(int argc,char *argv[])
{
    int r=atoi(argv[1]);
    int s=0;
    char *infile=argv[2];
    char *outfile=argv[3];
    if(argc!=4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }
    FILE *inptr=fopen(infile,"r");
    if (inptr == NULL)
    {
        printf( "Could not open %s.\n", infile);
        return 2;
    }
    FILE *outptr=fopen(outfile,"w");
    if(outptr == NULL)
    {
        fclose(inptr);
        printf("Could not open %s.\n",outfile);
        return 3;
    }

    BITMAPFILEHEADER bf;
    //read from inptr and store in buffer(bf)
    fread(&bf,sizeof(BITMAPFILEHEADER),1,inptr);

    BITMAPINFOHEADER bi;
    //read from inptr fileinfo and store in a bi
    fread(&bi,sizeof(BITMAPINFOHEADER),1,inptr);

    if(bf.bfType!=0x4d42 || bf.bfOffBits!=54 || bi.biSize!=40 || bi.biBitCount!=24 || bi.biCompression!=0)
    {
        fclose(inptr);
        fclose(outptr);
        fprintf(stderr,"Unsupported file format\n");
        return 4;
    }
    int width=bi.biWidth;
    int height=abs(bi.biHeight);
    //calculating outfiles width and height
    bi.biWidth*=r;
    bi.biHeight*=r;
    //padding of infile
    int paddingi = width % 4;
    //calculate padding of outfile using only width(since only padding is added to width)
    int paddingo = bi.biWidth % 4;
    RGBTRIPLE arr[bi.biWidth];
    //arr=malloc(sizeof(bi.biWidth+paddingo));
    //calculating image size
    bi.biSizeImage=((sizeof(RGBTRIPLE)*bi.biWidth) + paddingo)* abs(bi.biHeight);
    //to calculate total file size including headers
    bf.bfSize=sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER) + bi.biSizeImage;
    fwrite(&bf,sizeof(BITMAPFILEHEADER),1,outptr);
    fwrite(&bi,sizeof(BITMAPINFOHEADER),1,outptr);
     RGBTRIPLE triple;
    //iterating over each row
for(int i=0;i<height;i++)
{
    //iterate over every pixel
    for(int j=0;j<width;j++)
    {
        fread(&triple,sizeof(RGBTRIPLE),1,inptr);
        for(int q=0;q<r;q++)
        {
            //store r times pixel in array and loop over row
        arr[s]=triple;
        s++;
        }
    }
        for(int p=0;p<r;p++)
        {   //write whole row to outfile
            fwrite(arr,sizeof(arr),1,outptr);
        for(int l=0;l<paddingo;l++)
            fputc(0x00,outptr);
        }
        fseek(inptr,paddingi,SEEK_CUR);
        s=0;
}
    fclose(inptr);
    fclose(outptr);
    return 0;
}
