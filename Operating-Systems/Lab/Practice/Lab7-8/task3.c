#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>

int main() {
    int N;

    while (1) {
        printf("\nEnter a number between 1 and 9 (0 to exit): ");
        scanf("%d", &N);

        // Exit condition
        if (N == 0) {
            printf("Exiting program.\n");
            break;
        }

        // Input validation
        if (N < 1 || N > 9) {
            printf("Invalid input. Please enter a number between 1 and 9.\n");
            continue;
        }

        printf("Creating %d child processes...\n", N);

        // Create N child processes
        for (int i = 0; i < N; i++) {
            pid_t pid = fork();

            if (pid == 0) {
                // Child process
                srand(time(NULL) ^ getpid()); // seed random using PID + time
                int random_number = (rand() % 100) + 1; // random between 1 and 100
                printf("Child %d (PID=%d): Random Number = %d\n", i + 1, getpid(), random_number);
                exit(0); // child exits after printing
            } 
            else if (pid < 0) {
                perror("Fork failed");
                exit(1);
            }
        }

        // Parent process waits for all children
        for (int i = 0; i < N; i++) {
            wait(NULL);
        }

        printf("All %d child processes finished.\n", N);
    }

    return 0;
}
