#include <unistd.h>

int main(void)
{
    char *binaryPath="/bin/ls";
    char *arg1="ls";

    execl(binaryPath, arg1, NULL);
    return 0;

}