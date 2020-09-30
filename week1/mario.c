#include <stdio.h>

int main(void){
    int n;

    do{
        printf("Size: ");
        scanf("%i", &n);
    }
    while (n < 1);

    for (int c = 0; c < n; c++){
        for (int r = -1; r < c; r++){
            printf("#");
        }
        printf("\n");
    }
}
