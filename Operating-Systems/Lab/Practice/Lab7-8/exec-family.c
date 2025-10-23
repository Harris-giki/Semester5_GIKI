#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    printf("Before exec call...\n\n");

    // ====== 1️⃣ execl() ======
    // Uses full path and argument list.
    // execl("/bin/ls", "ls", "-l", NULL);

    // ====== 2️⃣ execlp() ======
    // Searches command in PATH automatically.
    // execlp("ls", "ls", "-a", NULL);

    // ====== 3️⃣ execv() ======
    // Uses an array of arguments, no PATH search.
    // char *args1[] = {"/bin/ls", "-l", NULL};
    // execv("/bin/ls", args1);

    // ====== 4️⃣ execvp() ======
    // Uses an array and PATH search (most common in real programs).
    // char *args2[] = {"ls", "-l", NULL};
    // execvp("ls", args2);

    // ====== 5️⃣ execve() ======
    // Lowest-level version; allows setting environment variables manually.
    // char *args3[] = {"/bin/echo", "Hello from execve!", NULL};
    // char *envp[] = {"MYVAR=123", NULL};
    // execve("/bin/echo", args3, envp);

    printf("If you see this line, exec() failed!\n");
    perror("exec");
    return 0;
}
