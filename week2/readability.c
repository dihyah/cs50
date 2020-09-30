#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void){
    char text[255];
    printf("Text: ");
    scanf("%[^\n]", text);
    printf("%s\n", text);
    int numletter = 0, numword = 0, numsentence = 0;

    for (int i = 0; i < strlen(text) ; i++){
        if (isalpha(text[i]))
            numletter++;
        if ((i == 0 && text[i++] != ' ') || (text[i] == ' ' && text[i + 1] != ' '))
            numword++;
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
            numsentence++;
    }
    float L = ((float) numletter / (float) numword) * 100;
    float S = ((float) numsentence / (float) numword) * 100;

    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index < 1)
        printf("Under Grade 1\n");
    else if (index >= 16)
        printf("Grade 16+\n");
    else
        printf("Grade %i\n", index);
}
