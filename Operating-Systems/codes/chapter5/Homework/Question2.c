// The parent opens output.txt, getting a file descriptor fd.
// fork() duplicates the process, so the child inherits a copy of the parent’s file descriptor.
// Both descriptors refer to the 'same open file' description (kernel structure), including the same file offset.


#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <string.h>
int main ()
{
    int fd = open("output.txt", O_CREAT | O_WRONLY | O_TRUNC, S_IRWXU);
    if (fd < 0)
    {
        fprintf(stderr, "open failed\n"); //or use perror("open"); 
        exit(1);    
    }
    write(fd, "I am parent before fork\n", strlen("I am parent before fork\n")); // parent writes to file before fork   
    int rc = fork();
    if(rc<0){
        fprintf(stderr, "Fork failed\n");
        exit(1);
    }
    if(rc==0){
        write(fd, "Child writes this line\n", strlen("Child writes this line\n"));
    }
    else {
        // parent process
        write(fd, "Parent writes this line\n", strlen("Parent writes this line\n"));
    }
    close(fd);
}