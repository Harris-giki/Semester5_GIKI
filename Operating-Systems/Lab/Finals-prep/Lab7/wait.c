#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
    if (fork() == 0) {          // First child
        if (fork() == 0) {      // Grandchild
            printf("Grandchild exiting\n");
            exit(0);
        } else {
            wait(NULL);         // Child waits for grandchild
            printf("Child exiting\n");
            exit(0);
        }
    } else {
        wait(NULL);             // Parent waits for child
        printf("Parent exiting\n");
    }
    return 0;
}
