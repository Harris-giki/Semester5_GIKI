#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>

int main(int argc, char *argv[])
{
    printf("hello (pid:%d)\n", (int)getpid());
    int rc = fork();
    if (rc < 0)
    {
        fprintf(stderr, "fork failed\n");
        exit(1);    
    }
    else if(rc == 0)
    {
        printf("hello, I am child (pid:%d)\n", (int)getpid());
        close(STDOUT_FILENO); // redirect child's stdout
         // STDOUT_FILENO is 1
        open("pc4.output", O_CREAT | O_WRONLY | O_TRUNC, S_IRWXU);
        char *myargs[3];
        myargs[0] = "wc"; // program: "wc" (word count)
        myargs[1] = "pc4.c"; // argument: file to count
        myargs[2] = NULL; // marks end of array
        execvp(myargs[0], myargs); // runs word count
        printf("this shouldn't print out because execvp() is supposed to run wc\n");
    }
    else
    {
        int wc = wait(NULL);
        printf("hello, I am parent of %d (wc:%d) (pid:%d)\n", rc, wc, (int)getpid());
    }
    return 0;
}

// O_CREAT - create file if it does not exist
// O_WRONLY - open file for write only
// O_TRUNC - if file already exists, truncate to zero length
// S_IRWXU - set read, write, execute permissions for owner