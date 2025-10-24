#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

int main() {
    const int N = 100000000;
    double *arr = malloc(N * sizeof(double));
    double sum = 0.0;

    // Initialize array
    for (int i = 0; i < N; i++)
        arr[i] = 1.0;  // or any other value

    double start = omp_get_wtime();

    // Parallel sum using reduction
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < N; i++) {
        sum += arr[i];
    }

    double end = omp_get_wtime();

    printf("Sum = %.2f\n", sum);
    printf("Time taken: %.5f seconds\n", end - start);

    free(arr);
    return 0;
}
