#include <stdio.h>

// typedef helps to create alias for existing datatypes

typedef unsigned int uint;

// a struct without Typedef
struct student {
    int id;
    char name[50];
};

// a struct with Typedef
typedef struct{
    int phone_number;
    char name[30];
} hostle;


int main()
{
    struct student s1; // without typedef
    hostle h1; // with typedef

    printf("Enter your name: \n");
    scanf("%s", s1.name);

    printf("Enter the name of your hostle \n");
    scanf("%s", h1.name);
}