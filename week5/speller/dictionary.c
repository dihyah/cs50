// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;
unsigned int word_count;
bool loaded;

// Hash table
node *table[N];

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary){
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    	return false;
    for (int i = 0; i < N; i++)
    	table[i] = NULL;
    
    char word[LENGTH + 1];
    node *new_node;
    while (fscanf(inptr, "%s", word) != EOF){
		word_count++;
		do{
		new_node = malloc(sizeof(node));
			if (new_node == NULL)
				free(new_node);
		}
		while (new_node == NULL);
		
		strcpy(new_node->word, word);
		int index = hash(word);
		new_node->next = table[index];
		table[index] = new_node;
	}
	loaded = true;
	fclose(inptr);
    return true;
}

// Hashes word to a number(HASH ALGORITHM RETRIEVED FROM [http://pages.cs.wisc.edu/~siff/CS367/Notes/hash.html])
unsigned int hash(const char *word){
  int hash = 0;
  for (int i=0; i != '\0'; i++) 
    hash += word[i];  // word[i] returns ASCII value of the ith character of word
  return (hash % N);
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void){
    if (!loaded)	
    	return 0;
    return word_count;
}

// Returns true if word is in dictionary else false
bool check(const char *word){
    char word_check[strlen(word)];
	strcpy(word_check, word);
	int index = hash(word_check);
	if (table[index] != NULL){
		for (node* cursor = table[index]; cursor != NULL; cursor = cursor->next)
			if (strcasecmp(cursor->word, word_check) == 0)
				return true;
	}
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void){
    if (!loaded)
    	return false;
    for (int i = 0; i < N; i++){
		if (table[i] != NULL){
			node *cursor = table[i];
			while (cursor != NULL){
				node *tmp = cursor;
				cursor = cursor->next;
				free(tmp);
			}
		}
	}
	return true;
}
