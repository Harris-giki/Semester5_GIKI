#include <stdio.h> // for using printf 
#include <stdlib.h> // for exit
#include <unistd.h> // for using fork and getpid()

int main (int argc, char *argv[]) //argc (how many arg passes) and argv (array for actual arguments) are cmd-line arguments
{
    printf("hello (pid:%d)\n", (int) getpid());

    int rc = fork();
    if (rc < 0)
    {
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if (rc == 0)
    {
        printf("hello, I am child (pid:%d)\n", (int) getpid());
    }
    else
    {
        printf("hello, I am parent of %d (pid:%d)\n", rc, (int) getpid());
    }
    return 0;

}