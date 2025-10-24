#include <stdio.h>
#include <omp.h>

int main()
{
    #pragma omp parallel
    {
        int id = omp_get_thread_num();
        printf("The thread with id: %d is running.", id);
    }
    return 0;
}