#include <stdio.h>
#include <unistd.h>
#include <unistd.h>


int main() {
    printf("Before execlp\n");
    execlp("ls", "ls", "-l", NULL);
    // no /bin/ls needed, it will search PATH unlike execl
    printf("This will not print if execlp succeeds\n");
    return 0;
}
