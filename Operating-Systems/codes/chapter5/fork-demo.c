#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main ()
{
    int rc = fork();

    if (rc<0){
        printf("fork failed\n");
    }
    else if (rc==0){
        printf("child says: I print numbers! (pid:%d\n)", (int) getpid());
        for (int i=0; i<=5; i++)
        {
            printf("%d\n", i);
        }
        printf("\n");
        }
        else{
            printf("Parent says: I print Alphabets (pid:%d)\n", (int) getpid());
            for (char c='a'; c<='e'; c++)
            {
                printf("%c\n", c);
            }
            printf("\n");
        }
        return 0;
}