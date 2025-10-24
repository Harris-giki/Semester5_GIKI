#include <stdio.h>
#include <omp.h>

int main() {
    // Create a parallel region with 8 threads
    #pragma omp parallel num_threads(8)
    {
        int tid = omp_get_thread_num();

        // First print (before barrier)
        printf("Thread %d reached before barrier\n", tid);

        // Barrier synchronization point
        #pragma omp barrier

        // Second print (after barrier)
        printf("Thread %d passed barrier\n", tid);
    }

    return 0;
}
