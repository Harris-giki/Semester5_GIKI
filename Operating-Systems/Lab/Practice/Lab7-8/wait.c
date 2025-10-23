#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid;
    int status;

    pid = fork();  // create a child process

    if (pid < 0) {
        // fork failed
        perror("fork failed");
        return 1;
    } 
    else if (pid == 0) {
        // Child process
        printf("Child process: PID = %d, Parent PID = %d\n", getpid(), getppid());
        sleep(2); // simulate some work
        printf("Child process finished work.\n");
        exit(42); // exit with a custom status code
    } 
    else {
        // Parent process
        printf("Parent process: PID = %d, waiting for child...\n", getpid());
        wait(&status); // wait for child to finish

        if (WIFEXITED(status)) {
            printf("Parent: Child exited with code %d\n", WEXITSTATUS(status));
        }
        printf("Parent process done.\n");
    }

    return 0;
}
