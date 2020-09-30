#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

bool key(char* argv1);

int main(int argc, char* argv[]){
    if (argc != 2 || !key(argv[1])){
        printf("Usage: ./caesar key.\n");
        return 1;
    }

    int k = atoi(argv[1]);
    char p[255];
    printf("plaintext: ");
    scanf("%[^\n]", p);
    printf("ciphertext: ");
    for (int i = 0; i < strlen(p); i++){
        char c = p[i];
        if (isalpha(c)){
            char a = 65;
            if (islower(c))
                a = 97;
            printf("%c", (c - a + k) % 26 + a);
        }
        else
        printf("%c", c);
    }
    printf("\n");
}

bool key(char* argv1){
    for (int i = 0; i < strlen(argv1); i++)
        if (!isdigit(argv1[i]))
            return false;
    return true;
}
