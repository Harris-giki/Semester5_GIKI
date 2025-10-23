#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

// Function to print Fibonacci series
void fibonacci(int n) {
    int first = 0, second = 1, next;

    printf("Child: Fibonacci Series up to %d terms:\n", n);

    for (int i = 0; i < n; i++) {
        if (i <= 1)
            next = i;
        else {
            next = first + second;
            first = second;
            second = next;
        }
        printf("%d ", next);
    }
    printf("\n");
}

int main() {
    pid_t pid;

    pid = fork();  // Create child process

    if (pid < 0) {
        // fork failed
        perror("fork failed");
        exit(1);
    }
    else if (pid == 0) {
        // Child process
        int terms;
        printf("Child: Enter number of terms for Fibonacci series: ");
        scanf("%d", &terms);

        fibonacci(terms);

        exit(0); // end child
    }
    else {
        // Parent process
        wait(NULL);  // Wait for child to finish
        printf("Parent: Fibonacci calculation completed.\n");
    }

    return 0;
}
