#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    //waiting for any one random child using -1
    //storing exiting info using &status
    // 0 means to block until the child terminates

    fork();   // Child 1
    fork();   // Child 2

    int status;
    pid_t cpid = waitpid(-1, &status, 0);

    printf("Reaped child PID: %d\n", cpid);
    return 0;
}
