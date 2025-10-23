#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main ()
{
    pid_t pid, mypid, myppid;

    pid = getpid();
    printf("Before the process is forked: Process ID is: %d. \n", pid);
    pid = fork();

    if(pid<0)
    {
        perror("Fork(), failed!\n");
    }
    if(pid==0)
    {
        printf("This process is a child process\n");
        mypid=getpid();
        myppid = getppid();
        printf("Process id %d and PPID is %d.\n", mypid, myppid);
    }
    else{
        sleep(2);
        printf("This is the parent process again");
    }
    return 0;

}