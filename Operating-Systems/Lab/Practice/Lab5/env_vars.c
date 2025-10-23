#include <stdio.h>

extern char **environ;

int main() {
    char **env = environ;
    while (*env) {
        printf("%s\n", *env);
        env++;
    }
    return 0;
}
//Loops through and prints all environment variables available to the process.