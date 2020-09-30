#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define MAX 9

struct candidate{
    char* name;
    int votes;
}candidates[MAX];

int candidate_count;

bool vote(char* name);
void print_winner();

int main(int argc, char* argv[]){

    candidate_count = argc - 1;

    for (int i = 0; i < argc-1; i++){
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    printf("\nNumber of voters: ");
    int voters = scanf("%i", &voters);
    bool choice;
    char* name;

    for (int i = 0; i <= voters; i++){
        choice = false;
        do {
            printf("Vote %i: ", i + 1);
            scanf("%s", name);

            choice = vote(name);

            if (choice == false){
                printf("INVALID VOTE!!\n");
            }
        }while (choice == false);
    }

    printf("======== No. of Votes========\n");
    for (int i = 0; i < argc-1; i++){
        printf("%s\t\t%d\n",candidates[i].name,candidates[i].votes);
    }

    printf("======== W I N N E R ========\n");
    print_winner();
}

//increments vote for every candidates' names entrered.
bool vote(char* name){
    for (int i = 0; i <= candidate_count; i++){
        if (strcmp(candidates[i].name, name) == 0){
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

//search and returns candidate with most votes.
void print_winner(void){
    int max = 0;

    // get max value of votes
    for (int i = 0; i < candidate_count; i++){
        if (max < candidates[i].votes){
            max = candidates[i].votes;
        }
    }

    // print candidate's name with most votes
    for (int i = 0; i < candidate_count; i++){
        if (max == candidates[i].votes){
            printf("%s\n",candidates[i].name);
        }
    }
}
