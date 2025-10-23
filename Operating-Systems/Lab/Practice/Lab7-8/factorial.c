#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

// Function to compute factorial
long long factorial(int n) {
    if (n == 0 || n == 1)
        return 1;
    else
        return n * factorial(n - 1);
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
        int num;
        printf("Child: Enter a number to calculate factorial: ");
        scanf("%d", &num);

        long long result = factorial(num);
        printf("Child: Factorial of %d is %lld\n", num, result);

        exit(0); // end child
    }
    else {
        // Parent process
        wait(NULL);  // wait for child to finish
        printf("Parent: Factorial calculation completed.\n");
    }

    return 0;
}
