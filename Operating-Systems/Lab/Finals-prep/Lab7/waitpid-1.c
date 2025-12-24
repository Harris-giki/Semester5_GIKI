#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main()
{
    // waiting using child id
    pid_t pid = fork();
    if (pid == 0)
    {
        sleep(2);
        printf("Child Exiting\n");
    }
    else{
        waitpid(pid, NULL, 0)
        printf("Parent will resume after the child is processed\n");
    }
}