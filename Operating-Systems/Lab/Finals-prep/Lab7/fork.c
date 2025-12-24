#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
    pid_t pid, mypid, myppid;
    pid=getpid();

    printf("Before fork: Process id is %d\n", pid);
    pid = fork();

    if(pid<0)
    {
        perror("fork() failure \n");
        return 1;
    }
    if(pid == 0)
    {
        printf("this is the child process\n");
        mypid = getpid();
        myppid = getppid();
        printf("the child pid: %d and its parent's pid is %d \n", mypid, myppid);
    }
    else
    {
        // you put the parent process logic here
        sleep(2);
        printf("This is the parent process\n");
        mypid=getpid();
        myppid=getppid();
        printf("the process id now is: %d and its parent's pid is %d \n", mypid, myppid);
        printf("its child's process id is %d\n", pid);
    }
}