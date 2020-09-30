#include <stdio.h>

int main(void){
    char name[20];
    printf("Hello, friend.\n");
    printf("Who are you?\n");
    scanf("%s", name);
    printf("%s, that is a nice name. Exciting times these days.\n", name);
}
