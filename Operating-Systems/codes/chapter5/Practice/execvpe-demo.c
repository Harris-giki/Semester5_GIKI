#define _GNU_SOURCE   // required for execvpe
#include <stdio.h>
#include <unistd.h>

int main() {
    printf("Before execvpe\n");
    char *args[] = {"env", NULL};
    char *envp[] = {"MYVAR=ExecvpeTest", NULL};
    execvpe("env", args, envp);  // search PATH, custom env
    return 0;
}
