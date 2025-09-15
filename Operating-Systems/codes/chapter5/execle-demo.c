#include <stdio.h>
#include <unistd.h>

int main() {
    printf("Before execle\n");
    char *envp[] = {"MYVAR=HelloWorld", NULL};
    execle("/usr/bin/env", "env", NULL, envp);
    // runs 'env' with custom environment
    return 0;
}
