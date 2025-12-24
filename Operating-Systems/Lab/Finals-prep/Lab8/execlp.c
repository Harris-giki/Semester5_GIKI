#include <unistd.h>
#include <stdio.h>

int main() {
    // execlp searches PATH for "myprogram"
    execlp("./myprogram", "myprogram", "hello", "world", NULL);

    // Only reached if execlp fails
    perror("execlp failed");
    return 1;
}
