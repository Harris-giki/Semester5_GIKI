#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
    int count =0;
    for(int i=0; i<3; i++)
    {
        count++;
        fork();
    }
    printf("the count is %d (pid:%d)\n", count, (int)getpid());
    return 0;
}
