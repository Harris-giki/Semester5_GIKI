#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid;

    pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }
    else if (pid == 0) {
        // child process
        printf("hello\n");
    }
    else {
        // parent process
        sleep(1);   // give child a chance to run first
        printf("goodbye\n");
    }

    return 0;
}
