#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;

bool NEW_JPEG(BYTE bytes[]);

int main(int argc, char *argv[]){
    if (argc != 2){
        fprintf(stderr, "Usage: ./recover file\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file){
        fprintf(stderr, "Error: File not found.\n");
        return 2;
    }

    BYTE bytes[512];
    bool JPEG = false;
    int img_track = 0;
    FILE *output;
    while (fread(bytes, 512, 1, file)){
        if (NEW_JPEG(bytes)){
            if (!JPEG)
                JPEG = true;
            else
                fclose(output);
            char IMGfile[8];
            sprintf(IMGfile, "%03i.jpg", img_track++);
            output = fopen(IMGfile, "w");
            fwrite(bytes, 512, 1, output);
        }
        else if (JPEG){
            fwrite(bytes, 512, 1, output);
        }
    }
    fclose(file);
    fclose(output);
}

bool NEW_JPEG(BYTE bytes[]){
    return bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0;
}