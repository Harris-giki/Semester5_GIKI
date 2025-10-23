#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid1, pid2;

    // Create first child
    pid1 = fork();

    if (pid1 < 0) {
        perror("fork failed");
        return 1;
    }
    else if (pid1 == 0) {
        // First child process
        printf("Child 1: PID = %d, Parent PID = %d\n", getpid(), getppid());
        sleep(2); // simulate work
        printf("Child 1 done.\n");
        exit(0);
    }

    // Create second child (only parent reaches here)
    pid2 = fork();

    if (pid2 < 0) {
        perror("fork failed");
        return 1;
    }
    else if (pid2 == 0) {
        // Second child process
        printf("Child 2: PID = %d, Parent PID = %d\n", getpid(), getppid());
        sleep(4); // simulate longer work
        printf("Child 2 done.\n");
        exit(0);
    }

    // Parent process waits for both children
    printf("Parent: waiting for children...\n");
    waitpid(pid1, NULL, 0);  // Wait for first child
    printf("Parent: Child 1 (PID %d) finished.\n", pid1);

    waitpid(pid2, NULL, 0);  // Wait for second child
    printf("Parent: Child 2 (PID %d) finished.\n", pid2);

    printf("Parent: All children finished.\n");
    return 0;
}
