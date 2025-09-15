#include <stdio.h>
#include <unistd.h>

int main() {
    printf("Before execv\n");
    char *args[] = {"ls", "-l", NULL};
    execv("/bin/ls", args);
    return 0;
}
