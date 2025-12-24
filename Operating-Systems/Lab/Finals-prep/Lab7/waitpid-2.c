#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

int main()
{
    // checking child status and not waiting using waitpid
    pid_t pid = fork();

    if (pid==0)
    {
        sleep(3);
        printf("child exiting now\n");
    }
    else{
        pid_t ret= waitpid(pid, NULL, WNOHANG);
        
        if(ret ==0)
        {
            printf("Child still running\n");
        }
        sleep(4);
        printf("Parent exiting\n");
    }
    return 0;
}