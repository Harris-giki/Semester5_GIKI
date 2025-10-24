// in the omp for the iteration of the loop were divided into chunks and then
// the loop iterations, Multiple threads access and modify the same memory (shared variables) without synchronization.
// thus it could cause a race condition to occur

// // however in reduction
// Each thread gets a private copy of the variable.
// Threads perform calculations independently.
// At loop completion, OpenMP combines all copies into the shared variable using the specified operator
//      (+, *, min, max, etc.).
// This prevents race conditions when updating a shared variable.

#include <stdio.h>
#include <omp.h>

int main()
{
    #pragma omp parallel
    {
        int sum = 0;
        #pragma omp parallel for reduction (+:sum)
        {
            for(int i=0; i<100; i++)
            {
                sum+=i;
            }
        }
        printf("the sum calculated is: %d", sum);
    }
}