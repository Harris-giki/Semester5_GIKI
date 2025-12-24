#include <stdio.h>
#include <unistd.h>
#include <unistd.h>

int main()
{
    char *args[] = {"./exec", NULL};
    execv(args[0],args);

    // all the statements after this are ignored

    printf("hello world\n");
}