#include <stdio.h>
#include <omp.h>

int main() {
    int counter = 0;

    #pragma omp parallel num_threads(16) shared(counter)
    {
        for (int i = 0; i < 100; i++) {
            #pragma omp atomic
            counter++;
        }
    }

    printf("Final counter with atomic: %d\n", counter);
    return 0;
}
