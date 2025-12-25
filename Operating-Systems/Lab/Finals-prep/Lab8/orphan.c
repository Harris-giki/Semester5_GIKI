#include <unistd.h>
#include <stdio.h>

int main() {
    if (fork() == 0) {
        sleep(5);
        printf("Child PID: %d, Parent PID: %d\n",
               getpid(), getppid());
    } else {
        //parent exited immediatedly without waiting for the child
        printf("Parent exiting\n");
        _exit(0);
    }
}
