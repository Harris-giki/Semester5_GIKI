#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>

void run_exec_variant(int variant) {
     if (variant == 1) {
    execl("/bin/ls", "ls", "-l", NULL);
    } else if (variant == 2) {
        char *const args[] = {"ls", "-l", NULL};
        execv("/bin/ls", args);
    } else if (variant == 3) {
        execlp("ls", "ls", "-l", NULL);
    } else if (variant == 4) {
        char *const args[] = {"ls", "-l", NULL};
        execvp("ls", args);
    } else if (variant == 5) {
        char *const args[] = {"ls", "-l", NULL};
        char *envp[] = {"MYVAR=ExecvpeTest", NULL};
        execvpe("ls", args, envp);
    } else if (variant == 6) 
    {
        char *envp[] = {"MYVAR=HelloWorld", NULL};
        execle("/bin/ls", "ls", "-l", NULL, envp);
    }
    }
int main() {
    for (int i = 1; i <= 6; i++) {
        pid_t pid = fork();

        if (pid < 0) {
            perror("fork failed");
            return 1;
        }
        else if (pid == 0) {
            // child process: run the chosen exec variant
            printf("\n=== Running exec variant %d ===\n", i);
            run_exec_variant(i);
            return 1; // if exec fails
        }
        else {
            // parent process waits
            wait(NULL);
        }
    }
    return 0;
}