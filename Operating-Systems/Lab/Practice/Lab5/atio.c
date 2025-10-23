#include <stdlib.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    if (argc ==2)
    {
        int val = atoi(argv[1]); //converts string into integer
        printf("The value converted is: %d\n", val)
        return 0;
    }
}