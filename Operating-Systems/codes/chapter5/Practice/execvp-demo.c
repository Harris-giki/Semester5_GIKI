#include <stdio.h>
#include <unistd.h>

int main() {
    printf("Before execvp\n");
    char *args[] = {"ls", "-l", NULL};
    execvp("ls", args);   // finds ls in PATH
    return 0;
}
