// wait() → waits for any child process to finish.
// waitpid(pid, ...) → waits for a specific child process (pid).
// If you pass -1, it behaves like wait() (waits for any child).

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    printf("start (pid:%d)\n", (int)getpid());

    int rc = fork();
    if (rc < 0) {
        // fork failed
        fprintf(stderr, "fork failed\n");
        exit(1);
    }
    else if (rc == 0) {
        // child process
        printf("hello, I am the child (pid:%d)\n", (int)getpid());

        // child tries waitpid (will fail, no children)
        int wc = waitpid(-1, NULL, 0);
        printf("child: waitpid() returned %d (pid:%d)\n", wc, (int)getpid());
    }
    else {
        // parent process waits for the specific child 'rc'
        int wc = waitpid(rc, NULL, 0);
        printf("I am the parent of %d (wc:%d) (pid:%d)\n", rc, wc, (int)getpid());
    }

    return 0;
}
