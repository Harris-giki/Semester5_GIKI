#include <stdio.h>
#include <omp.h>

int main() {
    int counter = 0;

    #pragma omp parallel num_threads(8)
    {
        #pragma omp critical
        {
            counter++;
            printf("Thread %d incremented counter (with sync)\n", omp_get_thread_num());
        }
    }

    printf("\nFinal Counter (with critical): %d\n", counter);
    return 0;
}
