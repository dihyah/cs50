#include <stdio.h>
#include <math.h>

int main(void){
    float change;
    do{
        printf("Change Owed: ");
        scanf("%f",&change);
    }
    while (change < 0);

    int cash = round(change * 100);
    int coins = 0;

    int cents[] = {25, 10, 5, 1};
    int size = sizeof(cents)/sizeof(cash);
    for (int i = 0; i < size; i++)
    {coins += cash / cents[i];
        cash %= cents[i];
    }
    printf("%i\n", coins);
}
