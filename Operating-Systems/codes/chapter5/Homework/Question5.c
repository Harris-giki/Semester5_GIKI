#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char *argv[])
{
    printf("start (pid:%d)\n", (int)getpid());

    int rc = fork();
    if (rc < 0) {
        // fork failed
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if (rc == 0) {
        // child process
        printf("hello, I am the child (pid:%d)\n", (int)getpid());

        // try using wait() in the child
        int wc = wait(NULL);
        printf("child: wait() returned %d (pid:%d)\n", wc, (int)getpid());
        // this will print -1 because child has no children
    }
    else{
        int status;
        int wc = wait(&status);
        printf("I am the parent of %d (wc:%d) (pid:%d)\n", rc, wc, (int)getpid());
        if (WIFEXITED(status)) {
            printf("child exited with status %d\n", WEXITSTATUS(status));
    }
}
    return 0;
}