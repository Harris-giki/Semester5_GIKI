#include <stdio.h>
#include <omp.h>

#define N 4

int main() {
    int A[N][N], B[N][N], C[N][N];
    int i, j, k;

    // Initialize matrices A and B
    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++) {
            A[i][j] = i + j;
            B[i][j] = i * j;
        }

    printf("=== Version 1: Without ordered ===\n");
    double start1 = omp_get_wtime();

    // Parallel for to compute each C[i][j]
    #pragma omp parallel for collapse(2) private(i, j, k) shared(A, B, C)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            int sum = 0;
            for (k = 0; k < N; k++)
                sum += A[i][k] * B[k][j];
            C[i][j] = sum;
            printf("Thread %d computed C[%d][%d] = %d\n",
                   omp_get_thread_num(), i, j, C[i][j]);
        }
    }

    double end1 = omp_get_wtime();
    printf("\nExecution Time (Without ordered): %f seconds\n\n", end1 - start1);

    // ==========================================================
    printf("=== Version 2: With ordered ===\n");
    double start2 = omp_get_wtime();

    // Parallel for with ordered section
    #pragma omp parallel for collapse(2) private(i, j, k) shared(A, B, C) ordered
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            int sum = 0;
            for (k = 0; k < N; k++)
                sum += A[i][k] * B[k][j];
            C[i][j] = sum;

            #pragma omp ordered
            {
                printf("Thread %d computed C[%d][%d] = %d\n",
                       omp_get_thread_num(), i, j, C[i][j]);
            }
        }
    }

    double end2 = omp_get_wtime();
    printf("\nExecution Time (With ordered): %f seconds\n", end2 - start2);

    return 0;
}
