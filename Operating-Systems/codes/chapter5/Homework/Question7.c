#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    printf("start (pid:%d)\n", (int)getpid());

    int rc = fork();
    if (rc < 0) {
        // fork failed
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if (rc == 0) {
        // child process
        printf("Child: before closing STDOUT\n");

        // close standard output
        close(STDOUT_FILENO);

        // this will not appear, because STDOUT is closed
        printf("Child: after closing STDOUT\n");
    }
    else {
        // parent process
        printf("Parent: I am the parent (pid:%d)\n", (int)getpid());
    }

    return 0;
}
