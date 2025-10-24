#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 4  // Try 100 or 500 for better timing

int main() {
    int A[N][N], B[N][N], C[N][N];
    int i, j, k;

    // Initialize matrices A and B
    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++) {
            A[i][j] = i + j;
            B[i][j] = i * j;
        }

    double start = omp_get_wtime();

    // Parallelize outer loop (distribute rows among threads)
    #pragma omp parallel for private(j, k) shared(A, B, C)
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            int sum = 0;

            // Use reduction to safely accumulate partial products
            #pragma omp parallel for reduction(+:sum)
            for (k = 0; k < N; k++) {
                sum += A[i][k] * B[k][j];
            }

            C[i][j] = sum;
        }
    }

    double end = omp_get_wtime();

    printf("Parallel Execution Time: %f seconds\n", end - start);

    // Print result (for small N)
    printf("\nResultant Matrix C:\n");
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++)
            printf("%d ", C[i][j]);
        printf("\n");
    }

    return 0;
}
