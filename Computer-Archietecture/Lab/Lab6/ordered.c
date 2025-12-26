#include <stdio.h>
#include <omp.h>

int main() {
    omp_set_num_threads(4); // fixed number of threads

    printf("Without ordered:\n");
    #pragma omp parallel for
    for (int i = 0; i < 10; i++) {
        printf("Iteration %d executed by thread %d\n", i, omp_get_thread_num());
    }

    printf("\nWith ordered:\n");
    #pragma omp parallel for ordered
    for (int i = 0; i < 10; i++) {
        // dummy computation
        int dummy = i * i;

        #pragma omp ordered
        {
            printf("Iteration %d executed by thread %d\n", i, omp_get_thread_num());
        }
    }

    return 0;
}
