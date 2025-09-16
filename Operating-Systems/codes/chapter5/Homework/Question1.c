#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    int x =428;
    printf("Before fork: %d\n", x);
    int rc = fork();

    if(rc<0){
        printf("fork failed\n");
    }
    else if (rc==0){
        printf("child says: x=%d (pid:%d)\n", x, (int) getpid());
        x = 100;
        printf("child says: x=%d (pid:%d)\n", x, (int) getpid());
    }
    else{
        printf("Parent says: x=%d (pid:%d)\n", x, (int) getpid());
        x = 200;
        printf("Parent says: x=%d (pid:%d)\n", x, (int) getpid());
    }
}