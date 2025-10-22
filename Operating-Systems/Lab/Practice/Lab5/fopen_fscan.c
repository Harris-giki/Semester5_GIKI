#include <stdio.h>

int main()
{
    FILE *fp;
    char name[30];
    int age;

    fp = fopen("text.txt", "w")
    if(fp==NULL)
    {
       printf("Error opening file!\n");
        return 1; 
    }
    // Step 2: Write to file
    fprintf(fp, "Haris %d", 21);
    fclose(fp);
    // Step 3: Open file for reading
    fp = fopen("info.txt", "r");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return 1;
    }
    // Step 4: Read from file
    fscanf(fp, "%s %d", name, &age);
    printf("Name: %s, Age: %d\n", name, age)
}