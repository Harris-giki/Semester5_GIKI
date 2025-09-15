#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
int main()
{
    printf("Before execl\n");
    execl("/bin/ls", "ls", "-l", NULL);
    printf("After execl\n"); // this line will not be printed if execl is successful
    return 0;
}