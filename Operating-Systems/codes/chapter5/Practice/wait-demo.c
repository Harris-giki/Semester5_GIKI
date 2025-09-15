#include <stdio.h> // for using printf
#include <stdlib.h> // for exit
#include <unistd.h> // for using fork and getpid()
#include <sys/wait.h> // for using wait

int main()
{
    printf("start the program (pid:%d)\n", (int)getpid());

    int rc=fork();
    if(rc<0)
    {
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if(rc==0)
    {
        printf("hello, I am child (pid:%d) and I am working for 2 seconds\n", (int)getpid());
        sleep(2);
        printf("hello, I am child (pid:%d) and I have worked for 2 seconds \n)", (int) getpid());
    }
    else
    {
        int wc=wait(NULL);
        printf("hello, I am parent of %d (wc:%d) (pid:%d)\n", rc, wc, (int)getpid());
    }
}