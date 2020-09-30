#include "helpers.h"

#include <math.h>

//undo image filter
void u(int height, int width, RGBTRIPLE image[heigh] [width]{
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            img = image[i][j];
        } 
    }
}

RGBTRIPLE img;

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{   for (int i = 0; i < height; i++){
        for (int j = 0; j < width; ++j){
            img = image[i][j];
            int avg = round((float)(img.rgbtRed + img.rgbtGreen + img.rgbtBlue) / 3);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = avg;
        }
    }
    return;
}

int limit(int value){
    return value > 255 ? 255 : value;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; ++j){
            img = image[i][j];
            int sepiaRed = limit(round((float)0.393 * img.rgbtRed + 0.769 * img.rgbtGreen + 0.189 * img.rgbtBlue));
            int sepiaGreen = limit(round((float)0.349 * img.rgbtRed + 0.686 * img.rgbtGreen + 0.168 * img.rgbtBlue));
            int sepiaBlue = limit(round((float)0.272 * img.rgbtRed + 0.534 * img.rgbtGreen + 0.131 * img.rgbtBlue));

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++){
        for (int j = 0; j < width; j++){
            img = image[i][j];
            img.rgbtRed = 255;
            img.rgbtGreen = 255;
            img.rgbtBlue = 255;
        }
    }
    return;
}

RGBTRIPLE surround(int initiali, int initialj, int h, int w, RGBTRIPLE image[h][w]){
    int hlow, hhigh, wlow, whigh;

    hlow = (initiali - 1) < 0 ? 0 : initiali - 1 ;
    hhigh = (initiali + 1) > h ? h : initiali + 1 ;

    wlow = (initialj - 1) < 0 ? 0 : initialj - 1;
    whigh = (initialj + 1) > w ? w : initialj + 1;

    int avgRed,  avgGreen,  avgBlue;
    avgRed =  avgGreen =  avgBlue = 0;

    int count=0;

    for (int i = hlow; i <= hhigh; i++){
        for (int j = wlow; j <= whigh; j++){
            img = image[i][j];
            count++;
            avgRed += img.rgbtRed;
            avgGreen += img.rgbtGreen;
            avgBlue  += img.rgbtBlue;
        }
    }

    RGBTRIPLE sur;
    sur.rgbtRed = limit(round((float)avgRed / count));
    sur.rgbtGreen = limit(round((float)avgGreen / count));
    sur.rgbtBlue = limit(round((float)avgBlue / count));

    return sur;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width]){
    RGBTRIPLE pix[height][width];

    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
             pix[i][j] = surround(i, j, height, width, image);

    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++){
             image[i][j]=pix[i][j];
        }

    return;
}
