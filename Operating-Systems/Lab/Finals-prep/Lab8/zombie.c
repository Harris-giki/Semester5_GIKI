#include <unistd.h>
#include <stdio.h>

int main() {
    if (fork() == 0) {
        printf("Child exiting\n");
        _exit(0);
    } else {
        sleep(30);   // Parent alive but not calling wait
        printf("Parent exiting\n");
    }
}
