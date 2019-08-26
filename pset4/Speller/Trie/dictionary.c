// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

// for next after root
node *branch;

// for word count
int wordcount=0;

// index for children len for word
int index;

// to keep track of where we are
node *cursor;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
            cursor=root;
            for(int i = 0,len = strlen(word); i < len; i++)
            {
            if(word[i]=='\'')
            index=26;
            else
            index = tolower(word[i]) - 'a';
            if(cursor->children[index] == NULL)
            {
            branch = malloc(sizeof(node));
            cursor->children[index] = branch;
                for(int j = 0; j < N;j++ )
                    branch->children[j] = NULL;
            branch->is_word = false;
            cursor=branch;
            }
            else
                cursor = cursor->children[index];
            }
            cursor -> is_word = true;
            wordcount++;
    }
    // to preserve root to access later
    cursor=root;
    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return wordcount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    cursor=root;
    for(int i = 0,len = strlen(word); i < len; i++)
    {
        if(word[i]=='\'')
        index=26;
        else
        index = tolower(word[i]) - 'a';
        // if the word doesnt exist
        if(cursor->children[index] == NULL)
        return false;
        else                                // continue the cursor pointer forward
        cursor = cursor->children[index];
    }
    // if cursor is now at endofword and the next node cursor points to contains true, then word exists
    if(cursor -> is_word == true)
        return true;
    return false;
}

void destroy(node *c)
{
    int i=0;
        for(i=0;i<27;i++)
        {
            if(c!=NULL)
            // recurse until hit a the last node
            destroy(c->children[i]);
        }

    free(c);
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    destroy(root);
    return true;
}




