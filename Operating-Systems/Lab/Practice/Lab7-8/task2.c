#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // Command and its arguments
    char *args[] = {"date", NULL};

    printf("Current Date and Time:\n\n");

    // Replace the current process with the "date" command
    execvp("date", args);

    // If execvp fails, this line executes
    perror("execvp failed");
    return 1;
}
